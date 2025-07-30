import logging
from contextlib import suppress
from pathlib import Path
from typing import NamedTuple
from lark import Token, Transformer, Tree, UnexpectedToken, v_args
from hcl2.transformer import Attribute, DictTransformer
from hcl2.api import reverse_transform, writes, parses
import rich

logger = logging.getLogger(__name__)


def update_attribute_object_str_value_for_block(
    tree: Tree, block_name: str, block_transformer: DictTransformer
) -> Tree:
    class BlockUpdater(Transformer):
        @v_args(tree=True)
        def block(self, block_tree: Tree) -> Tree:
            current_block_name = _identifier_name(block_tree)
            if current_block_name == block_name:
                tree_dict = block_transformer.transform(tree)
                tree_modified = reverse_transform(tree_dict)
                assert isinstance(tree_modified, Tree)
                body_tree = tree_modified.children[0]
                assert isinstance(body_tree, Tree)
                block_tree = body_tree.children[0]
                assert isinstance(block_tree, Tree)
                return block_tree
            return block_tree

    return BlockUpdater().transform(tree)


class AttributeChange(NamedTuple):
    attribute_name: str
    old_value: str | None
    new_value: str


def attribute_transfomer(attr_name: str, obj_key: str, new_value: str) -> tuple[DictTransformer, list[AttributeChange]]:
    changes: list[AttributeChange] = []

    class AttributeTransformer(DictTransformer):
        def attribute(self, args: list) -> Attribute:
            found_attribute = super().attribute(args)
            if found_attribute.key == attr_name:
                attribute_value = found_attribute.value
                if not isinstance(attribute_value, dict):
                    raise ValueError(f"Expected a dict for attribute {attr_name}, but got {type(attribute_value)}")
                old_value = attribute_value.get(obj_key)
                if old_value == new_value:
                    return found_attribute
                changes.append(AttributeChange(attr_name, old_value, new_value))
                return Attribute(attr_name, found_attribute.value | {obj_key: new_value})
            return found_attribute

    return AttributeTransformer(with_meta=True), changes


def _identifier_name(tree: Tree) -> str | None:
    with suppress(Exception):
        identifier_tree = tree.children[0]
        assert identifier_tree.data == "identifier"
        name_token = identifier_tree.children[0]
        assert isinstance(name_token, Token)
        if name_token.type == "NAME":
            return name_token.value


def write_tree(tree: Tree) -> str:
    return writes(tree)


def print_tree(path: Path) -> None:
    tree = safe_parse(path)
    if tree is None:
        return
    logger.info("=" * 10 + f"tree START of {path.parent.name}/{path.name}" + "=" * 10)
    rich.print(tree)
    logger.info("=" * 10 + f"tree END of {path.parent.name}/{path.name}" + "=" * 10)


def safe_parse(path: Path) -> Tree | None:
    try:
        return parses(path.read_text())  # type: ignore
    except UnexpectedToken as e:
        logger.warning(f"failed to parse {path}: {e}")

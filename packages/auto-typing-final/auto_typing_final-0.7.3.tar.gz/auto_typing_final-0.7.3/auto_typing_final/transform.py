from collections.abc import Iterable
from dataclasses import dataclass
from typing import Final, Literal

from ast_grep_py import SgNode

from auto_typing_final.finder import (
    ImportsResult,
    find_all_definitions_in_functions,
    find_imports_of_identifier_in_scope,
    has_global_identifier_with_name,
)


@dataclass
class ImportConfig:
    value: str
    import_text: str
    import_identifier: str


ImportStyle = Literal["typing-final", "final"]
IMPORT_STYLES_TO_IMPORT_CONFIGS: dict[ImportStyle, ImportConfig] = {
    "typing-final": ImportConfig(value="typing.Final", import_text="import typing", import_identifier="typing"),
    "final": ImportConfig(value="Final", import_text="from typing import Final", import_identifier="Final"),
}


@dataclass
class EditableAssignmentWithoutAnnotation:
    node: SgNode
    left: str
    right: str


@dataclass
class EditableAssignmentWithAnnotation:
    node: SgNode
    left: str
    annotation: SgNode
    right: str


@dataclass
class OtherDefinition:
    node: SgNode


Definition = EditableAssignmentWithoutAnnotation | EditableAssignmentWithAnnotation | OtherDefinition


@dataclass
class AddFinal:
    node: Definition


@dataclass
class RemoveFinal:
    nodes: list[Definition]


Operation = AddFinal | RemoveFinal


def _make_definition_from_definition_node(node: SgNode) -> Definition:
    if node.kind() != "assignment":
        return OtherDefinition(node)

    match tuple((child.kind(), child) for child in node.children()):
        case (
            ("identifier", left),
            ("=", _),
            (right_kind, right),
        ) if right_kind != "assignment" and not ((parent := node.parent()) and parent.kind() == "assignment"):
            return EditableAssignmentWithoutAnnotation(node=node, left=left.text(), right=right.text())
        case (
            ("identifier", left),
            (":", _),
            ("type", annotation),
            ("=", _),
            (right_kind, right),
        ) if right_kind != "assignment" and not ((parent := node.parent()) and parent.kind() == "assignment"):
            return EditableAssignmentWithAnnotation(
                node=node, left=left.text(), annotation=annotation, right=right.text()
            )
        case _:
            return OtherDefinition(node)


def _make_operation_from_definitions_of_one_name(nodes: list[SgNode]) -> Operation:
    value_definitions: Final[list[Definition]] = []
    has_node_inside_loop = False

    for node in nodes:
        if any(ancestor.kind() in {"for_statement", "while_statement"} for ancestor in node.ancestors()):
            has_node_inside_loop = True
        value_definitions.append(_make_definition_from_definition_node(node))

    if has_node_inside_loop:
        return RemoveFinal(value_definitions)

    match value_definitions:
        case [definition]:
            return AddFinal(definition)
        case definitions:
            return RemoveFinal(definitions)


def _match_exact_identifier(node: SgNode, imports_result: ImportsResult, identifier_name: str) -> str | None:
    match tuple((inner_child.kind(), inner_child) for inner_child in node.children()):
        case (("identifier", first_identifier), (".", _), ("identifier", second_identifier)):
            for alias in imports_result.module_aliases:
                if alias == first_identifier.text() and second_identifier.text() == identifier_name:
                    return node.text()
    return None


def _strip_identifier_from_type_annotation(  # noqa: C901, PLR0911
    node: SgNode, imports_result: ImportsResult, identifier_name: str
) -> tuple[str, str] | None:
    type_node_children: Final = node.children()
    if len(type_node_children) != 1:
        return None
    inner_type_node: Final = type_node_children[0]
    kind: Final = inner_type_node.kind()

    if kind == "subscript":
        match tuple((child.kind(), child) for child in inner_type_node.children()):
            case (("attribute", attribute), ("[", _), *kinds_and_nodes, ("]", _)):
                if existing_final := _match_exact_identifier(attribute, imports_result, identifier_name):
                    return existing_final, "".join(node.text() for _, node in kinds_and_nodes)
    elif kind == "generic_type" and imports_result.has_from_import:
        match tuple((child.kind(), child) for child in inner_type_node.children()):
            case (("identifier", identifier), ("type_parameter", type_parameter)):
                if identifier.text() != identifier_name:
                    return None
                match tuple((inner_child.kind(), inner_child) for inner_child in type_parameter.children()):
                    case (("[", _), *kinds_and_nodes, ("]", _)):
                        return identifier_name, "".join(node.text() for _, node in kinds_and_nodes)
    elif kind == "identifier" and inner_type_node.text() == identifier_name:
        return identifier_name, ""
    elif kind == "attribute" and (
        existing_final := _match_exact_identifier(inner_type_node, imports_result, identifier_name)
    ):
        return existing_final, ""
    return None


def _make_changed_text_from_operation(  # noqa: C901
    operation: Operation, final_value: str, imports_result: ImportsResult, identifier_name: str
) -> Iterable[tuple[SgNode, str]]:
    match operation:
        case AddFinal(assignment):
            match assignment:
                case EditableAssignmentWithoutAnnotation(node, left, right):
                    yield node, f"{left}: {final_value} = {right}"
                case EditableAssignmentWithAnnotation(node, left, annotation, right):
                    match _strip_identifier_from_type_annotation(annotation, imports_result, identifier_name):
                        case None:
                            yield node, f"{left}: {final_value}[{annotation.text()}] = {right}"
                        case existing_final, "":
                            yield node, f"{left}: {existing_final} = {right}"
                        case existing_final, new_annotation:
                            yield node, f"{left}: {existing_final}[{new_annotation}] = {right}"

        case RemoveFinal(assignments):
            for assignment in assignments:
                match assignment:
                    case EditableAssignmentWithoutAnnotation(node, left, right):
                        yield node, node.text()
                    case EditableAssignmentWithAnnotation(node, left, annotation, right):
                        match _strip_identifier_from_type_annotation(annotation, imports_result, identifier_name):
                            case _, "":
                                yield node, f"{left} = {right}"
                            case _, new_annotation:
                                yield node, f"{left}: {new_annotation} = {right}"


@dataclass
class Edit:
    node: SgNode
    new_text: str


@dataclass
class Replacement:
    operation_type: type[Operation]
    edits: list[Edit]


@dataclass
class MakeReplacementsResult:
    replacements: list[Replacement]
    import_text: str | None


def make_replacements(root: SgNode, import_config: ImportConfig) -> MakeReplacementsResult:
    replacements: Final = []
    has_added_final = False
    imports_result: Final = find_imports_of_identifier_in_scope(root, module_name="typing", identifier_name="Final")

    for current_definitions in find_all_definitions_in_functions(root):
        operation = _make_operation_from_definitions_of_one_name(current_definitions)
        edits = [
            Edit(node=node, new_text=new_text)
            for node, new_text in _make_changed_text_from_operation(
                operation=operation,
                final_value=import_config.value,
                imports_result=imports_result,
                identifier_name="Final",
            )
            if node.text() != new_text
        ]

        if (operation_type := type(operation)) == AddFinal and edits:
            has_added_final = True

        replacements.append(Replacement(operation_type=operation_type, edits=edits))

    return MakeReplacementsResult(
        replacements=replacements,
        import_text=(
            import_config.import_text
            if has_added_final and not has_global_identifier_with_name(root=root, name=import_config.import_identifier)
            else None
        ),
    )

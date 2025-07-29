__all__ = [
    "get_bolt_helpers",
]


from contextlib import ExitStack, contextmanager
from dataclasses import dataclass, replace
from functools import partial, wraps
from importlib import import_module
from typing import Any, Callable, Dict
from uuid import UUID

from mecha import (
    AstAdvancementPredicate,
    AstBool,
    AstChildren,
    AstColor,
    AstCommand,
    AstCoordinate,
    AstGamemode,
    AstGreedy,
    AstItemSlot,
    AstItemSlots,
    AstJson,
    AstJsonObject,
    AstMessage,
    AstNbt,
    AstNbtCompound,
    AstNbtPath,
    AstNode,
    AstNumber,
    AstObjective,
    AstObjectiveCriteria,
    AstPlayerName,
    AstRange,
    AstResourceLocation,
    AstScoreboardSlot,
    AstSortOrder,
    AstString,
    AstSwizzle,
    AstTeam,
    AstTime,
    AstUUID,
    AstVector2,
    AstVector3,
    AstWord,
)
from mecha.contrib.relative_location import resolve_relative_location
from tokenstream import set_location

from .utils import internal


def get_bolt_helpers() -> Dict[str, Any]:
    """Return a collection of helpers used by the generated code."""
    return {
        "replace": replace,
        "missing": object(),
        "exit_stack": ExitStack,
        "children": AstChildren,
        "operator_not": operator_not,
        "operator_in": operator_in,
        "operator_not_in": operator_not_in,
        "branch": branch_driver,
        "loop": loop_driver,
        "get_dup": get_dup,
        "get_rebind": get_rebind,
        "get_attribute_handler": AttributeHandler,
        "import_module": python_import_module,
        "macro_call": macro_call,
        "resolve_formatted_location": resolve_formatted_location,
        "interpolate_bool": converter(AstBool.from_value),
        "interpolate_numeric": converter(AstNumber.from_value),
        "interpolate_coordinate": converter(AstCoordinate.from_value),
        "interpolate_time": converter(AstTime.from_value),
        "interpolate_word": converter(AstWord.from_value),
        "interpolate_phrase": converter(AstString.from_value),
        "interpolate_greedy": converter(AstGreedy.from_value),
        "interpolate_json": converter(AstJson.from_value),
        "interpolate_json_object": JsonObjectConverter(converter(AstJson.from_value)),
        "interpolate_nbt": converter(AstNbt.from_value),
        "interpolate_nbt_compound": NbtCompoundConverter(converter(AstNbt.from_value)),
        "interpolate_nbt_path": converter(AstNbtPath.from_value),
        "interpolate_range": converter(AstRange.from_value),
        "interpolate_resource_location": converter(AstResourceLocation.from_value),
        "interpolate_item_slot": converter(AstItemSlot.from_value),
        "interpolate_item_slots": converter(AstItemSlots.from_value),
        "interpolate_uuid": converter(AstUUID.from_value),
        "interpolate_objective": converter(AstObjective.from_value),
        "interpolate_objective_criteria": converter(AstObjectiveCriteria.from_value),
        "interpolate_scoreboard_slot": converter(AstScoreboardSlot.from_value),
        "interpolate_swizzle": converter(AstSwizzle.from_value),
        "interpolate_team": converter(AstTeam.from_value),
        "interpolate_advancement_predicate": converter(
            AstAdvancementPredicate.from_value
        ),
        "interpolate_color": converter(AstColor.from_value),
        "interpolate_sort_order": converter(AstSortOrder.from_value),
        "interpolate_gamemode": converter(AstGamemode.from_value),
        "interpolate_message": converter(AstMessage.from_value),
        "interpolate_vec2": converter(AstVector2.from_value),
        "interpolate_vec3": converter(AstVector3.from_value),
        "interpolate_entity": EntityConverter(
            uuid_converter=converter(AstUUID.from_value),
            player_name_converter=converter(AstPlayerName.from_value),
        ),
    }


@internal
def operator_not(obj: Any):
    if func := getattr(type(obj), "__not__", None):
        return func(obj)
    return not obj


@internal
def operator_in(item: Any, container: Any):
    if func := getattr(type(item), "__within__", None):
        return func(item, container)
    if func := getattr(type(container), "__contains__", None):
        return func(container, item)
    return item in container


@internal
def operator_not_in(item: Any, container: Any):
    return operator_not(operator_in(item, container))


@contextmanager
@internal
def branch_driver(obj: Any):
    if func := getattr(type(obj), "__branch__", None):
        with func(obj) as condition:
            yield condition
    else:
        yield obj


@contextmanager
@internal
def loop_driver(obj: Any):
    if func := getattr(type(obj), "__loop__", None):
        with func(obj) as cont:
            yield True, cont
    else:
        yield False, True


@internal
def get_dup(obj: Any):
    if func := getattr(type(obj), "__dup__", None):
        return partial(func, obj)
    return None


@internal
def get_rebind(obj: Any):
    if func := getattr(type(obj), "__rebind__", None):
        return partial(func, obj)
    return None


@dataclass
class AttributeHandler:
    obj: Any
    item: bool = False

    @internal
    def __getitem__(self, attr: str) -> Any:
        try:
            return getattr(self.obj, attr)
        except AttributeError as exc:
            try:
                result = self.obj[attr]
                self.item = True
                return result
            except (TypeError, LookupError):
                raise exc from None

    @internal
    def __setitem__(self, attr: str, value: Any):
        try:
            current = self.__getitem__(attr)
        except AttributeError:
            pass
        else:
            if func := getattr(type(current), "__rebind__", None):
                value = func(current, value)
        if self.item:
            self.obj[attr] = value
        else:
            setattr(self.obj, attr, value)

    @internal
    def __delitem__(self, attr: str):
        try:
            self.__getitem__(attr)
        except AttributeError:
            pass
        if self.item:
            del self.obj[attr]
        else:
            delattr(self.obj, attr)


@internal
def python_import_module(name: str):
    try:
        return import_module(name)
    except Exception as exc:
        tb = exc.__traceback__
        tb = tb.tb_next.tb_next  # type: ignore
        while tb and tb.tb_frame.f_code.co_filename.startswith("<frozen importlib"):
            tb = tb.tb_next
        raise exc.with_traceback(tb)


@internal
def macro_call(runtime: Any, function: Any, command: AstCommand):
    with runtime.modules.error_handler(
        f'Macro "{command.identifier}" raised an exception.'
    ):
        return runtime.capture_output(function, *command.arguments)


@internal
def resolve_formatted_location(runtime: Any, nested_path: str) -> str:
    root = runtime.get_nested_location()
    namespace, resolved = resolve_relative_location(
        nested_path,
        root,
        include_root_file=True,
    )
    return f"{namespace}:{resolved}"


def converter(f: Callable[[Any], AstNode]) -> Callable[[Any, AstNode], AstNode]:
    internal(f)

    @internal
    @wraps(f)
    def wrapper(obj: Any, node: AstNode) -> AstNode:
        if isinstance(obj, AstNode):
            return set_location(obj, node)
        return set_location(f(obj), node)

    return wrapper


@dataclass
class JsonObjectConverter:
    """Converter for json objects."""

    json_converter: Callable[[Any, AstNode], AstNode]

    @internal
    def __call__(self, obj: Any, node: AstNode) -> AstNode:
        if isinstance(obj, AstNode):
            return set_location(obj, node)
        if isinstance(node := self.json_converter(obj, node), AstJsonObject):
            return node
        raise ValueError(f"Invalid json object of type {type(obj)!r}.")


@dataclass
class NbtCompoundConverter:
    """Converter for nbt compounds."""

    nbt_converter: Callable[[Any, AstNode], AstNode]

    @internal
    def __call__(self, obj: Any, node: AstNode) -> AstNode:
        if isinstance(obj, AstNode):
            return set_location(obj, node)
        if isinstance(node := self.nbt_converter(obj, node), AstNbtCompound):
            return node
        raise ValueError(f"Invalid nbt compound of type {type(obj)!r}.")


@dataclass
class EntityConverter:
    """Converter for entities."""

    uuid_converter: Callable[[Any, AstNode], AstNode]
    player_name_converter: Callable[[Any, AstNode], AstNode]

    @internal
    def __call__(self, obj: Any, node: AstNode) -> AstNode:
        if isinstance(obj, AstNode):
            return set_location(obj, node)
        if isinstance(obj, str):
            if obj.count("-") == 4:
                return self.uuid_converter(obj, node)
            return self.player_name_converter(obj, node)
        if isinstance(obj, UUID):
            return self.uuid_converter(obj, node)
        raise ValueError(f"Invalid entity value of type {type(obj)!r}.")

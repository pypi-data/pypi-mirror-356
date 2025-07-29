from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any, Optional, TypedDict, NotRequired

from .basics import Attrs


class MeasurementRecipe(TypedDict):
    measurement_group_id: NotRequired[str]
    label: NotRequired[str]
    resource_type: str
    attrs: NotRequired[Attrs]  # if value is Series or DataFrame, the attrs will be applied on top of existing
    ops: list[dict[str, Any]]  # see op_pipeline.py for details


@dataclass(kw_only=True)
class MeasurementManifest:
    recipes: list[MeasurementRecipe]
    meta: Optional[dict[str, Any]] = None


class AbstractMeasurementRecord(ABC):
    def __init__(
        self,
        *,
        id: str,
        value: Any,
        recipe: Optional[MeasurementRecipe] = None,
        source_id: Optional[str] = None,
    ):
        self.id = id
        self.value = value
        self.recipe = recipe
        self.source_id = source_id

    @abstractmethod
    def related_resource(self, resource_name: str) -> Any: ...

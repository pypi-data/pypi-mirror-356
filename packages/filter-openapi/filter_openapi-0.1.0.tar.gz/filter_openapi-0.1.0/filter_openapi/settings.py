import json
from typing import Dict, List, Set

from pydantic import BaseModel, Field


class Options(BaseModel):
    remove_unreferenced_schemas: bool = Field(True, alias="removeUnreferencedSchemas")


class PathFilter(BaseModel):
    allowed_methods: List[str] = Field(..., alias="allowedMethods")


class AppConfig(BaseModel):
    allowed_tags: Set[str] = Field(..., alias="allowedTags")
    path_filters: Dict[str, PathFilter] = Field(..., alias="pathFilters")
    properties_to_remove: List[str] = Field(default=[], alias="propertiesToRemove")
    options: Options = Field(default_factory=Options)

    @classmethod
    def from_file(cls, path: str) -> "AppConfig":
        """Loads configuration from a JSON file."""
        with open(path, "r") as f:
            data = json.load(f)
        return cls.model_validate(data)

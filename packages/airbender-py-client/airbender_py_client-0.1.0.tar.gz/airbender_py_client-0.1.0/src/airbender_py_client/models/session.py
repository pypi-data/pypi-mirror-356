"""Session-related models for Airbender Python client."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SessionState(str, Enum):
    """Session state enumeration."""

    NOT_STARTED = "notStarted"
    FETCHING = "fetching"
    SUCCESS = "success"
    ERROR = "error"


class ControlPoint(BaseModel):
    """Control point configuration."""

    key: str
    name: str
    settings: dict[str, Any] = Field(default_factory=dict)


class ControlPointConfig(BaseModel):
    """Control point configuration with type."""

    key: str
    name: str
    type: str
    settings: dict[str, Any] = Field(default_factory=dict)


class ProductConfig(BaseModel):
    """Product configuration from the dashboard."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    id: str | None = None
    key: str | None = None
    name: str | None = None
    is_default: bool | None = Field(None, alias="isDefault")
    control_points: list[ControlPointConfig] | dict[str, Any] | None = Field(
        None, alias="controlPoints"
    )

    @field_validator("control_points", mode="before")
    @classmethod
    def normalize_control_points(cls, v: Any) -> Any:
        """Convert control_points from dict to list format if needed."""
        if isinstance(v, dict):
            # If it's a dict, convert to list of ControlPointConfig objects
            control_points = []
            for key, config in v.items():
                if isinstance(config, dict) and "type" in config:
                    control_points.append(
                        ControlPointConfig(
                            key=key,
                            name=str(config.get("name", key)),
                            type=config["type"],
                            settings=config.get("settings", {}),
                        )
                    )
            return control_points
        return v


class SessionAPIResponse(BaseModel):
    """Response from session API calls."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    id: str
    product_id: str | None = Field(None, alias="productId")
    product_key: str | None = Field(None, alias="productKey")
    user: str | None = None
    ip_address: str | None = Field(None, alias="ipAddress")
    created_at: str | None = Field(None, alias="createdAt")
    updated_at: str | None = Field(None, alias="updatedAt")
    blocked: bool = False
    config: ProductConfig | None = None
    config_version_id: str | None = Field(None, alias="configVersionId")
    product_config_id: str | None = Field(None, alias="productConfigId")

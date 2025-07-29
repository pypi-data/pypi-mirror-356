from uuid import UUID
from typing import Literal
from flask import Flask
from werkzeug.routing import UUIDConverter


type UUIDVersion = Literal[1, 3, 4, 5]

MAP_VERSION_TO_REGEX: dict[UUIDVersion, str] = {
    1: r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-1[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
    3: r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-3[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
    4: r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
    5: r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-5[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
}
"""UUID version to regex string"""

class BaseUUIDConverter(UUIDConverter):
    version: UUIDVersion | None = None

    def to_python(self, value: str) -> UUID:
        return UUID(value, version=self.version)

class RouteUUID:
    def __init__(self, app: Flask | None = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        for version, regex in MAP_VERSION_TO_REGEX.items():
            app.url_map.converters[f"uuid{version}"] = type(
                f"UUID_Converter_UUID{version}",
                (BaseUUIDConverter,),
                { "version": version, "regex": regex }
            )

from typing import Any

from smartspace.core import (
    Block,
    metadata,
    step,
)
from smartspace.enums import BlockCategory


@metadata(
    description="Takes in inputs and creates an object containing the inputs",
    category=BlockCategory.MISC,
    icon="fa-cube",
    label="create object, build dictionary, construct object, make key-value map, generate object",
)
class CreateObject(Block):
    @step(output_name="object")
    async def build(self, **properties: Any) -> dict[str, Any]:
        return properties

from typing import Any, Literal, Sequence, Union

from pydantic import BaseModel, Field, RootModel
from pydantic.types import JsonValue

from pharia_skill.csi import tool


class ArgumentSerializer(BaseModel):
    name: str
    value: JsonValue


class InvokeRequestSerializer(BaseModel):
    """Serialization representation of a single tool invocation.

    Must be nested inside a `InvokeRequestsSerializer` that provides the `namespace`.
    """

    name: str
    arguments: list[ArgumentSerializer]


class InvokeRequestsSerializer(BaseModel):
    namespace: str
    requests: list[InvokeRequestSerializer]


def serialize_tool_requests(
    namespace: str, requests: Sequence[tool.InvokeRequest]
) -> dict[str, Any]:
    return InvokeRequestsSerializer(
        namespace=namespace,
        requests=[
            InvokeRequestSerializer(
                name=request.name,
                arguments=[
                    ArgumentSerializer(name=name, value=value)
                    for name, value in request.arguments.items()
                ],
            )
            for request in requests
        ],
    ).model_dump()


class Text(BaseModel):
    type: Literal["text"]
    text: str


# Pylance complains about a Union of only one type.
# However, for discriminated deserialization we do require the Union.
class ToolOutputDeserializer(RootModel[Union[Text]]):  # pyright: ignore[reportInvalidTypeArguments]
    root: Union[Text] = Field(discriminator="type")  # pyright: ignore[reportInvalidTypeArguments]


ToolOutputListDeserializer = RootModel[list[list[ToolOutputDeserializer]]]


def deserialize_tool_output(output: Any) -> list[tool.ToolOutput]:
    return [
        tool.ToolOutput(contents=[content.root.text for content in deserialized])
        for deserialized in ToolOutputListDeserializer(root=output).root
    ]

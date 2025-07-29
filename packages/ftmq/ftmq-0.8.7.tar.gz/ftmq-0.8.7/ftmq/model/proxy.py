from typing import Any, Iterable, Self, Sequence, TypeAlias, TypeVar, Union

from followthemoney.types import registry
from nomenklatura.publish.names import pick_caption
from pydantic import BaseModel, ConfigDict, Field, model_validator

from ftmq.types import CE
from ftmq.util import make_proxy, must_str

EntityProp = TypeVar("EntityProp", bound="Entity")
Properties: TypeAlias = dict[str, Sequence[Union[str, EntityProp]]]


class Entity(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., examples=["NK-A7z...."])
    caption: str = Field(..., examples=["Jane Doe"])
    schema_: str = Field(..., examples=["LegalEntity"], alias="schema")
    properties: Properties = Field(..., examples=[{"name": ["Jane Doe"]}])
    datasets: list[str] = Field([], examples=[["us_ofac_sdn"]])
    referents: list[str] = Field([], examples=[["ofac-1234"]])

    @classmethod
    def from_proxy(cls, entity: CE, adjacents: Iterable[CE] | None = None) -> Self:
        properties = dict(entity.properties)
        if adjacents:
            adjacents_: dict[str, Entity] = {
                must_str(e.id): Entity.from_proxy(e) for e in adjacents
            }
            for prop in entity.iterprops():
                if prop.type == registry.entity:
                    properties[prop.name] = [
                        adjacents_.get(i, i) for i in entity.get(prop)
                    ]
        return cls(
            id=must_str(entity.id),
            caption=entity.caption,
            schema=entity.schema.name,
            properties=properties,
            datasets=list(entity.datasets),
            referents=list(entity.referents),
        )

    def to_proxy(self) -> CE:
        return make_proxy(self.model_dump(by_alias=True))

    @model_validator(mode="before")
    @classmethod
    def get_caption(cls, data: Any) -> Any:
        if data.get("caption") is None:
            data["caption"] = pick_caption(make_proxy(data))
        return data

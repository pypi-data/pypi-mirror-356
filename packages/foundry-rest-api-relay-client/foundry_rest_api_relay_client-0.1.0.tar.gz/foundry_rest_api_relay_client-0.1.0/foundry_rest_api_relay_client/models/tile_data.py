from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.texture_data import TextureData


T = TypeVar("T", bound="TileData")


@_attrs_define
class TileData:
    """
    Attributes:
        field_id (Union[None, Unset, str]):
        alpha (Union[None, Unset, float]):
        elevation (Union[None, Unset, float]):
        height (Union[None, Unset, float]):
        hidden (Union[None, Unset, bool]):
        locked (Union[None, Unset, bool]):
        rotation (Union[None, Unset, float]):
        sort (Union[None, Unset, int]):
        texture (Union['TextureData', None, Unset]):
        width (Union[None, Unset, float]):
        x (Union[None, Unset, float]):
        y (Union[None, Unset, float]):
    """

    field_id: Union[None, Unset, str] = UNSET
    alpha: Union[None, Unset, float] = UNSET
    elevation: Union[None, Unset, float] = UNSET
    height: Union[None, Unset, float] = UNSET
    hidden: Union[None, Unset, bool] = UNSET
    locked: Union[None, Unset, bool] = UNSET
    rotation: Union[None, Unset, float] = UNSET
    sort: Union[None, Unset, int] = UNSET
    texture: Union["TextureData", None, Unset] = UNSET
    width: Union[None, Unset, float] = UNSET
    x: Union[None, Unset, float] = UNSET
    y: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.texture_data import TextureData

        field_id: Union[None, Unset, str]
        if isinstance(self.field_id, Unset):
            field_id = UNSET
        else:
            field_id = self.field_id

        alpha: Union[None, Unset, float]
        if isinstance(self.alpha, Unset):
            alpha = UNSET
        else:
            alpha = self.alpha

        elevation: Union[None, Unset, float]
        if isinstance(self.elevation, Unset):
            elevation = UNSET
        else:
            elevation = self.elevation

        height: Union[None, Unset, float]
        if isinstance(self.height, Unset):
            height = UNSET
        else:
            height = self.height

        hidden: Union[None, Unset, bool]
        if isinstance(self.hidden, Unset):
            hidden = UNSET
        else:
            hidden = self.hidden

        locked: Union[None, Unset, bool]
        if isinstance(self.locked, Unset):
            locked = UNSET
        else:
            locked = self.locked

        rotation: Union[None, Unset, float]
        if isinstance(self.rotation, Unset):
            rotation = UNSET
        else:
            rotation = self.rotation

        sort: Union[None, Unset, int]
        if isinstance(self.sort, Unset):
            sort = UNSET
        else:
            sort = self.sort

        texture: Union[None, Unset, dict[str, Any]]
        if isinstance(self.texture, Unset):
            texture = UNSET
        elif isinstance(self.texture, TextureData):
            texture = self.texture.to_dict()
        else:
            texture = self.texture

        width: Union[None, Unset, float]
        if isinstance(self.width, Unset):
            width = UNSET
        else:
            width = self.width

        x: Union[None, Unset, float]
        if isinstance(self.x, Unset):
            x = UNSET
        else:
            x = self.x

        y: Union[None, Unset, float]
        if isinstance(self.y, Unset):
            y = UNSET
        else:
            y = self.y

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_id is not UNSET:
            field_dict["_id"] = field_id
        if alpha is not UNSET:
            field_dict["alpha"] = alpha
        if elevation is not UNSET:
            field_dict["elevation"] = elevation
        if height is not UNSET:
            field_dict["height"] = height
        if hidden is not UNSET:
            field_dict["hidden"] = hidden
        if locked is not UNSET:
            field_dict["locked"] = locked
        if rotation is not UNSET:
            field_dict["rotation"] = rotation
        if sort is not UNSET:
            field_dict["sort"] = sort
        if texture is not UNSET:
            field_dict["texture"] = texture
        if width is not UNSET:
            field_dict["width"] = width
        if x is not UNSET:
            field_dict["x"] = x
        if y is not UNSET:
            field_dict["y"] = y

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.texture_data import TextureData

        d = dict(src_dict)

        def _parse_field_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        field_id = _parse_field_id(d.pop("_id", UNSET))

        def _parse_alpha(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        alpha = _parse_alpha(d.pop("alpha", UNSET))

        def _parse_elevation(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        elevation = _parse_elevation(d.pop("elevation", UNSET))

        def _parse_height(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        height = _parse_height(d.pop("height", UNSET))

        def _parse_hidden(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        hidden = _parse_hidden(d.pop("hidden", UNSET))

        def _parse_locked(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        locked = _parse_locked(d.pop("locked", UNSET))

        def _parse_rotation(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        rotation = _parse_rotation(d.pop("rotation", UNSET))

        def _parse_sort(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        sort = _parse_sort(d.pop("sort", UNSET))

        def _parse_texture(data: object) -> Union["TextureData", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                texture_type_0 = TextureData.from_dict(data)

                return texture_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TextureData", None, Unset], data)

        texture = _parse_texture(d.pop("texture", UNSET))

        def _parse_width(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        width = _parse_width(d.pop("width", UNSET))

        def _parse_x(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        x = _parse_x(d.pop("x", UNSET))

        def _parse_y(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        y = _parse_y(d.pop("y", UNSET))

        tile_data = cls(
            field_id=field_id,
            alpha=alpha,
            elevation=elevation,
            height=height,
            hidden=hidden,
            locked=locked,
            rotation=rotation,
            sort=sort,
            texture=texture,
            width=width,
            x=x,
            y=y,
        )

        tile_data.additional_properties = d
        return tile_data

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

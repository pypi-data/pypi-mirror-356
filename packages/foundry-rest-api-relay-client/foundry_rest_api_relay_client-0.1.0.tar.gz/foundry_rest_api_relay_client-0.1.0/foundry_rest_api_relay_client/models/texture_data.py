from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TextureData")


@_attrs_define
class TextureData:
    """
    Attributes:
        alpha_threshold (Union[None, Unset, float]):
        anchor_x (Union[None, Unset, float]):
        anchor_y (Union[None, Unset, float]):
        fit (Union[None, Unset, str]):
        offset_x (Union[None, Unset, float]):
        offset_y (Union[None, Unset, float]):
        rotation (Union[None, Unset, float]):
        scale_x (Union[None, Unset, float]):
        scale_y (Union[None, Unset, float]):
        src (Union[None, Unset, str]):
        tint (Union[None, Unset, str]):
    """

    alpha_threshold: Union[None, Unset, float] = UNSET
    anchor_x: Union[None, Unset, float] = UNSET
    anchor_y: Union[None, Unset, float] = UNSET
    fit: Union[None, Unset, str] = UNSET
    offset_x: Union[None, Unset, float] = UNSET
    offset_y: Union[None, Unset, float] = UNSET
    rotation: Union[None, Unset, float] = UNSET
    scale_x: Union[None, Unset, float] = UNSET
    scale_y: Union[None, Unset, float] = UNSET
    src: Union[None, Unset, str] = UNSET
    tint: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alpha_threshold: Union[None, Unset, float]
        if isinstance(self.alpha_threshold, Unset):
            alpha_threshold = UNSET
        else:
            alpha_threshold = self.alpha_threshold

        anchor_x: Union[None, Unset, float]
        if isinstance(self.anchor_x, Unset):
            anchor_x = UNSET
        else:
            anchor_x = self.anchor_x

        anchor_y: Union[None, Unset, float]
        if isinstance(self.anchor_y, Unset):
            anchor_y = UNSET
        else:
            anchor_y = self.anchor_y

        fit: Union[None, Unset, str]
        if isinstance(self.fit, Unset):
            fit = UNSET
        else:
            fit = self.fit

        offset_x: Union[None, Unset, float]
        if isinstance(self.offset_x, Unset):
            offset_x = UNSET
        else:
            offset_x = self.offset_x

        offset_y: Union[None, Unset, float]
        if isinstance(self.offset_y, Unset):
            offset_y = UNSET
        else:
            offset_y = self.offset_y

        rotation: Union[None, Unset, float]
        if isinstance(self.rotation, Unset):
            rotation = UNSET
        else:
            rotation = self.rotation

        scale_x: Union[None, Unset, float]
        if isinstance(self.scale_x, Unset):
            scale_x = UNSET
        else:
            scale_x = self.scale_x

        scale_y: Union[None, Unset, float]
        if isinstance(self.scale_y, Unset):
            scale_y = UNSET
        else:
            scale_y = self.scale_y

        src: Union[None, Unset, str]
        if isinstance(self.src, Unset):
            src = UNSET
        else:
            src = self.src

        tint: Union[None, Unset, str]
        if isinstance(self.tint, Unset):
            tint = UNSET
        else:
            tint = self.tint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if alpha_threshold is not UNSET:
            field_dict["alphaThreshold"] = alpha_threshold
        if anchor_x is not UNSET:
            field_dict["anchorX"] = anchor_x
        if anchor_y is not UNSET:
            field_dict["anchorY"] = anchor_y
        if fit is not UNSET:
            field_dict["fit"] = fit
        if offset_x is not UNSET:
            field_dict["offsetX"] = offset_x
        if offset_y is not UNSET:
            field_dict["offsetY"] = offset_y
        if rotation is not UNSET:
            field_dict["rotation"] = rotation
        if scale_x is not UNSET:
            field_dict["scaleX"] = scale_x
        if scale_y is not UNSET:
            field_dict["scaleY"] = scale_y
        if src is not UNSET:
            field_dict["src"] = src
        if tint is not UNSET:
            field_dict["tint"] = tint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_alpha_threshold(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        alpha_threshold = _parse_alpha_threshold(d.pop("alphaThreshold", UNSET))

        def _parse_anchor_x(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        anchor_x = _parse_anchor_x(d.pop("anchorX", UNSET))

        def _parse_anchor_y(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        anchor_y = _parse_anchor_y(d.pop("anchorY", UNSET))

        def _parse_fit(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        fit = _parse_fit(d.pop("fit", UNSET))

        def _parse_offset_x(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        offset_x = _parse_offset_x(d.pop("offsetX", UNSET))

        def _parse_offset_y(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        offset_y = _parse_offset_y(d.pop("offsetY", UNSET))

        def _parse_rotation(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        rotation = _parse_rotation(d.pop("rotation", UNSET))

        def _parse_scale_x(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        scale_x = _parse_scale_x(d.pop("scaleX", UNSET))

        def _parse_scale_y(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        scale_y = _parse_scale_y(d.pop("scaleY", UNSET))

        def _parse_src(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        src = _parse_src(d.pop("src", UNSET))

        def _parse_tint(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tint = _parse_tint(d.pop("tint", UNSET))

        texture_data = cls(
            alpha_threshold=alpha_threshold,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            fit=fit,
            offset_x=offset_x,
            offset_y=offset_y,
            rotation=rotation,
            scale_x=scale_x,
            scale_y=scale_y,
            src=src,
            tint=tint,
        )

        texture_data.additional_properties = d
        return texture_data

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

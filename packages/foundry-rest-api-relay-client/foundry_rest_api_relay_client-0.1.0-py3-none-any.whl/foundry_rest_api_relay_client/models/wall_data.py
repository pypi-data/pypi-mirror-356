from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WallData")


@_attrs_define
class WallData:
    """
    Attributes:
        field_id (Union[None, Unset, str]):
        c (Union[Unset, list[float]]):
        dir_ (Union[None, Unset, float]):
        door (Union[None, Unset, float]):
        door_sound (Union[None, Unset, str]):
        ds (Union[None, Unset, float]):
        light (Union[None, Unset, float]):
        move (Union[None, Unset, float]):
        sight (Union[None, Unset, float]):
        sound (Union[None, Unset, float]):
    """

    field_id: Union[None, Unset, str] = UNSET
    c: Union[Unset, list[float]] = UNSET
    dir_: Union[None, Unset, float] = UNSET
    door: Union[None, Unset, float] = UNSET
    door_sound: Union[None, Unset, str] = UNSET
    ds: Union[None, Unset, float] = UNSET
    light: Union[None, Unset, float] = UNSET
    move: Union[None, Unset, float] = UNSET
    sight: Union[None, Unset, float] = UNSET
    sound: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_id: Union[None, Unset, str]
        if isinstance(self.field_id, Unset):
            field_id = UNSET
        else:
            field_id = self.field_id

        c: Union[Unset, list[float]] = UNSET
        if not isinstance(self.c, Unset):
            c = self.c

        dir_: Union[None, Unset, float]
        if isinstance(self.dir_, Unset):
            dir_ = UNSET
        else:
            dir_ = self.dir_

        door: Union[None, Unset, float]
        if isinstance(self.door, Unset):
            door = UNSET
        else:
            door = self.door

        door_sound: Union[None, Unset, str]
        if isinstance(self.door_sound, Unset):
            door_sound = UNSET
        else:
            door_sound = self.door_sound

        ds: Union[None, Unset, float]
        if isinstance(self.ds, Unset):
            ds = UNSET
        else:
            ds = self.ds

        light: Union[None, Unset, float]
        if isinstance(self.light, Unset):
            light = UNSET
        else:
            light = self.light

        move: Union[None, Unset, float]
        if isinstance(self.move, Unset):
            move = UNSET
        else:
            move = self.move

        sight: Union[None, Unset, float]
        if isinstance(self.sight, Unset):
            sight = UNSET
        else:
            sight = self.sight

        sound: Union[None, Unset, float]
        if isinstance(self.sound, Unset):
            sound = UNSET
        else:
            sound = self.sound

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_id is not UNSET:
            field_dict["_id"] = field_id
        if c is not UNSET:
            field_dict["c"] = c
        if dir_ is not UNSET:
            field_dict["dir"] = dir_
        if door is not UNSET:
            field_dict["door"] = door
        if door_sound is not UNSET:
            field_dict["doorSound"] = door_sound
        if ds is not UNSET:
            field_dict["ds"] = ds
        if light is not UNSET:
            field_dict["light"] = light
        if move is not UNSET:
            field_dict["move"] = move
        if sight is not UNSET:
            field_dict["sight"] = sight
        if sound is not UNSET:
            field_dict["sound"] = sound

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_field_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        field_id = _parse_field_id(d.pop("_id", UNSET))

        c = cast(list[float], d.pop("c", UNSET))

        def _parse_dir_(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        dir_ = _parse_dir_(d.pop("dir", UNSET))

        def _parse_door(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        door = _parse_door(d.pop("door", UNSET))

        def _parse_door_sound(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        door_sound = _parse_door_sound(d.pop("doorSound", UNSET))

        def _parse_ds(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        ds = _parse_ds(d.pop("ds", UNSET))

        def _parse_light(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        light = _parse_light(d.pop("light", UNSET))

        def _parse_move(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        move = _parse_move(d.pop("move", UNSET))

        def _parse_sight(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        sight = _parse_sight(d.pop("sight", UNSET))

        def _parse_sound(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        sound = _parse_sound(d.pop("sound", UNSET))

        wall_data = cls(
            field_id=field_id,
            c=c,
            dir_=dir_,
            door=door,
            door_sound=door_sound,
            ds=ds,
            light=light,
            move=move,
            sight=sight,
            sound=sound,
        )

        wall_data.additional_properties = d
        return wall_data

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

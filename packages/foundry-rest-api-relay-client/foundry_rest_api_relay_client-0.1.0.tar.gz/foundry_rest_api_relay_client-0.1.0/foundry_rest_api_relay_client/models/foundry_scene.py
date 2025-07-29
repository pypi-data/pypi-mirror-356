from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.foundry_scene_ownership_type_0 import FoundrySceneOwnershipType0
    from ..models.tile_data import TileData
    from ..models.wall_data import WallData


T = TypeVar("T", bound="FoundryScene")


@_attrs_define
class FoundryScene:
    """
    Attributes:
        name (str):
        field_id (Union[None, Unset, str]):
        active (Union[None, Unset, bool]):
        navigation (Union[None, Unset, bool]):
        nav_name (Union[None, Unset, str]):
        nav_order (Union[None, Unset, int]):
        ownership (Union['FoundrySceneOwnershipType0', None, Unset]):
        tiles (Union[Unset, list['TileData']]):
        walls (Union[Unset, list['WallData']]):
    """

    name: str
    field_id: Union[None, Unset, str] = UNSET
    active: Union[None, Unset, bool] = UNSET
    navigation: Union[None, Unset, bool] = UNSET
    nav_name: Union[None, Unset, str] = UNSET
    nav_order: Union[None, Unset, int] = UNSET
    ownership: Union["FoundrySceneOwnershipType0", None, Unset] = UNSET
    tiles: Union[Unset, list["TileData"]] = UNSET
    walls: Union[Unset, list["WallData"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.foundry_scene_ownership_type_0 import FoundrySceneOwnershipType0

        name = self.name

        field_id: Union[None, Unset, str]
        if isinstance(self.field_id, Unset):
            field_id = UNSET
        else:
            field_id = self.field_id

        active: Union[None, Unset, bool]
        if isinstance(self.active, Unset):
            active = UNSET
        else:
            active = self.active

        navigation: Union[None, Unset, bool]
        if isinstance(self.navigation, Unset):
            navigation = UNSET
        else:
            navigation = self.navigation

        nav_name: Union[None, Unset, str]
        if isinstance(self.nav_name, Unset):
            nav_name = UNSET
        else:
            nav_name = self.nav_name

        nav_order: Union[None, Unset, int]
        if isinstance(self.nav_order, Unset):
            nav_order = UNSET
        else:
            nav_order = self.nav_order

        ownership: Union[None, Unset, dict[str, Any]]
        if isinstance(self.ownership, Unset):
            ownership = UNSET
        elif isinstance(self.ownership, FoundrySceneOwnershipType0):
            ownership = self.ownership.to_dict()
        else:
            ownership = self.ownership

        tiles: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tiles, Unset):
            tiles = []
            for tiles_item_data in self.tiles:
                tiles_item = tiles_item_data.to_dict()
                tiles.append(tiles_item)

        walls: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.walls, Unset):
            walls = []
            for walls_item_data in self.walls:
                walls_item = walls_item_data.to_dict()
                walls.append(walls_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if field_id is not UNSET:
            field_dict["_id"] = field_id
        if active is not UNSET:
            field_dict["active"] = active
        if navigation is not UNSET:
            field_dict["navigation"] = navigation
        if nav_name is not UNSET:
            field_dict["navName"] = nav_name
        if nav_order is not UNSET:
            field_dict["navOrder"] = nav_order
        if ownership is not UNSET:
            field_dict["ownership"] = ownership
        if tiles is not UNSET:
            field_dict["tiles"] = tiles
        if walls is not UNSET:
            field_dict["walls"] = walls

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.foundry_scene_ownership_type_0 import FoundrySceneOwnershipType0
        from ..models.tile_data import TileData
        from ..models.wall_data import WallData

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_field_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        field_id = _parse_field_id(d.pop("_id", UNSET))

        def _parse_active(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        active = _parse_active(d.pop("active", UNSET))

        def _parse_navigation(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        navigation = _parse_navigation(d.pop("navigation", UNSET))

        def _parse_nav_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        nav_name = _parse_nav_name(d.pop("navName", UNSET))

        def _parse_nav_order(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        nav_order = _parse_nav_order(d.pop("navOrder", UNSET))

        def _parse_ownership(data: object) -> Union["FoundrySceneOwnershipType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ownership_type_0 = FoundrySceneOwnershipType0.from_dict(data)

                return ownership_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FoundrySceneOwnershipType0", None, Unset], data)

        ownership = _parse_ownership(d.pop("ownership", UNSET))

        tiles = []
        _tiles = d.pop("tiles", UNSET)
        for tiles_item_data in _tiles or []:
            tiles_item = TileData.from_dict(tiles_item_data)

            tiles.append(tiles_item)

        walls = []
        _walls = d.pop("walls", UNSET)
        for walls_item_data in _walls or []:
            walls_item = WallData.from_dict(walls_item_data)

            walls.append(walls_item)

        foundry_scene = cls(
            name=name,
            field_id=field_id,
            active=active,
            navigation=navigation,
            nav_name=nav_name,
            nav_order=nav_order,
            ownership=ownership,
            tiles=tiles,
            walls=walls,
        )

        foundry_scene.additional_properties = d
        return foundry_scene

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

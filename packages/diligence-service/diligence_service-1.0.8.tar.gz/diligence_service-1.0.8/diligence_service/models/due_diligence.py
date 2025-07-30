import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DueDiligence")


@_attrs_define
class DueDiligence:
    """Schema for reading due diligence data."""

    due_diligence_id: UUID
    project_id: int
    data_pool_location: Union[None, Unset, str] = UNSET
    data_storage_type: Union[None, Unset, str] = UNSET
    vectorstore_location: Union[None, Unset, str] = UNSET
    owner: Union[None, Unset, str] = UNSET
    start_date: Union[None, Unset, datetime.datetime] = UNSET
    end_date: Union[None, Unset, datetime.datetime] = UNSET
    status: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        due_diligence_id = str(self.due_diligence_id)

        project_id = self.project_id

        data_pool_location: Union[None, Unset, str]
        if isinstance(self.data_pool_location, Unset):
            data_pool_location = UNSET
        else:
            data_pool_location = self.data_pool_location

        data_storage_type: Union[None, Unset, str]
        if isinstance(self.data_storage_type, Unset):
            data_storage_type = UNSET
        else:
            data_storage_type = self.data_storage_type

        vectorstore_location: Union[None, Unset, str]
        if isinstance(self.vectorstore_location, Unset):
            vectorstore_location = UNSET
        else:
            vectorstore_location = self.vectorstore_location

        owner: Union[None, Unset, str]
        if isinstance(self.owner, Unset):
            owner = UNSET
        else:
            owner = self.owner

        start_date: Union[None, Unset, str]
        if isinstance(self.start_date, Unset):
            start_date = UNSET
        elif isinstance(self.start_date, datetime.datetime):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date

        end_date: Union[None, Unset, str]
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.datetime):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        status: Union[None, Unset, str]
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "due_diligence_id": due_diligence_id,
                "project_id": project_id,
            }
        )
        if data_pool_location is not UNSET:
            field_dict["data_pool_location"] = data_pool_location
        if data_storage_type is not UNSET:
            field_dict["data_storage_type"] = data_storage_type
        if vectorstore_location is not UNSET:
            field_dict["vectorstore_location"] = vectorstore_location
        if owner is not UNSET:
            field_dict["owner"] = owner
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        due_diligence_id = UUID(d.pop("due_diligence_id"))

        project_id = d.pop("project_id")

        def _parse_data_pool_location(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        data_pool_location = _parse_data_pool_location(d.pop("data_pool_location", UNSET))

        def _parse_data_storage_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        data_storage_type = _parse_data_storage_type(d.pop("data_storage_type", UNSET))

        def _parse_vectorstore_location(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        vectorstore_location = _parse_vectorstore_location(d.pop("vectorstore_location", UNSET))

        def _parse_owner(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        owner = _parse_owner(d.pop("owner", UNSET))

        def _parse_start_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = isoparse(data)

                return start_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        start_date = _parse_start_date(d.pop("start_date", UNSET))

        def _parse_end_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data)

                return end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        end_date = _parse_end_date(d.pop("end_date", UNSET))

        def _parse_status(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        status = _parse_status(d.pop("status", UNSET))

        due_diligence = cls(
            due_diligence_id=due_diligence_id,
            project_id=project_id,
            data_pool_location=data_pool_location,
            data_storage_type=data_storage_type,
            vectorstore_location=vectorstore_location,
            owner=owner,
            start_date=start_date,
            end_date=end_date,
            status=status,
        )

        due_diligence.additional_properties = d
        return due_diligence

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

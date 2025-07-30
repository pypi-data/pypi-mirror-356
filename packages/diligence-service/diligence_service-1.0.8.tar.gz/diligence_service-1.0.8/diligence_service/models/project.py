import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Project")


@_attrs_define
class Project:
    project_id: int
    project_name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    owner: Union[None, Unset, str] = UNSET
    indication: Union[None, Unset, str] = UNSET
    target: Union[None, Unset, str] = UNSET
    drugname: Union[None, Unset, str] = UNSET
    moa: Union[None, Unset, str] = UNSET
    development_stage: Union[None, Unset, str] = UNSET
    pathway: Union[None, Unset, str] = UNSET
    asset_type: Union[None, Unset, str] = UNSET
    company: Union[None, Unset, str] = UNSET
    company_logo: Union[None, Unset, str] = UNSET
    scenario_npv: Union[None, Unset, str] = UNSET
    scenario_total_ptrs: Union[None, Unset, str] = UNSET
    scenario_total_cycle_time: Union[None, Unset, str] = UNSET
    scenario_total_cost: Union[None, Unset, str] = UNSET
    start_date: Union[None, Unset, datetime.date] = UNSET
    end_date: Union[None, Unset, datetime.date] = UNSET
    created_date: Union[None, Unset, datetime.datetime] = UNSET
    updated_date: Union[None, Unset, datetime.datetime] = UNSET
    created_by: Union[None, Unset, str] = UNSET
    updated_by: Union[None, Unset, str] = UNSET
    drug_due_diligence_enabled: Union[None, Unset, bool] = True
    valuation_risk_simulation_enabled: Union[None, Unset, bool] = True
    skip_drug_due_diligence: Union[None, Unset, bool] = False
    skip_valuation_risk_simulation: Union[None, Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        project_name: Union[None, Unset, str]
        if isinstance(self.project_name, Unset):
            project_name = UNSET
        else:
            project_name = self.project_name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        owner: Union[None, Unset, str]
        if isinstance(self.owner, Unset):
            owner = UNSET
        else:
            owner = self.owner

        indication: Union[None, Unset, str]
        if isinstance(self.indication, Unset):
            indication = UNSET
        else:
            indication = self.indication

        target: Union[None, Unset, str]
        if isinstance(self.target, Unset):
            target = UNSET
        else:
            target = self.target

        drugname: Union[None, Unset, str]
        if isinstance(self.drugname, Unset):
            drugname = UNSET
        else:
            drugname = self.drugname

        moa: Union[None, Unset, str]
        if isinstance(self.moa, Unset):
            moa = UNSET
        else:
            moa = self.moa

        development_stage: Union[None, Unset, str]
        if isinstance(self.development_stage, Unset):
            development_stage = UNSET
        else:
            development_stage = self.development_stage

        pathway: Union[None, Unset, str]
        if isinstance(self.pathway, Unset):
            pathway = UNSET
        else:
            pathway = self.pathway

        asset_type: Union[None, Unset, str]
        if isinstance(self.asset_type, Unset):
            asset_type = UNSET
        else:
            asset_type = self.asset_type

        company: Union[None, Unset, str]
        if isinstance(self.company, Unset):
            company = UNSET
        else:
            company = self.company

        company_logo: Union[None, Unset, str]
        if isinstance(self.company_logo, Unset):
            company_logo = UNSET
        else:
            company_logo = self.company_logo

        scenario_npv: Union[None, Unset, str]
        if isinstance(self.scenario_npv, Unset):
            scenario_npv = UNSET
        else:
            scenario_npv = self.scenario_npv

        scenario_total_ptrs: Union[None, Unset, str]
        if isinstance(self.scenario_total_ptrs, Unset):
            scenario_total_ptrs = UNSET
        else:
            scenario_total_ptrs = self.scenario_total_ptrs

        scenario_total_cycle_time: Union[None, Unset, str]
        if isinstance(self.scenario_total_cycle_time, Unset):
            scenario_total_cycle_time = UNSET
        else:
            scenario_total_cycle_time = self.scenario_total_cycle_time

        scenario_total_cost: Union[None, Unset, str]
        if isinstance(self.scenario_total_cost, Unset):
            scenario_total_cost = UNSET
        else:
            scenario_total_cost = self.scenario_total_cost

        start_date: Union[None, Unset, str]
        if isinstance(self.start_date, Unset):
            start_date = UNSET
        elif isinstance(self.start_date, datetime.date):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date

        end_date: Union[None, Unset, str]
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.date):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        created_date: Union[None, Unset, str]
        if isinstance(self.created_date, Unset):
            created_date = UNSET
        elif isinstance(self.created_date, datetime.datetime):
            created_date = self.created_date.isoformat()
        else:
            created_date = self.created_date

        updated_date: Union[None, Unset, str]
        if isinstance(self.updated_date, Unset):
            updated_date = UNSET
        elif isinstance(self.updated_date, datetime.datetime):
            updated_date = self.updated_date.isoformat()
        else:
            updated_date = self.updated_date

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        updated_by: Union[None, Unset, str]
        if isinstance(self.updated_by, Unset):
            updated_by = UNSET
        else:
            updated_by = self.updated_by

        drug_due_diligence_enabled: Union[None, Unset, bool]
        if isinstance(self.drug_due_diligence_enabled, Unset):
            drug_due_diligence_enabled = UNSET
        else:
            drug_due_diligence_enabled = self.drug_due_diligence_enabled

        valuation_risk_simulation_enabled: Union[None, Unset, bool]
        if isinstance(self.valuation_risk_simulation_enabled, Unset):
            valuation_risk_simulation_enabled = UNSET
        else:
            valuation_risk_simulation_enabled = self.valuation_risk_simulation_enabled

        skip_drug_due_diligence: Union[None, Unset, bool]
        if isinstance(self.skip_drug_due_diligence, Unset):
            skip_drug_due_diligence = UNSET
        else:
            skip_drug_due_diligence = self.skip_drug_due_diligence

        skip_valuation_risk_simulation: Union[None, Unset, bool]
        if isinstance(self.skip_valuation_risk_simulation, Unset):
            skip_valuation_risk_simulation = UNSET
        else:
            skip_valuation_risk_simulation = self.skip_valuation_risk_simulation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
            }
        )
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if description is not UNSET:
            field_dict["description"] = description
        if owner is not UNSET:
            field_dict["owner"] = owner
        if indication is not UNSET:
            field_dict["indication"] = indication
        if target is not UNSET:
            field_dict["target"] = target
        if drugname is not UNSET:
            field_dict["drugname"] = drugname
        if moa is not UNSET:
            field_dict["moa"] = moa
        if development_stage is not UNSET:
            field_dict["development_stage"] = development_stage
        if pathway is not UNSET:
            field_dict["pathway"] = pathway
        if asset_type is not UNSET:
            field_dict["asset_type"] = asset_type
        if company is not UNSET:
            field_dict["company"] = company
        if company_logo is not UNSET:
            field_dict["company_logo"] = company_logo
        if scenario_npv is not UNSET:
            field_dict["scenario_npv"] = scenario_npv
        if scenario_total_ptrs is not UNSET:
            field_dict["scenario_total_ptrs"] = scenario_total_ptrs
        if scenario_total_cycle_time is not UNSET:
            field_dict["scenario_total_cycle_time"] = scenario_total_cycle_time
        if scenario_total_cost is not UNSET:
            field_dict["scenario_total_cost"] = scenario_total_cost
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if created_date is not UNSET:
            field_dict["created_date"] = created_date
        if updated_date is not UNSET:
            field_dict["updated_date"] = updated_date
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if drug_due_diligence_enabled is not UNSET:
            field_dict["drug_due_diligence_enabled"] = drug_due_diligence_enabled
        if valuation_risk_simulation_enabled is not UNSET:
            field_dict["valuation_risk_simulation_enabled"] = valuation_risk_simulation_enabled
        if skip_drug_due_diligence is not UNSET:
            field_dict["skip_drug_due_diligence"] = skip_drug_due_diligence
        if skip_valuation_risk_simulation is not UNSET:
            field_dict["skip_valuation_risk_simulation"] = skip_valuation_risk_simulation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        def _parse_project_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_name = _parse_project_name(d.pop("project_name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_owner(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        owner = _parse_owner(d.pop("owner", UNSET))

        def _parse_indication(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        indication = _parse_indication(d.pop("indication", UNSET))

        def _parse_target(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        target = _parse_target(d.pop("target", UNSET))

        def _parse_drugname(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        drugname = _parse_drugname(d.pop("drugname", UNSET))

        def _parse_moa(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        moa = _parse_moa(d.pop("moa", UNSET))

        def _parse_development_stage(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        development_stage = _parse_development_stage(d.pop("development_stage", UNSET))

        def _parse_pathway(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pathway = _parse_pathway(d.pop("pathway", UNSET))

        def _parse_asset_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        asset_type = _parse_asset_type(d.pop("asset_type", UNSET))

        def _parse_company(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        company = _parse_company(d.pop("company", UNSET))

        def _parse_company_logo(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        company_logo = _parse_company_logo(d.pop("company_logo", UNSET))

        def _parse_scenario_npv(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        scenario_npv = _parse_scenario_npv(d.pop("scenario_npv", UNSET))

        def _parse_scenario_total_ptrs(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        scenario_total_ptrs = _parse_scenario_total_ptrs(d.pop("scenario_total_ptrs", UNSET))

        def _parse_scenario_total_cycle_time(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        scenario_total_cycle_time = _parse_scenario_total_cycle_time(d.pop("scenario_total_cycle_time", UNSET))

        def _parse_scenario_total_cost(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        scenario_total_cost = _parse_scenario_total_cost(d.pop("scenario_total_cost", UNSET))

        def _parse_start_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = isoparse(data).date()

                return start_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        start_date = _parse_start_date(d.pop("start_date", UNSET))

        def _parse_end_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data).date()

                return end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        end_date = _parse_end_date(d.pop("end_date", UNSET))

        def _parse_created_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_date_type_0 = isoparse(data)

                return created_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_date = _parse_created_date(d.pop("created_date", UNSET))

        def _parse_updated_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_date_type_0 = isoparse(data)

                return updated_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_date = _parse_updated_date(d.pop("updated_date", UNSET))

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_updated_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        updated_by = _parse_updated_by(d.pop("updated_by", UNSET))

        def _parse_drug_due_diligence_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        drug_due_diligence_enabled = _parse_drug_due_diligence_enabled(d.pop("drug_due_diligence_enabled", UNSET))

        def _parse_valuation_risk_simulation_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        valuation_risk_simulation_enabled = _parse_valuation_risk_simulation_enabled(
            d.pop("valuation_risk_simulation_enabled", UNSET)
        )

        def _parse_skip_drug_due_diligence(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        skip_drug_due_diligence = _parse_skip_drug_due_diligence(d.pop("skip_drug_due_diligence", UNSET))

        def _parse_skip_valuation_risk_simulation(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        skip_valuation_risk_simulation = _parse_skip_valuation_risk_simulation(
            d.pop("skip_valuation_risk_simulation", UNSET)
        )

        project = cls(
            project_id=project_id,
            project_name=project_name,
            description=description,
            owner=owner,
            indication=indication,
            target=target,
            drugname=drugname,
            moa=moa,
            development_stage=development_stage,
            pathway=pathway,
            asset_type=asset_type,
            company=company,
            company_logo=company_logo,
            scenario_npv=scenario_npv,
            scenario_total_ptrs=scenario_total_ptrs,
            scenario_total_cycle_time=scenario_total_cycle_time,
            scenario_total_cost=scenario_total_cost,
            start_date=start_date,
            end_date=end_date,
            created_date=created_date,
            updated_date=updated_date,
            created_by=created_by,
            updated_by=updated_by,
            drug_due_diligence_enabled=drug_due_diligence_enabled,
            valuation_risk_simulation_enabled=valuation_risk_simulation_enabled,
            skip_drug_due_diligence=skip_drug_due_diligence,
            skip_valuation_risk_simulation=skip_valuation_risk_simulation,
        )

        project.additional_properties = d
        return project

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

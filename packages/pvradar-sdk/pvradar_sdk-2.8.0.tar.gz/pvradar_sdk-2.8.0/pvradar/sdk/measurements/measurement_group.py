from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional, Self, override

import pandas as pd
from pvlib.location import Location

from ..client.pvradar_site import PvradarSite
from ..client.api_query import Query
from ..client.client import PvradarClient
from ..pv.design import PvradarSiteDesign, make_fixed_design, make_tracker_design
from ..modeling.utils import attrs_as_descriptor_mapping, is_attrs_convertible, convert_by_attrs
from ..modeling.basics import ResourceRecord
from ..common.pandas_utils import is_series_or_frame


fixed_design_spec_resource_type = 'fixed_design_spec'
tracker_design_spec_resource_type = 'tracker_design_spec'


class AbstractMeasurementGroup(PvradarSite, ABC):
    def __init__(
        self,
        id: str,
        *,
        location: Optional[Location | tuple | str] = None,
        interval: Optional[Any] = None,
        default_tz: Optional[str] = None,
        design: Optional[PvradarSiteDesign] = None,
        **kwargs,
    ):
        self.measurement_group_id = id
        super().__init__(location=location, interval=interval, default_tz=default_tz, design=design, **kwargs)

    @override
    def __repr__(self):
        response = self.__class__.__name__ + ' ' + self.measurement_group_id
        if 'location' in self:
            response += f' at {self.location}'
        if 'interval' in self:
            response += f' with interval {self.interval}'
        return response

    @override
    def copy(self: Self) -> Self:
        c = self.__class__(id=self.measurement_group_id)
        self._copy_self(c)
        return c

    @abstractmethod
    def measurement(self, subject: Any) -> Any:
        raise NotImplementedError()


class MeasurementGroup(AbstractMeasurementGroup):
    def __init__(
        self,
        id: str,
        *,
        location: Optional[Location | tuple | str] = None,
        interval: Optional[Any] = None,
        default_tz: Optional[str] = None,
        design: Optional[PvradarSiteDesign] = None,
        **kwargs,
    ):
        self.measurement_group_id = id
        location_resource = self.measurement('location')
        location = (location_resource['latitude'], location_resource['longitude'])
        interval_resource = self.measurement('interval')
        min_timestamp, max_timestamp = tuple(map(pd.Timestamp, interval_resource.split('..')))
        interval = pd.Interval(min_timestamp, max_timestamp)

        self._resource_type_map = self._get_resource_record_list()

        if 'fixed_design_spec' in self._resource_type_map:
            fixed_design_spec_resource = self.measurement(fixed_design_spec_resource_type)
            design = make_fixed_design(**fixed_design_spec_resource)
        elif 'tracker_design_spec' in self._resource_type_map:
            tracker_design_spec_resource = self.measurement('tracker_design_spec')
            design = make_tracker_design(**tracker_design_spec_resource)
        super().__init__(id=id, location=location, interval=interval, default_tz=default_tz, design=design, **kwargs)

    def _get_resource_record_list(self) -> Mapping[str, ResourceRecord]:
        parsed = PvradarClient.instance().get_json(
            Query(
                path=f'/measurements/groups/{self.measurement_group_id}/resources',
                provider='dock',
            )
        )
        result: dict[str, ResourceRecord] = {}
        for record in parsed['data']:
            result[record['resource_type']] = ResourceRecord(**record)
        return result

    @override
    def measurement(self, subject: Any, label: Optional[str] = None) -> Any:
        if isinstance(subject, str):
            user_defined_attrs = None
            resource_type = subject
        elif is_attrs_convertible(subject):
            user_defined_attrs = dict(attrs_as_descriptor_mapping(subject))
            resource_type = user_defined_attrs['resource_type']
        else:
            raise ValueError('Unsupported subject type: ' + str(subject))
        resource = PvradarClient.instance().get_data_case(
            Query(
                path=f'/measurements/groups/{self.measurement_group_id}/resources/{resource_type}',
                provider='dock',
            )
        )
        result = convert_by_attrs(resource, user_defined_attrs) if user_defined_attrs else resource
        if label and is_series_or_frame(result):
            result.attrs['label'] = label
        return result

from os import getcwd
from os.path import join
from pathlib import Path
from typing import Optional, Any, override

import pandas as pd

from . import fixed_design_spec_resource_type, tracker_design_spec_resource_type, AbstractMeasurementGroup
from .. import PvradarLocation, PvradarSiteDesign, make_fixed_design, make_tracker_design
from ..common.op_pipeline import StdExecutor
from ..common.settings import SdkSettings
from ..common.source import LocalSource
from ..modeling.utils import is_attrs_convertible, attrs_as_descriptor_mapping, convert_by_attrs


class LocalMeasurementGroup(AbstractMeasurementGroup):
    def __init__(
        self,
        source: str | Path | LocalSource,
        id: Optional[str] = None,
        *,
        location: Optional[PvradarLocation] = None,
        interval: Optional[str] = None,
        default_tz: Optional[str] = None,
        design: Optional[PvradarSiteDesign] = None,
        **kwargs,
    ):
        if isinstance(source, LocalSource):
            manifest = source.get_measurement_manifest()
            if manifest is None:
                raise ValueError(
                    f'Invalid LocalSource provided for local measurement group: "{source}". '
                    'It must contain a valid measurement manifest file.'
                )
            self.manifest = manifest
            self.source = source
        else:
            # try 1: `source` is a valid absolute or relative to cwd path
            self.source = LocalSource(source)
            manifest = self.source.get_measurement_manifest()
            sources_path = SdkSettings.instance().sources_path
            if manifest is None:
                # try 2: `source` is a relative path to the configured sources path
                if sources_path is not None:
                    self.source = LocalSource(join(sources_path, source))
                    manifest = self.source.get_measurement_manifest()
            if manifest is None:
                # try 3: `source` is a relative to cwd path passed to LocalSource as an absolute path
                self.source = LocalSource(join(getcwd(), source))
                manifest = self.source.get_measurement_manifest()
            if manifest is None:
                raise ValueError(
                    'Invalid directory path for local measurement group: "'
                    + str(source)
                    + f'". It must be an absolute path or a relative path to the current working directory "{getcwd()}"'
                    + (f' or to "{sources_path}"' if sources_path else '.')
                )
            self.manifest = manifest
        recipes = self.manifest.recipes
        source_dir_name = self.source.dir.name
        grouped = any(
            recipe.get('measurement_group_id') is not None and recipe.get('measurement_group_id') != source_dir_name
            for recipe in manifest.recipes
        )
        if id is None:
            if grouped:
                raise ValueError(
                    'Measurement group ID must be provided when recipes are grouped by custom measurement_group_id.'
                )
            id = self.source.dir.name
        if not grouped:
            for recipe in manifest.recipes:
                recipe['measurement_group_id'] = id
        self.executor = StdExecutor().register_op(self.source.to_op())
        if isinstance(recipes, list) and len(recipes) > 0:
            design_recipe = None
            design_maker = None
            for recipe in recipes:
                resource_type = recipe.get('resource_type')
                measurement_group_id = recipe.get('measurement_group_id')
                if resource_type == 'location':
                    if measurement_group_id == id or measurement_group_id is None:
                        location_json = self.executor.execute(ops=recipe.get('ops', []))
                        location = PvradarLocation(
                            latitude=location_json.get('latitude'), longitude=location_json.get('longitude')
                        )
                elif resource_type == fixed_design_spec_resource_type:
                    if measurement_group_id == id or measurement_group_id is None:
                        design_recipe = recipe
                        design_maker = make_fixed_design
                elif resource_type == tracker_design_spec_resource_type:
                    if measurement_group_id == id or measurement_group_id is None:
                        design_recipe = recipe
                        design_maker = make_tracker_design
            if design_recipe is not None and design_maker is not None:
                design = design_maker(**self.executor.execute(ops=design_recipe.get('ops', [])))
        super().__init__(
            id=id,
            location=location,
            interval=interval,
            default_tz=default_tz,
            design=design,
            **kwargs,
        )

    @override
    def measurement(self, subject: Any) -> Any:
        if isinstance(subject, str):
            resource_type = subject
            attrs = {'resource_type': resource_type}
        elif is_attrs_convertible(subject):
            attrs = dict(attrs_as_descriptor_mapping(subject))
            resource_type = attrs.get('resource_type', None)
        else:
            raise ValueError('Unsupported subject type for local measurement group: ' + str(subject))
        if resource_type is None:
            raise ValueError('Resource type is required for local measurement group.')
        recipes = self.manifest.recipes
        for recipe in recipes:
            if recipe.get('resource_type') == resource_type and (
                recipe.get('measurement_group_id') == self.measurement_group_id or recipe.get('measurement_group_id') is None
            ):
                series = self.executor.execute(ops=recipe.get('ops', []))
                if isinstance(series, (pd.Series, pd.DataFrame)):
                    series.attrs = dict(attrs_as_descriptor_mapping(recipe.get('attrs', {})))  # pyright: ignore [reportAttributeAccessIssue]
                    series = convert_by_attrs(series, attrs)
                    series.attrs.update(attrs)
                return series
        raise ValueError(
            f'No measurement found for resource type "{resource_type}" in local measurement group "{self.measurement_group_id}".'
        )

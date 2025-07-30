# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Copyright (c) 2024-2025 Mira Geoscience Ltd.                                     '
#                                                                                   '
#  This file is part of peak-finder-app package.                                    '
#                                                                                   '
#  peak-finder-app is distributed under the terms and conditions of the MIT License '
#  (see LICENSE file at the root of this source code package).                      '
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from __future__ import annotations

import string
from copy import deepcopy

import numpy as np
from geoapps_utils.driver.params import BaseParams
from geoh5py import Workspace
from geoh5py.data import Data, ReferencedData
from geoh5py.groups import PropertyGroup, UIJsonGroup
from geoh5py.objects import Curve
from geoh5py.ui_json import InputFile
from geoh5py.ui_json.utils import fetch_active_workspace
from peak_finder.constants import default_ui_json, defaults, validations


class PeakFinderParams(BaseParams):  # pylint: disable=R0902, R0904
    """
    Parameter class for peak finder application.
    """

    def __init__(self, input_file: InputFile | None = None, **kwargs):
        self._default_ui_json: dict | None = deepcopy(default_ui_json)
        self._defaults: dict | None = deepcopy(defaults)
        self._free_parameter_keys: list = ["data", "color"]
        self._free_parameter_identifier: str = "group"
        self._validations: dict | None = validations
        self._objects: Curve | None = None
        self._line_field: ReferencedData | None = None
        self._flip_sign: bool = False
        self._masking_data: Data | None = None
        self._smoothing: int = 0
        self._min_amplitude: int = 1
        self._min_value: float = -np.inf
        self._min_width: float = 0.0
        self._max_migration: float = np.inf
        self._min_channels: int = 1
        self._n_groups: int = 1
        self._max_separation: float = np.inf
        self._ga_group_name: str | None = None
        self._structural_markers: bool | None = None
        self._trend_lines: bool | None = None
        self._line_id: int | None = None
        self._group_a_data: PropertyGroup | None = None
        self._group_a_color: str | None = None
        self._group_b_data: PropertyGroup | None = None
        self._group_b_color: str | None = None
        self._group_c_data: PropertyGroup | None = None
        self._group_c_color: str | None = None
        self._group_d_data: PropertyGroup | None = None
        self._group_d_color: str | None = None
        self._group_e_data: PropertyGroup | None = None
        self._group_e_color: str | None = None
        self._group_f_data: PropertyGroup | None = None
        self._group_f_color: str | None = None
        self._property_groups: dict | None = None
        self._template_data: Data | None = None
        self._template_color: str | None = None
        self._plot_result: bool = True
        self._survey: Curve | None = None
        self._title: str | None = None
        self._temp_workspace: Workspace | None = None
        self._out_group: UIJsonGroup | None = None

        if input_file is None:
            ui_json = deepcopy(self._default_ui_json)
            input_file = InputFile(
                ui_json=ui_json,
                validations=self.validations,
                validate=False,
            )
        super().__init__(input_file=input_file, **kwargs)

    @property
    def conda_environment(self):
        return self._conda_environment

    @conda_environment.setter
    def conda_environment(self, val):
        self.setter_validator("conda_environment", val)

    @property
    def conda_environment_boolean(self):
        return self._conda_environment_boolean

    @conda_environment_boolean.setter
    def conda_environment_boolean(self, val):
        self.setter_validator("conda_environment_boolean", val)

    @property
    def flip_sign(self) -> bool:
        """
        Flip sign of data.
        """
        return self._flip_sign

    @flip_sign.setter
    def flip_sign(self, val):
        self.setter_validator("flip_sign", val)

    @property
    def ga_group_name(self) -> str | None:
        """
        Name of group to save results to.
        """
        return self._ga_group_name

    @ga_group_name.setter
    def ga_group_name(self, val):
        self.setter_validator("ga_group_name", val)

    @property
    def line_field(self) -> ReferencedData | None:
        """
        Object containing line ids and associated names.
        """
        return self._line_field

    @line_field.setter
    def line_field(self, val):
        self.setter_validator("line_field", val, fun=self._uuid_promoter)

    @property
    def masking_data(self) -> Data | None:
        """
        Mask object to focus peak finding within an area of interest.
        """
        return self._masking_data

    @masking_data.setter
    def masking_data(self, val):
        self.setter_validator("masking_data", val)

    @property
    def line_id(self) -> int | None:
        """
        Index of the currently selected line.
        """
        return self._line_id

    @line_id.setter
    def line_id(self, val):
        self.setter_validator("line_id", val)

    @property
    def max_migration(self) -> float:
        """
        Threshold on the lateral shift (m) of peaks within a grouping of anomalies.
        """
        return self._max_migration

    @max_migration.setter
    def max_migration(self, val):
        self.setter_validator("max_migration", val)

    @property
    def min_amplitude(self) -> int:
        """
        Threshold on the minimum amplitude of the anomaly, expressed as
        a percent of the height scaled by the minimum value.
        """
        return self._min_amplitude

    @min_amplitude.setter
    def min_amplitude(self, val):
        self.setter_validator("min_amplitude", val)

    @property
    def min_channels(self) -> int:
        """
        Minimum number of data channels required to form a group.
        """
        return self._min_channels

    @min_channels.setter
    def min_channels(self, val):
        self.setter_validator("min_channels", val)

    @property
    def min_value(self) -> float:
        """
        Minimum absolute data value to be considered for anomaly detection.
        """
        return self._min_value

    @min_value.setter
    def min_value(self, val):
        self.setter_validator("min_value", val)

    @property
    def min_width(self) -> float:
        """
        Minimum anomaly width (m) measured between start and end of bounding minima.
        """
        return self._min_width

    @min_width.setter
    def min_width(self, val):
        self.setter_validator("min_width", val)

    @property
    def monitoring_directory(self) -> str | None:
        """
        Monitoring directory path.
        """
        return self._monitoring_directory

    @monitoring_directory.setter
    def monitoring_directory(self, val):
        self.setter_validator("monitoring_directory", val)

    @property
    def objects(self) -> Curve | None:
        """
        Objects to use for line profile.
        """
        return self._objects

    @objects.setter
    def objects(self, val):
        self.setter_validator("objects", val, fun=self._uuid_promoter)

    @property
    def out_group(self) -> UIJsonGroup | None:
        """
        UIJson group to use store results.
        """
        return self._out_group

    @out_group.setter
    def out_group(self, val):
        self.setter_validator("out_group", val, fun=self._uuid_promoter)

    @property
    def plot_result(self):
        return self._plot_result

    @plot_result.setter
    def plot_result(self, val):
        self._plot_result = val

    @property
    def smoothing(self) -> int:
        """
        Number of neighbors used in running mean smoothing.
        """
        return self._smoothing

    @smoothing.setter
    def smoothing(self, val):
        self.setter_validator("smoothing", val)

    @property
    def trend_lines(self) -> bool | None:
        """
        Create trend lines.
        """
        return self._trend_lines

    @trend_lines.setter
    def trend_lines(self, val):
        self.setter_validator("trend_lines", val)

    @property
    def n_groups(self) -> int:
        """
        Number of consecutive peaks to merge into a single anomaly.
        """
        return self._n_groups

    @n_groups.setter
    def n_groups(self, val):
        self.setter_validator("n_groups", val)

    @property
    def max_separation(self) -> float:
        """
        Maximum separation between peaks to merge into single anomaly.
        """
        return self._max_separation

    @max_separation.setter
    def max_separation(self, val):
        self.setter_validator("max_separation", val)

    @property
    def structural_markers(self) -> bool | None:
        """
        Use structural markers.
        """
        return self._structural_markers

    @structural_markers.setter
    def structural_markers(self, val):
        self.setter_validator("structural_markers", val)

    @property
    def template_data(self):
        return self._template_data

    @template_data.setter
    def template_data(self, val):
        self.setter_validator("template_data", val)

    @property
    def template_color(self):
        return self._template_color

    @template_color.setter
    def template_color(self, val):
        self.setter_validator("template_color", val)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self.setter_validator("title", val)

    @property
    def group_a_data(self) -> PropertyGroup | None:
        """
        Property group a data.
        """
        return self._group_a_data

    @group_a_data.setter
    def group_a_data(self, val):
        self.setter_validator("group_a_data", val)

    @property
    def group_a_color(self) -> str | None:
        """
        Property group a color.
        """
        return self._group_a_color

    @group_a_color.setter
    def group_a_color(self, val):
        self.setter_validator("group_a_color", val)

    @property
    def group_b_data(self) -> PropertyGroup | None:
        """
        Property group b data.
        """
        return self._group_b_data

    @group_b_data.setter
    def group_b_data(self, val):
        self.setter_validator("group_b_data", val)

    @property
    def group_b_color(self) -> str | None:
        """
        Property group b color.
        """
        return self._group_b_color

    @group_b_color.setter
    def group_b_color(self, val):
        self.setter_validator("group_b_color", val)

    @property
    def group_c_data(self) -> PropertyGroup | None:
        """
        Property group c data.
        """
        return self._group_c_data

    @group_c_data.setter
    def group_c_data(self, val):
        self.setter_validator("group_c_data", val)

    @property
    def group_c_color(self) -> str | None:
        """
        Property group c color.
        """
        return self._group_c_color

    @group_c_color.setter
    def group_c_color(self, val):
        self.setter_validator("group_c_color", val)

    @property
    def group_d_data(self) -> PropertyGroup | None:
        """
        Property group d data.
        """
        return self._group_d_data

    @group_d_data.setter
    def group_d_data(self, val):
        self.setter_validator("group_d_data", val)

    @property
    def group_d_color(self) -> str | None:
        """
        Property group d color.
        """
        return self._group_d_color

    @group_d_color.setter
    def group_d_color(self, val):
        self.setter_validator("group_d_color", val)

    @property
    def group_e_data(self) -> PropertyGroup | None:
        """
        Property group e data.
        """
        return self._group_e_data

    @group_e_data.setter
    def group_e_data(self, val):
        self.setter_validator("group_e_data", val)

    @property
    def group_e_color(self) -> str | None:
        """
        Property group e color.
        """
        return self._group_e_color

    @group_e_color.setter
    def group_e_color(self, val):
        self.setter_validator("group_e_color", val)

    @property
    def group_f_data(self) -> PropertyGroup | None:
        """
        Property group f data.
        """
        return self._group_f_data

    @group_f_data.setter
    def group_f_data(self, val):
        self.setter_validator("group_f_data", val)

    @property
    def group_f_color(self) -> str | None:
        """
        Property group f color.
        """
        return self._group_f_color

    @group_f_color.setter
    def group_f_color(self, val):
        self.setter_validator("group_f_color", val)

    def get_property_groups(self):
        """
        Generate a dictionary of groups with associate properties from params.
        """
        count = 0
        property_groups = {}
        for name in string.ascii_lowercase[:6]:
            prop_group = getattr(self, f"group_{name}_data", None)
            if prop_group is not None:
                count += 1
                property_groups[prop_group.name] = {
                    "param": name,
                    "data": prop_group.uid,
                    "color": getattr(self, f"group_{name}_color", None),
                    "label": [count],
                    "properties": prop_group.properties,
                }
        return property_groups

    def get_line_field(self, survey: Curve) -> ReferencedData:
        """
        Get the line field object.
        """
        if self.line_field is None:
            unique_parts = np.unique(survey.parts.astype(int)) + 1
            line_field_obj = survey.add_data(
                {
                    "Line ID": {
                        "values": survey.parts.astype(int) + 1,
                        "value_map": {ind: f"Line {ind}" for ind in unique_parts},
                        "type": "referenced",
                    }
                }
            )
            if not isinstance(line_field_obj, ReferencedData):
                raise TypeError("Issue creating a ReferencedData'line_field'.")

            return line_field_obj

        return self.line_field

    @property
    def survey(self):
        if self._survey is None and self.objects is not None:
            self._temp_workspace = Workspace()
            with fetch_active_workspace(self.geoh5):
                self._survey = self.objects.copy(parent=self._temp_workspace)

        return self._survey

    @survey.setter
    def survey(self, val: Curve | None):
        if not isinstance(val, Curve | type(None)):
            raise TypeError(f"Survey must be of type {Curve}")

        self._survey = val

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Copyright (c) 2024-2025 Mira Geoscience Ltd.                                     '
#                                                                                   '
#  This file is part of peak-finder-app package.                                    '
#                                                                                   '
#  peak-finder-app is distributed under the terms and conditions of the MIT License '
#  (see LICENSE file at the root of this source code package).                      '
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np


if TYPE_CHECKING:
    from .line_data import LineData


@dataclass
class Anomaly:
    """
    Anomaly class.

    Contains indices for the maxima, minima, inflection points.
    """

    parent: LineData
    start: int
    end: int
    inflect_up: int
    inflect_down: int
    peak: int
    amplitude: float = field(init=False)

    def __post_init__(self):
        for attr in ["start", "end", "inflect_up", "inflect_down", "peak"]:
            if not isinstance(getattr(self, attr), np.integer):
                raise TypeError(f"Attribute '{attr}' must be an integer.")

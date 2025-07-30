# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#  Copyright (c) 2024-2025 Mira Geoscience Ltd.                                     '
#                                                                                   '
#  This file is part of peak-finder-app package.                                    '
#                                                                                   '
#  peak-finder-app is distributed under the terms and conditions of the MIT License '
#  (see LICENSE file at the root of this source code package).                      '
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# pylint: disable=too-many-arguments

from __future__ import annotations


import numpy as np

from peak_finder.anomaly_group import AnomalyGroup
from peak_finder.line_data import LineData
from peak_finder.line_position import LinePosition


# pylint: disable=duplicate-code


class LineGroup:
    """
    Contains list of AnomalyGroup objects.
    """

    def __init__(
        self,
        position: LinePosition,
        line_dataset: list[LineData],
        property_group: str,
        *,
        max_migration: float,
        min_channels: int,
        n_groups: int,
        max_separation: float,
        minimal_output: bool,
    ):
        """
        :param line_dataset: List of line data with all anomalies.
        :param groups: List of anomaly groups.
        :param max_migration: Maximum peak migration.
        """
        self._position = position
        self.line_dataset = line_dataset
        self.property_group = property_group
        self._max_migration = max_migration
        self._min_channels = min_channels
        self._n_groups = n_groups
        self._max_separation = max_separation
        self._minimal_output = minimal_output
        self._groups: list[AnomalyGroup] | None = None

    @property
    def groups(self) -> list[AnomalyGroup]:
        """
        List of anomaly groups.
        """
        if self._groups is None:
            self._groups = self.compute()
        return self._groups

    @property
    def position(self) -> LinePosition:
        """
        Line Position.
        """
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def line_dataset(self) -> list[LineData]:
        """
        List of line data.
        """
        return self._line_dataset

    @line_dataset.setter
    def line_dataset(self, value):
        self._line_dataset = value

    @property
    def property_group(self) -> str:
        """
        Property group.
        """
        return self._property_group

    @property_group.setter
    def property_group(self, value):
        self._property_group = value

    @property
    def max_migration(self) -> float:
        """
        Maximum peak migration.
        """
        return self._max_migration

    @max_migration.setter
    def max_migration(self, value):
        self._max_migration = value

    @property
    def min_channels(self) -> int:
        """
        Minimum number of channels in anomaly.
        """
        return self._min_channels

    @min_channels.setter
    def min_channels(self, value):
        self._min_channels = value

    @property
    def n_groups(self) -> int:
        """
        Number of peaks to merge.
        """
        return self._n_groups

    @n_groups.setter
    def n_groups(self, value):
        self._n_groups = value

    @property
    def max_separation(self) -> float:
        """
        Max separation between peaks to merge.
        """
        return self._max_separation

    @max_separation.setter
    def max_separation(self, value):
        self._max_separation = value

    @property
    def minimal_output(self) -> bool:
        """
        Whether to return minimal output.
        """
        return self._minimal_output

    @minimal_output.setter
    def minimal_output(self, value):
        self._minimal_output = value

    def get_near_peaks(
        self,
        ind: int,
        full_channel: np.ndarray,
        peaks_position: np.ndarray,
    ) -> np.ndarray:
        """
        Get indices of peaks within the migration distance.

        :param ind: Index of anomaly.
        :param full_channel: Array of channels.
        :param peaks_position: Array of peak positions.

        :return: Array of indices of peaks within the migration distance.
        """
        dist = np.abs(peaks_position[ind] - peaks_position)
        # Find anomalies across channels within horizontal range
        near = np.where(dist < self.max_migration)[0]

        # Reject from group if channel gap > 1
        u_gates, u_count = np.unique(full_channel[near], return_counts=True)
        if len(u_gates) > 1 and np.any((u_gates[1:] - u_gates[:-1]) > 2):
            cutoff = u_gates[np.where((u_gates[1:] - u_gates[:-1]) > 2)[0][0]]
            near = near[full_channel[near] <= cutoff]  # Remove after cutoff

        # Check for multiple nearest peaks on single channel
        # and keep the nearest
        u_gates, u_count = np.unique(full_channel[near], return_counts=True)
        for gate in u_gates[np.where(u_count > 1)]:
            mask = np.ones_like(near, dtype="bool")
            sub_ind = full_channel[near] == gate
            sub_ind[np.where(sub_ind)[0][np.argmin(dist[near][sub_ind])]] = False
            mask[sub_ind] = False
            near = near[mask]

        return near

    def get_anomaly_attributes(self, line_data_subset: list[LineData]) -> tuple:
        """
        Get full lists of anomaly attributes from line_dataset.

        :param line_data_subset: List of line data corresponding to property group.

        :return: Full list of anomalies, group ids, channels, peak positions,
            peak values, and channel groups.
        """
        locs = self.position.locations_resampled

        full_anomalies = []
        full_channels = []
        full_peak_positions = []

        for ind, line_data in enumerate(line_data_subset):
            for anom in line_data.anomalies:
                full_anomalies.append(anom)
                full_channels.append(ind)
                full_peak_positions.append(locs[anom.peak])

        return (
            full_anomalies,
            np.array(full_channels),
            np.array(full_peak_positions),
        )

    @staticmethod
    def accumulate_groups(
        path: np.ndarray, neighbourhood: np.ndarray, max_length: int
    ) -> list[np.ndarray]:
        """
        Accumulate neighbouring groups.

        :param path: Current path made up of coupled anomaly indices.
        :param neighbourhood: Array of all neighbouring couple indices.
        :param max_length: Maximum number of anomalies in a path.

        :return: List of all possible paths.
        """
        if len(np.unique(path)) == max_length:
            return [path]

        next_neighbours = np.where(path[-1, 1] == neighbourhood[:, 0])[0]

        if len(next_neighbours) == 0:
            return [path]

        branches = []
        for next_neighbour in next_neighbours:
            current = np.vstack([path, neighbourhood[next_neighbour]])
            paths = LineGroup.accumulate_groups(current, neighbourhood, max_length)

            for branch in paths:
                branches.append(branch)

        return branches

    @staticmethod
    def find_neighbour_groups(groups: list[AnomalyGroup], max_separation: int) -> list:
        """
        Loop through all anomaly groups and find neighbours within the
        maximum separation.

        :param groups: List of anomaly groups.
        :param max_separation: Maximum number of indices separating anomalies to form a group.

        :return: List of indices for all group pairs.
        """
        all_starts = np.asarray([group.start for group in groups])
        all_ends = np.asarray([group.end for group in groups])

        neighbours_list = []
        for cur, end in enumerate(all_ends):
            dist = np.abs(all_starts - end)
            next_neighbour = np.where(dist < max_separation)[0]
            neighbours_list += [[cur, nn] for nn in next_neighbour if nn != cur]

        return neighbours_list

    def group_n_groups(self, groups: list[AnomalyGroup]) -> list[AnomalyGroup]:
        """
        Merge consecutive peaks into groups of n_groups.

        :param groups: List of anomaly groups.

        :return: List of merged anomaly groups.
        """
        if self.position.sampling is None:
            return groups

        return_groups: list[AnomalyGroup] = []
        all_starts = np.array([group.start for group in groups])
        sort_inds = np.argsort(all_starts)
        sorted_groups: list[AnomalyGroup] = list(np.array(groups)[sort_inds])

        max_separation = np.ceil(self.max_separation / self.position.sampling)
        neighbours_list = self.find_neighbour_groups(sorted_groups, max_separation)

        if len(neighbours_list) == 0:
            return return_groups

        neighbourhood = np.vstack(neighbours_list)

        for couple in neighbourhood:
            branches = self.accumulate_groups(
                couple[np.newaxis, :], neighbourhood, self.n_groups
            )

            for branch in branches:
                indices = np.unique(branch)

                if len(indices) < self.n_groups:
                    continue

                new_group = AnomalyGroup(
                    np.concatenate([sorted_groups[ind].anomalies for ind in indices]),
                    self.property_group,
                    subgroups={sorted_groups[ind] for ind in indices},
                )
                return_groups.append(new_group)

        return return_groups

    def compute(  # pylint: disable=R0913, R0914
        self,
    ) -> list[AnomalyGroup] | list:
        """
        Group anomalies.

        :return: List of groups of anomalies.
        """
        groups: list = []
        group_id = -1

        if self.n_groups is None:
            return groups

        # Get full lists of anomaly attributes
        (
            full_anomalies,
            full_channels,
            full_peak_positions,
        ) = self.get_anomaly_attributes(self.line_dataset)

        full_group_ids = np.ones(len(full_anomalies), dtype="bool") * -1
        for ind, _ in enumerate(full_anomalies):
            # Skip if already labeled
            if full_group_ids[ind] != -1:
                continue

            group_id += 1

            # Find nearest peaks
            near = self.get_near_peaks(
                ind,
                full_channels,
                full_peak_positions,
            )

            if (
                len(np.unique(full_channels[near])) < self.min_channels
                or len(near) == 0
            ):
                continue

            full_group_ids[near] = group_id

            # Make AnomalyGroup
            near_anomalies = np.array(full_anomalies)[near]

            group = AnomalyGroup(
                near_anomalies,
                self.property_group,
                set(),
            )
            groups += [group]

        if self.n_groups > 1:
            groups = self.group_n_groups(groups)

        return groups

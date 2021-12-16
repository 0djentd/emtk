# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import copy
import time
from .clusters_operation import ClustersOperation


class ClustersController():
    """
    This is object responsible for managing
    ClustersOperations buffer.
    """
    """
    What should be done when running dry operation on cluster?

    1) Ask ClustersLayer layer belongs to.

        Case 1: is ClustersLayer.
        1.1) Ask ClustersLayer layer belongs to.

        Case 1: is FirstLayer.
        1.1) Ask first layer.

    2) Ask object itself.

        Case 1: operation on ModifiersCluster.
        2.1) Ask ModifiersCluster itself.

        Case 2: operation on ClustersLayer.
        2.1) Asking ClustersLayer.
            2.1.1) Ask all its ModifiersClusters.
            2.1.2) Ask all its ClustersLayers.

    3) Return result as set of additional operations that will be 
    performed when running operation.
    """
    """
    Example:
    Removing cluster 2 in layer 1 that is part of first layer and
    doesnt allow removing clusters without removing layer.

    result = cluster2.check_operation(op_on_cluster2)

    get trace to cluster2.
    for x in trace:
        # This will return empty op if no operation needed.
        # If not allowed, returns NEED_TO_REMOVE_X
        result = x.check_opertation(operation_in_x_clusters)
        ops+=result

    result:
    DO REMOVE cluster2
    NEED REMOVE layer1
    DO REMOVE layer1
    EMPTY first
    """

    def _check_operation(self, task):
        if not isinstance(task, ClustersOperation):
            raise TypeError

    def add(self, task):
        self._check_operation(task)
        self._tasks.append(time.time(), task)

    def remove(self, taks):
        self._check_operation(task)
        tasks_to_test = self._tasks[self._tasks.index(task):-1]

    def ask(self, task):
        self._check_operation(task)
        self._tasks.append(time.time(), task)
        return self.run_task_dry(task)

    def run_task(self, task):
        self._check_operation(task)
        result = True
        tasks_to_run = self._tasks[0:self._tasks.index(task)]

        for x in tasks_to_run 
            if not self.unwrap_and_run(x):
                result = False

            self._finished_tasks.append(self._tasks.pop(x))
        return result

    def run_task_dry(self, task):
        self._check_operation(task)
        result = True
        tasks_to_run = self._tasks[0:self._tasks.index(task)]

        for x in tasks_to_run:
            if not self.unwrap_and_run_dry(x):
                result = False

            self._finished_tasks.append(self._tasks.pop(x))
        return result

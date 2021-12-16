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


class Action():
    def __init__(self, action_type, action, val, obj):
        self.type = action_type
        self.name = action
        self.value = val
        self.obj = obj

def remove_this_cluster(self):
    task = Action('DO', 'REMOVE', self, self)
    if self._controller.ask(task):
        self._controller.do(task)
        self._cluster_removed = True
        return True
    else:
        return False

def _check_if_cluster_removed(self):
    if self._cluster_removed:
        raise ValueError(f'Cluster {self} already removed.')
        
class Controller():
    """
    This is object responsible for managing Actions buffer.
    """
    """
    Example:
    Removing cluster 2 in layer 1 that is part of first layer and
    doesnt allow removing clusters without removing layer 1.

    result = cluster2.check_operation(action_on_cluster2)

    get trace to cluster2.
    for x in trace:
        # This will return empty action if no action needed.
        # If not allowed, returns NEED_TO_REMOVE_X
        result = x.check_opertation(action_in_x_clusters)
        actions+=result

    result:
    DO REMOVE cluster2
    NEED REMOVE layer1
    DO REMOVE layer1
    EMPTY first
    """

    def _check_action(self, task):
        if not isinstance(task, Action):
            raise TypeError

    def add(self, task):
        self._check_action(task)
        self._tasks.append(time.time(), task)

    def remove(self, taks):
        self._check_action(task)
        tasks_to_test = self._tasks[self._tasks.index(task):-1]

    def ask(self, task):
        self._check_action(task)
        self._tasks.append(time.time(), task)
        return self.run_task_dry(task)

    def do(self, task):
        self._check_action(task)
        result = True
        tasks_to_run = self._tasks[0:self._tasks.index(task)]
        for x in tasks_to_run 
            if not self.unwrap_and_run(x):
                result = False

            self._finished_tasks.append(self._tasks.pop(x))
        return result

    def run_task_dry(self, task):
        self._check_action(task)
        result = True
        tasks_to_run = self._tasks[0:self._tasks.index(task)]

        for x in tasks_to_run:
            if not self.unwrap_and_run_dry(x):
                result = False

            self._finished_tasks.append(self._tasks.pop(x))
        return result

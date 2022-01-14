# ##### BEGIN GPL LICENSE BLOCK #####
#
# Copyright 2022, Sergey Shapochkin
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

def check_if_removed(func):
    def wrapper_check_if_removed(self, *args, **kwargs):
        # logger.debug(f'Method is {func}')
        self._check_if_cluster_removed()
        return func(self, *args, **kwargs)
    return wrapper_check_if_removed


def check_obj_ref(func):
    def wrapper_check_obj_ref(self, obj, *args, **kwargs):
        obj = self._check_cluster_or_modifier(obj)
        return func(self, obj, *args, **kwargs)
    return wrapper_check_obj_ref


__ALL__ = [check_if_removed, check_obj_ref]

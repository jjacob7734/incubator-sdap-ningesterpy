# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from nexusproto.serialization import from_shaped_array, to_shaped_array

from sdap.processors import NexusTileProcessor


class ForceAscendingLatitude(NexusTileProcessor):
    def process_nexus_tile(self, nexus_tile):
        """
        This method will reverse the ordering of latitude values in a tile if necessary to ensure that the latitude values are ascending.

        :param self:
        :param nexus_tile: The nexus_tile
        :return: Tile data with altered latitude values
        """

        the_tile_type = nexus_tile.tile.WhichOneof("tile_type")

        the_tile_data = getattr(nexus_tile.tile, the_tile_type)

        latitudes = from_shaped_array(the_tile_data.latitude)

        data = from_shaped_array(the_tile_data.data)

        # Only reverse latitude ordering if current ordering is descending.
        if len(latitudes) > 1:
            delta = latitude[1] - latitude[0]
            if delta < 0:
                latitudes = np.flip(latitudes)
                data = np.flip(data, axis=0)
                the_tile_data.latitude.CopyFrom(to_shaped_array(latitudes))
                the_tile_data.data.CopyFrom(to_shaped_array(data))

        yield nexus_tile


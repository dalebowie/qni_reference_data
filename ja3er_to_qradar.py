#!/usr/bin/env python3
# Copyright 2022 Dale Bowie
#
# This file is part of qni_reference_data.
# See https://github.com/dalebowie/qni_reference_data for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from QRadarArgumentParser import QRadarArgumentParser
from QRadarAPI import QRadarAPI
from JA3er import JA3er

parser = QRadarArgumentParser()
args = parser.parse_args()

qapi = QRadarAPI(args.qradar_host, args.qradar_token, args.skip_verify_qradar)

ref_map_name = "QNI : JA3er Hashes"
ref_map = qapi.get_or_create_reference_map(ref_map_name,
                                           "ja3_hash",
                                           "user_agent")

ja3er = JA3er(args.force_download)
hashes = ja3er.get_as_dict()

map_data = qapi.update_reference_map_values(ref_map_name, hashes)
print(f"{map_data['number_of_elements']} hashes included in QRadar reference data.")
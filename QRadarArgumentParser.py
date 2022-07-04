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

import argparse

class QRadarArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("qradar_host", 
                                 help="The IP address or hostname of the QRadar instance you wish to connect to.",
                                 type=str)
        self.parser.add_argument("qradar_token", 
                                 help="A QRadar authorised token that has access to the Reference Data APIs.",
                                 type=str)
        self.parser.add_argument("--skip_verify_qradar", 
                                 help="Include this flag if you wish to skip verifying HTTPS communications to the QRadar host. This might be useful if you host is still using the default X509 certificate.",
                                 action='store_false')
        self.parser.add_argument("--force_download", 
                                 help="Include this flag if you wish to force the re-download of the relevant database every time this script is run.",
                                 action='store_true')
    
    def parse_args(self):
        return self.parser.parse_args()
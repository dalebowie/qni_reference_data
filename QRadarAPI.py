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

import requests
try:
    from urllib.parse import quote_plus as quote_plus
    from urllib.parse import urlencode as urlencode
except:
    from urllib import quote_plus as quote_plus
    from urllib import urlencode as urlencode

class QRadarAPI():
    def __init__(self, ip, token, verify):
        self.ip         = ip
        self.token      = token
        self.verify     = verify
        
        self.headers    = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "SEC": token
        }
        
        self.base_url   = "https://" + ip + "/api/%s"
    
    def get(self, path):
        resp = requests.get(self.base_url % path, headers=self.headers, verify=self.verify)
        if resp.status_code == 404:
            return None
        elif resp.status_code == 200:
            print("Operation successful.")
            return resp.json()
        elif resp.status_code == 401 or resp.status_code == 403:
            raise Exception("Invalid security token.")
        else:
            raise Exception("Unhandled status code.")
    
    def post(self, path, data=None):
        resp = requests.post(self.base_url % path, headers=self.headers, json=data, verify=self.verify)
        if resp.status_code == 201 or resp.status_code == 200:
            print("Operation successful.")
            return resp.json()
        elif resp.status_code == 401 or resp.status_code == 403:
            raise Exception("Invalid security token.")
        else: 
            raise Exception("Unhandled status code.")
    
    def get_or_create_reference_map(self, name, key_label, value_label):
        resp = self.get("reference_data/maps/%s" % quote_plus(name))
        
        if resp == None:
            data = {
                "element_type": "ALNIC",
                "name": name,
                "key_label": key_label,
                "value_label": value_label
            }
            path = "reference_data/maps?%s" % (urlencode(data))
            resp = self.post(path)
        
        return resp
    
    def update_reference_map_values(self, name, data):
        return self.post('reference_data/maps/bulk_load/%s' % quote_plus(name), data)


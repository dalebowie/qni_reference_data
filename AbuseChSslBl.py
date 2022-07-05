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
import csv
import os

class AbuseChSslBl():
    FILE_NAME = "abuse_ch_sslbl.csv"

    # Column orders
    COL_DATE    = 0
    COL_HASH    = 1
    COL_REASON  = 2

    def __init__(self, force_download=False):
        """
        @param force_download:
            Whether or not to force a fresh download of the database, or re-use the local downloaded copy.
        """
        database_exists = os.path.exists(self.FILE_NAME)

        if force_download or not database_exists:
            self.download_full_database()

        self.load_file_contents()

    def download_full_database(self):
        print("Attempting to download full database from abuse.ch...")
        resp = requests.get('https://sslbl.abuse.ch/blacklist/sslblacklist.csv')
        print("Download complete. Saving file...");
        with open(self.FILE_NAME, "w") as outFile:
            outFile.write(resp.text)
        print(f"Local file saved as: {self.FILE_NAME}")

    def load_file_contents(self):
        self.hashes = {}
        with open(self.FILE_NAME, "r") as inFile:
            contents = csv.reader(inFile)

            for content in contents:
                if len(content) != 3 or content[0][0] == '#':
                    # All rows should have 3 columns and should not begin with a comment symbol
                    # Skip over this row if it matches
                    continue
                
                self.hashes[content[self.COL_HASH]] = f"{content[self.COL_REASON]} (added on {content[self.COL_DATE]})"

        print(f"Database processed. We have {len(self.hashes)} blocklist entries.")

    def get_as_dict(self):
        return self.hashes

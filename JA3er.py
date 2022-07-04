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
import json
import os

class JA3er():
    FILE_NAME = "ja3er.json"

    # Originally I had a longer blocklist here, but the BAD_USER_AGENT_STARTS 
    # combined with the MIN_THRESHOLD of 50 seemed to filter out enough entries
    # that it was no longer needed.
    BAD_USER_AGENTS = [""]

    BAD_USER_AGENT_STARTS = [
        '<',
        '{',
        '(',
        "'",
        '"',
        "[",
        "$",
        "-"
    ]

    MIN_THRESHOLD = 50

    def __init__(self, force_download=False):
        """
        @param force_download:
            Whether or not to force a fresh download of the JA3er database, or re-use the local downloaded copy.
        """

        database_exists = os.path.exists(self.FILE_NAME)

        if force_download or not database_exists:
            self.download_full_database()

        self.load_file_contents()

    def download_full_database(self):
        print("Attempting to download full database from ja3er.com. This file is over 300MB and may take a while to download...")
        resp = requests.get('https://ja3er.com/getAllUasJson')
        print("Download complete. Saving file...");
        with open(self.FILE_NAME, "w") as outFile:
            outFile.write(resp.text)
        print(f"Local file saved as: {self.FILE_NAME}")

    def load_file_contents(self):
        contents = []
        with open(self.FILE_NAME, "r") as inFile:
            contents = json.load(inFile)

        print("Filtering JA3er database for potential spam...")
        filtered = list(filter(lambda content: content["User-Agent"] not in self.BAD_USER_AGENTS and content['User-Agent'][0] not in self.BAD_USER_AGENT_STARTS and content["Count"] > self.MIN_THRESHOLD, contents))
        print(f"Database filtered. We have {len(filtered)} user agents to process")
        self.hashes = filtered

    def get_as_dict(self):
        hash_dict   = {}
        hash_best   = {}
        hash_counts = {}

        # Do a first pass to find our best matches for each hash
        for hash in self.hashes:
            new_hash = hash["md5"] not in hash_dict
            existing_better_hash = hash["md5"] in hash_dict and hash["Count"] > hash_best[hash["md5"]]
            if new_hash or existing_better_hash:
                hash_dict  [hash["md5"]] = hash["User-Agent"]
                hash_best  [hash["md5"]] = hash["Count"]
            
            if new_hash:
                hash_counts[hash["md5"]] = 1
            else:
                hash_counts[hash["md5"]] += 1
        
        # Do a second pass to aggregate our findings together
        hash_return = {}
        for hash in hash_dict:
            hash_return[hash] = f"{hash_dict[hash]} (matched {hash_best[hash]} times, with {hash_counts[hash]} other reported user agents)"
        print(f"{len(hash_return)} hashes ready for import")
        return hash_return

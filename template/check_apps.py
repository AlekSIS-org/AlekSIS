#!/usr/bin/env python3

# Copyright 2020 Dominik George <dominik.george@teckids.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import difflib
import glob
import os
from typing import List

import toml

my_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.join(my_dir, ".."))


class DiffError(Exception):
    pass


def get_app_files(proj_file: str) -> List[str]:
    return glob.glob(os.path.join("apps", "*", "*", proj_file))


def compare_flatfile(in_file: str, proj_file: str):
    with open(os.path.join(my_dir, in_file), "r") as f:
        in_lines = f.readlines()

    diffs = []
    for path in get_app_files(proj_file):
        with open(path, "r") as f:
            proj_lines = f.readlines()

        diff = list(difflib.unified_diff(in_lines, proj_lines, in_file, path))
        if diff:
            diffs.append("".join(diff))

    if diffs:
        diff_out = "\n\n----\n\n".join(diffs)
        raise DiffError(f"Flat files differ for {proj_file} (from {in_file}:\n\n{diff_out}")


config = toml.load(os.path.join(my_dir, "check_apps.toml"))
if "flat" in config.keys():
    for in_file, proj_file in config["flat"].items():
        compare_flatfile(in_file, proj_file)

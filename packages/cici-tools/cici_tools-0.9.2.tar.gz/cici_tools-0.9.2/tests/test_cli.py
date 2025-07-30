# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: MIT

import filecmp
import os
import shutil
from contextlib import contextmanager

import pytest

from cici.constants import BASE_DIR
from cici.main import main as cici

FIXTURES_DIR = BASE_DIR / ".." / "tests" / "fixtures"


@contextmanager
def pushd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


@pytest.mark.parametrize(
    "platform,name",
    [
        (
            "gitlab",
            "helm",
        ),
        (
            "gitlab",
            "terraform",
        ),
    ],
)
def test_end_to_end_bundle(platform, name, tmp_path):
    fixture_dir = FIXTURES_DIR / platform / name
    test_dir = tmp_path

    test_cici_dir = test_dir / ".cici"
    test_cici_dir.mkdir()

    files = [".cici/.gitlab-ci.yml", *[path.name for path in fixture_dir.glob("*.yml")]]
    for file in files:
        shutil.copyfile(fixture_dir / file, test_dir / file)
    with pushd(test_dir):
        print(list(test_dir.glob("*")))
        cici(["bundle"])

    match, mismatch, errors = filecmp.cmpfiles(
        fixture_dir, test_dir, files, shallow=True
    )
    print(match, mismatch, errors)

import pytest

from src.ross_cli.cli import *

def test_01_init(temp_dir):
    name = "test_package_no_git"
    init_command(name, temp_dir)

def test_02_init_with_git_no_github(temp_dir_with_git_repo):
    name = "test_package"
    # Create package with git
    init_command(name, temp_dir_with_git_repo)

def test_03_init_with_git_and_github(temp_dir_with_github_repo):
    name = "test_package"
    # Create package in folder with git and github
    init_command(name, temp_dir_with_github_repo)

def test_04_init_twice(temp_dir):
    name = "test_package"
    # Create package first time
    init_command(name, temp_dir)
    # Try to create same package again
    init_command(name, temp_dir)

def test_05_init_empty_name(temp_dir):
    name = ""
    init_command(name, temp_dir)

def test_06_init_no_name(temp_dir):
    name = None
    init_command(name, temp_dir)

def test_07_init_with_hyphen(temp_dir):
    name = "test-package"
    # Create package in folder with git and github
    init_command(name, temp_dir)
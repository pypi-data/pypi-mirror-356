"""This script is used to bump the version of the package. pyproject.toml is used to store the version."""

import argparse
import re
import sys

import requests
import toml


def check_version_on_pypi(package_name: str, version: str) -> bool:
    """Checks if the given version of the package exists on PyPI.

    Args:
        package_name (str): The name of the package
        version (str): The version to check

    Returns:
        bool: True if the version exists, False otherwise
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        versions = data.get("releases", {}).keys()
        return version in versions
    except requests.RequestException as e:
        print(f"Error checking version on PyPI: {e}")
        return False


def read_version():
    with open("pyproject.toml", "r") as file:
        data = toml.load(file)
    return data["project"]["version"]


def read_package_name():
    with open("pyproject.toml", "r") as file:
        data = toml.load(file)
    return data["project"]["name"]


def write_version(new_version):
    # Read the content of the file
    with open("pyproject.toml", "r") as file:
        content = file.readlines()

    # Find and update the version line
    for i, line in enumerate(content):
        if line.startswith("version = "):
            content[i] = f'version = "{new_version}"\n'
            break

    # Write the updated content back to the file
    with open("pyproject.toml", "w") as file:
        file.writelines(content)


if __name__ == "__main__":
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Bump the package version.")
    parser.add_argument("--version", required=True, help="The new version number to apply.")
    args = parser.parse_args()

    new_version = args.version

    package_name = read_package_name()

    version_pattern = r"^\d+\.\d+\.\d+$"

    # check if the new_version is provided
    if not new_version:
        print("Usage: python3 bump_version.py x.x.x")
        sys.exit(1)

    # Check if the new_version matches the required pattern
    if not re.match(version_pattern, new_version):
        print("Error: Version must be in the format x.x.x, where x is a digit.")
        sys.exit(1)

    # Check if the new version already exists on PyPI

    if check_version_on_pypi(package_name, new_version):
        print(f"Error: Version {new_version} already exists on PyPI.")
        sys.exit(1)

    # if all checks pass, update the version
    write_version(new_version)
    print(f"Version updated to: {new_version}")

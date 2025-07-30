import re


def extract_latest_version(changelog_path: str) -> str:
    """Extract the latest release version from the changelog file

    Args:
        changelog_path (str): path to the changelog file

    Returns:
        str: the latest release version
    """
    # it has to follow the pattern: ## [x.y.z] - yyyy-mm-dd
    version_pattern = re.compile(r"## \[(\d+\.\d+\.\d+)\] - \d{4}-\d{2}-\d{2}")
    with open(changelog_path, "r", encoding="utf-8") as file:
        for line in file:
            match = version_pattern.match(line)
            if match:
                return match.group(1)  # Return the first matched version
    return None  # Return None if no version is found


if __name__ == "__main__":
    changelog_path = "CHANGELOG.md"  # Update this path to your actual changelog file
    latest_version = extract_latest_version(changelog_path)
    if latest_version:
        print(f"Latest release version: {latest_version}")
    else:
        print("No release version found in the changelog.")
        raise SystemExit(1)

    with open("version.txt", "w") as version_file:
        version_file.write(latest_version)
    print(f"Version written to version.txt: {latest_version}")

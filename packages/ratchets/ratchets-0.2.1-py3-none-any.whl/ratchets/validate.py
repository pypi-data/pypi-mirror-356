import re
import toml
import argparse
from typing import Dict, Any, Optional
from .run_tests import (
    get_file_path,
)


def evaluate_single_regex(regex: str, input_str: str) -> Optional[re.Match[str]]:
    """Evaluate a single regexp based on 'input_str'."""
    pattern = re.compile(regex)
    return pattern.search(input_str)


def check_valid(regex_tests: Dict[str, Dict[str, Any]]) -> None:
    """Given a dict of regex test and strings, returns if none of the regexps match their strings."""
    for test in regex_tests:
        regex: str = regex_tests[test]["regex"]
        for validation in regex_tests[test]["valid"]:
            for line in validation.splitlines():
                if evaluate_single_regex(regex, line):
                    raise Exception(f"Regex: {regex} matched {line}")


def check_invalid(regex_tests: Dict[str, Dict[str, Any]]) -> int:
    """Given a dict of regex test and strings, returns if all of the regexps match all of their strings."""
    for test in regex_tests:
        regex: str = regex_tests[test]["regex"]
        for validation in regex_tests[test]["invalid"]:
            found: bool = False
            for line in validation.splitlines():
                if evaluate_single_regex(regex, line):
                    found = True
            if not found:
                raise Exception(f"Regex: {regex} not matched in {validation}")
    return 0


def validate(filename: Optional[str]) -> Optional[bool]:
    """Verify the given file's example expressions match the regexps."""
    test_path: str = get_file_path(filename)
    config: Dict[str, Any] = toml.load(test_path)
    regex_tests: Optional[Dict[str, Dict[str, Any]]] = config.get("ratchet", {}).get(
        "regex"
    )

    if regex_tests is None:
        print("No regex tests found, there is nothing to validate.")
        return True

    check_valid(regex_tests)
    check_invalid(regex_tests)
    return True


if __name__ == "__main__":
    """Entry point to parse CLI inputs and evaluate .toml test file."""
    parser = argparse.ArgumentParser(description="Regex ratchet validation")
    parser.add_argument("-f", "--file")
    args = parser.parse_args()
    file: Optional[str] = args.file
    validate(file)

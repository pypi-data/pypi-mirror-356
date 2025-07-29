"""A CLI tool for sorting YAML files recursively.

This script provides functionality to load a YAML file, sort its contents
recursively, and save the sorted result to a new file. It can be used as a
command-line tool with various options for input, output, and sorting behavior.
"""

import argparse
import sys
from collections import OrderedDict
from typing import Any, Dict, List, Union

import yaml


def sort_dict(d: Dict[str, Any]) -> OrderedDict:
    """Sort a dictionary by its keys.

    Args:
        d: The dictionary to be sorted.

    Returns:
        An OrderedDict with sorted keys.
    """
    return OrderedDict(sorted(d.items(), key=lambda x: x[0]))


def dict_representer(dumper: yaml.Dumper, data: OrderedDict) -> yaml.nodes.MappingNode:
    """Custom representer for OrderedDict to maintain order in YAML output.

    Args:
        dumper: The YAML Dumper object.
        data: The OrderedDict to be represented.

    Returns:
        A YAML mapping node.
    """
    return dumper.represent_mapping("tag:yaml.org,2002:map", data.items())


yaml.add_representer(OrderedDict, dict_representer)


def sort_recursive(
    obj: Union[Dict[str, Any], List[Any], Any]
) -> Union[OrderedDict, List[Any], Any]:
    """Recursively sort a nested structure of dictionaries and lists.

    Args:
        obj: The object to be sorted. Can be a dict, list, or any other type.

    Returns:
        A sorted version of the input object.
    """
    if isinstance(obj, dict):
        return sort_dict({k: sort_recursive(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [sort_recursive(item) for item in obj]
    return obj


def load_yaml(file_path: str) -> Dict[str, Any]:
    """Load a YAML file and return its contents as a dictionary.

    Args:
        file_path: The path to the YAML file to be loaded.

    Returns:
        A dictionary containing the YAML file contents.

    Raises:
        yaml.YAMLError: If there's an error parsing the YAML file.
        FileNotFoundError: If the specified file is not found.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)


def save_yaml(data: OrderedDict, file_path: str) -> None:
    """Save a dictionary as a YAML file.

    Args:
        data: The dictionary to be saved.
        file_path: The path where the YAML file should be saved.

    Raises:
        IOError: If there's an error writing to the file.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False)
    except IOError as e:
        print(f"Error writing to file: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main function to handle CLI arguments and execute the sorting process."""
    parser = argparse.ArgumentParser(description="Sort a YAML file recursively.")
    parser.add_argument("input", help="Input YAML file path")
    parser.add_argument(
        "-o", "--output", help="Output YAML file path (default: <input>_sorted.yaml)"
    )
    parser.add_argument(
        "--no-sort-lists", action="store_true", help="Don't sort list contents"
    )
    args = parser.parse_args()

    # Set default output file name if not provided
    if not args.output:
        args.output = args.input.rsplit(".", 1)[0] + "_sorted.yaml"

    # Load, sort, and save the YAML file
    config_dict = load_yaml(args.input)

    def sort_recursive_custom(
        obj: Union[Dict[str, Any], List[Any], Any]
    ) -> Union[OrderedDict, List[Any], Any]:
        if isinstance(obj, dict):
            return sort_dict({k: sort_recursive_custom(v) for k, v in obj.items()})
        if isinstance(obj, list) and not args.no_sort_lists:
            return [sort_recursive_custom(item) for item in obj]
        return obj

    sorted_config = sort_recursive_custom(config_dict)
    save_yaml(sorted_config, args.output)
    print(f"Sorted YAML saved to: {args.output}")


if __name__ == "__main__":
    main()

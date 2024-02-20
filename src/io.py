import csv
import json
from typing import List, Dict, Any, Iterator

import jsonlines

from src.constants import (
    SUPPORTED_OUTPUT_EXTENSIONS,
)




def write_results_to_file(
    data: Iterator[Iterator[Dict[str, Any]]],
    file_name: str,
    field_names: List[str],
) -> None:
    """
    Writes the given generator of dictionaries to a file with the given name. The file type is inferred from the file
    extension, and the data is written accordingly.
    :param data:
    :param file_name:
    :param field_names:
    :return:
    """
    if file_name.lower().endswith(".csv"):
        _write_results_to_csv(data, field_names, file_name)
    elif file_name.lower().endswith(".jsonl"):
        _write_results_to_jsonlines(data, file_name)
    elif file_name.lower().endswith(".json"):
        _write_results_to_json(data, file_name)
    else:
        raise ValueError(
            f"Unsupported file extension for destination file: {file_name} (should be one of {','.join(SUPPORTED_OUTPUT_EXTENSIONS)})"
        )

def _write_results_to_json(
    data: Iterator[Iterator[Dict[str, Any]]], file_name: str
) -> None:
    """
    Writes the given generator of dictionaries as an array of dictionaries to a JSON file.

    :param data: Iterator of iterators of dictionaries to write to the JSON file
    :param file_name: Name of the JSON Lines file to write to
    """
    results = []
    for results_list_iterators in data:
        for r in results_list_iterators:
            results.append(r)
    with open(file_name, "a") as f:
        f.write(json.dumps(results, indent=4))
    print(f"Successfully wrote data to {file_name}.")

def _write_results_to_jsonlines(
    data: Iterator[Iterator[Dict[str, Any]]], file_name: str
) -> None:
    """
    Writes the given generator of dictionaries to a JSON Lines file. Assumes all dictionaries have the same keys.

    :param data: Iterator of iterators of dictionaries to write to the JSON Lines file
    :param file_name: Name of the JSON Lines file to write to
    """

    with jsonlines.open(file_name, mode="a") as writer:
        for results_list_iterators in data:
            for r in results_list_iterators:
                writer.write(r)


def _write_results_to_csv(
    data: Iterator[Iterator[Dict[str, Any]]], fields_names: List[str], file_name: str
) -> None:
    """
    Writes the given generator of dictionaries to a CSV file. Assumes all dictionaries have the same keys,
    and that the keys are the column names. If file is already present, it appends the data to the file.

    Only writes the header once, and then writes the rows.

    :param data: Iterator of iterators of dictionaries to write to the CSV file
    :param file_name: Name of the CSV file to write to
    """

    with open(file_name, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields_names)
        if f.tell() == 0:
            writer.writeheader()
        for results_list_iterators in data:
            for r in results_list_iterators:
                writer.writerow(r)
    print(f"Successfully wrote data to {file_name}.")

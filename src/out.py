from typing import List, Dict, Any, Iterator


def to_csv(data: Iterator[Dict[str, Any]], filename: str): ...


def to_json(data: List[Dict[str, Any]]): ...


def to_jsonlines(data: List[Dict[str, Any]]): ...

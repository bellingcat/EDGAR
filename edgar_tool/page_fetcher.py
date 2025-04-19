import time
from random import uniform
from typing import Any, Callable, Optional


class ResultsTableNotFoundError(Exception):
    pass


class PageCheckFailedError(Exception):
    pass


class NoResultsFoundError(Exception):
    pass

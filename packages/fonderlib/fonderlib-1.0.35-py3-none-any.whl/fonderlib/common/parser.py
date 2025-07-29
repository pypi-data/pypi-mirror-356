# lib/parser.py

import argparse
from typing import Optional, Any


class CustomParser:
    """
    Class to handle dynamically arguments
    """

    def __init__(self, description="Parser de línea de comandos dinámico"):
        self.parser = argparse.ArgumentParser(description=description)

    def add_argument(
        self,
        name,
        type=str,
        required=False,
        help_text=Optional[str],
        default_param=Optional[Any],
        nargs=None,
        choices=None,
    ):
        """
        Adds an argument to the parser

        Args:
            name (str): Argument name(ej. "--edad").
            type (type): Data type (str, int, float, bool).
            required (bool): Mandatory or not
            help_text (str): Description of the argument.
        """
        self.parser.add_argument(
            name,
            type=type,
            required=required,
            default=default_param,
            help=help_text,
            nargs=nargs,
            choices=choices,
        )

    def parse(self):
        """
        Parse command line arguments

        Returns:
            Namespace: Object with parsed values
        """
        return self.parser.parse_args()

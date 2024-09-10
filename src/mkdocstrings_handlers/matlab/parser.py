from textmate_grammar.parsers.base import LanguageParser
from pathlib import Path


import logging
import yaml


logging.getLogger("textmate_grammar").setLevel(logging.ERROR)


class MatlabParser(LanguageParser):
    """
    Represents a grammar for the MATLAB language.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new instance of the MatlabGrammar class.

        Args:
            remove_line_continuations (bool, optional): Whether to remove line continuations. Defaults to False.
        """

        with open(Path(__file__).parent / "resources" / "grammar.yml") as file:
            try:
                grammar = yaml.load(file.read(), Loader=yaml.CLoader)
            except ImportError:
                grammar = yaml.load(file.read(), Loader=yaml.Loader)

        super().__init__(grammar, **kwargs)

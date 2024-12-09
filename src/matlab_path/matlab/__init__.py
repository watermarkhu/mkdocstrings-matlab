import logging

from textmate_grammar.parsers.matlab import MatlabParser
from textmate_grammar.utils import cache

logging.getLogger("textmate_grammar").setLevel(logging.ERROR)
cache.init_cache("shelve")

TM_PARSER = MatlabParser(remove_line_continuations=True)

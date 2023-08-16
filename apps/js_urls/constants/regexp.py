# Python Standard Library Imports
import re


URL_ARG_RE = re.compile(r"(\(.*?\))")
URL_KWARG_RE = re.compile(r"(\(\?P\<(.*?)\>.*?\))")
URL_OPTIONAL_CHAR_RE = re.compile(r"(?:\w|/)(?:\?|\*)")
URL_OPTIONAL_GROUP_RE = re.compile(r"\(\?\:.*\)(?:\?|\*)")
URL_PATH_RE = re.compile(r"(\<.*?\>)")

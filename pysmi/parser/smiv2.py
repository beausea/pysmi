#
# This file is part of pysmi software.
#
# Copyright (c) 2015-2017, Ilya Etingof <etingof@gmail.com>
# License: http://pysmi.sf.net/license.html
#
from pysmi.parser.smi import parserFactory
from pysmi.parser.dialect import smiV2

# compatibility stub
SmiV2Parser = parserFactory(**smiV2)

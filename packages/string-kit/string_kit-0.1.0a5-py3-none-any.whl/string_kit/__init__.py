# https://peps.python.org/pep-3101/
# https://stackoverflow.com/questions/19864302/add-custom-conversion-types-for-string-formatting

import re
from .formatter.power_formatter import PowerFormatter


RE_FORMAT_SPEC = re.compile(
    r'(?:(?P<fill>[\s\S])?(?P<align>[<>=^]))?'
    r'(?P<sign>[- +])?'
    r'(?P<pos_zero>z)?'
    r'(?P<alt>#)?'
    r'(?P<zero_padding>0)?'
    r'(?P<width_str>\d+)?'
    r'(?P<grouping>[_,])?'
    r'(?:(?P<decimal>\.)(?P<precision_str>\d+))?'
    r'(?P<type>[bcdeEfFgGnosxX%])?')
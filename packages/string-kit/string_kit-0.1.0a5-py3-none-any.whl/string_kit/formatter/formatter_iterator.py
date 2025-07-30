from collections.abc import Iterator
from functools import reduce
from typing import Hashable


class FormatterIterator(Iterator):
    def __init__(self,
                 format_string: str,
                 field_prefix: str = "{",
                 field_prefix_escape: str = "{",
                 field_suffix: str = "}",
                 field_suffix_escape: str = "}",
                 conversion_prefix: str = "!",
                 spec_prefix: str = ":"):
        self._format_string = self._clean_parm(
            format_string,
            "format_string",
            empty_allowed=True
        )
        self._field_prefix = self._clean_parm(
            field_prefix,
            "field_prefix"
        )
        self._field_prefix_escape = self._clean_parm(
            field_prefix_escape,
            "field_prefix_escape"
        )
        self._field_prefix_escaped = (self._field_prefix_escape
                                      + self._field_prefix)
        self._field_suffix = self._clean_parm(
            field_suffix,
            "field_suffix"
        )
        self._field_suffix_escape = self._clean_parm(
            field_suffix_escape,
            "field_suffix_escape",
        )
        self._field_suffix_escaped = (self._field_suffix_escape
                                      + self._field_suffix)
        self._conversion_prefix = self._clean_parm(
            conversion_prefix,
            "conversion_prefix"
        )
        self._spec_prefix = self._clean_parm(
            spec_prefix,
            "spec_prefix"
        )

        # parms containing same values are not allowed
        test_parms = {
            "field_prefix": self._field_prefix,
            "field_suffix": self._field_suffix,
            "conversion_prefix": self._conversion_prefix,
            "spec_prefix": self._spec_prefix
        }
        for test_parm, test_parm_value in test_parms.items():
            for test_with_parm, test_with_parm_value in test_parms.items():
                if test_with_parm == test_parm:
                    continue
                elif test_parm_value in test_with_parm_value:
                    raise ValueError(
                        f"Parm value {test_parm_value} for parm {test_parm}"
                        f" must not be equal or contained in parm value"
                        f" {test_with_parm_value} for parm {test_with_parm}")

    def __next__(self):
        if self._format_string:
            field_name, conversion_spec = None, []

            pos_map = {
                None: 0,
                "field_prefix_escaped":
                    self._format_string.find(self._field_prefix_escaped),
                "field_suffix_escaped":
                    self._format_string.find(self._field_suffix_escaped),
                "field_prefix": self._format_string.find(self._field_prefix),
                "field_suffix": self._format_string.find(self._field_suffix),
            }
            nearest, pos = _nearest(pos_map)

            if nearest == "field_prefix_escaped":
                literal = self._format_string[:pos] + self._field_prefix
                head = pos + len(self._field_prefix_escaped)
                self._format_string = self._format_string[head:]
            elif nearest == "field_suffix_escaped":
                literal = self._format_string[:pos] + self._field_suffix
                head = pos + len(self._field_suffix_escaped)
                self._format_string = self._format_string[head:]
            elif nearest == "field_prefix":
                literal = self._format_string[:pos]
                head = pos + len(self._field_prefix)
                self._format_string = self._format_string[head:]

                next_item = "field_name"
                while True:
                    curr_item, next_item = next_item, None
                    pos_map_cs = {
                        None: 0,
                        "conversion":
                            self._format_string.find(self._conversion_prefix),
                        "spec":
                            self._format_string.find(self._spec_prefix),
                        "field_suffix":
                            self._format_string.find(self._field_suffix)
                    }
                    nearest_cs, pos_cs = _nearest(pos_map_cs)

                    if nearest_cs == "conversion":
                        next_item = nearest_cs
                        curr_item_value = self._format_string[:pos_cs]
                        head = pos_cs + len(self._conversion_prefix)
                        self._format_string = self._format_string[head:]
                    elif nearest_cs == "spec":
                        next_item = nearest_cs
                        curr_item_value = self._format_string[:pos_cs]
                        head = pos_cs + len(self._spec_prefix)
                        self._format_string = self._format_string[head:]
                    elif nearest_cs == "field_suffix":
                        curr_item_value = self._format_string[:pos_cs]
                        head = pos_cs + len(self._field_suffix)
                        self._format_string = self._format_string[head:]
                    else:
                        raise ValueError(f"expected '{self._field_suffix}'"
                                         f" before end of string")

                    if curr_item == "field_name":
                        field_name = curr_item_value
                    elif curr_item in ["conversion", "spec"]:
                        conversion_spec.append((curr_item, curr_item_value))

                    if not next_item:
                        break
            elif nearest == "field_suffix":
                raise ValueError(f"Field closing '{self._field_suffix}'"
                                 f" encountered without opening"
                                 f" '{self._field_prefix}'")
            else:
                literal = self._format_string
                self._format_string = ""

            if literal or field_name is not None or conversion_spec:
                return literal, field_name, conversion_spec
            else:
                raise StopIteration
        else:
            raise StopIteration

    def _clean_parm(self,
                    parm: str,
                    parm_name: str,
                    *,
                    empty_allowed: bool = False):
        exception_prefix = f"{self.__class__.__name__}.{parm_name}: "
        if isinstance(parm, str):
            if not parm and not empty_allowed:
                raise ValueError(f"{exception_prefix}cannot be empty")
        else:
            raise TypeError(f"{exception_prefix}expected `str`, got"
                            f" `{parm.__class__.__name__}`")
        return parm


def _nearest(pos_map: dict[Hashable, int]) -> tuple[Hashable, int]:
    nearest = reduce(lambda x, y:
                     y if pos_map[y] >= 0
                          and (x is None or pos_map[y] < pos_map[x])
                     else x,
                     pos_map)
    return nearest, pos_map[nearest]

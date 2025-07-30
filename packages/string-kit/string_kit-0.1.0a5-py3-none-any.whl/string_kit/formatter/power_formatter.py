from datetime import datetime
import re
from string import Formatter
from typing import Any, Mapping, Self, Sequence
import uuid
from .convertors import slugify
from .formatter_iterator import FormatterIterator


class _InexistentField:
    """
    Used for fields not matched by the args or kwargs. Implements __getitem__
    (called when accessed by subscript i.e. []) and __getattr__ (called when
    accessed as attribute, i.e. .attr) that return self so that it works in
    chains.
    """
    def __getitem__(self, key: object) -> Self:
        return self

    def __getattr__(self, attr: str) -> Self:
        return self

    def __str__(self):
        return ""


_inexistent_field = _InexistentField()


class PowerFormatter(Formatter):
    """
    We try to follow the Python format-specification as much as possible.
    https://docs.python.org/3/library/string.html#format-specification-mini-language

    This is the flow of str.Formatter for reference:
    .format(...)
    |  *args converted to args, **kwargs to kwargs and vformat called
    |__ .vformat(...)
        |  creates used_vars empty set, calls _vformat, then calls
        |  check_unused_args which does nothing, could be overidden by subclass
        |__ ._vformat(...)
            |__ .parse(...)
            |      gets a tuple of parsed input at a time
            |__ .get_field(...)
            |   |__ .get_value(...)
            |__ .convert_field(...)
            |__ ._vformat(...)
            |__ .format_field(...)
            |__ .check_unused_args(...)
                   does nothing but provided as a method for subclass to
                   overwrite
    """
    _format_spec_pattern = re.compile(r"(?P<precision>\.\d+)?(?P<type>[\w]+)?")
    _default_convertors = {"capitalize": lambda s: s.capitalize(),
                           "lower": lambda s: s.lower(),
                           "lstrip": lambda s: s.lstrip(),
                           "rstrip": lambda s: s.rstrip(),
                           "slug": slugify,
                           "strip": lambda s: s.strip(),
                           "title": lambda s: s.title(),
                           "upper": lambda s: s.upper()}
    _default_fields = {"now": datetime.now,
                       "uuid1": uuid.uuid1,
                       "uuid4": uuid.uuid4,
                       "uuid5": uuid.uuid5}

    def __init__(self,
                 silence_missing_fields: bool = False,
                 field_defaults: Mapping = {},
                 convertors: Mapping = {},
                 field_namespaces: list[Mapping] | tuple[Mapping] = [],
                 field_prefix: str = "{",
                 field_prefix_escape: str = "{",
                 field_suffix: str = "}",
                 field_suffix_escape: str = "}",
                 conversion_prefix : str = "!",
                 spec_prefix: str = ":"):
        self._silence_missing_fields = silence_missing_fields
        self._field_defaults = {**self._default_fields, **field_defaults}
        self._field_prefix = field_prefix
        self._field_prefix_escape = field_prefix_escape
        self._field_suffix = field_suffix
        self._field_suffix_escape = field_suffix_escape
        self._conversion_prefix = conversion_prefix
        self._spec_prefix = spec_prefix

        for conversion, convertor in convertors.items():
            if not callable(convertor):
                raise ValueError(
                    f"Convertor associated with '{conversion}' is"
                    f" required to be a callable with exactly one argument."
                )
        self._convertors = {**self._default_convertors, **convertors}

        if not isinstance(field_namespaces, (list, tuple)):
            field_namespaces = [field_namespaces]
        self._field_namespaces = field_namespaces

    def convert_field(self, value, conversion):
        if conversion in self._convertors:
            return self._convertors[conversion](value)
        return super().convert_field(value, conversion)

    # def format_field(self, value, format_specs):
    #     # custom format spec can be processed here
    #     for format_spec in format_specs.split(":"):
    #         precision, ftype = (self._format_spec_pattern.match(format_spec)
    #                             .groups())
    #         if precision:
    #             precision = int(precision.lstrip("."))
    #         if ftype == "slug":
    #             value = slugify(value, allow_unicode=False)[:precision]
    #         else:
    #             value = super().format_field(value=value,
    #                                          format_spec=format_spec)
    #     return value

    # given a field_name, find the object it references.
    #  field_name:   the field being looked up, e.g. "0.name"
    #                 or "lookup[3]"
    #  used_args:    a set of which args have been used
    #  args, kwargs: as passed in to vformat
    def get_field(self, field_name, args, kwargs):
        obj, first = super().get_field(field_name, args, kwargs)
        if isinstance(obj, _InexistentField):
            obj = str(obj)
        return obj, first

    def get_value(self,
                  key: int | str,
                  args: Sequence[Any],
                  kwargs: Mapping[str, Any]) -> Any:
        """
        Searches for a value first in keywords sent to Formatter.format(), then
        looks in the field_namespaces in order and uses the first one found.
        """
        try:
            return super().get_value(key, args, kwargs)
        except IndexError as e:
            if self._silence_missing_fields:
                return _inexistent_field
            else:
                raise e
        except KeyError as e:
            for namespace in self._field_namespaces:
                if key in namespace:
                    return namespace[key]
            if key in self._field_defaults:
                value = self._field_defaults[key]
                if callable(value):
                    value = value()
                return str(value)
            if self._silence_missing_fields:
                return _inexistent_field
            else:
                raise e

    # returns an iterable that contains tuples of the form:
    # (literal_text, field_name, format_spec, conversion)
    # literal_text can be zero length
    # field_name can be None, in which case there's no
    #  object to format and output
    # if field_name is not None, it is looked up, formatted
    #  with format_spec and conversion and then used
    def parse(self, format_string):
        return FormatterIterator(
            format_string=format_string,
            field_prefix=self._field_prefix,
            field_prefix_escape=self._field_prefix_escape,
            field_suffix=self._field_suffix,
            field_suffix_escape=self._field_suffix_escape,
            conversion_prefix=self._conversion_prefix,
            spec_prefix=self._spec_prefix
        )
        # return super().parse(format_string)

    def _vformat(self,
                 format_string,
                 args,
                 kwargs,
                 used_args,
                 recursion_depth,
                 auto_arg_index=0):
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')

        result = []
        for literal_text, field_name, conversion_spec in (
                self.parse(format_string)):
            if literal_text:
                result.append(literal_text)

            if field_name is None:
                continue

            # handle arg indexing when empty field_names are given.
            if field_name == '':
                if auto_arg_index is False:
                    raise ValueError('cannot switch from manual field '
                                     'specification to automatic field '
                                     'numbering')
                field_name = str(auto_arg_index)
                auto_arg_index += 1
            elif field_name.isdigit():
                if auto_arg_index:
                    raise ValueError('cannot switch from manual field '
                                     'specification to automatic field '
                                     'numbering')
                # disable auto arg incrementing, if it gets
                # used later on, then an exception will be raised
                auto_arg_index = False

            # given the field_name, find the object it references
            #  and the argument it came from
            obj, arg_used = self.get_field(field_name, args, kwargs)
            used_args.add(arg_used)

            for oper_type, oper in conversion_spec:
                if oper_type == "conversion":
                    conversion = oper
                    obj = self.convert_field(obj, conversion)
                elif oper_type == "spec":
                    spec = oper
                    # expand spec if needed
                    spec, auto_arg_index = self._vformat(
                        spec,
                        args,
                        kwargs,
                        used_args,
                        recursion_depth-1,
                        auto_arg_index=auto_arg_index
                    )
                    # format the object and append to the result
                    obj = self.format_field(obj, spec)
            result.append(obj)

        return ''.join(result), auto_arg_index


# class ExtendedUUID(uuid.UUID):
#     import base64
#     format_spec_pattern = re.compile(r"(\.\d+)?(\w+)?")
#
#     def __format__(self, format_spec):
#         precision, ftype = \
#                 self.format_spec_pattern.match(format_spec).groups()
#         if precision:
#             precision = int(precision.lstrip("."))
#         if ftype == "":
#             return str(self)[:precision]
#         if ftype == "s":
#             return str(self)[:precision]
#         if ftype == "i":
#             return str(self.int)[:precision]
#         if ftype == "x":
#             return self.hex.lower()[:precision]
#         if ftype == "X":
#             return self.hex.upper()[:precision]
#         if ftype == "base32":
#             return (
#                 base64.b32encode(self.bytes).decode("utf-8").rstrip("=\n")
#                 [:precision]
#             )
#         if ftype == "base64":
#             return (
#                 base64.urlsafe_b64encode(self.bytes)
#                 .decode("utf-8")
#                 .rstrip("=\n")[:precision]
#             )
#         return super().__format__(format_spec)

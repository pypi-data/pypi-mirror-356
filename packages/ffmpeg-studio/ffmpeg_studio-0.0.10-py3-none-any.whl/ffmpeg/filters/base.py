from typing import Union
from ..inputs.streams import StreamSpecifier
from ..inputs.base_input import BaseInput
from ..utils import build_name_kvargs_format

"""
-i 1.png
-i 2.png
-i 3.png

-f  [1]filter=2=d:s:d[a] ;
    [a]filter=2=d:s:d[b]
    |----Filter-----|

Whole node in command
----
-f  [1]filter=2=d:s:d[a]
    [a]filter=2=d:s:d[b]
    |----Filter-----|

Node in Object form
FilterNode holds :
    parent node reference 
    Filter reference that will be used make filter expression
"""


class BaseFilter:
    """Base class for all FFmpeg filters."""

    def __init__(self, filter_name: str) -> None:

        self.filter_name = filter_name
        self.flags: dict = {}  # all args

        self.parent_nodes: list[BaseInput | StreamSpecifier] = []
        self.parent_stream: list[int | str | None] = []

        self.output_count = 1

    def add_input(self, node: Union[BaseInput, StreamSpecifier]):
        self.parent_nodes.append(node)

    def build(self) -> str:
        return build_name_kvargs_format(self.filter_name, self.flags)

    def get_outputs(self):
        return (
            StreamSpecifier(self)
            if self.output_count == 1
            else [StreamSpecifier(self, i) for i in range(self.output_count)]
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}, flags={self.flags}>"  # TODO get better printing scheme

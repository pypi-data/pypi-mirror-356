from collections.abc import Callable
import enum
from typing import Annotated, Any, overload

from numpy.typing import ArrayLike


class VpxGen(enum.Enum):
    Vp8 = 0

    Vp9 = 1

class VpxEncoder:
    @overload
    def __init__(self, config: VpxEncoder.Config) -> None: ...

    @overload
    def __init__(self, width: int, height: int) -> None: ...

    def encode(self, writer: Callable[[Any], Any]) -> None: ...

    def yPlane(self) -> Annotated[ArrayLike, dict(dtype='uint8', order='C')]: ...

    def copyGray(self, image: Annotated[ArrayLike, dict(dtype='uint8', order='C')]) -> None: ...

    class Config:
        def __init__(self, width: int, height: int) -> None: ...

        @property
        def width(self) -> int: ...

        @width.setter
        def width(self, arg: int, /) -> None: ...

        @property
        def height(self) -> int: ...

        @height.setter
        def height(self, arg: int, /) -> None: ...

        @property
        def fps(self) -> int: ...

        @fps.setter
        def fps(self, arg: int, /) -> None: ...

        @property
        def bitrate(self) -> int: ...

        @bitrate.setter
        def bitrate(self, arg: int, /) -> None: ...

        @property
        def threads(self) -> int: ...

        @threads.setter
        def threads(self, arg: int, /) -> None: ...

        @property
        def cpu_used(self) -> int: ...

        @cpu_used.setter
        def cpu_used(self, arg: int, /) -> None: ...

        @property
        def gen(self) -> VpxGen: ...

        @gen.setter
        def gen(self, arg: VpxGen, /) -> None: ...

class VpxDecoder:
    def __init__(self, gen: VpxGen) -> None: ...

    def decode(self, packet: bytes, on_frame_decoded: Callable[[Annotated[ArrayLike, dict(dtype='uint8', order='C')]], None]) -> None: ...

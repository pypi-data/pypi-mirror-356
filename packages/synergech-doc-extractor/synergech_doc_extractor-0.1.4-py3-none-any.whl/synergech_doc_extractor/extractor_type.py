
from typing import Union, BinaryIO, IO
import pathlib

ExtractorInputType = Union[str, pathlib.Path, IO[bytes], BinaryIO, bytes]

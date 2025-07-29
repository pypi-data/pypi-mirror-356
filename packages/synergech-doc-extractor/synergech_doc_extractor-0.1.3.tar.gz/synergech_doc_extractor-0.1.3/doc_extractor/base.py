from abc import ABC, abstractmethod
from typing import Union, BinaryIO, IO
import pathlib
from doc_extractor.extractor_type import ExtractorInputType 
from doc_extractor.exception_handling import FileReadError


class BaseExtractor(ABC):
    """
    Abstract base class for all document extractors.
    All extractors must implement extract_text().
    """
    def __init__(self, source: ExtractorInputType):
        self.source = self._normalize_source(source)

    def _normalize_source(self, source: ExtractorInputType) -> Union[pathlib.Path, bytes, BinaryIO]:
        if isinstance(source, (str, pathlib.Path)):
            return pathlib.Path(source)
        elif isinstance(source, bytes):
            return source
        elif hasattr(source, "read"):
            return source  # file-like object (BinaryIO)
        else:
            raise FileReadError("Unsupported input type provided to extractor.")

    @abstractmethod
    def extract_text(self):
        """
        Extract text content from the document.
        Should return a list of dicts like:
        [{"page": "1", "text": "..."}] or [{"sheet": "Sheet1", "text": "..."}]
        """
        pass

    def get_preview_images(self):
        """
        Optional: For formats like PDF, return page-wise preview images (in-memory PIL images).
        """
        return []


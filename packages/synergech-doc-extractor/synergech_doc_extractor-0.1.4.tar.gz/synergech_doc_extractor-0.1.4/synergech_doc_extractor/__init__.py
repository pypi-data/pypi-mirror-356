from synergech_doc_extractor.extractor_type import ExtractorInputType
from synergech_doc_extractor.base import BaseExtractor
from synergech_doc_extractor.extractors import DocxExtractor,ExcelExtractor,PDFExtractor
from synergech_doc_extractor.exception_handling import UnsupportedFormatError
from synergech_doc_extractor.utils import resolve_file_extension

class Extractor:
    @staticmethod
    def get_extractor(source: ExtractorInputType) -> BaseExtractor:
        match resolve_file_extension(source):
            case ".pdf":
                return PDFExtractor(source)
            case ".docx":
                return DocxExtractor(source)
            case ".xlsx" | ".xlsm":
                return ExcelExtractor(source)
            case ext:
                raise UnsupportedFormatError(f"Unsupported file type: {ext}")
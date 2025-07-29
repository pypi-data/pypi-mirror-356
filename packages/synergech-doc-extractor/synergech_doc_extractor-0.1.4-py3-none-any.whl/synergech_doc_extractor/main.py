# from extractor_type import ExtractorInputType
# from base import BaseExtractor
# from extractors import DocxExtractor,ExcelExtractor,PDFExtractor
# from exception_handling import UnsupportedFormatError
# from utils import resolve_file_extension

# class Extractor:
#     @staticmethod
#     def get_extractor(source: ExtractorInputType) -> BaseExtractor:
#         match resolve_file_extension(source):
#             case ".pdf":
#                 return PDFExtractor(source)
#             case ".docx":
#                 return DocxExtractor(source)
#             case ".xlsx" | ".xlsm":
#                 return ExcelExtractor(source)
#             case ext:
#                 raise UnsupportedFormatError(f"Unsupported file type: {ext}")
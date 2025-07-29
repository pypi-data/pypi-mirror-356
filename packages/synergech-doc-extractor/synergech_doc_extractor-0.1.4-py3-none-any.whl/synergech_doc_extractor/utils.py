import pathlib
from synergech_doc_extractor.extractor_type import ExtractorInputType

import pathlib
from typing import Union, IO, BinaryIO

ExtractorInputType = Union[str, pathlib.Path, IO[bytes], BinaryIO, bytes, bytearray]

def resolve_file_extension(source: ExtractorInputType) -> str:
    if isinstance(source, (str, pathlib.Path)):
        return pathlib.Path(source).suffix.lower()

    if hasattr(source, 'name'):
        return pathlib.Path(getattr(source, 'name')).suffix.lower()

    if isinstance(source, (bytes, bytearray)):
        header = source[:8]

        # PDF
        if header.startswith(b'%PDF'):
            return '.pdf'

        # DOCX, XLSX, PPTX, XLSM (all ZIP-based Office formats)
        if header.startswith(b'PK\x03\x04'):
            # Look deeper for [Content_Types].xml (requires full ZIP parsing)
            # But shortcut: check for common "magic" paths in the raw content
            if b'word/' in source:
                return '.docx'
            elif b'ppt/' in source:
                return '.pptx'
            elif b'xl/' in source and b'workbook' in source:
                if b'macrosheets' in source or b'vbaProject.bin' in source:
                    return '.xlsm'
                return '.xlsx'

        # XLS (legacy binary Excel) - D0 CF 11 E0 A1 B1 1A E1 = OLE compound
        if header.startswith(b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'):
            # We’d need full parsing to know if it’s Excel or Word
            # But most commonly XLS is used this way
            return '.xls'

    return ""

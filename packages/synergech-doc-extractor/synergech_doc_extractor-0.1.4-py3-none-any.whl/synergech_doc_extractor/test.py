from synergech_doc_extractor import Extractor
import pathlib
import json


# extractor = Extractor.get_extractor("pdfs/image-doc.pdf")

# data = extractor.extract_text()
# print(data)

# From str path
extractor = Extractor.get_extractor("doc_extractor/xl/macro.xlsm")
text = extractor.extract_text()


print(text[0]["formatted"])
# with open("output1.json", "w", encoding="utf-8") as f:
#     json.dump({"text": text}, f, ensure_ascii=False, indent=2)

# # From pathlib.Path
# extractor = Extractor.get_extractor(pathlib.Path("pdfs/image-doc.pdf"))
# print(extractor.extract_text())


# # From raw bytes
# with open("pdfs/image-doc.pdf", "rb") as f:
#     pdf_bytes = f.read()
# extractor = Extractor.get_extractor(pdf_bytes)
# print(extractor.extract_text())

# # From file-like object
# with open("pdfs/image-doc.pdf", "rb") as f:
#     extractor = Extractor.get_extractor(f)
#     print(extractor.extract_text())

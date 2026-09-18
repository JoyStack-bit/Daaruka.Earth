from pathlib import Path
from pypdf import PdfReader
import json


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


# --------------------------------------------------
# PDF PAGE EXTRACTION
# --------------------------------------------------

def extract_pages_from_pdf(pdf_path):
    """Extract text from a PDF while preserving page numbers."""

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text and text.strip():

            pages.append({
                "page": page_number,
                "text": text
            })

    return pages


# --------------------------------------------------
# TEXT CLEANING
# --------------------------------------------------

def clean_text(text):
    """Basic text cleaning."""

    text = " ".join(text.split())

    return text


# --------------------------------------------------
# CHUNKING
# --------------------------------------------------

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks."""

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


# --------------------------------------------------
# PROCESS ALL PDFs
# --------------------------------------------------

def process_all_pdfs():

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files.")

    all_chunks = []

    for pdf_path in pdf_files:

        print(f"\nProcessing: {pdf_path.name}")

        # ------------------------------------------
        # 1. Extract pages
        # ------------------------------------------

        pages = extract_pages_from_pdf(pdf_path)

        print(f"Extracted pages: {len(pages)}")

        document_chunk_count = 0

        # ------------------------------------------
        # 2. Process each page separately
        # ------------------------------------------

        for page_data in pages:

            page_number = page_data["page"]

            text = page_data["text"]

            print(
                f"  Page {page_number}: "
                f"{len(text)} characters"
            )

            # Clean
            text = clean_text(text)

            # Chunk
            chunks = chunk_text(text)

            # --------------------------------------
            # 3. Store metadata
            # --------------------------------------

            for chunk_index, chunk in enumerate(chunks):

                all_chunks.append({
                    "text": chunk,
                    "source": pdf_path.name,
                    "page": page_number,
                    "chunk_id": chunk_index
                })

                document_chunk_count += 1

        print(
            f"Created {document_chunk_count} chunks "
            f"from {pdf_path.name}"
        )

    print(
        f"\nTOTAL CHUNKS CREATED: "
        f"{len(all_chunks)}"
    )

    return all_chunks


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    chunks = process_all_pdfs()

    output_file = PROCESSED_DIR / "chunks.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"\nChunks saved to: "
        f"{output_file}"
    )
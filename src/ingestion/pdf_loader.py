from pathlib import Path
import fitz


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")


def extract_text_from_pdf(pdf_path):
    """Extract text from every page of a PDF."""
    
    document = fitz.open(pdf_path)
    
    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        pages.append({
            "page": page_number,
            "text": text
        })

    document.close()

    return pages


def main():
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(RAW_DATA_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")

        pages = extract_text_from_pdf(pdf_path)

        total_characters = sum(
            len(page["text"]) for page in pages
        )

        print(f"Pages: {len(pages)}")
        print(f"Characters extracted: {total_characters}")

        # Save extracted text
        output_file = (
            PROCESSED_DATA_DIR /
            f"{pdf_path.stem}.txt"
        )

        with open(output_file, "w", encoding="utf-8") as file:
            for page in pages:
                file.write(
                    f"\n\n===== PAGE {page['page']} =====\n\n"
                )
                file.write(page["text"])

        print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()
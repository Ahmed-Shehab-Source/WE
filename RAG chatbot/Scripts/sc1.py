from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup

START_URL = "https://te.eg/en/personal"

loader = RecursiveUrlLoader(
    url=START_URL,
    max_depth=2,              # Follow links up to 2 levels deep
    use_async=True,
    extractor=lambda html: BeautifulSoup(html, "html.parser").get_text(
        separator="\n", strip=True
    ),
)

docs = loader.load()

# Limit to first 10 pages
docs = docs[:10]

print(f"Loaded {len(docs)} pages")

for i, doc in enumerate(docs, start=1):
    print("=" * 80)
    print(f"Page {i}")
    print("URL:", doc.metadata.get("source"))
    print(doc.page_content[:500])
    print()


    from pathlib import Path

output_dir = Path("te_docs")
output_dir.mkdir(exist_ok=True)

for i, doc in enumerate(docs, start=1):
    filename = output_dir / f"page_{i}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"URL: {doc.metadata.get('source')}\n\n")
        f.write(doc.page_content)

print("Done.")
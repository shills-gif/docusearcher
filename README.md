Text Analysis Project
=====================

📘 Overview
-----------
This project extracts and analyzes word frequency data from PDF documents, with a focus on memory efficiency and modular analysis.

It is built in Python and uses libraries such as `PyMuPDF`, `NLTK`, and `matplotlib` to:
- Extract text from PDFs page-by-page
- Tokenize and clean text (lowercase, punctuation removal, stopword filtering)
- Count word frequencies per page
- Visualize distribution of specific keywords
- Aggregate global word frequencies from the per-page analysis

🎯 Objectives
-------------
- Enable scalable analysis of large PDFs (e.g. government reports, academic papers)
- Store both per-page and overall word usage frequency
- Support filtering and visualization of specific terms like “AI” or “safety”
- Use modular scripts for clean separation of concerns

📁 Project Structure
--------------------
- `src/analyze_pdf.py` – Extracts text from PDF and creates `word_frequencies.txt` per page
- `src/glob_count.py` – Reads per-page frequency file and generates a global count
- `data/word_frequencies.txt` – Per-page word counts
- `data/global_word_frequencies.txt` – Aggregated counts across document
- `venv/` – Python virtual environment (not included in repo)
- `requirements.txt` – Package dependencies

⚙️ How to Run
-------------
1. Install dependencies in a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Run the main analysis script to extract per-page frequencies:
   ```bash
   python src/analyze_pdf.py
   ```

3. Generate global word frequency from the output file:
   ```bash
   python src/glob_count.py
   ```

📦 Dependencies
---------------
- fitz (PyMuPDF)
- nltk
- matplotlib

📝 Notes
--------
- NLTK stopwords must be downloaded on first use via `nltk.download('stopwords')`
- Make sure the `data/` folder exists or will be created by the script.
- Uses generator functions to efficiently handle large PDF files.

📄 License
----------
MIT License

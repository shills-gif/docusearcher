import re
import os
import fitz  # PyMuPDF for extracting text from PDFs
from collections import Counter
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

# Ensure NLTK stopwords are available
nltk.download('stopwords')

# Define additional words to filter out, including function words, citation tokens, etc.
EXTRA_STOPWORDS = {
    "pp", "2022", "2023", "2024",
    "many", "often", "use", "however",
    "example", "used", "proceedings", "also", "arxiv"
}

# Combine NLTK stopwords with our additional words
STOPWORDS = set(stopwords.words('english')).union(EXTRA_STOPWORDS)

# Determine the base directory reliably:
# If the script is in src, go one level up to the project root.
if '__file__' in globals():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
else:
    BASE_DIR = os.path.abspath(os.getcwd())

# Define paths relative to the project root
PDF_PATH = os.path.join(BASE_DIR, "data", "international_scientific_report_ai_interim_2024.pdf")
OUTPUT_DIR = os.path.join(BASE_DIR, "data")

# Define the number of top words to analyze
NUM_WORDS = 100  # Change this value to, for example, 100 to analyze the top 100 words

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file page by page."""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text("text")
            if text.strip():
                yield text

def preprocess_text(text):
    """
    Cleans and tokenizes text: converts to lowercase, removes punctuation,
    filters out stopwords and single-character tokens.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    return [word for word in words if word not in STOPWORDS and len(word) > 1]

def analyze_pdf_and_save_cumulative(pdf_path, output_file):
    """
    Processes the PDF to compute cumulative word frequency analysis and writes
    the top NUM_WORDS most common words to the output file.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    print(f"\n🔄 Processing PDF and saving cumulative word frequencies to: {output_file}")

    cumulative_counter = Counter()

    try:
        # Aggregate word frequencies from all pages
        for text in extract_text_from_pdf(pdf_path):
            words = preprocess_text(text)
            cumulative_counter.update(words)
        
        # Write cumulative word frequency summary to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("Cumulative Word Frequency Analysis\n")
            f.write("=" * 50 + "\n")
            for word, count in cumulative_counter.most_common(NUM_WORDS):
                f.write(f"{word}: {count}\n")

        print(f"\n✅ Cumulative word frequency data successfully saved to: {output_file}")

    except Exception as e:
        print(f"\n❌ Error saving file: {e}")

def visualize_word_distribution(pdf_path, target_word):
    """
    Creates a graph showing the distribution of a target word across pages.
    (This function still operates on a per-page basis for visualization purposes.)
    """
    pages, frequencies = [], []
    page_num = 1

    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text("text")
            words = preprocess_text(text)
            word_count = Counter(words)
            pages.append(page_num)
            frequencies.append(word_count.get(target_word, 0))
            page_num += 1

    plt.figure(figsize=(10, 5))
    plt.plot(pages, frequencies, marker="o", linestyle="-", color="b", label=target_word)
    plt.xlabel("Page Number")
    plt.ylabel("Word Frequency")
    plt.title(f"Distribution of '{target_word}' in AI Safety Report")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Set how many output files you want to generate.
    NUM_OUTPUTS = 1

    for i in range(1, NUM_OUTPUTS + 1):
        output_file = os.path.join(OUTPUT_DIR, f"cumulative_word_frequencies_{i}.txt")
        analyze_pdf_and_save_cumulative(PDF_PATH, output_file)
    
    # Optional: Visualization for a target word; change target_word as needed.
    target_word = "ai"
    visualize_word_distribution(PDF_PATH, target_word)

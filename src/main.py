import re
from collections import Counter

def preprocess_text(text):
    """Lowercases, removes punctuation, and tokenizes text."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    words = text.split()
    return words

def word_frequency(filepath):
    """Reads a file and counts word frequency."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    words = preprocess_text(text)
    return Counter(words)

if __name__ == "__main__":
    filepath = "../data/sample.txt"
    word_counts = word_frequency(filepath)
    
    print("Word Frequency Count:")
    for word, count in word_counts.most_common(10):
        print(f"{word}: {count}")

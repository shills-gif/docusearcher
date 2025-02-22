import os
import matplotlib.pyplot as plt
import numpy as np

def parse_frequency_file(file_path):
    """
    Parses a cumulative frequency file.
    Expects a header followed by lines in the format: "word: count".
    Returns two dictionaries:
      - freq_dict: mapping words to their raw counts.
      - normalized_dict: mapping words to their relative frequency (count / total words).
    """
    freq_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' not in line:
                continue  # Skip header or malformed lines
            parts = line.strip().split(':')
            if len(parts) != 2:
                continue
            word = parts[0].strip()
            try:
                count = int(parts[1].strip())
                freq_dict[word] = count
            except ValueError:
                continue
    total_count = sum(freq_dict.values())
    normalized_dict = {word: count / total_count for word, count in freq_dict.items()}
    return freq_dict, normalized_dict

def compare_normalized_frequency_files(file1, file2, top_n=100, top_common=20, txt_output_path=None):
    """
    Compares two cumulative frequency files using normalized word frequencies.
    
    Parameters:
      file1, file2: Paths to the frequency files.
      top_n: Consider only the top_n words (by raw frequency) from each file.
      top_common: From the intersection of the two top_n lists, display the top_common words.
      txt_output_path: If provided, the raw analysis output will be saved to this text file.
    
    The function:
      1. Parses each file and computes normalized frequencies.
      2. Limits analysis to the top_n words of each file.
      3. Finds common words and sorts them by the sum of their normalized frequencies.
      4. Prints a comparison table.
      5. Saves the raw table to a text file if a path is provided.
      6. Visualizes the comparison with a grouped bar chart and a scatter plot.
    """
    freq1, norm1 = parse_frequency_file(file1)
    freq2, norm2 = parse_frequency_file(file2)
    
    # Limit to the top_n words by raw count for each file
    top_words1 = dict(sorted(freq1.items(), key=lambda item: item[1], reverse=True)[:top_n])
    top_words2 = dict(sorted(freq2.items(), key=lambda item: item[1], reverse=True)[:top_n])
    
    # Find common words among the two top_n sets
    common_words = set(top_words1.keys()).intersection(set(top_words2.keys()))
    
    # Sort common words by combined normalized frequency (relative frequency)
    sorted_common = sorted(common_words, key=lambda w: norm1[w] + norm2[w], reverse=True)
    display_words = sorted_common[:top_common]
    
    # Build and print the comparison table with normalized frequencies as percentages
    output_lines = []
    header = "Word\t2024 (%)\t2025 (%)\tDifference (%)"
    output_lines.append(header)
    print(header)
    for word in display_words:
        freq_2024_percent = norm1[word] * 100
        freq_2025_percent = norm2[word] * 100
        diff_percent = freq_2025_percent - freq_2024_percent
        line = f"{word}\t{freq_2024_percent:.2f}\t{freq_2025_percent:.2f}\t{diff_percent:.2f}"
        output_lines.append(line)
        print(line)
        
    # Save the raw analysis output into a text file if a path is provided.
    if txt_output_path:
        os.makedirs(os.path.dirname(txt_output_path), exist_ok=True)
        with open(txt_output_path, 'w', encoding='utf-8') as f:
            f.write("Word Frequency Analysis Comparison\n")
            f.write("="*50 + "\n")
            for line in output_lines:
                f.write(line + "\n")
        print(f"\nAnalysis successfully saved to {txt_output_path}")
        
    # Prepare data for visualization
    percentages_2024 = [norm1[word] * 100 for word in display_words]
    percentages_2025 = [norm2[word] * 100 for word in display_words]
    x = np.arange(len(display_words))
    width = 0.35

    # Create a grouped bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, percentages_2024, width, label='2024')
    ax.bar(x + width/2, percentages_2025, width, label='2025')
    ax.set_xlabel('Words')
    ax.set_ylabel('Relative Frequency (%)')
    ax.set_title('Comparison of Normalized Word Frequencies')
    ax.set_xticks(x)
    ax.set_xticklabels(display_words, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    # Create a scatter plot for further comparison
    plt.figure(figsize=(8, 8))
    plt.scatter(percentages_2024, percentages_2025, color='purple')
    plt.xlabel('2024 Relative Frequency (%)')
    plt.ylabel('2025 Relative Frequency (%)')
    plt.title('Scatter Plot of Normalized Word Frequencies')
    max_val = max(max(percentages_2024), max(percentages_2025))
    plt.plot([0, max_val], [0, max_val], 'r--', label='y = x')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

if __name__ == "__main__":
    # Paths to the cumulative frequency files (adjust if needed)
    file_2024 = os.path.join("data", "cum_freq_2024.txt")
    file_2025 = os.path.join("data", "cum_freq_2025.txt")
    # Define the path for the text file output in the data folder
    txt_output = os.path.join("data", "analysis_output.txt")
    compare_normalized_frequency_files(file_2024, file_2025, top_n=100, top_common=20, txt_output_path=txt_output)

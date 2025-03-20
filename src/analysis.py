import os
import csv
import numpy as np
from collections import defaultdict

def parse_frequency_file(file_path):
    """Parses a cumulative frequency file and returns raw counts and normalized frequencies."""
    freq_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' not in line:
                continue  # Skip header or malformed lines
            parts = line.strip().split(':')
            if len(parts) != 2:
                continue
            word = parts[0].strip().lower()  # Convert to lowercase
            try:
                count = int(parts[1].strip())
                freq_dict[word] = count
            except ValueError:
                continue
    total_count = sum(freq_dict.values()) or 1  # Prevent division by zero
    normalized_dict = {word: count / total_count for word, count in freq_dict.items()}
    return freq_dict, normalized_dict, total_count

def group_plural_words(freq_dict):
    """Groups singular and plural words together (e.g., risk and risks)."""
    grouped_dict = defaultdict(int)
    mapping = defaultdict(list)
    irregulars = {"children": "child", "mice": "mouse", "geese": "goose"}  # Add common exceptions
    
    for word in freq_dict:
        singular = word
        if word in irregulars:
            singular = irregulars[word]
        elif word.endswith('s') and len(word) > 3 and word[:-1] in freq_dict:
            singular = word[:-1]
        
        grouped_dict[singular] += freq_dict[word]
        if word != singular:
            mapping[singular].append(word)
    
    return grouped_dict, mapping

def compare_frequency_files(file1, file2, top_n=100, txt_output_path=None, csv_output_path=None):
    """Compares two frequency files and generates analysis for top words, including unique words."""
    freq1, norm1, total_count1 = parse_frequency_file(file1)
    freq2, norm2, total_count2 = parse_frequency_file(file2)

    grouped_freq1, mapping1 = group_plural_words(freq1)
    grouped_freq2, mapping2 = group_plural_words(freq2)

    total_count1 = sum(grouped_freq1.values()) or 1
    total_count2 = sum(grouped_freq2.values()) or 1
    norm1 = {word: count / total_count1 for word, count in grouped_freq1.items()}
    norm2 = {word: count / total_count2 for word, count in grouped_freq2.items()}

    all_words = set(grouped_freq1.keys()).union(set(grouped_freq2.keys()))
    common_words = set(grouped_freq1.keys()).intersection(set(grouped_freq2.keys()))

    sorted_all_words = sorted(all_words, key=lambda w: norm1.get(w, 0) + norm2.get(w, 0), reverse=True)[:top_n]
    
    unique_to_file1 = sorted(set(grouped_freq1.keys()) - common_words, key=lambda w: norm1.get(w, 0), reverse=True)[:top_n]
    unique_to_file2 = sorted(set(grouped_freq2.keys()) - common_words, key=lambda w: norm2.get(w, 0), reverse=True)[:top_n]

    def generate_analysis(word_list, title, txt_file, csv_file, norm_dict, mapping_dict):
        output_lines = []
        header = "Word\tRelative Frequency (%)\tGrouped"
        output_lines.append(header)
        print(f"\n{title}")
        print(header)

        csv_data = [["Word", "Relative Frequency (%)", "Grouped"]]

        for word in word_list:
            freq_percent = norm_dict.get(word, 0) * 100
            grouped_words = ', '.join(mapping_dict.get(word, []))
            
            line = f"{word}\t{freq_percent:.2f}\t{grouped_words}"
            output_lines.append(line)
            csv_data.append([word, f"{freq_percent:.2f}", grouped_words])
            print(line)

        # Save to text file
        if txt_file:
            os.makedirs(os.path.dirname(txt_file), exist_ok=True)
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.truncate(0)  # Clear old data
                f.write(f"{title}\n")
                f.write("="*50 + "\n")
                f.write(header + "\n")
                for line in output_lines:
                    f.write(line + "\n")
            print(f"\nAnalysis successfully saved to {txt_file}")

        # Save to CSV file
        if csv_file:
            os.makedirs(os.path.dirname(csv_file), exist_ok=True)
            with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                f.truncate(0)  # Clear old data
                writer = csv.writer(f)
                writer.writerow(["Total Word Count", f"2024: {total_count1} (File 1)", f"2025: {total_count2} (File 2)", "", ""])
                writer.writerows(csv_data)
            print(f"\nAnalysis successfully saved to {csv_file}")

    # Generate reports for words unique to each file
    generate_analysis(unique_to_file1, "Words Unique to 2024 (File 1)", 
                      txt_output_path.replace(".txt", "_unique_2024.txt"), 
                      csv_output_path.replace(".csv", "_unique_2024.csv"),
                      norm1, mapping1)

    generate_analysis(unique_to_file2, "Words Unique to 2025 (File 2)", 
                      txt_output_path.replace(".txt", "_unique_2025.txt"), 
                      csv_output_path.replace(".csv", "_unique_2025.csv"),
                      norm2, mapping2)

if __name__ == "__main__":
    # Ensure the script finds files relative to its own directory
    base_dir = os.path.dirname(os.path.abspath(__file__))  

    file_2024 = os.path.join(base_dir, "..", "data", "cum_freq_2024.txt")
    file_2025 = os.path.join(base_dir, "..", "data", "cum_freq_2025.txt")

    txt_output = os.path.join(base_dir, "..", "data", "analysis_output.txt")
    csv_output = os.path.join(base_dir, "..", "data", "analysis_output.csv")

    # Verify files exist before proceeding
    if not os.path.exists(file_2024):
        print(f"Error: File not found -> {file_2024}")
        exit(1)

    if not os.path.exists(file_2025):
        print(f"Error: File not found -> {file_2025}")
        exit(1)

    compare_frequency_files(file_2024, file_2025, top_n=100, txt_output_path=txt_output, csv_output_path=csv_output)


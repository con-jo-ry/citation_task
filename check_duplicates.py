#!/usr/bin/env python3
"""
Script to detect potential duplicate samples in a text file.
Samples are separated by '---' and duplicates are identified by matching first words.
Provides exact line numbers for each sample.
"""

import re
from collections import defaultdict

def analyze_file(filename):
    """
    Analyze the file for potential duplicate samples based on first words.
    
    Args:
        filename (str): Path to the file to analyze
    
    Returns:
        dict: Dictionary with first words as keys and list of (sample_num, exact_line_num) as values
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file '{filename}'. Trying with different encoding...")
        try:
            with open(filename, 'r', encoding='latin-1') as file:
                lines = file.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return {}
    
    # Dictionary to store first words and their occurrences
    first_words = defaultdict(list)
    
    sample_num = 0
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for separator
        if line == '---':
            sample_num += 1
            i += 1
            
            # Skip empty lines after separator
            while i < len(lines) and lines[i].strip() == '':
                i += 1
            
            # Now we should be at the first content line of the sample
            if i < len(lines):
                content_line = lines[i].strip()
                
                # Extract first word from this line
                if content_line:
                    # Find first meaningful word
                    first_word_match = re.search(r'\b\w+', content_line)
                    
                    if first_word_match:
                        first_word = first_word_match.group().lower()
                        
                        # Store sample number and exact line number (1-indexed)
                        exact_line_num = i + 1
                        first_words[first_word].append((sample_num, exact_line_num))
        
        i += 1
    
    return first_words

def report_duplicates(first_words_dict):
    """
    Report potential duplicates based on first words.
    
    Args:
        first_words_dict (dict): Dictionary from analyze_file function
    """
    duplicates_found = False
    
    print("=== DUPLICATE SAMPLE ANALYSIS ===\n")
    
    for first_word, occurrences in first_words_dict.items():
        if len(occurrences) > 1:
            duplicates_found = True
            print(f"First word: '{first_word}' appears {len(occurrences)} times:")
            for sample_num, line_num in occurrences:
                print(f"  - Sample #{sample_num} at line {line_num}")
            print()
    
    if not duplicates_found:
        print("No potential duplicates found based on first words.")
    
    # Summary statistics
    total_samples = sum(len(occurrences) for occurrences in first_words_dict.values())
    unique_first_words = len(first_words_dict)
    
    print(f"=== SUMMARY ===")
    print(f"Total samples analyzed: {total_samples}")
    print(f"Unique first words: {unique_first_words}")
    
    if duplicates_found:
        duplicate_groups = sum(1 for occurrences in first_words_dict.values() if len(occurrences) > 1)
        potential_duplicates = sum(len(occurrences) - 1 for occurrences in first_words_dict.values() if len(occurrences) > 1)
        print(f"Groups with potential duplicates: {duplicate_groups}")
        print(f"Total potential duplicate samples: {potential_duplicates}")

def main():
    filename = "todo_āryadeva_sūtaka.txt"
    
    print(f"Analyzing file: {filename}")
    print("Looking for potential duplicates based on first words...\n")
    
    # Analyze the file
    first_words_dict = analyze_file(filename)
    
    if first_words_dict:
        # Report results
        report_duplicates(first_words_dict)
    else:
        print("Analysis failed or no data found.")

if __name__ == "__main__":
    main()

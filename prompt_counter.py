#!/usr/bin/env python3
"""
Sample Analyzer
Counts the number of samples in all .txt files in the current directory.
Samples are separated by lines containing only '---'.
Analyzes quote tags to identify positive and negative examples.
"""
import os
import glob
import re
from typing import Dict, Tuple, List

def analyze_samples_in_file(filename: str) -> Tuple[int, int, int]:
    """
    Analyze samples in a single file.
    
    Returns:
        Tuple of (total_samples, samples_with_quotes, samples_without_quotes)
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Error reading {filename}: {e}")
        return 0, 0, 0
    
    lines = content.split('\n')
    total_samples = 0
    samples_with_quotes = 0
    samples_without_quotes = 0
    current_sample_content = []
    
    # Regex pattern to match <quote> tags with optional attributes
    quote_pattern = re.compile(r'<quote[^>]*>', re.IGNORECASE)
    
    for line in lines:
        if line.strip() == '---':
            # Process the current sample if it has content
            if any(line.strip() for line in current_sample_content):
                total_samples += 1
                sample_text = '\n'.join(current_sample_content)
                
                # Check if sample contains any <quote> tags
                if quote_pattern.search(sample_text):
                    samples_with_quotes += 1
                else:
                    samples_without_quotes += 1
            
            current_sample_content = []
        else:
            current_sample_content.append(line)
    
    # Process the last sample if it has content
    if any(line.strip() for line in current_sample_content):
        total_samples += 1
        sample_text = '\n'.join(current_sample_content)
        
        if quote_pattern.search(sample_text):
            samples_with_quotes += 1
        else:
            samples_without_quotes += 1
    
    return total_samples, samples_with_quotes, samples_without_quotes

def main():
    """Main function to analyze samples in all .txt files."""
    # Get all .txt files in the current directory
    txt_files = glob.glob('*.txt')
    
    if not txt_files:
        print("No .txt files found in the current directory.")
        return
    
    total_samples = 0
    total_with_quotes = 0
    total_without_quotes = 0
    file_results: Dict[str, Tuple[int, int, int]] = {}
    
    print("Analyzing samples in .txt files...")
    print("=" * 80)
    print(f"{'File':<30} {'Total':<8} {'With <quote>':<12} {'Without <quote>':<15} {'Negative %':<10}")
    print("-" * 80)
    
    for filename in sorted(txt_files):
        samples, with_quotes, without_quotes = analyze_samples_in_file(filename)
        file_results[filename] = (samples, with_quotes, without_quotes)
        
        total_samples += samples
        total_with_quotes += with_quotes
        total_without_quotes += without_quotes
        
        # Calculate percentage of negative examples
        negative_percent = (without_quotes / samples * 100) if samples > 0 else 0
        
        print(f"{filename:<30} {samples:<8} {with_quotes:<12} {without_quotes:<15} {negative_percent:<10.1f}%")
    
    print("=" * 80)
    
    # Calculate overall percentages
    overall_negative_percent = (total_without_quotes / total_samples * 100) if total_samples > 0 else 0
    overall_positive_percent = (total_with_quotes / total_samples * 100) if total_samples > 0 else 0
    
    print(f"{'TOTAL':<30} {total_samples:<8} {total_with_quotes:<12} {total_without_quotes:<15} {overall_negative_percent:<10.1f}%")
    print()
    print("SUMMARY:")
    print(f"  Total samples: {total_samples}")
    print(f"  Positive examples (with <quote> tags): {total_with_quotes} ({overall_positive_percent:.1f}%)")
    print(f"  Negative examples (without <quote> tags): {total_without_quotes} ({overall_negative_percent:.1f}%)")
    print(f"  Files processed: {len(txt_files)}")
    
    # Additional analysis
    if total_samples > 0:
        print()
        print("DATASET BALANCE:")
        if abs(overall_positive_percent - 50) < 10:
            print("  ✓ Dataset is well-balanced")
        elif overall_negative_percent > 60:
            print("  ⚠ Dataset is skewed towards negative examples")
        elif overall_positive_percent > 60:
            print("  ⚠ Dataset is skewed towards positive examples")
        else:
            print("  ℹ Dataset has moderate class imbalance")

if __name__ == "__main__":
    main()

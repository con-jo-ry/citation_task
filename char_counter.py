#!/usr/bin/env python3
"""
Script to analyze character count of samples in text files.
Samples are separated by '---' and reports any samples over 2000 characters.
Analyzes all .txt files in the current directory.
"""

import os
import glob
from collections import defaultdict

def analyze_file(filename):
    """
    Analyze the file for sample character counts.
    
    Args:
        filename (str): Path to the file to analyze
    
    Returns:
        list: List of tuples (sample_num, char_count, start_line, end_line) for samples over 2000 chars
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file '{filename}'. Trying with different encoding...")
        try:
            with open(filename, 'r', encoding='latin-1') as file:
                lines = file.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
    
    oversized_samples = []
    sample_num = 0
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for separator
        if line == '---':
            sample_num += 1
            separator_line = i
            i += 1
            
            # Skip empty lines after separator
            sample_start_line = i
            while i < len(lines) and lines[i].strip() == '':
                i += 1
            
            # Mark the actual content start
            content_start_line = i
            sample_content = []
            
            # Collect all lines until next separator or end of file
            while i < len(lines):
                current_line = lines[i].rstrip('\n\r')  # Remove only line endings, keep other whitespace
                
                # Check if we hit the next separator
                if current_line.strip() == '---':
                    break
                
                sample_content.append(current_line)
                i += 1
            
            # Calculate character count (excluding the separator line breaks)
            # Join with newlines to preserve original structure
            if sample_content:
                # Remove trailing empty lines
                while sample_content and sample_content[-1].strip() == '':
                    sample_content.pop()
                
                if sample_content:  # Only process if there's actual content
                    content_text = '\n'.join(sample_content)
                    char_count = len(content_text)
                    
                    # If over 2000 characters, record it
                    if char_count > 2000:
                        content_end_line = content_start_line + len(sample_content)
                        oversized_samples.append((sample_num, char_count, content_start_line + 1, content_end_line))
            
            # Don't increment i here since we might have stopped at a separator
            continue
        
        i += 1
    
    return oversized_samples

def report_oversized_samples(filename, oversized_samples):
    """
    Report samples that exceed 2000 characters.
    
    Args:
        filename (str): Name of the file being analyzed
        oversized_samples (list): List from analyze_file function
    """
    if not oversized_samples:
        return
    
    print(f"\n=== FILE: {filename} ===")
    print(f"Found {len(oversized_samples)} sample(s) over 2000 characters:\n")
    
    for sample_num, char_count, start_line, end_line in oversized_samples:
        print(f"Sample #{sample_num}:")
        print(f"  - Character count: {char_count:,}")
        print(f"  - Content starts at line: {start_line}")
        print(f"  - Content ends at line: {end_line}")
        print(f"  - Exceeds limit by: {char_count - 2000:,} characters")
        print()

def main():
    """
    Main function to analyze all .txt files in current directory.
    """
    # Find all .txt files in current directory
    txt_files = glob.glob("*.txt")
    
    if not txt_files:
        print("No .txt files found in current directory.")
        return
    
    print(f"Analyzing {len(txt_files)} .txt file(s) for samples over 2000 characters...")
    print("=" * 60)
    
    total_oversized = 0
    files_with_oversized = 0
    
    for filename in sorted(txt_files):
        oversized_samples = analyze_file(filename)
        
        if oversized_samples:
            files_with_oversized += 1
            total_oversized += len(oversized_samples)
            report_oversized_samples(filename, oversized_samples)
    
    # Summary
    print("=" * 60)
    print(f"=== SUMMARY ===")
    print(f"Files analyzed: {len(txt_files)}")
    print(f"Files with oversized samples: {files_with_oversized}")
    print(f"Total oversized samples: {total_oversized}")
    
    if total_oversized == 0:
        print("\n✅ All samples are within the 2000 character limit!")
    else:
        print(f"\n⚠️  Found {total_oversized} sample(s) exceeding 2000 characters across {files_with_oversized} file(s).")

if __name__ == "__main__":
    main()

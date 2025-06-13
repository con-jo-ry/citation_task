#!/usr/bin/env python3
"""
Sanskrit Prompt Counter

Counts the number of prompts in all .txt files in the current directory.
Prompts are separated by lines containing only '---'.
"""

import os
import glob
from typing import Dict

def count_prompts_in_file(filename: str) -> int:
    """Count the number of prompts in a single file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Error reading {filename}: {e}")
        return 0
    
    lines = content.split('\n')
    prompt_count = 0
    current_prompt_content = []
    
    for line in lines:
        if line.strip() == '---':
            # If we have content in the current prompt, count it
            if any(line.strip() for line in current_prompt_content):
                prompt_count += 1
            current_prompt_content = []
        else:
            current_prompt_content.append(line)
    
    # Count the last prompt if it has content
    if any(line.strip() for line in current_prompt_content):
        prompt_count += 1
    
    return prompt_count

def main():
    """Main function to count prompts in all .txt files."""
    # Get all .txt files in the current directory
    txt_files = glob.glob('*.txt')
    
    if not txt_files:
        print("No .txt files found in the current directory.")
        return
    
    total_prompts = 0
    file_counts: Dict[str, int] = {}
    
    print("Counting prompts in .txt files...")
    print("=" * 50)
    
    for filename in sorted(txt_files):
        prompt_count = count_prompts_in_file(filename)
        file_counts[filename] = prompt_count
        total_prompts += prompt_count
        print(f"{filename:<30} {prompt_count:>5} prompts")
    
    print("=" * 50)
    print(f"{'TOTAL':<30} {total_prompts:>5} prompts")
    print(f"\nProcessed {len(txt_files)} file(s)")

if __name__ == "__main__":
    main()

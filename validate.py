#!/usr/bin/env python3
"""
Sanskrit Citation Markup Validator

Validates Sanskrit text markup according to the specified format:
- Valid tags: <quote>, <author>, <title>
- Valid attributes: id, authorid, titleid, type
- Proper tag closure
- Unique IDs within each prompt (separated by ---)
- Proper attribute usage
"""

import re
import xml.etree.ElementTree as ET
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass

@dataclass
class ValidationError:
    line_number: int
    error_type: str
    message: str

class SanskritValidator:
    def __init__(self):
        self.valid_tags = {'quote', 'author', 'title'}
        self.valid_attributes = {'id', 'authorid', 'titleid', 'type'}
        self.valid_type_values = {'generic'}  # Add more as needed
        self.errors: List[ValidationError] = []
    
    def validate_file(self, filename: str) -> List[ValidationError]:
        """Validate a Sanskrit markup file."""
        self.errors = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            self.errors.append(ValidationError(0, "FILE_ERROR", f"File not found: {filename}"))
            return self.errors
        except UnicodeDecodeError:
            self.errors.append(ValidationError(0, "ENCODING_ERROR", "File encoding error - expected UTF-8"))
            return self.errors
        
        # Split into prompts
        prompts = self._split_into_prompts(content)
        
        for prompt_idx, (prompt_content, start_line) in enumerate(prompts):
            self._validate_prompt(prompt_content, start_line, prompt_idx + 1)
        
        return self.errors
    
    def _split_into_prompts(self, content: str) -> List[Tuple[str, int]]:
        """Split content into prompts separated by --- at line start."""
        lines = content.split('\n')
        prompts = []
        current_prompt = []
        start_line = 1
        
        for line_num, line in enumerate(lines, 1):
            if line.strip() == '---':
                if current_prompt:
                    prompts.append(('\n'.join(current_prompt), start_line))
                current_prompt = []
                start_line = line_num + 1
            else:
                current_prompt.append(line)
        
        # Add the last prompt if it exists
        if current_prompt:
            prompts.append(('\n'.join(current_prompt), start_line))
        
        return prompts
    
    def _validate_prompt(self, prompt_content: str, start_line: int, prompt_number: int):
        """Validate a single prompt."""
        lines = prompt_content.split('\n')
        used_ids: Set[str] = set()
        
        for line_offset, line in enumerate(lines):
            current_line = start_line + line_offset
            
            # Find all XML-like tags in the line
            tags = re.findall(r'<(/?)(\w+)([^>]*)>', line)
            
            for is_closing, tag_name, attributes_str in tags:
                # Validate tag name
                if tag_name not in self.valid_tags:
                    self.errors.append(ValidationError(
                        current_line, 
                        "INVALID_TAG", 
                        f"Invalid tag '<{tag_name}>' in prompt {prompt_number}. Valid tags are: {', '.join(self.valid_tags)}"
                    ))
                    continue
                
                # Skip validation for closing tags
                if is_closing:
                    continue
                
                # Parse and validate attributes
                if attributes_str.strip():
                    self._validate_attributes(attributes_str.strip(), current_line, prompt_number, used_ids, tag_name)
        
        # Validate XML structure
        self._validate_xml_structure(prompt_content, start_line, prompt_number)
    
    def _validate_attributes(self, attr_str: str, line_number: int, prompt_number: int, used_ids: Set[str], tag_name: str):
        """Validate attributes in a tag."""
        # Parse attributes
        attr_pattern = r'(\w+)=(["\'])([^"\']*)\2'
        attributes = re.findall(attr_pattern, attr_str)
        
        # Check for malformed attributes
        if not attributes:
            # Check if there's an attempt at attributes but they're malformed
            if '=' in attr_str:
                self.errors.append(ValidationError(
                    line_number,
                    "MALFORMED_ATTRIBUTE",
                    f"Malformed attribute syntax in prompt {prompt_number}: '{attr_str}'"
                ))
            return
        
        parsed_attrs = {name: value for name, _, value in attributes}
        
        # Validate attribute names
        for attr_name in parsed_attrs:
            if attr_name not in self.valid_attributes:
                self.errors.append(ValidationError(
                    line_number,
                    "INVALID_ATTRIBUTE",
                    f"Invalid attribute '{attr_name}' in prompt {prompt_number}. Valid attributes are: {', '.join(self.valid_attributes)}"
                ))
        
        # Validate ID uniqueness within prompt
        if 'id' in parsed_attrs:
            id_value = parsed_attrs['id']
            if id_value in used_ids:
                self.errors.append(ValidationError(
                    line_number,
                    "DUPLICATE_ID",
                    f"Duplicate ID '{id_value}' in prompt {prompt_number}"
                ))
            else:
                used_ids.add(id_value)
        
        # Validate type attribute values
        if 'type' in parsed_attrs:
            type_value = parsed_attrs['type']
            if type_value not in self.valid_type_values:
                self.errors.append(ValidationError(
                    line_number,
                    "INVALID_TYPE_VALUE",
                    f"Invalid type value '{type_value}' in prompt {prompt_number}. Valid values are: {', '.join(self.valid_type_values)}"
                ))
        
        # Validate tag-specific attribute usage
        self._validate_tag_specific_attributes(tag_name, parsed_attrs, line_number, prompt_number)
    
    def _validate_tag_specific_attributes(self, tag_name: str, attributes: Dict[str, str], line_number: int, prompt_number: int):
        """Validate that attributes are used appropriately for specific tags."""
        # Check for authorid/titleid usage in non-quote tags
        if tag_name != 'quote':
            if 'authorid' in attributes:
                self.errors.append(ValidationError(
                    line_number,
                    "INVALID_ATTRIBUTE_USAGE",
                    f"Attribute 'authorid' should only be used in <quote> tags, not <{tag_name}> in prompt {prompt_number}"
                ))
            if 'titleid' in attributes:
                self.errors.append(ValidationError(
                    line_number,
                    "INVALID_ATTRIBUTE_USAGE",
                    f"Attribute 'titleid' should only be used in <quote> tags, not <{tag_name}> in prompt {prompt_number}"
                ))
        
        # Check for type attribute usage (currently only valid for title tags)
        if 'type' in attributes and tag_name != 'title':
            self.errors.append(ValidationError(
                line_number,
                "INVALID_ATTRIBUTE_USAGE",
                f"Attribute 'type' should only be used in <title> tags, not <{tag_name}> in prompt {prompt_number}"
            ))
    
    def _validate_xml_structure(self, prompt_content: str, start_line: int, prompt_number: int):
        """Validate XML structure for proper tag closure."""
        # Extract just the XML tags to check structure
        xml_tags = re.findall(r'<[^>]*>', prompt_content)
        
        # Create a simplified XML structure to validate
        tag_stack = []
        line_offset = 0
        
        for line_offset, line in enumerate(prompt_content.split('\n')):
            current_line = start_line + line_offset
            
            # Find all tags in this line
            line_tags = re.findall(r'<(/?)(\w+)[^>]*>', line)
            
            for is_closing, tag_name in line_tags:
                if tag_name not in self.valid_tags:
                    continue  # Already reported as invalid tag
                
                if is_closing:
                    if not tag_stack:
                        self.errors.append(ValidationError(
                            current_line,
                            "UNMATCHED_CLOSING_TAG",
                            f"Closing tag </{tag_name}> without matching opening tag in prompt {prompt_number}"
                        ))
                    elif tag_stack[-1][0] != tag_name:
                        self.errors.append(ValidationError(
                            current_line,
                            "MISMATCHED_TAG",
                            f"Closing tag </{tag_name}> doesn't match opening tag <{tag_stack[-1][0]}> from line {tag_stack[-1][1]} in prompt {prompt_number}"
                        ))
                    else:
                        tag_stack.pop()
                else:
                    tag_stack.append((tag_name, current_line))
        
        # Check for unclosed tags
        for tag_name, line_num in tag_stack:
            self.errors.append(ValidationError(
                line_num,
                "UNCLOSED_TAG",
                f"Opening tag <{tag_name}> not closed in prompt {prompt_number}"
            ))

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python sanskrit_validator.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    validator = SanskritValidator()
    errors = validator.validate_file(filename)
    
    if not errors:
        print(f"✅ File '{filename}' is valid!")
    else:
        print(f"❌ Found {len(errors)} error(s) in '{filename}':")
        print()
        
        # Group errors by type for better readability
        error_groups = {}
        for error in errors:
            if error.error_type not in error_groups:
                error_groups[error.error_type] = []
            error_groups[error.error_type].append(error)
        
        for error_type, error_list in error_groups.items():
            print(f"## {error_type.replace('_', ' ').title()}")
            for error in error_list:
                print(f"  Line {error.line_number}: {error.message}")
            print()
        
        sys.exit(1)

if __name__ == "__main__":
    main()

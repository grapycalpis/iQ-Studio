# Copyright (c) 2025 Innodisk Corp.
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import glob
import re

def analyze_markdowns(root_dir):
    files = glob.glob(os.path.join(root_dir, '**/*.md'), recursive=True)
    report = []
    
    for f in files:
        if 'node_modules' in f or '.env' in f: continue
        rel_path = os.path.relpath(f, root_dir)
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                lines = content.split('\n')
                
                issues = []
                
                # Check 1: Images in fig/ or img/
                # Regex for markdown images: ![alt](path) and HTML <img src="path"
                md_imgs = re.findall(r'!\[.*?\]\((.*?)\)', content)
                html_imgs = re.findall(r'<img.*?src="(.*?)".*?>', content)
                for img in md_imgs + html_imgs:
                    if img.startswith('http'): continue
                    if 'fig/' not in img and 'img/' not in img:
                        issues.append(f"Image not in fig/ or img/ directory: {img}")
                        
                # Check 2: Code blocks language (bash for commands)
                # Just flag any ``` without a language identifier
                for i, line in enumerate(lines):
                    if line.strip() == '```':
                        # Check if it contains shell-like commands inside
                        j = i + 1
                        is_shell = False
                        while j < len(lines) and not lines[j].strip().startswith('```'):
                            if lines[j].strip().startswith('$') or lines[j].strip().startswith('apt ') or lines[j].strip().startswith('git ') or lines[j].strip().startswith('./'):
                                is_shell = True
                                break
                            j += 1
                        if is_shell:
                            issues.append(f"Line {i+1}: Terminal command code block missing 'bash' language tag.")
                            
                # Check 3: Notes formatting
                # Look for "Note:" or "Warning:" that doesn't start with ">"
                for i, line in enumerate(lines):
                    stripped = line.strip()
                    if stripped.lower().startswith('note:') or stripped.lower().startswith('warning:'):
                        issues.append(f"Line {i+1}: Note/Warning not properly quoted (missing '>'). Found: '{stripped}'")
                        
                # Check 4: Absolute links instead of relative for local files
                links = re.findall(r'\[.*?\]\((.*?)\)', content)
                hrefs = re.findall(r'href="(.*?)"', content)
                for link in links + hrefs:
                    if link.startswith('http') or link.startswith('#') or link.startswith('mailto:'):
                        continue
                    if link.startswith('/') or link.startswith('file://') or link.startswith('D:') or link.startswith('C:'):
                        issues.append(f"Absolute or invalid internal link: {link}")
                        
                if issues:
                    report.append(f"### {rel_path}")
                    for iss in issues:
                        report.append(f"- [ ] {iss}")
        except Exception as e:
            report.append(f"### {rel_path}\n- [ ] Error reading file: {e}")
            
    return '\n'.join(report)

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    report_content = analyze_markdowns(project_root)
    if report_content:
        print(report_content)
    else:
        print("No issues found! Perfect compliance.")

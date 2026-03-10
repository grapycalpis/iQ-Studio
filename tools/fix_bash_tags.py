# Copyright (c) 2025 Innodisk Corp.
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import glob
import re

def fix_markdowns(root_dir):
    files = glob.glob(os.path.join(root_dir, '**/*.md'), recursive=True)
    count = 0
    
    for f in files:
        if 'node_modules' in f or '.env' in f: continue
        try:
            with open(f, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            modified = False
            i = 0
            while i < len(lines):
                line = lines[i]
                if line.strip() == '```':
                    # Look ahead to guess language
                    j = i + 1
                    lang = ''
                    while j < len(lines) and not lines[j].strip() == '```':
                        content = lines[j].strip()
                        if content.startswith('$') or content.startswith('apt ') or content.startswith('git ') or content.startswith('./') or content.startswith('curl ') or content.startswith('sudo ') or content.startswith('pkill ') or content.startswith('gst-launch') or content.startswith('tar ') or content.startswith('benchmark_') or 'mount -o rw' in content or 'opkg ' in content or 'dpkg ' in content:
                            lang = 'bash'
                            break
                        elif 'import ' in content or 'print(' in content or 'ollama.chat' in content:
                            lang = 'python'
                            break
                        elif '{' in content or '"' in content:
                            # Might be JSON but let's be conservative
                            pass
                        j += 1
                    
                    if lang:
                        # Replace matched ``` with ```lang
                        # preserving leading whitespace
                        ws = line[:len(line) - len(line.lstrip())]
                        lines[i] = f"{ws}```{lang}\n"
                        modified = True
                i += 1
                
            if modified:
                with open(f, 'w', encoding='utf-8') as file:
                    file.writelines(lines)
                count += 1
                print(f"Fixed tags in: {f}")
        except Exception as e:
            print(f"Error reading/writing file {f}: {e}")
            
    print(f"Total files modified: {count}")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    fix_markdowns(project_root)

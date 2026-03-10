import os
import glob

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
files = glob.glob(os.path.join(project_root, '**/*.md'), recursive=True)
for f in files:
    if 'node_modules' in f or '.env' in f: continue
    try:
        with open(f, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            headings = [l.strip() for l in lines if l.startswith('#')]
            if headings:
                print(f"FILE: {f}")
                for h in headings:
                    print(f"  {h}")
    except Exception as e:
        pass

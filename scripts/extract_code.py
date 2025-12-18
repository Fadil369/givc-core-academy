#!/usr/bin/env python3
import os, re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TXT_PATH = os.path.join(BASE_DIR, 'givic-core-academy-code.txt')

if not os.path.exists(TXT_PATH):
    raise FileNotFoundError(f'File not found: {TXT_PATH}')

with open(TXT_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_path = None
buffer = []
for raw_line in lines:
    # Remove leading line numbers if present (e.g., "123: code")
    line = raw_line
    m = re.match(r"\d+:\s?(.*)", raw_line)
    if m:
        line = m.group(1) + '\n'
    if line.startswith('# '):
        # New file marker
        if current_path and buffer:
            # Write previous file
            out_path = os.path.join(BASE_DIR, current_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'w', encoding='utf-8') as out_f:
                out_f.writelines(buffer)
            print(f'Wrote {out_path}')
        # Extract path after '# '
        current_path = line[2:].strip()
        buffer = []
    else:
        if current_path:
            buffer.append(line)
# Write last file
if current_path and buffer:
    out_path = os.path.join(BASE_DIR, current_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as out_f:
        out_f.writelines(buffer)
    print(f'Wrote {out_path}')

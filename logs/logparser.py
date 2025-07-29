import re

def parse_log(file_path, keyword=None):
    entries = []
    with open(file_path, 'r') as file:
        for line in file:
            if keyword and keyword.lower() not in line.lower():
                continue
            entries.append({
                'timestamp': line[:15],
                'content': line.strip()
            })
    return entries

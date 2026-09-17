import os, re

def extract_repo(dump_path, target_dir='.'):
    with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split by ### FICHIER:
    parts = re.split(r'### FICHIER:\s*', content)
    for part in parts[1:]:
        lines = part.split('\n', 1)
        header = lines[0].strip()
        body = lines[1] if len(lines) > 1 else ''

        match = re.match(r'^(.*?)\s*\(\d+\s*octets\)', header)
        if match:
            rel_path = match.group(1).strip()
        else:
            rel_path = header.split()[0]

        # Clean trailing section separator
        if '################################################################################' in body:
            body = body.rsplit('################################################################################', 1)[0]

        body_str = body.strip()
        if body_str == '[fichier vide]' or '[fichier vide]' in body_str:
            content_to_write = ''
        else:
            content_to_write = body.lstrip('\n')

        full_path = os.path.join(target_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as out:
            out.write(content_to_write)

if __name__ == '__main__':
    extract_repo('/tmp/file_attachments/Übergestalt/uberokx-main.txt', '.')
    print("Extraction completed cleanly.")

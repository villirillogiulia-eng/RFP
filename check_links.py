import os
import re

def check_links(file_path):
    print(f"Checking links in {file_path}...")
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all href and src
    links = re.findall(r'(?:href|src)="([^"]+)"', content)
    for link in links:
        if link.startswith('http') or link.startswith('#'):
            continue
        
        # Check if local file exists
        if not os.path.exists(link):
            print(f"  [BROKEN] {link}")
        else:
            print(f"  [OK] {link}")

if __name__ == "__main__":
    check_links('index.html')
    check_links('map.html')

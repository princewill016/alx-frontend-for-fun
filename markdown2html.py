#!/usr/bin/python3
"""
markdown2html.py - Converts Markdown file to HTML
"""
import sys
import os
import hashlib

def md5_convert(text):
    """Converts text to MD5 hash"""
    return hashlib.md5(text.encode()).hexdigest()

def remove_c(text):
    """Removes all 'c' and 'C' characters from text"""
    return ''.join(ch for ch in text if ch.lower() != 'c')

def convert_markdown_line(line):
    """Converts a markdown line to its HTML equivalent"""
    # Headings
    for i in range(6, 0, -1):
        if line.startswith('#' * i + ' '):
            return f"<h{i}>{line[i+1:].strip()}</h{i}>"

    # Bold and Emphasis
    line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
    line = line.replace('__', '<em>', 1).replace('__', '</em>', 1)

    # MD5
    while '[[' in line and ']]' in line:
        start = line.index('[[')
        end = line.index(']]', start)
        content = line[start+2:end]
        line = line[:start] + md5_convert(content) + line[end+2:]

    # Remove 'c'
    while '((' in line and '))' in line:
        start = line.index('((')
        end = line.index('))', start)
        content = line[start+2:end]
        line = line[:start] + remove_c(content) + line[end+2:]

    return line.strip()

def process_markdown(lines):
    """Processes the markdown content and returns HTML"""
    html = []
    ul_open = False
    ol_open = False
    paragraph = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if paragraph:
                html.append("<p>\n    " + "<br />\n    ".join(paragraph) + "\n</p>")
                paragraph = []
            if ul_open:
                html.append("</ul>")
                ul_open = False
            if ol_open:
                html.append("</ol>")
                ol_open = False
            continue

        if stripped.startswith('- '):
            if ol_open:
                html.append("</ol>")
                ol_open = False
            if not ul_open:
                html.append("<ul>")
                ul_open = True
            html.append(f"    <li>{stripped[2:]}</li>")
        elif stripped.startswith('* '):
            if ul_open:
                html.append("</ul>")
                ul_open = False
            if not ol_open:
                html.append("<ol>")
                ol_open = True
            html.append(f"    <li>{stripped[2:]}</li>")
        elif stripped.startswith('#'):
            if paragraph:
                html.append("<p>\n    " + "<br />\n    ".join(paragraph) + "\n</p>")
                paragraph = []
            html.append(convert_markdown_line(stripped))
        else:
            paragraph.append(convert_markdown_line(stripped))

    if paragraph:
        html.append("<p>\n    " + "<br />\n    ".join(paragraph) + "\n</p>")
    if ul_open:
        html.append("</ul>")
    if ol_open:
        html.append("</ol>")

    return html

def main():
    """Main execution function"""
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(md_file):
        sys.stderr.write(f"Missing {md_file}\n")
        sys.exit(1)

    try:
        with open(md_file, 'r') as f:
            lines = f.readlines()

        html_lines = process_markdown(lines)

        with open(html_file, 'w') as f:
            f.write('\n'.join(html_lines))

        sys.exit(0)

    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(1)

if __name__ == "__main__":
    main()


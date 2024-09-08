import os
import markdown

def remove_chars(text, chars):
    for char in chars:
        text = text.replace(char, '')
    return text

def get_tao():
    tao = []

    files = [f for f in os.listdir('tao') if f.endswith('.md')]
    files.sort(key=lambda s: int(s.replace('.md', '')))

    for file in files:
        if file.endswith('.md'):
            with open(f'tao/{file}') as f:
                text = f.read()
                html = markdown.markdown(text)
                html = '\n'.join([remove_chars(line, '[]^123456789¹²³') for line in html.splitlines() if '[' not in line[:6] and ']' not in line[:6]])
                tao.append(html)

    return tao

if __name__ == '__main__':
    tao = get_tao()
    for i, chapter in enumerate(tao):
        print(f"\n{i}\n{chapter}")
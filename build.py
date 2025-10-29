import os
import shutil
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
ASSETS_DIR = BASE_DIR / 'assets'
DATA_FILE = BASE_DIR / 'data' / 'site.yml'
OUTPUT_DIR = BASE_DIR / 'dist'

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def ensure_out():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def copy_static():
    # Copy static files (css, js, fonts)
    dest = OUTPUT_DIR / 'static'
    shutil.copytree(STATIC_DIR, dest)

def copy_assets():
    dest = OUTPUT_DIR / 'assets'
    shutil.copytree(ASSETS_DIR, dest)

def render_templates(data):
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(['html', 'xml'])
    )

    pages = [
        ('index.html', 'index.html'),
        ('about.html', 'about.html'),
        ('music.html', 'music.html'),
        ('movies.html', 'movies.html'),
    ]

    for tpl_name, out_name in pages:
        tpl = env.get_template(tpl_name)
        rendered = tpl.render(site=data)
        out_path = OUTPUT_DIR / out_name
        out_path.write_text(rendered, encoding='utf-8')
        print(f'Wrote {out_path}')

def main():
    data = load_data()
    ensure_out()
    render_templates(data)
    copy_static()
    copy_assets()
    print('Build complete. Open dist/index.html')

if __name__ == '__main__':
    main()
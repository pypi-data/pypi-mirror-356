from pelican import signals
import os
import htmlmin
import csscompressor
import rjsmin
from bs4 import BeautifulSoup
import json
import re

MINIFY_ENABLED = True  # Can be toggled from Pelican config

def minify_file(path, filetype):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if filetype == 'html':
            soup = BeautifulSoup(content, 'html.parser')

            # Minify inline <style> tags
            for style_tag in soup.find_all('style'):
                if style_tag.string:
                    try:
                        minified_css = csscompressor.compress(style_tag.string)
                        style_tag.string.replace_with(minified_css)
                    except Exception as e:
                        print(f"⚠️ CSS minify error in {path}: {e}")

            # Minify inline <script> tags
            for script_tag in soup.find_all('script'):
                if script_tag.get('type') == 'application/ld+json':
                    # JSON-LD
                    try:
                        data = json.loads(script_tag.string)
                        minified_json = json.dumps(data, separators=(',', ':'))
                        script_tag.string.replace_with(minified_json)
                    except Exception as e:
                        print(f"⚠️ JSON-LD minify error in {path}: {e}")
                elif not script_tag.get('src') and script_tag.string:
                    # Inline JS
                    try:
                        minified_js = rjsmin.jsmin(script_tag.string)
                        script_tag.string.replace_with(minified_js)
                    except Exception as e:
                        print(f"⚠️ JS minify error in {path}: {e}")

            # Now minify entire HTML
            content = htmlmin.minify(
                str(soup),
                remove_comments=True,
                remove_empty_space=True
            )

        elif filetype == 'css':
            content = csscompressor.compress(content)

        elif filetype == 'js':
            content = rjsmin.jsmin(content)

        elif filetype == 'json':
            data = json.loads(content)
            content = json.dumps(data, separators=(',', ':'))

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Minified: {path}")

    except Exception as e:
        print(f"⚠️ Skipped {path} due to error: {e}")
        

def run_minifier(generator):
    global MINIFY_ENABLED
    if not MINIFY_ENABLED:
        print("⚠️ Skipping minification (MINIFY = False)")
        return

    output_path = generator.output_path

    for root, dirs, files in os.walk(output_path):
        for name in files:
            filepath = os.path.join(root, name)
            if name.endswith('.html'):
                minify_file(filepath, 'html')
            elif name.endswith('.css'):
                minify_file(filepath, 'css')
            elif name.endswith('.js'):
                minify_file(filepath, 'js')
            elif name.endswith('.json'):
                minify_file(filepath, 'json')

def load_settings(pelican_obj):
    global MINIFY_ENABLED
    MINIFY_ENABLED = pelican_obj.settings.get('MINIFY', True)

def register():
    signals.initialized.connect(load_settings)
    signals.finalized.connect(run_minifier)

# Pelican Minifier

Minify your Pelican blog's output — including HTML, CSS, JS, and JSON — automatically after generation.

---

## ✨ Features

- ✅ Minifies HTML, CSS, JavaScript, and JSON
- ✅ Handles inline `<style>`, `<script>`, and JSON-LD inside HTML
- ✅ Automatically runs after Pelican build
- ✅ Lightweight and dependency-minimal
- ✅ Works with Pelican 4.5+ namespace plugin system

---

## 📦 Installation

```bash
pip install pelican-minifier
````

Or install from source:

```bash
git clone https://github.com/layoutshub/pelican-minifier.git
cd pelican-minifier
pip install -e .
```

---

## ⚙️ Usage

In your `pelicanconf.py`:

```python
PLUGINS = ["minifier"]
```

Optionally, to disable minification during dev builds:

```python
MINIFY = False
```

---

## 📁 Files Handled

| File Type | Action                                    |
| --------- | ----------------------------------------- |
| `.html`   | Minifies HTML, inline CSS/JS, and JSON-LD |
| `.css`    | Minifies using `csscompressor`            |
| `.js`     | Minifies using `rjsmin`                   |
| `.json`   | Compact JSON formatting                   |

---

## 📚 Documentation

Full documentation:
📄 [https://layoutshub.github.io/pelican-minifier-plugin.html](https://layoutshub.github.io/pelican-minifier-plugin.html)

---

## 🔗 Links

* 🏠 Homepage: [https://github.com/layoutshub/pelican-minifier/](https://github.com/layoutshub/pelican-minifier/)
* 📦 PyPI: Coming soon!
* 🛠 Issues: Use [GitHub Issues](https://github.com/layoutshub/pelican-minifier/issues)

---

## 🧑‍💻 Authors

Built by [Vishal Chopra](https://github.com/vishalchopra666) | [Twitter](https://twitter.com/vishalchopra666)
See `pyproject.toml` for full author list.

---

## 📝 License

MIT License.
Free to use and modify.

---


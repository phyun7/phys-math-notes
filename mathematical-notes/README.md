# Mathematical Notes

A blank Zensical math blog with a chronological journal, category archives, full-text search, and stable statement links.

## Run locally

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
zensical serve
```

Open http://localhost:8000. On Windows, activate with `.venv\Scripts\activate`.

## Publish on GitHub Pages

1. Create a GitHub repository (for a personal homepage, use `YOUR_USERNAME.github.io`).
2. Upload this source tree, including `.github/workflows/pages.yml`, and push to `main`.
3. Under **Settings → Pages → Build and deployment**, choose **GitHub Actions**.
4. Open **Actions → Publish mathematical notes** and run it, or push a change. The workflow sets `site_url` to the actual Pages address automatically.

For an existing Git checkout:

```sh
git remote add github https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push github HEAD:main
```

No server or database is required.

Search engine indexing is disabled with a `noindex` meta tag in `overrides/main.html`. Remove that meta tag if you later want the blog indexed. This setting does not hide the public repository.

The configuration includes 662 shared macros. MathJax extensions for mathtools, upright Greek, bold symbols, and equation colors are enabled. Compatibility differences are documented in comments at the top of `docs/javascripts/mathjax.js`.

## Write a post

Create `docs/posts/your-note.md`:

```markdown
---
date: 2026-10-19
categories:
  - Topology
slug: your-note
---

# Your title

A short introduction shown on the homepage.

<!-- more -->

The rest of the post. Inline math: $H_2(X; \mathbb{Z})$.

\[ a^2 + b^2 = c^2\text. \]

<div class="statement" id="TO02" markdown>
<a class="statement-tag" href="#TO02">TO02</a>
**Lemma 2.** State your lemma here.

*Proof.* Write your argument. $\square$
</div>
```

The blog homepage, archives, categories, and search update automatically. `subjects.md` and `statements.md` are curated indexes; add new links there when useful. Link between posts using Markdown file paths, e.g. `[Lemma](another-note.md#TO01)` from another post. Never rename a statement ID once it has been shared.

Use `draft: true` in the front matter to exclude a post from production builds. The blog starts with no posts.

## Math and styling

MathJax configuration and custom macros live in `docs/javascripts/mathjax.js`. Existing macros include `\bbZ`, `\bbR`, `\bbC`, `\bbQ`, `\calB`, and `\wtilde`. Add your other TeX macros there. MathJax is a browser renderer, not a full TeX compiler: package-specific commands and diagrams may need alternatives.

Typography and colors live in `docs/stylesheets/notes.css`. Main site settings are in `zensical.toml`. Build the static output with `zensical build --clean`.

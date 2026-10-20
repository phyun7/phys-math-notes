# Mathematical Notes — sidebar edition

A blank, undated mathematical notebook with expandable subjects and chapters.
Pure white background, Times New Roman prose, 662 shared math macros, full-text
search, and no real name. Equations retain MathJax's math fonts. No mathematical
notes are supplied. Search indexing is disabled via the noindex tag in
overrides/main.html; the public GitHub repository itself remains discoverable.

## Update your existing GitHub site

1. Extract this ZIP. Open the extracted folder so you see docs, scripts,
   overrides, zensical.toml, etc.
2. Open your repository's main Code page, then Add file -> Upload files.
3. Drag the CONTENTS into the upload area, preserving each folder. Do not drag
   an enclosing sidebar-ready or mathematical-notes folder.
4. Commit to main. Existing files at matching paths are replaced.
5. Keep your existing .github/workflows/pages.yml. It does not need changing.
6. Wait for the Actions run to finish and refresh the site.

The key changes are zensical.toml, docs/stylesheets/notes.css, docs/index.md,
and the new docs/foundations/, docs/geometry/, and docs/topology/ directories.
Upload overrides/main.html to retain the noindex setting and
javascripts/mathjax.js inside docs/ to retain the latest shared macros.

If you have already written something in docs/index.md or another replaced
starter page, keep its text and remove only the front matter that says
hide: [navigation, toc]. Existing posts under docs/posts are not deleted by an
upload. This version disables the blog plugin; old files are still built but
will not appear in the explicit sidebar unless you add them to nav.

## Write notes without dates

Edit docs/foundations/category-theory/chapter-1/section-1.md, for example:

```markdown
# Your section title

Write here. Inline mathematics: $H_2(X; \bbZ)$.

\[ H_2(X; \bbZ) \cong \bbZ\text. \]

**Lemma.** State the lemma.

*Proof.* Write the proof. $\square$
```

No date, categories block, or <!-- more --> separator is required.

Use ## for subsections and ### for smaller subsections. The page headings
populate the right-hand table of contents. To link to another note, use a
relative Markdown file path. Statement blocks and custom MathJax macros still
work exactly as in the previous version.

## Change or add sidebar entries

The nav list near the top of zensical.toml controls the sidebar. All paths are
relative to docs/. Change the label before = to rename an entry.

For example, to add Section 2 in Chapter 1, create
`docs/foundations/category-theory/chapter-1/section-2.md` and add this next to
the Section 1 entry inside the existing Chapter 1 list:

```toml
{ "Section 2" = "foundations/category-theory/chapter-1/section-2.md" },
```

A named list creates an expandable group. A path creates a page link.
The index.md at the beginning of Chapter 1 makes the chapter heading clickable.
The initial Foundations / Category Theory / Chapter 1 structure is a blank
example of the hierarchy and can be renamed to your own subjects.

## Write locally with VS Code and GitHub Desktop (no terminal required)

1. Install GitHub Desktop from https://desktop.github.com/ and VS Code from
   https://code.visualstudio.com/ .
2. Sign in to GitHub Desktop with your GitHub account.
3. Choose File -> Clone repository, select your website repository, and choose
   a local folder. This downloads the current site, including your own edits.
4. Open that local repository folder in VS Code.
5. Edit .md files under docs/. Save your files.
6. In GitHub Desktop, review Changes, enter a summary, and click Commit to main.
7. Click Push origin. GitHub Actions builds and publishes the changes.
8. Before editing on another computer, use Fetch origin / Pull origin to get
   the latest changes. Avoid maintaining a separate extracted ZIP as your
   working copy once you have cloned the repository.

A Markdown editor preview may not support your custom macros. For an accurate
preview, optionally install Python and use Zensical locally:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\zensical serve
```

Run these commands in the repository folder and visit http://localhost:8000.
The preview automatically rebuilds when you save. No changes go online until
you commit and push.

## Settings

- Site title: site_name in zensical.toml.
- Fonts and colors: docs/stylesheets/notes.css.
- Shared math macros: docs/javascripts/mathjax.js (compatibility notes at top).
- Google indexing: remove the noindex meta tag from overrides/main.html if
  you later want the blog pages included in search results.
- The deployment workflow automatically sets site_url to your actual Pages URL.

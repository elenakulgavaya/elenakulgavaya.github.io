# QA Explained — Claude Code Instructions

## OG Image Generation

Every new post needs an OG image. The generator lives at `generate_og.py` (project root).

**When you create a new post, generate its OG image before finishing:**

```python
python3 generate_og.py
```

Or call directly from Python:

```python
from generate_og import render_og
render_og(
    title="Post Title.",          # append a period — matches the site style
    eyebrow="Category · Category · N min read",   # categories from front matter + word_count÷200
    out_path="assets/img/posts/<slug>-og.png",
)
```

Then add to the post's front matter:

```yaml
image:
  path: /assets/img/posts/<slug>-og.png
  alt: "Post Title"
```

**Eyebrow format:** capitalised categories joined by ` · `, then ` · N min read`
Read time comes from the post page (Chirpy theme: `strip_html | number_of_words: 'auto'` ÷ 180 wpm).
Check the live post at http://127.0.0.1:4000/ after serving locally.

**Title style:** append a trailing period to match the site's OG image convention.

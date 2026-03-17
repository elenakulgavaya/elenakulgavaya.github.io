# QA Explained

Personal blog by [Elena Kulgavaya](https://linkedin.com/in/ekulgavaya) — QA Tech Lead writing about test automation, CI/CD, and quality engineering.

**Live at:** [qaexplained.com](https://qaexplained.com)

## Stack

- [Jekyll](https://jekyllrb.com/) with the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme
- Hosted on GitHub Pages
- Comments via [Giscus](https://giscus.app/)

## Local development

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://localhost:4000`.

## Adding a post

Create a file in `_posts/` named `YYYY-MM-DD-post-title.md` with this front matter:

```yaml
---
layout: post
title: "Post Title"
date: YYYY-MM-DD 09:00:00 +0000
excerpt: "One sentence summary."
permalink: /post-title/
categories: [category]
tags: [tag1, tag2]
toc: true
---
```

Images go in `/images/` and are referenced as `/images/filename.png`.

## License

Content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
Theme: [MIT](https://github.com/cotes2020/jekyll-theme-chirpy/blob/master/LICENSE)

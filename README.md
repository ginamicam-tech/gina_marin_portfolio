# Gina Marín — Jekyll content

All projects, research entries and artworks live together as individual Markdown files. Content files contain YAML metadata and Markdown only. Templates control rendering; styling has not been redesigned.

## Structure

```text
content/
  _pages/           Home, About, Contact, Work and supporting overview pages
  _work/            One .md file per project, research entry or artwork
  _data/
    navigation.yml  Work, About, Contact (the wordmark links Home)
  media/            Images, videos and caption tracks
_layouts/
  default.html      Shared document, navigation and footer
  page.html         Pages and configurable work lists
  work.html         A project, research entry or artwork
_includes/
  work-list.html    Shared selection and list rendering
  media.html        Shared image, caption and video markup
  content.html      Base-path handling for Markdown links
  redirect.html     Compatibility for old page URLs
assets/             Existing template CSS and favicon
_site/              Generated output — never edit this
```

There are currently **51 entries**: 14 projects, 3 research entries and 34 artworks. BODY.INTERFACE is the research parent of Clinical Fold and Self Archive. The Work page shows every entry, without filtering. Each artwork has its own year, technique, dimensions, image and series.

## Edit or add an entry

Edit a file under `content/_work/`, or duplicate one and give it a unique `key` and `permalink`. The filename is for organisation; the permalink preserves the public URL.

```yaml
---
key: care-lab
name: CARE LAB | GRASP FESTIVAL
title: How can artistic experimentation open conversations about care?
type: project
tags:
  - participation
  - installation
  - learning
year: 2026
featured: true
order: 1
permalink: /work/care-lab/
role: Installation Designer & Facilitator at CARE LAB
cover:
  src: /content/media/home/care-lab.jpg
  alt: CARE LAB light-based physical installation with a visitor
---
```

Write the body as Markdown below the closing `---`.

- `type`: `project`, `research` or `artwork`.
- `tags`: reusable thematic categories, using consistent lowercase labels.
- `parent`: the stable `key` of a parent entry, when applicable.
- `series`: artwork grouping (`body-interface`, `chromatic-body`, `optical-pulse`).
- `order`: default list order; every entry has a numeric value.
- `featured`: available for future selections; Work currently ignores this flag and displays everything.
- `year`: taken from existing documentation where available; for projects it may be the first year of an activity spanning several years.
- `context`, `role`, `technique`, `dimensions`: facts displayed by the entry template.
- `cover`, `media`: image/video data rendered by the shared media template.
- `archive_notes`: original supplementary archive text, retained once with its project.
- `legacy_anchors`: compatibility for links from the former long artwork and research pages.

Keep prose in Markdown and facts in YAML. No HTML, Liquid includes or CSS belongs in these files. Layout defaults are configured centrally in `_config.yml`.

## Lists on pages

Pages select work through YAML. The current Work page uses:

```yaml
work_lists:
  - sort: order
```

That lists **all entries**, including projects, research and artworks. An example of a filtered list elsewhere:

```yaml
work_lists:
  - tags: [participation, installation]
    match: any
    sort: year
    reverse: true
    limit: 3
```

Supported selectors: `type`, `tags`, `match` (`any` by default, or `all`), `series`, `parent`, `featured`, `sort`, `reverse`, and `limit`. Multiple selectors combine as AND. Multiple lists can be configured in `work_lists`. The templates decide where and how they appear.

Studio, Artworks and Exhibitions have been removed. Their practice and series descriptions are in About; individual entries remain in Work. No redirects are provided for these removed pages or the old Practice alias. Home and the other general pages retain their existing prose; no copy editing was performed.

## Old URLs

Existing project URLs are preserved, even where they begin with `/portfolio/`. The Video Editing showcase is consolidated into Alta Gracia, with `/portfolio/moving-image/` redirecting to that project. Duplicate overview pages redirect: `/portfolio/` → `/work/`, `/profile/` → `/about/`. The research material is consolidated into BODY.INTERFACE and its children; `/research/` redirects to `/work/body-interface/`. Redirect templates retain URL fragments and provide a plain link without JavaScript.

## Run locally

```sh
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
cd /Users/madshobye/Media/codeRepo/ginewebsite/gina_marin_portfolio
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve --baseurl ""
```

Open http://localhost:4000. **Restart an already-running Jekyll server after this collection change**, because `_config.yml` is not reloaded automatically.

## Verify

```sh
bundle exec jekyll build
python3 scripts/validate-content.py _site
ruby scripts/validate-work.rb
```

Checks cover the 25 retained routes, all 51 work entries, unique keys/URLs, parent references, all-entry index, local media, links and fragments, and the absence of HTML/Liquid in content. `scripts/migration.json` records the original route-to-source mapping.

## GitHub Pages

Use this folder as the repository root, including `.github/`. Configure `url` and `baseurl` in `_config.yml`, select **Settings → Pages → Source → GitHub Actions**, and push to `main`. The workflow takes its hosting prefix from GitHub Pages. Nothing has been published by this restructuring.

Services is a single page at `/services/`, combining the existing service descriptions and methods. Its three former subpages have been deleted without redirects.

## Covers and square grids

Every page and work entry has a `cover` image in its YAML. The template displays it at full viewport height, with navigation over the image and content below. Existing work images are also retained uncropped in the body. Missing images use `content/media/placeholder.png` (the supplied white XX on black).

```yaml
cover:
  src: /content/media/example.jpg
  alt: Description of the image
  position: 50% 50%
thumbnail:
  src: /content/media/example-detail.jpg
  position: 50% 50%
```

`position` is optional and controls the crop focal point. `thumbnail` is optional; square listing cards use the cover by default. Listing grids adapt from three columns to two and then one on small screens. The homepage's `selected_work` references work keys and preserves its existing descriptions; `work_intro` and `after_work` hold the surrounding Markdown.

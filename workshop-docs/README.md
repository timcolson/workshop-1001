# HTMX & Datastar Workshop Documentation

This folder contains the workshop documentation site built with [Astro Starlight](https://starlight.astro.build/).

## Viewing the Documentation

### Development Server

```bash
cd workshop-docs
npm install      # First time only
npm run dev      # Starts at http://localhost:4321
```

### Production Build

```bash
npm run build    # Outputs to ./dist/
npm run preview  # Preview the build locally
```

## Structure

```
workshop-docs/
├── astro.config.mjs          # Starlight config & sidebar
├── src/
│   └── content/
│       └── docs/
│           ├── index.mdx           # Introduction
│           ├── part-1/             # Baseline app setup
│           ├── part-2/             # HTMX upgrades
│           ├── part-3/             # Datastar comparison
│           └── extras/             # Side quests & troubleshooting
└── package.json
```

## Features

- **Expressive Code** - Syntax highlighting with `ins={}` for additions (green) and `del={}` for deletions
- **Starlight Components** - Steps, Tabs, Cards, Asides (`:::tip`, `:::note`, `:::caution`)
- **Collapsible Navigation** - Sidebar sections can be expanded/collapsed
- **Dark/Light Mode** - Toggle in header
- **Search** - Built-in full-text search

## Adding Content

Pages are `.mdx` files in `src/content/docs/`. Example frontmatter:

```mdx
---
title: Page Title
description: Brief description for SEO
---

import { Steps, Tabs, TabItem } from '@astrojs/starlight/components';

Your content here...
```

## Learn More

- [Starlight Documentation](https://starlight.astro.build/)
- [Expressive Code](https://expressive-code.com/)
- [Astro Documentation](https://docs.astro.build)

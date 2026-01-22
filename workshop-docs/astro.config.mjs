// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';


// https://astro.build/config
export default defineConfig({
    site: 'https://timcolson.github.io',
    base: '/workshop-1001',
    integrations: [
        starlight({
            title: 'Workshop: Intro to HTMX & Datastar',
            customCss: [
                // Relative path to your custom CSS file
                './src/styles/custom.css',
            ],
            social: [
                { icon: 'github', label: 'GitHub', href: 'https://github.com/timcolson/workshop-1001' }
            ],
            sidebar: [
                {
                    label: 'Introduction',
                    slug: 'index',
                },
                {
                    label: 'Part I: Baseline App',
                    items: [
                        { label: 'Setup & Run', slug: 'part-1/setup' },
                        { label: 'Why Upgrade?', slug: 'part-1/why-upgrade' },
                        { label: 'App Structure', slug: 'part-1/app-structure' },
                    ],
                },
                {
                    label: 'Part II: HTMX',
                    collapsed: true,
                    items: [
                        { label: 'Inline Recipe Details', slug: 'part-2/inline-details' },
                        { label: 'Live Search Results', slug: 'part-2/live-search' },
                        { label: 'Infinite Scroll', slug: 'part-2/infinite-scroll' },
                    ],
                },
                {
                    label: 'Part III: Datastar',
                    collapsed: true,
                    items: [
                        { label: 'Introduction', slug: 'part-3' },
                    ],
                },
                {
                    label: 'Extras',
                    collapsed: true,
                    items: [
                        { label: 'Side Quests', slug: 'extras/side-quests' },
                        { label: 'Troubleshooting', slug: 'extras/troubleshooting' },
                    ],
                },
            ],
        }),
        mermaid({
            theme: 'forest',
            autoTheme: true,
            mermaidConfig: {
                flowchart: {
                    curve: 'basis'
                }
            }
        })
    ],
});

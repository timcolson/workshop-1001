// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'HTMX & Datastar Workshop',
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
					],
				},
				{
					label: 'Part II: HTMX Upgrades',
					collapsed: false,
					items: [
						{ label: 'Overview', slug: 'part-2' },
						{ label: 'Inline Recipe Details', slug: 'part-2/inline-details' },
						{ label: 'Live Search Results', slug: 'part-2/live-search' },
						{ label: 'Infinite Scroll', slug: 'part-2/infinite-scroll' },
					],
				},
				{
					label: 'Part III: Datastar',
					collapsed: true,
					items: [
						{ label: 'Comparison', slug: 'part-3' },
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
			// Expressive Code configuration for highlighting HTMX additions
			expressiveCode: {
				themes: ['github-dark', 'github-light'],
				styleOverrides: {
					// Custom styles for marked (ins) lines - green for additions
					textMarkers: {
						markHue: '130', // Green hue
						lineDiffIndicatorMarginLeft: '0.5em',
					},
				},
			},
		}),
	],
});

import { pluginLineNumbers } from '@expressive-code/plugin-line-numbers'

/** @type {import('@astrojs/starlight/expressive-code').StarlightExpressiveCodeOptions} */
export default {
  plugins: [pluginLineNumbers()],
  defaultProps: {
    // Disable line numbers by default
    showLineNumbers: false,
    // But enable line numbers for certain languages
    // overridesByLang: {
    //   'js,ts,html': {
    //     showLineNumbers: true,
    //   },
    // },
  },

  // You can set configuration options here
  themes: ['github-dark', 'github-light'],
  styleOverrides: {
    // You can also override styles
    borderRadius: '0.5rem',
    frames: {
      shadowColor: '#124',
    },
    // Custom styles for marked (ins) lines - green for additions
    textMarkers: {
        markHue: '130', // Green hue
        lineDiffIndicatorMarginLeft: '0.5em',
    },
  },
}

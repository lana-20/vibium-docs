// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Vibium CLI',
  tagline: 'The complete command reference for the Vibium browser automation CLI',
  favicon: 'img/favicon.ico',

  future: {v4: true},

  url: 'https://lana-20.github.io',
  baseUrl: '/vibium-docs/',

  organizationName: 'lana-20',
  projectName: 'vibium-docs',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenAnchors: 'throw',

  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },

  i18n: {defaultLocale: 'en', locales: ['en']},

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/lana-20/vibium-docs/tree/main/',
        },
        blog: false,
        theme: {customCss: './src/css/custom.css'},
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/docusaurus-social-card.jpg',
      colorMode: {respectPrefersColorScheme: true},
      navbar: {
        title: 'Vibium CLI',
        logo: {alt: 'Vibium', src: 'img/logo.svg'},
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docs',
            position: 'left',
            label: 'Docs',
          },
          {
            to: '/docs/commands',
            label: 'Command reference',
            position: 'left',
          },
          {
            href: 'https://github.com/VibiumDev/vibium',
            label: 'Vibium on GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Reference',
            items: [
              {label: 'Introduction', to: '/docs/intro'},
              {label: 'Global flags', to: '/docs/global-flags'},
              {label: 'All commands', to: '/docs/commands'},
            ],
          },
          {
            title: 'Upstream',
            items: [
              {label: 'Vibium', href: 'https://github.com/VibiumDev/vibium'},
              {label: 'Official docs', href: 'https://vibium.com'},
            ],
          },
        ],
        copyright:
          'An independent, community-maintained reference. Not affiliated with the Vibium project.',
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['bash', 'json'],
      },
    }),
};

export default config;

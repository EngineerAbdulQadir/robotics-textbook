import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Learn robotics through ROS 2, simulation, and hands-on exercises',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://engineerabdulqadir.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/robotics-textbook/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'EngineerAbdulQadir', // Usually your GitHub org/user name.
  projectName: 'robotics-textbook', // Usually your repo name.

  onBrokenLinks: 'warn', // Allow deployment with "coming soon" chapters

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: 'docs',
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/EngineerAbdulQadir/robotics-textbook/tree/master/book',
          showLastUpdateTime: false,
        },
        blog: false, // Disable blog feature
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'light',
      disableSwitch: true,
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'Robotics',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Learn',
        },
        {
          href: 'https://github.com/EngineerAbdulQadir/robotics-textbook',
          label: 'GitHub',
          position: 'right',
        },
        {
          type: 'custom-authButton',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learning Modules',
          items: [
            {
              label: 'Module 1: ROS 2 Fundamentals',
              to: '/docs/module-1/',
            },
            {
              label: 'Module 2: Sensors & Perception',
              to: '/docs/module-2/',
            },
            {
              label: 'Module 3: Navigation & SLAM',
              to: '/docs/module-3/',
            },
            {
              label: 'Module 4: Manipulation',
              to: '/docs/module-4/',
            },
            {
              label: 'Module 5: Advanced Topics',
              to: '/docs/module-5/',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub Repository',
              href: 'https://github.com/EngineerAbdulQadir/robotics-textbook',
            },
            {
              label: 'Report Issues',
              href: 'https://github.com/EngineerAbdulQadir/robotics-textbook/issues',
            },
            {
              label: 'Discussions',
              href: 'https://github.com/EngineerAbdulQadir/robotics-textbook/discussions',
            },
            {
              label: 'ROS Discourse',
              href: 'https://discourse.ros.org/',
            },
            {
              label: 'ROS Answers',
              href: 'https://answers.ros.org/',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'ROS 2 Documentation',
              href: 'https://docs.ros.org/en/humble/',
            },
            {
              label: 'Gazebo Simulator',
              href: 'https://gazebosim.org/',
            },
            {
              label: 'MoveIt 2',
              href: 'https://moveit.ros.org/',
            },
            {
              label: 'Nav2 Documentation',
              href: 'https://navigation.ros.org/',
            },
            {
              label: 'Contributing Guide',
              href: 'https://github.com/EngineerAbdulQadir/robotics-textbook/blob/master/CONTRIBUTING.md',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with ❤️ by Abdul Qadir. Powered by Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    docs: {
      sidebar: {
        hideable: false,
        autoCollapseCategories: true,
      },
    },
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 4,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

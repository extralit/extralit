/*
 * coding=utf-8
 * Copyright 2021-present, the Recognai S.L. team.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import Mode from "frontmatter-markdown-loader/mode";
import { NuxtConfig } from "@nuxt/types";
import pkg from "./package.json";

const LOCAL_ENVIRONMENT = "http://0.0.0.0:6900";
const BASE_URL = process.env.API_BASE_URL ?? LOCAL_ENVIRONMENT;
const DIST_FOLDER = process.env.DIST_FOLDER || "dist";

const config: NuxtConfig = {
  // Disable server-side rendering (https://go.nuxtjs.dev/ssr-mode)
  ssr: false,
  telemetry: false,
  generate: {
    dir: DIST_FOLDER,
  },

  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: "Extralit",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "" },
    ],
    link: [
      { rel: "icon", type: "image/x-icon", href: "favicon.ico" },
      {
        rel: "apple-touch-icon",
        sizes: "180x180",
        href: "apple-touch-icon.png",
      },
      { rel: "icon", sizes: "32x32", href: "favicon-32x32.png" },
      { rel: "icon", sizes: "16x16", href: "favicon-16x16.png" },
      { rel: "manifest", href: "site.webmanifest" },
    ],
    script: [
      ...(process.env.NODE_ENV === 'development' ? [{ src: 'http://localhost:8098', defer: true }] : [])
    ]
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: ["~assets/styles.scss"],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [{ src: "~/plugins" }],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: [
    {
      path: "~/components",
      pattern: "**/*.vue",
      pathPrefix: false,
      level: 1,
    },
  ],

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    "@nuxt/typescript-build",
    "@nuxtjs/composition-api/module",
    [
      "@pinia/nuxt",
      {
        disableVuex: false,
      },
    ],
    [
      "nuxt-compress",
      {
        gzip: {
          cache: true,
        },
        brotli: {
          threshold: 10240,
        },
      },
    ],
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    "@nuxtjs/style-resources",
    "@nuxtjs/axios",
    "@nuxtjs/auth-next",
    [
      "nuxt-highlightjs",
      {
        style: "obsidian",
      },
    ],
    "@nuxtjs/i18n",
  ],

  i18n: {
    locales: [
      {
        code: "en",
        name: "English",
        file: "en.js",
      },
      {
        code: "de",
        name: "Deutsch",
        file: "de.js",
      },
      {
        code: "es",
        name: "Español",
        file: "es.js",
      },
    ],
    detectBrowserLanguage: false,
    vueI18n: {
      fallbackLocale: "en",
    },
    lazy: true,
    langDir: "translation/",
    defaultLocale: "en",
    strategy: "no_prefix",
  },

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {
    proxy: true,
    browserBaseURL: "api",
  },

  proxy: {
    "/api/": {
      target: BASE_URL,
    },
    "/share-your-progress": {
      target: BASE_URL,
    },
  },
  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    cssSourceMap: false,
    cache: true,
    parallel: true,
    quiet: true,
    analyze: false,
    extend(config) {
      config.resolve.alias.vue = "vue/dist/vue.common";
      config.module.rules.push({
        test: /\.md$/,
        loader: "frontmatter-markdown-loader",
        options: {
          mode: [Mode.BODY],
        },
      });
      config.module.rules.push({
        test: /\.mjs$/,
        include: /node_modules/,
        type: 'javascript/auto',
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
            plugins: [
              ['@babel/plugin-transform-private-methods', { loose: true }],
              ['@babel/plugin-transform-class-properties', { loose: true }]
            ],
            compact: false,
          },
        },
      });
      config.module.rules.push({
        test: /\.js$/,
        include: /node_modules\/tabulator-tables/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
            plugins: [
              ['@babel/plugin-transform-private-methods', { loose: true }],
              ['@babel/plugin-transform-class-properties', { loose: true }]
            ],
            compact: false,
          },
        },
      });
    },
    postcss: {
      postcssOptions: {
        order: "presetEnvAndCssnanoLast",
        plugins: {
          cssnano:
            process.env.NODE_ENV === "production"
              ? {
                  preset: [
                    "default",
                    {
                      discardComments: {
                        removeAll: true,
                      },
                    },
                  ],
                }
              : false,
        },
      },
    },
    babel: {
      plugins: [
        ['@babel/plugin-transform-private-methods', { loose: true }],
        ['@babel/plugin-transform-class-properties', { loose: true }],
        ['@babel/plugin-proposal-class-properties', { loose: true }],
        ["@babel/plugin-transform-private-property-in-object", { loose: true }],
      ],
      presets: [
        ['@babel/preset-env', { targets: { node: 'current' }, loose: true }],
      ],
    },
    transpile: ['pdfjs-dist'],
    terser: {
      terserOptions: {
        keep_classnames: true,
        keep_fnames: true,
        compress: {
          drop_console: process.env.NODE_ENV === 'production'
        }
      },
    },
    extractCSS: true,
    splitChunks: {
      pages: false,
      commons: false,
      layouts: false,
    },
    optimization: {
      splitChunks: {
        name: false,
      },
    },
    filenames: {
      css: ({ isDev }) => (isDev ? "[name].css" : "[contenthash].css"),
    },
    publicPath: "/_nuxt/",
  },

  webpack: {
    devMiddleware: {
      stats: 'minimal'
    },
    watchOptions: {
      aggregateTimeout: 300,
      poll: 1000,
      ignored: /node_modules/
    }
  },

  // https://github.com/nuxt-community/style-resources-module
  styleResources: {
    scss: "./assets/scss/abstract.scss",
  },

  loading: false,

  auth: {
    strategies: {
      local: {
        endpoints: {
          logout: false,
          user: false,
          login: false,
        },
      },
    },
    cookie: false,
    resetOnError: true,
    redirect: { login: "/sign-in", logout: "/sign-in" },
  },

  router: {
    middleware: ["route-guard", "me"],
    base: process.env.BASE_URL ?? "/",
  },

  publicRuntimeConfig: {
    clientVersion: pkg.version,
    communityLink:
      "https://join.slack.com/t/extralit/shared_invite/zt-32blg3602-0m0XewPBXF7776BQ3m7ZlA",
    documentationSite: "https://docs.extralit.ai/",
    documentationPersistentStorage:
      "https://docs.extralit.ai/latest/getting_started/how-to-configure-argilla-on-huggingface/#persistent-storage",
  },
};
export default config;

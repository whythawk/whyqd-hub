// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  app: {
      head: {
        title: "whyqd.com",
        meta: [
          { charset: "utf-8" },
          // <meta name="viewport" content="width=device-width, initial-scale=1">
          { name: "viewport", content: "width=device-width, initial-scale=1" },
          {
            hid: "description",
            name: "description",
            content:
              "Perform schema-to-schema transforms for interoperability and data reuse. Transform messy data into structured schemas using readable, auditable methods.",
          },
        ],
        link: [
          { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
        ],
        script: [
          // <script src="https://myawesome-lib.js"></script>
          { src: "https://js.stripe.com/v3/" }
        ],
        noscript: [
          // <noscript>Javascript is required</noscript>
          { children: "Javascript is required" }
        ]
      },
      // pageTransition: { name: "page", mode: "out-in" }
    },
  runtimeConfig: {
    // https://nuxt.com/docs/api/composables/use-runtime-config#using-the-env-file
    // Private keys are only available on the server
    apiSecret: process.env.VUE_PRIVATE_TERM,
    // Public keys that are exposed to the client
    public: {
      appName: process.env.VUE_APP_NAME,
      appEnv: process.env.VUE_APP_ENV,
      apiWS: process.env.VUE_APP_DOMAIN_WS,
      apiUrl: process.env.VUE_APP_DOMAIN_API,
      appCookieExpire: 60 * 60 * 24 * 90,
      stripeKey: process.env.STRIPE_PUBLIC_KEY,
      // idbName: process.env.VUE_IDB_NAME,
      // idbVersion: process.env.VUE_IDB_VERSION,
    }
  },
  modules: [
      [
        "@pinia/nuxt",
        {
          autoImports: [
            // automatically imports `defineStore`
            "definePiniaStore",
            "defineStore", // import { defineStore } from "pinia"
          ],
        },
      ],
      "@pinia-plugin-persistedstate/nuxt",
      "@nuxt/content",
      "tailwindcss",
      // "@nuxtjs/i18n",
      "@kevinmarrec/nuxt-pwa"
  ],
  piniaPersistedstate: {
    cookieOptions: {
      path: "/",
      secure: true,
    },
  },
  content: {
    // https://content.nuxtjs.org/api/configuration
    watch: false,
    // @ts-ignore
    api: { baseURL: "/apc/_content" },
    navigation: {
      fields: ["title", "author", "publishedAt"]
    }
  },
  // PWA module configuration: https://go.nuxtjs.dev/pwa
  // @ts-ignore
  pwa: {
    meta: {
      name: "whyqd.com",
      author: "Gavin Chait",
      description:
        "Perform schema-to-schema transforms for interoperability and data reuse. Transform messy data into structured schemas using readable, auditable methods.",
      theme_color: "#c0651f",
      ogHost: "https://whyqd.com/",
      ogImage: {
        path: "https://whyqd.com/img/crosswalk.jpg",
        width: 1753,
        height: 806,
        type: "image/x-png"
      }
    },
    manifest: {
      name: "whyqd.com",
      short_name: "whyqd",
      description:
        "Perform schema-to-schema transforms for interoperability and data reuse. Transform messy data into structured schemas using readable, auditable methods.",
      lang: "en",
    },
  },
  css: ["~/assets/css/main.css"],
  postcss: {
      plugins: {
          tailwindcss: {},
          autoprefixer: {},
      },
  },
  build: {
    transpile: ["@heroicons/vue", "@headlessui/vue"]
  },
  vite: {
    base: "/_nuxt/"
  }
})

<template>
  <aside class="fixed inset-y-0 right-0 hidden w-52 md:w-72 overflow-y-auto py-6 md:px-2 md:block">
    <!-- Secondary column (hidden on smaller screens) -->
    <div class="hidden lg:block">
      <footer class="fixed bottom-0">
        <div class="mx-auto max-w-md overflow-hidden py-8 px-4 sm:max-w-3xl sm:px-6 lg:max-w-7xl">
          <nav class="-mx-5 -my-2 flex flex-wrap justify-center" aria-label="Footer">
            <div v-for="item in footerNavigation.main" :key="item.name">
              <NuxtLink :to="item.to" class="text-sm text-gray-400 hover:text-gray-300">{{ item.name }}</NuxtLink>
              <span v-show="item.dot" class="text-sm text-gray-400 px-2">&middot;</span>
            </div>
          </nav>
          <div class="mt-8 flex justify-center space-x-3">
            <a v-for="item in footerNavigation.social" :key="item.name" :href="item.href"
              class="text-gray-400 hover:text-gray-300">
              <span class="sr-only">{{ item.name }}</span>
              <component :is="item.icon" class="h-5 w-14" aria-hidden="true" />
            </a>
          </div>
          <div class="mt-5 text-left text-xs text-gray-400 content">
            <img src="/img/eu.svg" class="float-left w-9 mr-2 pt-1" />
            <p>Whyqd has
              <a href="https://eoscfuture-grants.eu/meet-the-grantees/implementation-no-code-method-schema-schema-data-transformations-interoperability"
                class="hover:text-gray-300">
                received funding</a> from the European Union’s Horizon 2020 research and innovation programme under grant
              agreement no 101017536.
            </p>
          </div>
          <p class="mt-5 text-center text-xs text-gray-400">&copy; 2023 {{ siteName }}. All rights reserved.</p>
        </div>
      </footer>
    </div>
  </aside>
</template>

<script setup lang="ts">
const siteName: String = "Whythawk"

const footerNavigation = {
  main: [
    { name: "About", to: "/about", dot: true },
    { name: "Pricing", to: "/pricing", dot: true },
    { name: "Developers", to: "https://whyqd.readthedocs.io/", dot: true },
    { name: "Privacy", to: "/privacy", dot: true },
    { name: "Contact", to: "/contact", dot: false },
  ],
  social: [
    {
      name: "Whythawk",
      href: "https://whythawk.com",
      icon: defineComponent({
        render: () =>
          h("svg", { fill: "currentColor", viewBox: "0 0 172 89" }, [
            h("path", {
              "fill-rule": "evenodd",
              d: "M83 5.4c0 2.2-.7 3.8-2 4.7-1.2.8-2.5 3.5-3.2 6.6L76.5 22h-11c-12.3 0-15-.9-25.4-7.9-6.9-4.7-13.2-6.7-18.3-5.7-4.2.8-19 7.9-20.7 10-.9 1.1.1 1.8 4.8 4 3.2 1.4 6.6 2.6 7.4 2.6 3.5 0 2.3 1.8-2.9 4.5-4.9 2.6-5.3 3.1-3.9 4.1.9.7 3.9 1.8 6.6 2.5 4.6 1.2 6.6 2.9 3.4 2.9-2.8 0-1.4 1.5 4.8 5.2C38.2 54.1 49 57.6 68.9 59.6c3.9.3 7.1 1 7.1 1.4 0 .5-2.8 4.5-6.1 9.1l-6.2 8.3 2.4 1.9c3 2.4 10.2 6 15.2 7.7 2.9.9 4.9.9 8.7 0 4.8-1.2 17-8.1 17-9.7 0-.5-2.7-4.4-6-8.8s-6-8.3-6-8.6c0-.4 3-1 6.8-1.4 8.4-.8 23.2-4 29.2-6.2 5-1.8 17.9-8.6 22.3-11.6 2.2-1.5 2.6-2.2 1.6-2.8-1.7-1-1.5-1.2 5.4-3.3 3.1-.9 5.7-2 5.7-2.4 0-.4-2.4-2-5.2-3.6l-5.2-2.8 6.2-2.3c10.2-3.7 10.4-4.2 2.9-9C158 11.2 149.6 8 145.1 8c-3.3.1-8.9 2.6-17 7.8-8.2 5.4-11.4 6.2-23.7 6.2H94.3l-.6-4.5c-.7-4.8-2.5-8.3-6.6-12.8-3.2-3.5-4.1-3.4-4.1.7zm6.5 5.6c1.4 2.8 2.5 6.6 2.5 9v4h11.3c13.7 0 17.1-.9 26.2-6.8 7.4-4.8 12.5-7.1 16.3-7.2 4.9-.1 21.2 7.4 21.2 9.8 0 1-8.1 3.9-13.3 4.8l-3.8.6 6.2 3.9 6.3 3.8-3 1.2c-1.6.7-6.7 1.5-11.4 1.8l-8.5.6 5.2 1.3c2.9.8 5.5 1.8 5.8 2.2.6.9-10.5 7.5-18.3 10.9-5.8 2.4-26.9 7-33 7.2-8.7.2-8.7.4-1.1 10.6l6.9 9.2-4.3 2.9c-6.5 4.4-13 6.6-17.4 5.7-4.4-.8-15.3-6.3-16-8.1-.2-.7 2.5-5.2 6.2-10.1 7.4-9.8 7.4-10-2.2-10.2-2.3-.1-9.7-1.2-16.5-2.6-9.7-1.9-14.4-3.5-22.3-7.4-15.1-7.5-15-7.4-7.9-9.9l5.9-2-5.9-.1c-5.4-.1-13.2-1.7-14.8-3-.4-.3 2-2.1 5.2-4 3.3-1.9 5.7-3.8 5.5-4.1-.3-.4-2.3-1-4.5-1.4-4.8-.8-12-3.5-12-4.6 0-1.6 14.1-8.1 18.7-8.7 5.7-.6 9.6.8 19.2 7 9 6 11.6 6.7 25.1 6.7h11.8l.6-5.4c.5-3.8 1.4-6 3.2-7.7C83.9 9.7 85 8.1 85 7.3c0-2.8 2.1-1.1 4.5 3.7z",
              "clip-rule": "evenodd",
            }),
          ]),
      }),
    },
    {
      name: "GitHub",
      href: "https://github.com/whythawk/whyqd-hub",
      icon: defineComponent({
        render: () =>
          h("svg", { fill: "currentColor", viewBox: "0 0 24 24" }, [
            h("path", {
              "fill-rule": "evenodd",
              d: "M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z",
              "clip-rule": "evenodd",
            }),
          ]),
      }),
    },
    {
      name: "Mastodon",
      href: "https://wandering.shop/@GavinChait",
      icon: defineComponent({
        render: () =>
          h("svg", { fill: "currentColor", viewBox: "0 0 512 512" }, [
            h("path", {
              "fill-rule": "evenodd",
              d: "M480,173.59c0-104.13-68.26-134.65-68.26-134.65C377.3,23.15,318.2,16.5,256.8,16h-1.51c-61.4.5-120.46,7.15-154.88,22.94,0,0-68.27,30.52-68.27,134.65,0,23.85-.46,52.35.29,82.59C34.91,358,51.11,458.37,145.32,483.29c43.43,11.49,80.73,13.89,110.76,12.24,54.47-3,85-19.42,85-19.42l-1.79-39.5s-38.93,12.27-82.64,10.77c-43.31-1.48-89-4.67-96-57.81a108.44,108.44,0,0,1-1-14.9,558.91,558.91,0,0,0,96.39,12.85c32.95,1.51,63.84-1.93,95.22-5.67,60.18-7.18,112.58-44.24,119.16-78.09C480.84,250.42,480,173.59,480,173.59ZM399.46,307.75h-50V185.38c0-25.8-10.86-38.89-32.58-38.89-24,0-36.06,15.53-36.06,46.24v67H231.16v-67c0-30.71-12-46.24-36.06-46.24-21.72,0-32.58,13.09-32.58,38.89V307.75h-50V181.67q0-38.65,19.75-61.39c13.6-15.15,31.4-22.92,53.51-22.92,25.58,0,44.95,9.82,57.75,29.48L256,147.69l12.45-20.85c12.81-19.66,32.17-29.48,57.75-29.48,22.11,0,39.91,7.77,53.51,22.92Q399.5,143,399.46,181.67Z",
              "clip-rule": "evenodd",
            }),
          ]),
      }),
    },
  ],
}
</script>
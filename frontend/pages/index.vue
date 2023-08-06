<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-7xl mx-auto">
    <div class="isolate mb-10">
      <svg
        class="absolute inset-0 -z-10 h-full w-full stroke-gray-200 [mask-image:radial-gradient(100%_100%_at_top_right,white,transparent)]"
        aria-hidden="true">
        <defs>
          <pattern id="0787a7c5-978c-4f66-83c7-11c213f99cb7" width="90" height="30" x="50%" y="-1"
            patternUnits="userSpaceOnUse">
            <path d="M.5 200V.5H200" fill="none" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" stroke-width="0" fill="url(#0787a7c5-978c-4f66-83c7-11c213f99cb7)" />
      </svg>
      <div v-if="auth.loggedIn">
        <CommonStartCard />
      </div>
      <div v-else>
        <div class="relative py-12 sm:py-16">
          <div class="mx-auto max-w-7xl px-6 lg:px-8">
            <div class="mx-auto max-w-2xl text-center">
              <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">Do more research,<br>for less
                wrangling
              </h1>
              <p class="mt-6 text-lg leading-8 text-gray-600">Transform messy data into structured schemas using
                readable,
                auditable methods. Perform schema-to-schema crosswalks for interoperability and data reuse.</p>
              <div class="mt-6 flex items-center justify-center gap-x-6">
                <NuxtLink v-if="!auth.loggedIn" to="/login"
                  class="rounded-md bg-ochre-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-ochre-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ochre-600">
                  Get started</NuxtLink>
                <NuxtLink to="/about" class="text-sm font-semibold leading-6 text-gray-900">Learn more <span
                    aria-hidden="true">→</span></NuxtLink>
              </div>
            </div>
            <div class="mt-12 flow-root sm:mt-20">
              <div
                class="-m-2 rounded-xl bg-gray-900/5 p-2 ring-1 ring-inset ring-gray-900/10 lg:-m-4 lg:rounded-2xl lg:p-4">
                <img class="rounded-md shadow-2xl ring-1 ring-gray-900/10" src="/img/crosswalk.jpg"
                  alt="Ugly data and the transformation method giving it a makeover." />
              </div>
            </div>
          </div>
        </div>
        <!-- Alternating Features -->
        <div class="mx-auto max-w-2xl px-4 sm:px-6 lg:max-w-5xl lg:px-8">
          <div class="mx-auto max-w-3xl text-center">
            <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Transform data management</h2>
            <p class="mt-4 text-gray-500">Your data are the foundation for research and decision-support. Ensure
              interoperability, transparency and probity by using readable, auditable crosswalks.</p>
          </div>
          <div class="mt-12 space-y-6">
            <div v-for="(feature, featureIdx) in features" :key="feature.name"
              class="flex flex-col-reverse lg:grid lg:grid-cols-12 lg:items-center lg:gap-x-4">
              <div
                :class="[featureIdx % 2 === 0 ? 'lg:col-start-1' : 'lg:col-start-5 xl:col-start-6', 'mt-6 lg:mt-0 lg:row-start-1 lg:col-span-8 xl:col-span-7']">
                <h3 class="text-lg font-medium text-gray-900">{{ feature.name }}</h3>
                <p class="mt-2 text-sm text-gray-500">{{ feature.description }}</p>
              </div>
              <div
                :class="[featureIdx % 2 === 0 ? 'lg:col-start-9 xl:col-start-8' : 'lg:col-start-1', 'flex-auto lg:row-start-1 lg:col-span-4 xl:col-span-5']">
                <div class="aspect-w-5 aspect-h-2 overflow-hidden rounded-lg bg-gray-100">
                  <img :src="feature.imageSrc" :alt="feature.imageAlt" class="mb-[-12%] object-cover object-center" />
                </div>
                <div class="relative" aria-hidden="true">
                  <div class="absolute -inset-x-0 bottom-0 bg-gradient-to-t from-white pb-[20%]" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useAuthStore } from "@/stores"
import { tokenIsTOTP } from "@/utilities"

const route = useRoute()
const appSettings = useSettingStore()
const auth = useAuthStore()

definePageMeta({
  layout: "home",
});

const redirectTOTP = "/totp"
const redirectAfterLogin = "/"

onMounted(async () => {
  appSettings.setPageName("Home")
  if (auth.loggedIn) console.log("Welcome back :)")
  else console.log("A Whyqd welcome :)")
  // Check if email is being validated
  if (route.query && route.query.magic) {
    // No idea: https://stackoverflow.com/q/74759799/295606
    await new Promise((resolve) => {
      setTimeout(() => {
        resolve(true)
      }, 100)
    })
    if (!auth.loggedIn) await auth.magicLogin(route.query.magic as string)
    if (tokenIsTOTP(auth.authTokens.token)) await navigateTo(redirectTOTP)
    else await navigateTo(redirectAfterLogin)
  }
})

// https://github.com/nuxt/nuxt/issues/14766
// Issues related to referencing '~/assets/img/...'
const features = [
  {
    name: "Derive schemas from source data",
    description:
      "Import CSV, XLS or XLSX source files. Derive or coerce unruly data into a defined schema.",
    imageSrc: "/img/schemas.jpg",
    imageAlt: "Bring us your ugly data, your mounds of dead files yearning to breathe free. [photo by Aditya at Unsplash]",
  },
  {
    name: "Define schema-to-schema crosswalks",
    description:
      "Drag 'n drop sequential actions to define structured and readable schema-to-schema transform methods.",
    imageSrc: "/img/transform.jpg",
    imageAlt: "Cry neatness, and unleash the methods of transformation. [photo by Nana Smirnova at Unsplash]",
  },
  {
    name: "Manage data science research teams",
    description:
      "Manage teams with authentication, and assign rights and tasks. Schedule and track a calendar of data updates and transforms.",
    imageSrc: "/img/teams.jpg",
    imageAlt: "Get thee to the sunny table and let us discurse upon the nature of data management. [photo by Dylan Gillis at Unsplash]",
  },
  {
    name: "Execute and fetch data transforms",
    description:
      "Make API calls to bulk create tasks or export transformed data for local automation. Download restructured data as CSV, Excel, Parquet or Feather.",
    imageSrc: "/img/fetch.jpg",
    imageAlt: "Send forth the dogs of data discovery and let them retrieve what they find there. [photo by Anthony Duran at Unsplash]",
  },
  {
    name: "Ensure interoperable standards and validation",
    description:
      "Document BibTeX-compliant metadata for projects, collections and source data. Validate output data against an associated transformation method.",
    imageSrc: "/img/interoperable.jpg",
    imageAlt: "Data swaddled in metadata are like a port in a storm, ensuring safety and onward motion. [photo by Ousa Chea at Unsplash]",
  },
  {
    name: "Integrate Whyqd into your workflows",
    description:
      "Deploy the open source Whyqd stack as a standalone data science hub on your own infrastructure, or integrated as a Python package in your software.",
    imageSrc: "/img/integrate.jpg",
    imageAlt: "Data are tools and the best investment is to ensure their safe custody. [photo by Benjamin Lehman at Unsplash]",
  },
]

// METADATA - START
// https://nuxt.com/docs/getting-started/seo-meta
const title = ref("whyqd.com — more research, less wrangling")
const description = ref("Perform schema-to-schema transforms for interoperability and data reuse. Transform messy data into structured schemas using readable, auditable methods.")
useHead({
  title,
  meta: [{
    name: "description",
    content: description
  }]
})
useServerSeoMeta({
  title,
  ogTitle: title,
  description: description,
  ogDescription: description,
  ogImage: "https://whyqd.com/img/crosswalk.jpg"
})
// METADATA - END
</script>
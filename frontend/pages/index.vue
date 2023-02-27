<template>
  <div>
    <!-- Banner -->
    <AlertsBanner banner-link="https://www.rd-alliance.org/rdas-20th-plenary-draft-programme-0"
      banner-bold="Research Data Alliance's 20th Plenary" banner-text="Join us in Gothenburg from 20 to 24 March&nbsp" />
    <!-- Hero -->
    <main class="relative isolate overflow-hidden">
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
      <div class="relative py-12 sm:py-16">
        <div class="mx-auto max-w-7xl px-6 lg:px-8">
          <div class="mx-auto max-w-2xl text-center">
            <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">More research,<br>less wrangling</h1>
            <p class="mt-6 text-lg leading-8 text-gray-600">Transform messy data into structured schemas using readable,
              auditable methods. Perform schema-to-schema transforms for interoperability and data reuse.</p>
            <div class="mt-6 flex items-center justify-center gap-x-6">
              <NuxtLink v-if="!auth.loggedIn" to="/login"
                class="rounded-md bg-ochre-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-ochre-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ochre-600">
                Get notified</NuxtLink>
              <NuxtLink to="/about" class="text-sm font-semibold leading-6 text-gray-900">Learn more <span
                  aria-hidden="true">→</span></NuxtLink>
            </div>
          </div>
          <div class="relative overflow-hidden pt-12 lg:pt-14">
            <div class="mx-auto max-w-7xl px-6 lg:px-8">
              <img class="mb-[-12%] rounded-xl ring-4 ring-ochre-700/10" src="/img/ugly-data.png"
                alt="Ugly data and the transformation method giving it a makeover." />
              <div class="relative" aria-hidden="true">
                <div class="absolute -inset-x-20 bottom-0 bg-gradient-to-t from-white pt-[7%]" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
    <!-- Alternating Features -->
    <div class="mx-auto max-w-2xl px-4 sm:px-6 lg:max-w-5xl lg:px-8">
      <div class="mx-auto max-w-3xl text-center">
        <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Transform data management</h2>
        <p class="mt-4 text-gray-500">Your data are the foundation for research and decision-support. Ensure
          interoperability, transparency and probity by using readable, auditable transformation methods.</p>
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
    <!-- Launch Notification -->
    <AuthenticationMagicLoginCard card-text="We can let you know when we launch." />
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores"
import { tokenIsTOTP } from "@/utilities"

const auth = useAuthStore()
definePageMeta({
  layout: "home",
});

const redirectTOTP = "/totp"
const redirectAfterLogin = "/"

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
    name: "Define schema-to-schema transforms",
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
      "Make API calls to execute transforms, or save methods for local automation. Download restructured data as CSV, Excel, Parquet or Feather.",
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

onMounted(async () => {
  // Check if email is being validated
  const route = useRoute()
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
</script>
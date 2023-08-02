<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-7xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done'">
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
        <div class="mx-auto max-w-4xl text-center">
          <h2 class="text-base font-semibold leading-7 text-ochre-600">Pricing</h2>
          <p class="mt-2 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">Pricing plans for research
            at&nbsp;every&nbsp;scale</p>
        </div>
        <p class="mx-auto mt-6 max-w-2xl text-center text-lg leading-8 text-gray-600">Choose an affordable plan with the
          best features for serving your research team, study needs, and scaled to the extent of your source data.</p>
        <div class="mt-16 flex justify-center">
          <RadioGroup v-model="frequency"
            class="grid grid-cols-2 gap-x-1 rounded-full p-1 text-center text-xs font-semibold leading-5 ring-1 ring-inset ring-gray-200">
            <RadioGroupLabel class="sr-only">Payment frequency</RadioGroupLabel>
            <RadioGroupOption as="template" v-for="option in frequencies" :key="option.value" :value="option"
              v-slot="{ checked }">
              <div
                :class="[checked ? 'bg-ochre-600 text-white' : 'text-gray-500', 'cursor-pointer rounded-full px-2.5 py-1']">
                <span>{{ option.label }}</span>
              </div>
            </RadioGroupOption>
          </RadioGroup>
        </div>
        <div
          class="isolate mx-auto mt-10 grid max-w-md grid-cols-1 gap-8 md:max-w-2xl md:grid-cols-2 lg:max-w-4xl xl:mx-0 xl:max-w-none xl:grid-cols-4">
          <div v-for="tier in  tiers " :key="tier.id"
            :class="[tier.mostPopular ? 'ring-2 ring-ochre-600' : 'ring-1 ring-gray-200', 'rounded-3xl p-8']">
            <h3 :id="tier.id"
              :class="[tier.mostPopular ? 'text-ochre-600' : 'text-gray-900', 'text-lg font-semibold leading-8']">{{
                tier.name }}</h3>
            <p class="mt-4 text-sm leading-6 text-gray-600">{{ tier.description }}</p>
            <p v-if="['EXPLORER', 'RESEARCHER'].includes(tier.subscription)" class="mt-6 flex items-baseline gap-x-1">
              <span class="text-4xl font-bold tracking-tight text-gray-900">
                {{ getPrintablePrice(tier.subscription) }}
              </span>
              <span class="text-sm font-semibold leading-6 text-gray-600">{{ frequency.priceSuffix }}</span>
            </p>
            <p v-if="'REVIEWER' === tier.subscription" class="mt-6 flex items-baseline gap-x-1">
              <span class="text-4xl font-bold tracking-tight text-gray-900">
                Free
              </span>
              <span class="text-sm font-semibold leading-6 text-gray-600">always</span>
            </p>
            <p v-if="'INVESTIGATOR' === tier.subscription" class="mt-6 flex items-baseline gap-x-1">
              <span class="text-4xl font-bold tracking-tight text-gray-900">
                Hosted
              </span>
              <span class="text-sm font-semibold leading-6 text-gray-600">& scaled</span>
            </p>
            <form v-if="['EXPLORER', 'RESEARCHER'].includes(tier.subscription)">
              <!-- @vue-ignore -->
              <button id="checkout-and-portal-button" type="button" :aria-describedby="tier.id"
                :class="[tier.mostPopular ? 'bg-ochre-600 text-white shadow-sm hover:bg-ochre-500' : 'text-ochre-600 ring-1 ring-inset ring-ochre-200 hover:ring-ochre-300', 'mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ochre-600 w-full']"
                :disabled="isSubscribed(tier.subscription)" @click.prevent="subscribeWithCard(tier.subscription)">
                Subscribe
              </button>
            </form>
            <NuxtLink v-if="'REVIEWER' === tier.subscription" to="/login"
              :class="[auth.loggedIn ? 'pointer-events-none' : '', 'text-ochre-600 ring-1 ring-inset ring-ochre-200 hover:ring-ochre-300 mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ochre-600 w-full']"
              :disabled="auth.loggedIn">
              Join us
            </NuxtLink>
            <NuxtLink v-if="'INVESTIGATOR' === tier.subscription" to="/contact"
              :class="[tier.mostPopular ? 'bg-ochre-600 text-white shadow-sm hover:bg-ochre-500' : 'text-ochre-600 ring-1 ring-inset ring-ochre-200 hover:ring-ochre-300', 'mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ochre-600 w-full']">
              Contact us
            </NuxtLink>
            <ul role="list" class="mt-8 space-y-3 text-sm leading-6 text-gray-600">
              <li v-for=" feature  in  tier.features " :key="feature" class="flex gap-x-3">
                <CheckIcon class="h-6 w-5 flex-none text-ochre-600" aria-hidden="true" />
                {{ replaceWithTerms(feature, tier.subscription) }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from "@headlessui/vue"
import { CheckIcon } from "@heroicons/vue/20/solid"
import {
  IStripeCheckoutIntent,
  IProductPricing,
  ICode,
  IProductTypes,
  IKeyable,
} from "@/interfaces"
import { storeToRefs } from "pinia"
import { useSettingStore, useAuthStore, useSubscriptionsStore } from "@/stores"
import { apiSubscriptions } from "@/api"
import { readableNumber, tokenIsTOTP } from "@/utilities"

definePageMeta({
  layout: "home",
})

const route = useRoute()
const auth = useAuthStore()
const subscriptionStore = useSubscriptionsStore()
const { stripeRedirect } = storeToRefs(subscriptionStore)
const appSettings = useSettingStore()
const pricing = ref<IProductPricing[]>([] as IProductPricing[])
const ip = ref("")
const currencyIcon: IKeyable = {
  USD: "$",
  GBP: "£",
  EUR: "€",
}
const frequencies = [
  { value: "monthly", label: "Monthly", priceSuffix: "/month" },
  { value: "annually", label: "Annually", priceSuffix: "/year" },
]
const frequency = ref(frequencies[0])


watch(() => stripeRedirect.value, () => {
  const redirect = subscriptionStore.stripeRedirect
  subscriptionStore.setStripeRedirect("")
  if (redirect !== "") window.location.href = redirect
})

onMounted(async () => {
  appSettings.setPageName("Pricing")
  appSettings.setPageState("loading")
  // Check if email is being validated
  if (route.query && route.query.magic) {
    // No idea: https://stackoverflow.com/q/74759799/295606
    await new Promise((resolve) => {
      setTimeout(() => {
        resolve(true)
      }, 100)
    })
    if (!auth.loggedIn) await auth.magicLogin(route.query.magic as string)
    if (tokenIsTOTP(auth.authTokens.token)) {
      const redirectTOTP = `/totp?subscription=${route.query.subscription}`
      await navigateTo(redirectTOTP)
    }
  }
  if (process.client) {
    ip.value = await getIP()
    const payload: ICode = { ip: ip.value }
    try {
      const { data: response } = await apiSubscriptions.getSubscriptionProducts(payload)
      if (response.value && response.value.length) {
        pricing.value = response.value
      }
    } catch (error) {
      appSettings.setPageState("error")
    }
    if (!pricing.value || !pricing.value.length)
      throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
    if (route.query && route.query.subscription)
      await subscribeWithCard(route.query.subscription as string)
    appSettings.setPageState("done")
  }
})

function getPrice(subscription: IProductTypes) {
  const product = pricing.value.find(
    (s) => s.subscription === subscription
  )
  if (product) {
    if (frequency.value.value === "annually") return product.per_annum
    if (frequency.value.value === "monthly") return product.per_month
  }
  return null
}

function getPrintablePrice(subscription: IProductTypes) {
  const price = getPrice(subscription)
  if (price) {
    if (frequency.value.value === "annually")
      return `${currencyIcon[price.currency]}${readableNumber(price.per_annum / 100)}`
    if (frequency.value.value === "monthly")
      return `${currencyIcon[price.currency]}${readableNumber(price.per_month / 100)}`
  }
  return null
}

function replaceWithTerms(text: string, subscription: IProductTypes) {
  if (text.includes("${rows}") || text.includes("{transforms}")) {
    const product = pricing.value.find((price) => price.subscription === subscription)
    if (product && text.includes("${rows}")) return text.replace("${rows}", readableNumber(product.rows))
    if (product && text.includes("${transforms}")) return text.replace("${transforms}", readableNumber(product.transforms))
  }
  return text
}

function isSubscribed(text: string): boolean {
  if (text === "EXPLORER" && auth.hasExplorerSubscription) return true
  if (text === "RESEARCHER" && auth.hasResearcherSubscription) return true
  return false
}

async function subscribeWithCard(lookup: string) {
  if (auth.loggedIn) {
    const price = getPrice(lookup as IProductTypes)
    if (price) {
      const stripeCheckout: IStripeCheckoutIntent = {
        price_id: price.id,
        subscriber_id: auth.profile.id,
        ip: ip.value,
      }
      await subscriptionStore.createStripeCheckout(stripeCheckout)
    }
  } else {
    const joinRoute = `/login?subscription=${lookup}`
    return await navigateTo(joinRoute)
  }
}

async function getIP() {
  // https://www.ipify.org/ for passing in payment details,
  // otherwise not stored.
  try {
    const res = await fetch("https://api.ipify.org?format=json")
    return await res.json().then((data) => data.ip)
  } catch {
    return null
  }
}

const tiers: IKeyable[] = [
  {
    name: "Reviewer",
    subscription: "REVIEWER",
    id: "tier-reviewer",
    price: false,
    description: "The essentials to support your research planning.",
    features: [
      "Define & manage data schema.",
      "Develop schema-to-schema crosswalks to restructure data with a powerful drag 'n drop toolkit.",
      "Create, join & manage teams & projects.",
      "Review complete audit trails from source to transformed output.",
    ],
    mostPopular: false,
  },
  {
    name: "Explorer",
    subscription: "EXPLORER",
    id: "tier-explorer",
    price: true,
    description: "The core infrastructure for your work with manageable data sources.",
    features: [
      "Define & manage data schema.",
      "Develop schema-to-schema crosswalks to restructure data with a powerful drag 'n drop toolkit.",
      "Import up to ${rows} rows per tabular data source.",
      "Create & schedule up to ${transforms} import & restructuring tasks per month.",
      "Create, join & manage teams & projects.",
      "Review complete audit trails from source to transformed output.",
    ],
    mostPopular: false,
  },
  {
    name: "Researcher",
    subscription: "RESEARCHER",
    id: "tier-researcher",
    price: true,
    description: "Infrastructure scaled for your inconveniently-sized data.",
    features: [
      "Define & manage data schema.",
      "Develop schema-to-schema crosswalks to restructure data with a powerful drag 'n drop toolkit.",
      "Import up to ${rows} rows per tabular data source.",
      "Create & schedule up to ${transforms} import & restructuring tasks per month.",
      "Create, join & manage teams & projects.",
      "Review complete audit trails from source to transformed output.",
      "Integrate API endpoints for exporting restructured data into your apps.",
    ],
    mostPopular: true,
  },
  {
    name: "Investigator",
    subscription: "INVESTIGATOR",
    id: "tier-investigator",
    price: false,
    description: "Dedicated support & infrastructure for your organisation.",
    features: [
      "Define & manage data schema.",
      "Develop schema-to-schema crosswalks to restructure data with a powerful drag 'n drop toolkit.",
      "Import any number of rows per tabular data source.",
      "Create & schedule unlimited import & restructuring tasks per month.",
      "Create, join & manage teams & projects.",
      "Review complete audit trails from source to transformed output.",
      "Integrate API endpoints for exporting restructured data into your apps.",
    ],
    mostPopular: false,
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
  ogImage: "https://whyqd.com/img/ugly-data.png"
})
// METADATA - END
</script>
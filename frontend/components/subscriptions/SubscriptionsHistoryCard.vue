<template>
  <div class="flex-auto p-3">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done'">
      <div class="shadow rounded-md">
        <div class="space-y-6 bg-white py-6 px-6">
          <div>
            <h3 class="text-lg font-medium leading-6 text-gray-900">{{ title }}</h3>
            <p class="mt-1 text-sm text-gray-500">{{ description }}</p>
          </div>
          <div>
            <div class="flex w-full items-center justify-between">
              <div class="text-xs font-medium text-gray-700">
                <div class="inline-flex text-xs">
                  <svg class="text-eucalyptus-600 h-4 w-4 mr-2" viewBox="0 0 16 16" fill="currentColor"
                    xmlns="http://www.w3.org/2000/svg">
                    <circle cx="8" cy="8" r="6" />
                  </svg>
                  {{ authStore.subscriptionState.membership }}
                </div>
                <div v-if="authStore.subscriptionState.ends" class="truncate py-0.5 text-xs text-gray-500">
                  <time :datetime="(authStore.subscriptionState.ends.toString())"
                    class="flex-none py-0.5 text-xs text-gray-500">
                    Until: {{ readableDate(authStore.subscriptionState.ends) }}</time>
                </div>
              </div>
              <div>
                <button v-if="['EXPLORER', 'RESEARCHER'].includes(authStore.subscriptionState.membership)" type="button"
                  @click.prevent="manageStripeAccount"
                  class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                  <CreditCardIcon class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                  <span class="hidden md:block">Manage your subscription at Stripe</span>
                </button>
                <NuxtLink v-else to="/pricing"
                  class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                  <CreditCardIcon class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                  <span class="hidden md:block">Subscribe</span>
                </NuxtLink>
              </div>
            </div>
          </div>
          <div v-if="subscriptionStore.orderHistory.length" class="space-y-1">
            <div class="shadow sm:overflow-hidden sm:rounded-md min-w-max">
              <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50">
                  <tr>
                    <th v-for="(th, i) in defaultHeaders" :key="`header-${i}`"
                      class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                      {{ printableHeaders[th] }}
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200 bg-white">
                  <tr v-for="(tr, j) in subscriptionStore.orderHistory" :key="`row-${j}`">
                    <td v-for="(td, k) in defaultHeaders" :key="`row-${j}-column-${k}`"
                      class="w-full max-w-0 py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:w-auto sm:max-w-none sm:pl-6">
                      <span v-if="['created'].includes(td)">{{ readableDate(tr[td as keyof IOrder] as string)
                      }}</span>
                      <span v-if="[
                          'subscription_event_type',
                          'country_name',
                          'subscription_type',
                          'currency',
                        ].includes(td)
                        ">{{ tr[td as keyof IOrder] }}</span>
                      <span v-if="['amount'].includes(td)">
                        {{ getPrintablePrice(tr['currency'], tr[td as keyof IOrder] as string) }}
                      </span>
                      <a v-if="['invoice_url'].includes(td)" :href="(tr[td as keyof IOrder] as string)" target="_blank"
                        rel="noopener noreferrer">
                        <LinkIcon class="h-6 w-5 flex-none text-ochre-600" aria-hidden="true" />
                      </a>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <CommonPagination />
    </div>
  </div>
</template>

<script setup lang="ts">
import { CreditCardIcon, LinkIcon } from "@heroicons/vue/20/solid"
import { storeToRefs } from "pinia"
import { useAuthStore, useSubscriptionsStore, useSettingStore } from "@/stores"
import { readableNumber, readableDate } from "@/utilities"
import type { IKeyable, IOrder } from "@/interfaces"

const route = useRoute()
const authStore = useAuthStore()
const appSettings = useSettingStore()
const subscriptionStore = useSubscriptionsStore()
const { stripeRedirect } = storeToRefs(subscriptionStore)
const title = "Account history"
const description = ref("Collaborative data wrangling at speed. Collaborate with unlimited teams, projects and team members.")
const defaultHeaders: string[] = [
  "created",
  "subscription_event_type",
  "country_name",
  "subscription_type",
  "currency",
  "amount",
  "invoice_url",
]
const printableHeaders: IKeyable = {
  created: "Created",
  subscription_event_type: "Status",
  country_name: "Country",
  subscription_type: "Subscription",
  currency: "Currency",
  amount: "Amount",
  invoice_url: "Invoice",
}
const currencyIcon: IKeyable = {
  USD: "$",
  GBP: "£",
  EUR: "€",
}

watch(() => [route.query], async () => {
  await updateOrders()
})

watch(() => stripeRedirect.value, () => {
  const redirect = subscriptionStore.stripeRedirect
  subscriptionStore.setStripeRedirect("")
  if (redirect !== "") window.location.href = redirect
})

async function updateOrders() {
  if (route.query && route.query.page) subscriptionStore.setPage(route.query.page as string)
  await subscriptionStore.getOrders()
}

onMounted(async () => {
  // refresh user info
  await authStore.getUserProfile(true)
  await updateOrders()
  if (authStore.hasExplorerSubscription)
    description.value = "Import and restructure up to 50,000 rows per data source with a powerful drag 'n drop toolkit."
  if (authStore.hasResearcherSubscription)
    description.value = "Import and restructure up to 500,000 rows per data source with a powerful drag 'n drop toolkit."
})

function getPrintablePrice(currency: string, price: string) {
  return `${currencyIcon[currency]}${readableNumber(+price / 100)}`
}

async function manageStripeAccount() {
  await subscriptionStore.redirectToStripeAccount()
}

onBeforeUnmount(() => {
  const router = useRouter()
  router.replace({ query: {} })
})
</script>
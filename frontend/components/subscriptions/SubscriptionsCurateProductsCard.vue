<template>
  <div class="flex-auto p-3">
    <div class="shadow sm:overflow-hidden sm:rounded-md">
      <div v-if="appSettings.current.pageState === 'loading'">
        <LoadingCardSkeleton />
      </div>
      <form v-if="appSettings.current.pageState === 'done'" class="space-y-2">
        <div class="flex w-full items-center justify-between gap-x-6 p-2">
          <div class="flex items-center justify-left w-full">
            <h1 class="text-lg leading-7 text-gray-900">
              Products
            </h1>
          </div>
          <div class="flex flex-inline items-center space-x-2">
            <!-- Separator -->
            <div class="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-900/10" aria-hidden="true" />
            <button type="button" @click.prevent="reset"
              class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
              <ArrowPathIcon class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
              <span class="hidden md:block">Reset</span>
            </button>
            <button type="submit" @click.prevent="submit"
              class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
              <ArrowUpTrayIcon class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
              <span class="hidden md:block">Save</span>
            </button>
          </div>
        </div>
        <div class="flex items-center justify-left w-full px-2">
          <p class="text-sm leading-5 text-gray-900">
            Map fields from Stripe to the fields here. Pay attention to Monthly and Annual fields. Yes, I should have done
            this differently.
          </p>
        </div>
        <Disclosure v-for="(product, i) in products" :key="`product-${i}`" v-slot="{ open }">
          <DisclosureButton
            class="flex w-full justify-between rounded-lg bg-ochre-100 px-4 py-2 text-left text-sm font-medium text-ochre-900 hover:bg-ochre-200 focus:outline-none focus-visible:ring focus-visible:ring-ochre-500 focus-visible:ring-opacity-75">
            <span>{{ product.name }}</span>
            <ChevronUpIcon :class="open ? 'rotate-180 transform' : ''" class="h-5 w-5 text-ochre-500" />
          </DisclosureButton>
          <DisclosurePanel class="px-4 pb-2 text-sm text-gray-500">
            <div class="space-y-2">
              <div class="relative">
                <label for="product-description" class="label">
                  <span class="block text-xs text-gray-500 leading-5">Description</span>
                </label>
                <textarea v-model="product.description" type="text" name="product-description" id="product-description"
                  placeholder="Product description"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
              </div>
              <div class="relative">
                <label for="product-id" class="label">
                  <span class="block text-xs text-gray-500 leading-5">Product ID</span>
                </label>
                <input v-model="product.id" type="text" name="product-id" id="product-id" placeholder="Stripe product ID"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6"
                  required />
              </div>
              <div class="grid grid-cols-2 gap-x-6">
                <div class="relative">
                  <label for="row-limit" class="label">
                    <span class="block text-xs text-gray-500 leading-5 -mb-2">Row limit</span>
                  </label>
                  <div class="mt-2">
                    <input v-model="product.rows" type="text" name="row-limit" id="row-limit" placeholder="50000"
                      class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6"
                      required />
                  </div>
                </div>
                <div class="relative">
                  <label for="transform-limit" class="label">
                    <span class="block text-xs text-gray-500 leading-5 -mb-2">Transform limit</span>
                  </label>
                  <div class="mt-2">
                    <input v-model="product.transforms" type="text" name="transform-limit" id="transform-limit"
                      placeholder="1000"
                      class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6"
                      required />
                  </div>
                </div>
              </div>
              <div v-for="(prc, j) in product.prices" :key="`product-${i}-price-${j}`">
                <div class="grid grid-flow-col auto-cols-auto gap-2">
                  <div class="flex flex-shrink text-sm justify-center items-center">
                    {{ prc.currency }}
                  </div>
                  <div class="col-span-6">
                    <label class="label">
                      <span class="block text-xs text-gray-500 leading-5">Price ID</span>
                    </label>
                    <input v-model="prc.id" type="text" placeholder="Stripe price ID"
                      class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6"
                      required />
                  </div>
                  <div class="w-32">
                    <label class="label">
                      <span class="block text-xs text-gray-500 leading-5">Monthly in cents</span>
                    </label>
                    <input v-model="prc.per_month" type="text" placeholder="Price"
                      class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-ochre-600"
                      required />
                  </div>
                  <div class="w-32">
                    <label class="label">
                      <span class="block text-xs text-gray-500 leading-5">Annual in cents</span>
                    </label>
                    <input v-model="prc.per_annum" type="text" placeholder="Price"
                      class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-ochre-600"
                      required />
                  </div>
                </div>
              </div>
            </div>
          </DisclosurePanel>
        </Disclosure>
      </form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import { ArrowPathIcon, ArrowUpTrayIcon } from "@heroicons/vue/24/outline"
import { ChevronUpIcon } from "@heroicons/vue/20/solid"
import { useSubscriptionsStore, useSettingStore } from "@/stores"
import type { IProduct } from "@/interfaces"

const appSettings = useSettingStore()
const subscriptionStore = useSubscriptionsStore()
const products = ref<IProduct[]>([] as IProduct[])

async function submit() {
  await subscriptionStore.updateAllSubscriptionProducts(products.value)
}

function reset() {
  // https://stackoverflow.com/a/23481096/295606
  // subscriptionStore.subscriptionProducts.map(p => { return { ...p } })
  products.value = JSON.parse(JSON.stringify(subscriptionStore.subscriptionProducts))
}

onMounted(async () => {
  await subscriptionStore.getAllSubscriptionProducts()
  reset()
})

</script>

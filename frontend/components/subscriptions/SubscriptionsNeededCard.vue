<template>
  <div class="flex-auto">
    <div class="shadow rounded-md">
      <div class="p-3 rounded-md">
        <div>
          <div class="flex w-full items-center justify-between">
            <div class="text-sm font-medium text-gray-700">
              <div class="inline-flex text-sm items-center">
                <svg class="text-ochre-600 h-4 w-4 mr-2" viewBox="0 0 16 16" fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg">
                  <circle cx="8" cy="8" r="6" />
                </svg>
                You will need
                <span v-if="props.needed === 'EXPLORER'">&nbsp;at least an&nbsp;</span>
                <span v-else>&nbsp;a&nbsp;</span>
                {{ $props.needed }} subscription to use this feature.
              </div>
            </div>
            <div>
              <NuxtLink to="/pricing"
                class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-white  bg-ochre-600 hover:bg-ochre-700">
                <CreditCardIcon class="sm:-ml-0.5 h-4 w-4 text-white" aria-hidden="true" />
                <span class="hidden sm:block">Subscribe</span>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CreditCardIcon } from "@heroicons/vue/20/solid"
import type { IProductTypes } from "@/interfaces"

const props = defineProps<{
  needed: IProductTypes
}>()
</script>
<template>
  <div v-if="show" class="flex items-center gap-x-6 bg-gray-900 py-2.5 px-6 sm:px-3.5 sm:before:flex-1">
    <p class="text-sm leading-6 text-white">
      <NuxtLink :to="props.bannerLink"><strong class="font-semibold">{{ props.bannerBold }}</strong><svg viewBox="0 0 2 2"
          class="mx-2 inline h-0.5 w-0.5 fill-current" aria-hidden="true">
          <circle cx="1" cy="1" r="1" />
        </svg>{{ props.bannerText }}<span aria-hidden="true">&rarr;</span></NuxtLink>
    </p>
    <div class="flex flex-1 justify-end">
      <button type="button" @click="show = false" class="-m-3 p-3 focus-visible:outline-offset-[-4px]">
        <span class="sr-only">Dismiss</span>
        <XMarkIcon class="h-5 w-5 text-white" aria-hidden="true" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { XMarkIcon } from "@heroicons/vue/20/solid"

const show = ref(true)

const props = defineProps({
  bannerBold: String,
  bannerText: String,
  bannerLink: String
})
</script>
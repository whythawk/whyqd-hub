<template>
  <nav class="flex items-center justify-between mb-14 px-4 sm:px-0">
    <div class="-mt-px flex w-0 flex-1">
      <NuxtLink :to="{ path, query: { page: pagePrevious } }" :event="pagePrevious === '0' ? '' : 'click'"
        class="inline-flex items-center border-t-2 border-transparent pr-1 pt-4 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700">
        <ArrowLongLeftIcon class="mr-3 h-5 w-5 text-gray-400" aria-hidden="true" />
        Previous
      </NuxtLink>
    </div>
    <div class="-mt-px flex w-0 flex-1 justify-end">
      <NuxtLink :to="{ path, query: { page: pageNext } }"
        class="inline-flex items-center border-t-2 border-transparent pl-1 pt-4 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700">
        Next
        <ArrowLongRightIcon class="ml-3 h-5 w-5 text-gray-400" aria-hidden="true" />
      </NuxtLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ArrowLongLeftIcon, ArrowLongRightIcon } from '@heroicons/vue/20/solid'

const route = useRoute()
const pageNext = ref("")
const pagePrevious = ref("")
const path = ref("")

onMounted(async () => {
  path.value = route.path as string
  let page = 0
  if (route.query && route.query.page) {
    if (!isNaN(+route.query.page)) {
      page = +route.query.page
    }
  }
  pageNext.value = "" + (page + 1)
  pagePrevious.value = page > 0 ? "" + (page - 1) : "0"
})
</script>
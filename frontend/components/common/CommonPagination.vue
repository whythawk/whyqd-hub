<template>
  <nav class="flex items-center justify-between mb-14 px-4 sm:px-0">
    <div class="-mt-px flex w-0 flex-1">
      <NuxtLink :to="{ path, query: { page: pagePrevious } }" :event="showPrevious ? 'click' : ''"
        :class="[showPrevious ? '' : 'pointer-events-none', 'group inline-flex items-center pr-1 pt-4 text-sm font-medium text-gray-500 hover:text-ochre-500']">
        <ArrowLongLeftIcon class="mr-3 h-5 w-5" aria-hidden="true" />
        Previous
      </NuxtLink>
    </div>
    <div class="-mt-px flex w-0 flex-1 justify-end">
      <NuxtLink :to="{ path, query: { page: pageNext } }" :event="settingsStore.current.pageNext ? 'click' : ''"
        :class="[settingsStore.current.pageNext ? '' : 'pointer-events-none', 'group inline-flex items-center pr-1 pt-4 text-sm font-medium text-gray-500 hover:text-ochre-500']">
        Next
        <ArrowLongRightIcon class="ml-3 h-5 w-5" aria-hidden="true" />
      </NuxtLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ArrowLongLeftIcon, ArrowLongRightIcon } from '@heroicons/vue/20/solid'
import { useSettingStore } from "@/stores"

const route = useRoute()
const router = useRouter()
const settingsStore = useSettingStore()
const pageNext = ref("")
const pagePrevious = ref("")
const showPrevious = ref(false)
const path = ref("")

watch(() => [route.query], async () => {
    await updatePagination()
})

async function updatePagination() {
    path.value = route.path as string
    let page = 0
    if (route.query && route.query.page) {
        if (!isNaN(+route.query.page)) {
            page = +route.query.page
        }
        if (!settingsStore.current.pageNext) {
            // Went to the next page and got no data - must reset to the previous page
            router.push({ path: route.path, query: { ...route.query, page: "" + (page - 1) } })
        }
    }
    if (page > 0) showPrevious.value = true
    pageNext.value = "" + (page + 1)
    pagePrevious.value = page > 0 ? "" + (page - 1) : "0"
}

onMounted(async () => {
  await updatePagination()
})
</script>
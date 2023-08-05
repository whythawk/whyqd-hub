<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done' && referenceStore.term">
      <div class="mt-6 border-b border-t border-gray-200 py-3 md:px-8">
        <ReferenceCard :reference="referenceStore.term" :last-card="true" />
      </div>
      <ReferenceFilterPanel />
      <div v-if="referenceStore.multi.length === 0" class="space-y-2">
        <CommonEmptyCard
          term="Nothing right now. Create schemas, import data or start tasks to see those references here." />
      </div>
      <ul role="list" class="space-y-2">
        <li v-for="(reference, i) in referenceStore.multi" :key="`reference-${i}`">
          <ReferenceCard :reference="reference" :last-card="i === referenceStore.multi.length - 1" />
        </li>
      </ul>
      <CommonPagination />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useReferenceStore } from "@/stores"
import { IReferenceFilters } from "@/interfaces"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const referenceStore = useReferenceStore()

watch(() => [route.query], async () => {
  await updateMulti()
})

async function updateMulti() {
  if (route.query && route.query.page) referenceStore.setPage(route.query.page as string)
  await referenceStore.getMulti()
}

onMounted(async () => {
  appSettings.setPageName("References")
  await referenceStore.getTerm(route.params.id as string)
  if (!referenceStore.term || Object.keys(referenceStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  let filters: IReferenceFilters = { ...referenceStore.filters }
  filters.reference_type = "SCHEMA"
  referenceStore.resetFilters()
  referenceStore.setFilters(filters)
  updateMulti()
})


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
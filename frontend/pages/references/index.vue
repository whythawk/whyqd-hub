<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <CommonLaunchCard />
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <ReferenceFilterPanel />
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

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const referenceStore = useReferenceStore()

watch(() => [route.query], () => {
  updateMulti()
})

async function updateMulti() {
  if (route.query && route.query.page) referenceStore.setPage(route.query.page as string)
  await referenceStore.getMulti()
}

onMounted(async () => {
  appSettings.setPageName("References")
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
  ogImage: "https://whyqd.com/img/ugly-data.png"
})
// METADATA - END
</script>
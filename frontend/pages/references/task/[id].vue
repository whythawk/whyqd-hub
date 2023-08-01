<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <div class="mt-6 border-b border-t border-gray-200 py-3 md:px-8">
        <TaskCard :task="taskStore.term" :last-card="true" />
      </div>
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
import { useSettingStore, useReferenceStore, useTaskStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const referenceStore = useReferenceStore()
const taskStore = useTaskStore()

watch(() => [route.query], async () => {
  await updateMulti()
})

async function updateMulti() {
  if (route.query && route.query.page) referenceStore.setPage(route.query.page as string)
  await referenceStore.getMulti()
}

onMounted(async () => {
  await taskStore.getTerm(route.params.id as string)
  appSettings.setPageName("References")
  updateMulti()
})

onBeforeUnmount(() => {
  const router = useRouter()
  router.replace({ query: {} })
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
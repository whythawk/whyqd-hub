<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done' && taskStore.term">
      <div class="mt-6 border-b border-t border-gray-200 py-3 md:px-8">
        <TaskCard :task="taskStore.term" :last-card="true" />
      </div>
      <ResourceFilterPanel />
      <div v-if="resourceStore.multi.length === 0" class="space-y-2">
        <CommonEmptyCard
          term="Nothing right now. Create schemas, import data or start tasks to see those resources here." />
      </div>
      <ul role="list" class="space-y-6">
        <li v-for="(resource, i) in resourceStore.multi" :key="`resource-${i}`">
          <ResourceCard :resource="resource" :last-card="i === resourceStore.multi.length - 1" />
        </li>
      </ul>
      <CommonPagination />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useResourceStore, useTaskStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const taskStore = useTaskStore()
const resourceStore = useResourceStore()

watch(() => [route.query], async () => {
  await updateMulti()
})

async function updateMulti() {
  if (route.query && route.query.page) resourceStore.setPage(route.query.page as string)
  await resourceStore.getMultiByTask(taskStore.term.id as string)
}

onMounted(async () => {
  appSettings.setPageName("Resources")
  await taskStore.getTerm(route.params.id as string)
  if (!taskStore.term || Object.keys(taskStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
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
  ogImage: "https://whyqd.com/img/crosswalk.jpg"
})
// METADATA - END
</script>
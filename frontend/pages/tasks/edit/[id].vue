<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done'">
      <TaskEditCard />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useTaskStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const appSettings = useSettingStore()
const route = useRoute()
const taskStore = useTaskStore()

onMounted(async () => {
  appSettings.setPageName("Tasks")
  if (route.params.id !== "create") {
    await taskStore.getTerm(route.params.id as string)
    if (!taskStore.term || Object.keys(taskStore.term).length === 0)
      throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  }
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
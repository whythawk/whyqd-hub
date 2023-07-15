<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <div class="mt-6 border-b border-t border-gray-200 py-3 md:px-8">
        <ProjectCard :project="projectStore.term" :last-card="true" />
      </div>
      <TaskFilterPanel />
      <ul role="list" class="space-y-2">
        <li v-for="(task, i) in taskStore.multi" :key="`task-${i}`">
          <TaskCard :task="task" :last-card="i === taskStore.multi.length - 1" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useTaskStore, useProjectStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const taskStore = useTaskStore()
const projectStore = useProjectStore()

onMounted(async () => {
  await projectStore.getTerm(route.params.id as string)
  appSettings.setPageName("Tasks")
  if (projectStore.term.id)
    await taskStore.getMultiByProject(projectStore.term.id)
  else
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
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
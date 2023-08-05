<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done'">
      <TaskFilterPanel />
      <div v-if="taskStore.scheduled.length === 0" class="space-y-2">
        <CommonEmptyCard
          term="Nothing right now. Create tasks & assign update frequencies & priorities to see them here." />
      </div>
      <ul role="list" class="space-y-2">
        <li v-for="(task, i) in taskStore.scheduled" :key="`task-${i}`">
          <TaskScheduleCard :task="task" :last-card="i === taskStore.scheduled.length - 1" />
        </li>
      </ul>
      <CommonPagination />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useTaskStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const taskStore = useTaskStore()

watch(() => [route.query], async () => {
  await updateScheduledMulti()
})

async function updateScheduledMulti() {
  if (route.query && route.query.page) taskStore.setPage(route.query.page as string)
  await taskStore.getScheduledMulti()
}

onMounted(async () => {
  appSettings.setPageName("Schedule")
  updateScheduledMulti()
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
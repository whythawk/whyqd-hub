<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done' && taskStore.term">
      <div class="mt-6 border-b border-t border-gray-200 py-3 md:px-8">
        <TaskScheduleCard :task="taskStore.term" :last-card="true" />
      </div>
      <ActivityFilterPanel />
      <div v-if="activityStore.multi.length === 0" class="space-y-2">
        <CommonEmptyCard
          term="Nothing right now, but when you start working, or join a team, you'll see your activities here." />
      </div>
      <ul role="list" class="space-y-2">
        <li v-for="(activity, i) in activityStore.multi" :key="`activity-${i}`">
          <ResourceActivityCard :resource="activity" :last-card="i === activityStore.multi.length - 1" />
        </li>
      </ul>
      <CommonPagination />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useActivityStore, useTaskStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const activityStore = useActivityStore()
const taskStore = useTaskStore()

watch(() => [route.query], async () => {
  await updateMulti()
})

async function updateMulti() {
  if (route.query && route.query.page) activityStore.setPage(route.query.page as string)
  if (taskStore.term.id)
    await activityStore.getMultiByTask(taskStore.term.id)
  else
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
}

onMounted(async () => {
  await taskStore.getTerm(route.params.id as string)
  appSettings.setPageName("Activity")
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
<template>
  <!-- Hero -->
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done'">
      <ActivityFilterPanel />
      <div v-if="activityStore.multi.length === 0" class="space-y-2">
        <CommonEmptyCard
          term="Nothing right now, but when you start working, or join a team, you'll see your activities here." />
      </div>
      <ul role="list" class="space-y-2">
        <li v-for="(activity, i) in activityStore.multi" :key="`activity-${i}`">
          <ActivityCard :activity="activity" :last-card="i === activityStore.multi.length - 1" />
        </li>
      </ul>
      <CommonPagination />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useActivityStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const activityStore = useActivityStore()

watch(() => [route.query], async () => {
  await updateMulti()
})

async function updateMulti() {
  if (route.query && route.query.page) activityStore.setPage(route.query.page as string)
  await activityStore.getMulti()
}

onMounted(async () => {
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
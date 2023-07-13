<template>
  <!-- Hero -->
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <ActivityFilterPanel />
      <ul role="list" class="space-y-2">
        <li v-for="(activity, i) in activityStore.multi" :key="`activity-${i}`">
          <ActivityCard :activity="activity" :last-card="i === activityStore.multi.length - 1" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useActivityStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const appSettings = useSettingStore()
const activityStore = useActivityStore()

onMounted(async () => {
  appSettings.setPageName("Activity")
  await activityStore.getMulti()
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
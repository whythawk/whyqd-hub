<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-7xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done'">
      Starter
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore } from "@/stores"

definePageMeta({
  layout: "home",
})

const appSettings = useSettingStore()

onMounted(async () => {
  appSettings.setPageName("Schedule")
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
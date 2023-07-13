<template>
  <div>
    <!-- Hero -->
    <main class="md:pl-20 lg:pl-60 xl:pl-72">
      <div class="md:pr-52 lg:pr-72">
        <CommonLaunchCard />
        <LoadingCardSkeleton />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const appSettings = useSettingStore()

onMounted(async () => {
  appSettings.setPageName("Bookmarks")
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
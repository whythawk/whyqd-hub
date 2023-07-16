<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div class="mt-6 flex justify-center border-b border-t border-gray-200 py-6 md:px-12">
      <NuxtLink to="/projects/edit" class="flex items-center space-x-2 rounded-lg hover:bg-gray-50 pr-1">
        <div class="bg-cerulean-500 flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg">
          <BeakerIcon class="h-6 w-6 text-white" aria-hidden="true" />
        </div>
        <h3 class="text-sm font-bold text-gray-900">
          Create a project
        </h3>
      </NuxtLink>
    </div>
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <ProjectFilterPanel />
      <ul role="list" class="space-y-2">
        <li v-for="(project, i) in projectStore.multi" :key="`project-${i}`">
          <ProjectCard :project="project" :last-card="i === projectStore.multi.length - 1" />
        </li>
      </ul>
      <CommonPagination />
    </div>
  </div>
</template>

<script setup lang="ts">
import { BeakerIcon } from "@heroicons/vue/24/outline"
import { useSettingStore, useProjectStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const projectStore = useProjectStore()

watch(() => [route.query], () => {
  updateMulti()
})

async function updateMulti() {
  if (route.query && route.query.page) projectStore.setPage(route.query.page as string)
  await projectStore.getMulti()
}

onMounted(async () => {
  appSettings.setPageName("Projects")
  updateMulti()
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
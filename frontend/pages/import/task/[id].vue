<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done' && taskStore.term">
      <div class="mt-6 border-b border-t border-gray-200 py-3 md:px-8">
        <TaskCard :task="taskStore.term" :last-card="true" />
      </div>
      <div v-if="!authStore.hasExplorerSubscription" class="my-2">
        <SubscriptionsNeededCard needed="EXPLORER" />
      </div>
      <div v-else>
        <CommonImportCard v-if="!showImportTemplate" reference="DATA" @set-import="watchSetUpload" />
        <div v-else>
          <ul role="list" class="pt-1 space-y-2">
            <li v-for="(source, sIdx) in dataSources" :key="`source-${sIdx}`" class="space-y-10">
              <UploadTemplateCard v-if="!uploaded.includes(sIdx)" :source="source" :idx="sIdx"
                :last-card="sIdx === dataSources.length - 1" @pop-request="watchUploadRequests" />
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FileWithHandle } from "browser-fs-access"
import { useSettingStore, useTaskStore, useAuthStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const appSettings = useSettingStore()
const authStore = useAuthStore()
const route = useRoute()
const taskStore = useTaskStore()
const showImportTemplate = ref(false)
const dataSources = ref<File[]>([])
const uploaded = ref<number[]>([])

onMounted(async () => {
  await taskStore.getTerm(route.params.id as string)
  if (!taskStore.term || Object.keys(taskStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  appSettings.setPageName("Import")
})

// FILE IMPORTER - START
async function watchSetUpload(data: FileWithHandle[]) {
  for (const f of data) {
    if (f.handle) {
      const fData = await f.handle.getFile()
      dataSources.value.push(fData)
    }
  }
  if (dataSources.value.length) showImportTemplate.value = true
}

async function watchUploadRequests(request: number) {
  uploaded.value.push(request)
  // dataSources.value.splice(request, 1)
  if (dataSources.value.length == uploaded.value.length) showImportTemplate.value = false
}
// FILE IMPORTER - END

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
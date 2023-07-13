<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <div class="mt-6 border-b border-t border-gray-200 py-3 md:px-8">
        <ResourceCard :resource="resourceStore.term" :last-card="true" />
      </div>
      <p class="mt-6 text-sm text-gray-900 text-center">
        Reprocessing will reset your crosswalk and delete your transform.
      </p>
      <div class="mt-6">
        <UploadReprocessTemplateCard :source="resourceTemplate" :reference="resourceStore.term.data" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useResourceStore } from "@/stores"
import { IDataSourceTemplate, IMimeType } from "@/interfaces"
import { apiResource } from "@/api"

definePageMeta({
  middleware: ["authenticated"],
});

const appSettings = useSettingStore()
const route = useRoute()
const resourceStore = useResourceStore()
const resourceTemplate = ref<IDataSourceTemplate>({} as IDataSourceTemplate)
const IMimeReference: { [key: string]: IMimeType } = {
  "text/csv": "CSV",
  "application/vnd.ms-excel": "XLS",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "XLSX",
  "application/vnd.apache.parquet": "PARQUET",
  "application/vnd.apache.feather": "FEATHER"
}

onMounted(async () => {
  appSettings.setPageName("Import")
  await resourceStore.getTerm(route.params.id as string)
  if (!resourceStore.term || Object.keys(resourceStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  await resourceStore.authTokens.refreshTokens()
  if (resourceStore.authTokens.token) {
    try {
      appSettings.setPageState("loading")
      const { data: response } = await apiResource.getTermTemplate(resourceStore.authTokens.token, route.params.id as string)
      if (response.value) {
        response.value.mime = IMimeReference[response.value.mime]
        resourceTemplate.value = response.value
      }
      appSettings.setPageState("done")
    } catch (error) {
      throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
    }
  }
})

// FILE IMPORTER - START
async function watchUploadRequests(request: number) { }
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
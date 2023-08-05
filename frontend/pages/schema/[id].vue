<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done' && schemaStore.term && schemaStore.term.name">
      <CommonHeadingView purpose="Schema" :name="schemaStore.term.name" :title="schemaStore.term.title"
        @set-edit-request="watchHeadingRequest" />
      <dl class="divide-y divide-gray-100">
        <div class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Name</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ schemaStore.term.name }}</dd>
        </div>
        <div v-if="schemaStore.term.title" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Title</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ schemaStore.term.title }}</dd>
        </div>
        <div v-if="schemaStore.term.description" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Description</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ schemaStore.term.description }}
          </dd>
        </div>
        <div v-if="schemaStore.term.missingValues && schemaStore.term.missingValues.length"
          class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Missing Values</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ schemaStore.term.missingValues }}
          </dd>
        </div>
        <div v-if="schemaStore.term.primaryKey" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Primary key/s</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ schemaStore.term.primaryKey }}
          </dd>
        </div>
        <div v-if="schemaStore.term.index" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Index (row count)</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ schemaStore.term.index }}
          </dd>
        </div>
      </dl>
    </div>
    <div class="space-y-2 mx-2">
      <CommonCitationCard :citation="schemaStore.term.citation" />
    </div>
    <div class="space-y-2 mx-2">
      <h2 class="text-sm font-semibold leading-7 text-gray-900 pt-2">Fields</h2>
      <ul v-if="schemaStore.term.fields && schemaStore.term.fields.length" role="list" class="space-y-6">
        <li v-for="(field, fIdx) in schemaStore.term.fields" :key="`field-${field.uuid}`">
          <SchemaFieldCard :field="field" :last-card="fIdx === schemaStore.term.fields.length - 1" />
        </li>
      </ul>
    </div>
    <div class="space-y-2 mx-2">
      <h2 class="text-sm font-semibold leading-7 text-gray-900 pt-2">Version</h2>
      <ul v-if="schemaStore.term.version && schemaStore.term.version.length" role="list" class="space-y-6">
        <li v-for="(version, vIdx) in schemaStore.term.version" :key="`schema-version-${vIdx}`">
          <CommonVersionCard :version="version" :last-card="vIdx === schemaStore.term.version.length - 1" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useSchemaStore, useReferenceStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const schemaStore = useSchemaStore()
const referenceStore = useReferenceStore()

async function watchHeadingRequest(request: string) {
  switch (request) {
    case "remove":
      await referenceStore.removeTerm(route.params.id as string)
      return await navigateTo("/references")
    case "edit":
      return await navigateTo(`/schema/edit/${route.params.id}`)
  }
}

onMounted(async () => {
  await schemaStore.getTerm(route.params.id as string)
  if (!schemaStore.term || Object.keys(schemaStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  appSettings.setPageName("Schema")
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
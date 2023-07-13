<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div class="flex w-full items-center justify-between gap-x-6 pb-2">
      <div class="flex flex-inline space-x-4">
        <img class="relative h-8 w-8 flex-none rounded-lg ring-1 ring-offset-2 ring-ochre-200 text-gray-700" :src="avatar"
          :alt="heading" />
        <h1 class="truncate text-lg font-semibold leading-7 text-gray-900">
          Schema: {{ heading }}
        </h1>
      </div>
      <div class="flex flex-inline space-x-2">
        <button @click.prevent="showDelete = !showDelete">
          <ExclamationCircleIcon
            :class="[showDelete ? 'text-sienna-600' : 'text-cerulean-600', 'h-6 w-6  hover:text-ochre-600']" />
        </button>
        <NuxtLink :to="`/schema/edit/${route.params.id}`" type="button"
          class="text-sm leading-6 text-gray-900 rounded-lg px-2 py-1 ring-1 ring-inset ring-gray-200 hover:bg-gray-100">
          Edit
        </NuxtLink>
      </div>
    </div>
    <div v-if="showDelete"
      class="flex gap-x-3 items-center text-sm leading-6 text-gray-900 rounded-lg p-3 ring-1 ring-inset ring-gray-200">
      <button type="button" @click.prevent="removeReference"
        class="text-sm leading-6 text-gray-900 rounded-lg px-2 py-1 ring-1 ring-inset ring-sienna-200 hover:bg-sienna-200">
        Delete
      </button>
      <span class="italic">Zero history deletion.</span>
    </div>
    <div>
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
import { ExclamationCircleIcon } from "@heroicons/vue/24/outline"
import { getAvatar } from "@/utilities"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const schemaStore = useSchemaStore()
const referenceStore = useReferenceStore()
const heading = ref("")
const avatar = ref("")
const showDelete = ref(false)

onMounted(async () => {
  await schemaStore.getTerm(route.params.id as string)
  if (!schemaStore.term || Object.keys(schemaStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  if (schemaStore.term.title) heading.value = schemaStore.term.title
  else heading.value = schemaStore.term.name
  avatar.value = await getAvatar(schemaStore.term.uuid)
  appSettings.setPageName("Schema definition")
})

async function removeReference() {
  await referenceStore.removeTerm(route.params.id as string)
  return await navigateTo("/references")
}

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
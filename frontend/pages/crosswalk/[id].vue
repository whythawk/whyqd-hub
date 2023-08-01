<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <CommonHeadingView v-if="crosswalkStore.term.name" purpose="Crosswalk" :name="crosswalkStore.term.name"
        :title="crosswalkStore.term.title" @set-edit-request="watchHeadingRequest" />
      <dl class="divide-y divide-gray-100">
        <div class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Name</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ crosswalkStore.term.crosswalk.name
          }}</dd>
        </div>
        <div v-if="crosswalkStore.term.crosswalk.title" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Title</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ crosswalkStore.term.crosswalk.title
          }}</dd>
        </div>
        <div v-if="crosswalkStore.term.crosswalk.description" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Description</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
            {{ crosswalkStore.term.crosswalk.description }}
          </dd>
        </div>
      </dl>
      <div class="space-y-2 mx-2">
        <h2 class="text-sm font-semibold leading-7 text-gray-900 pt-2">Actions</h2>
        <ul v-if="crosswalkStore.term.crosswalk.actions && crosswalkStore.term.crosswalk.actions.length" role="list">
          <li v-for="(action, aIdx) in crosswalkStore.term.crosswalk.actions" :key="`action-${aIdx}`">
            <ActionCard :action="action" :last-card="aIdx === crosswalkStore.term.crosswalk.actions.length - 1" />
          </li>
        </ul>
      </div>
      <div class="space-y-2 mx-2">
        <h2 class="text-sm font-semibold leading-7 text-gray-900 pt-2">Workflow</h2>
        <ul role="list" class="space-y-1">
          <li v-if="crosswalkStore.term.data">
            <ResourceDataCard :resource-id="crosswalkStore.term.id" :reference="crosswalkStore.term.data"
              :state="crosswalkStore.term.state" :last-card="false" />
          </li>
          <li>
            <ResourceSchemaCard :resource-id="crosswalkStore.term.id" :reference="crosswalkStore.term.schema_subject"
              :state="crosswalkStore.term.state" :last-card="false" />
          </li>
          <li>
            <ResourceSchemaCard :resource-id="crosswalkStore.term.id" :reference="crosswalkStore.term.schema_object"
              schema-head="object" :state="crosswalkStore.term.state" :last-card="true" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useCrosswalkStore, useReferenceStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const crosswalkStore = useCrosswalkStore()
const appSettings = useSettingStore()
const referenceStore = useReferenceStore()

async function watchHeadingRequest(request: string) {
  switch (request) {
    case "remove":
      await referenceStore.removeTerm(route.params.id as string)
      return await navigateTo("/references")
    case "edit":
      return await navigateTo(`/crosswalk/edit/${route.params.id}`)
  }
}

onMounted(async () => {
  await crosswalkStore.getTerm(route.params.id as string)
  if (!crosswalkStore.term || Object.keys(crosswalkStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  appSettings.setPageName("Crosswalk")
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
<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done' && crosswalkStore.term && crosswalkStore.term.name">
      <CommonHeadingView purpose="Crosswalk" :name="crosswalkStore.term.name" :title="crosswalkStore.term.title"
        @set-edit-request="watchHeadingRequest" />
      <div class="mb-6 border-b border-gray-200 py-3 md:px-8">
        <div class="flex w-full items-center justify-between">
          <div>
            <div class="group flex flex-row text-xs font-medium text-gray-700 leading-8 items-center">
              <MapPinIcon class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="ml-1">
                {{ crosswalkStore.term.state }}
              </span>
            </div>
            <p v-if="crosswalkStore.term.latest_activity && crosswalkStore.term.latest_activity.alert" class="text-xs text-gray-500">
              {{ crosswalkStore.term.latest_activity.message }}
            </p>
          </div>
          <div>
            <NuxtLink
              :to="`/resources/${crosswalkStore.term.id}`"
              class="group flex text-sm flex-row text-gray-700 hover:text-ochre-600 gap-x-1 font-semibold items-center">
              <RectangleGroupIcon class="h-5 w-5 shrink-0" aria-hidden="true" />
              <span class="ml-1">
                {{ crosswalkStore.term.crosswalk.title }}
              </span>
            </NuxtLink>
            <p class="text-xs text-center text-gray-500">{{ crosswalkStore.term.crosswalk.name }}</p>
          </div>
        </div>
      </div>
      <div class="space-y-2 mx-2">
        <h2 class="text-sm font-semibold leading-7 text-gray-900">Actions</h2>
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
            <ResourceSchemaCard v-if="!crosswalkStore.term.data" :resource-id="crosswalkStore.term.id"
              :reference="crosswalkStore.term.schema_subject" :state="crosswalkStore.term.state" :last-card="false" />
            <ResourceSchemaCategoriseCard v-else :resource-id="crosswalkStore.term.id"
              :reference="crosswalkStore.term.schema_subject" :state="crosswalkStore.term.state" :last-card="false" />
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
import { MapPinIcon, RectangleGroupIcon } from "@heroicons/vue/24/outline"
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
  ogImage: "https://whyqd.com/img/crosswalk.jpg"
})
// METADATA - END
</script>
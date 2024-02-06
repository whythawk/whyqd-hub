<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done' && resourceStore.term && resourceStore.term.name">
      <CommonHeadingView purpose="Resource" :name="resourceStore.term.name" :title="resourceStore.term.title"
        @set-edit-request="watchHeadingRequest" />
      <div class="mb-6 border-b border-gray-200 py-3 md:px-8">
        <div class="flex w-full items-center justify-between">
          <div>
            <div class="group flex flex-row text-xs font-medium text-gray-700">
              <MapPinIcon class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="ml-1">
                {{ resourceStore.term.state }}
              </span>
            </div>
            <p v-if="resourceStore.term.latest_activity && resourceStore.term.latest_activity.alert" class="text-xs leading-6 text-gray-500">
              {{ resourceStore.term.latest_activity.message }}
            </p>
          </div>
          <div>
            <div class="flex justify-between gap-x-4">
              <div class="truncate py-0.5 text-xs text-gray-500 text-right">
                <div class="truncate py-0.5 text-xs text-gray-500">
                  <div class="truncate py-0.5">
                    <time :datetime="resourceStore.term.created" class="flex-none py-0.5 text-xs text-gray-500">
                      Created: {{ readableDate(resourceStore.term.created) }}</time>
                  </div>
                  <div class="truncate py-0.5">
                    <time :datetime="resourceStore.term.modified" class="flex-none py-0.5 text-xs text-gray-500">
                      Updated: {{ readableDate(resourceStore.term.modified) }}</time>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div>
        <dl class="divide-y divide-gray-100">
          <div v-if="resourceStore.term.description" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt class="text-sm font-medium text-gray-900">Description</dt>
            <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ resourceStore.term.description }}
            </dd>
          </div>
        </dl>
      </div>
      <div class="space-y-2 mx-2">
        <h2 class="text-sm font-semibold leading-7 text-gray-900 pt-2">Workflow</h2>
        <ul v-if="resourceStore.term" role="list" class="space-y-6">
          <li v-if="resourceStore.term.data">
            <ResourceDataCard :resource-id="resourceStore.term.id" :reference="resourceStore.term.data"
              :state="resourceStore.term.state" :last-card="false" />
          </li>
          <li>
            <ResourceSchemaCard v-if="!resourceStore.term.data" :resource-id="resourceStore.term.id"
              :reference="resourceStore.term.schema_subject" :state="resourceStore.term.state" :last-card="false" />
            <ResourceSchemaCategoriseCard v-else :resource-id="resourceStore.term.id"
              :reference="resourceStore.term.schema_subject" :state="resourceStore.term.state" :last-card="false" />
          </li>
          <li>
            <ResourceReferenceCard :resource-id="resourceStore.term.id" model-type="CROSSWALK"
              :reference="resourceStore.term.crosswalk" :state="resourceStore.term.state" :last-card="false" />
          </li>
          <li>
            <ResourceReferenceCard :resource-id="resourceStore.term.id" model-type="SCHEMA"
              :reference="resourceStore.term.schema_object" :state="resourceStore.term.state" :last-card="false" />
          </li>
          <li v-if="resourceStore.term.data">
            <ResourceDataCard :resource-id="resourceStore.term.id" :reference="resourceStore.term.transformdata"
              :state="resourceStore.term.state" :last-card="true" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useResourceStore } from "@/stores"
import { MapPinIcon, } from "@heroicons/vue/24/outline"
import { readableDate } from "@/utilities"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const resourceStore = useResourceStore()

async function watchHeadingRequest(request: string) {
  switch (request) {
    case "remove":
      let projectID = resourceStore.term.project_id
      await resourceStore.removeTerm(route.params.id as string)
      if (projectID !== null) return await navigateTo(`/activity/project/${projectID}`)
      else return await navigateTo("/activity")
  }
}

onMounted(async () => {
  await resourceStore.getTerm(route.params.id as string)
  if (!resourceStore.term || Object.keys(resourceStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  appSettings.setPageName("Resources")
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
<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <div class="flex w-full items-center justify-between gap-x-6 pb-2">
        <div class="flex flex-inline space-x-4">
          <img class="relative h-8 w-8 flex-none rounded-lg ring-1 ring-offset-2 ring-ochre-200 text-gray-700"
            :src="avatar" :alt="heading" />
          <h1 class="truncate text-lg font-semibold leading-7 text-gray-900">
            Resource: {{ heading }}
          </h1>
        </div>
        <div class="flex flex-inline space-x-2">
          <button @click.prevent="showDelete = !showDelete">
            <ExclamationCircleIcon
              :class="[showDelete ? 'text-sienna-600' : 'text-cerulean-600', 'h-6 w-6  hover:text-ochre-600']" />
          </button>
        </div>
      </div>
      <div v-if="showDelete"
        class="flex gap-x-3 items-center text-sm leading-6 text-gray-900 rounded-lg p-3 ring-1 ring-inset ring-gray-200">
        <button type="button" @click.prevent="removeResource"
          class="text-sm leading-6 text-gray-900 rounded-lg px-2 py-1 ring-1 ring-inset ring-sienna-200 hover:bg-sienna-200">
          Delete
        </button>
        <span class="italic">Zero history deletion.</span>
      </div>
      <div class="my-6 border-b border-t border-gray-200 py-3 md:px-8">
        <div class="flex w-full items-center justify-between">
          <div class="group flex flex-row text-xs font-medium text-gray-700">
            <MapPinIcon class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
            <span class="ml-1">
              {{ resourceStore.term.state }}
            </span>
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
          <li>
            <ResourceDataCard :resource-id="resourceStore.term.id" :reference="resourceStore.term.data"
              :state="resourceStore.term.state" :last-card="false" />
          </li>
          <li>
            <ResourceSchemaCategoriseCard :resource-id="resourceStore.term.id"
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
          <li>
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
import { ExclamationCircleIcon, MapPinIcon, } from "@heroicons/vue/24/outline"
import { readableDate, getAvatar } from "@/utilities"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const appSettings = useSettingStore()
const resourceStore = useResourceStore()
const heading = ref("")
const avatar = ref("")
const showDelete = ref(false)

onMounted(async () => {
  appSettings.setPageName("Resources")
  await resourceStore.getTerm(route.params.id as string)
  if (!resourceStore.term || Object.keys(resourceStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  if (resourceStore.term.title) heading.value = resourceStore.term.title
  else heading.value = resourceStore.term.name
  avatar.value = await getAvatar(resourceStore.term.id)
})

async function removeResource() {
  await resourceStore.removeTerm(route.params.id as string)
  return await navigateTo("/resources")
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
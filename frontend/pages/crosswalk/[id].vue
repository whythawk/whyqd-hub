<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done' && crosswalkStore.term.crosswalk">
      <div class="flex w-full items-center justify-between gap-x-6 pb-2">
        <div class="flex flex-inline space-x-4">
          <img class="relative h-8 w-8 flex-none rounded-lg ring-1 ring-offset-2 ring-ochre-200 text-gray-700"
            :src="avatar" :alt="heading" />
          <h1 class="truncate text-lg font-semibold leading-7 text-gray-900">
            Crosswalk: {{ heading }}
          </h1>
        </div>
        <div class="flex flex-inline space-x-2">
          <button @click.prevent="showDelete = !showDelete">
            <ExclamationCircleIcon
              :class="[showDelete ? 'text-sienna-600' : 'text-cerulean-600', 'h-6 w-6  hover:text-ochre-600']" />
          </button>
          <NuxtLink :to="`/crosswalk/edit/${route.params.id}`" type="button"
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
      </div>
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
import { useSettingStore, useCrosswalkStore } from "@/stores"
import { ExclamationCircleIcon } from "@heroicons/vue/24/outline"
import { getAvatar } from "@/utilities"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const crosswalkStore = useCrosswalkStore()
const appSettings = useSettingStore()
const heading = ref("")
const avatar = ref("")
const showDelete = ref(false)

onMounted(async () => {
  if (route.params.id) {
    await crosswalkStore.getTerm(route.params.id as string)
    crosswalkStore.term
  }
  if (!crosswalkStore.term || Object.keys(crosswalkStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  if (crosswalkStore.term.crosswalk.title) heading.value = crosswalkStore.term.crosswalk.title
  else heading.value = crosswalkStore.term.crosswalk.name as string
  avatar.value = await getAvatar(crosswalkStore.term.crosswalk.id as string)
  appSettings.setPageName("Crosswalk definition")
})

async function removeReference() {
  // await referenceStore.removeTerm(route.params.id as string)
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
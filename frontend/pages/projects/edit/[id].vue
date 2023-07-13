<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <div class="flex w-full items-center justify-between gap-x-6 pb-2">
        <div class="flex flex-inline space-x-4">
          <img v-if="saveApproach === 'Update'"
            class="relative h-8 w-8 flex-none rounded-lg ring-1 ring-offset-2 ring-ochre-200 text-gray-700" :src="avatar"
            :alt="heading" />
          <BeakerIcon v-else
            class="relative h-6 w-6 flex-none rounded-lg ring-1 ring-offset-2 ring-ochre-200 text-gray-700" />
          <h1 class="truncate text-lg font-semibold leading-7 text-gray-900">
            Project: {{ heading }}
          </h1>
        </div>
        <div class="flex flex-inline space-x-2">
          <button v-if="saveApproach === 'Update'" @click.prevent="showDelete = !showDelete">
            <ExclamationCircleIcon
              :class="[showDelete ? 'text-sienna-600' : 'text-cerulean-600', 'h-6 w-6  hover:text-ochre-600']" />
          </button>
          <NuxtLink :to="saveApproach === 'Update' ? `/projects/${route.params.id}` : '/projects'" type="button"
            class="text-sm leading-6 text-gray-900 rounded-lg px-2 py-1 ring-1 ring-inset ring-gray-200 hover:bg-gray-100">
            Cancel
          </NuxtLink>
        </div>
      </div>
      <div v-if="showDelete"
        class="flex gap-x-3 items-center text-sm leading-6 text-gray-900 rounded-lg p-3 ring-1 ring-inset ring-gray-200">
        <button type="button" @click.prevent="removeProject"
          class="text-sm leading-6 text-gray-900 rounded-lg px-2 py-1 ring-1 ring-inset ring-sienna-200 hover:bg-sienna-200">
          Delete
        </button>
        <span class="italic">Zero history deletion.</span>
      </div>
      <ProjectEditCard />
    </div>
  </div>
</template>

<script setup lang="ts">
import { BeakerIcon, ExclamationCircleIcon } from "@heroicons/vue/24/outline"
import { getAvatar } from "@/utilities"
import { useSettingStore, useProjectStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const appSettings = useSettingStore()
const route = useRoute()
const projectStore = useProjectStore()
const heading = ref("Create")
const avatar = ref("")
const showDelete = ref(false)
const saveApproach = ref("Create")

async function removeProject() {
  await projectStore.removeTerm(route.params.id as string)
  return await navigateTo("/projects")
}

onMounted(async () => {
  if (route.params.id !== "create") {
    await projectStore.getTerm(route.params.id as string)
    if (!projectStore.term || Object.keys(projectStore.term).length === 0)
      throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
    if (
      projectStore.draft
      && Object.keys(projectStore.draft).length !== 0
      && projectStore.draft.id !== projectStore.term.id)
      projectStore.setDraft(projectStore.term)
    avatar.value = await getAvatar(route.params.id as string)
    if (projectStore.term.title) heading.value = projectStore.term.title
    else heading.value = projectStore.term.name
    saveApproach.value = "Update"
  }
})

// onBeforeRouteLeave((to, from, next) => {
//   projectStore.setDraft(draft.value)
//   next()
// })

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
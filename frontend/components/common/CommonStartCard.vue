<template>
  <div class="max-w-3xl mx-auto">
    <div class="mt-6 border-b border-t border-gray-200 py-6 md:px-12">
      <h1 class="text-lg font-bold leading-8 my-1">Welcome - let's get started ...</h1>
      <p class="text-sm my-2 mb-3">
        Whyqd (/wɪkɪd/) has a relatively simple workflow, and these quick-links will guide you.
      </p>
    <div class="mt-6 md:px-12">
      <ul role="list" class="space-y-1">
        <li v-for="(start, startIdx) in launch" :key="startIdx"
          class="relative flex items-center space-x-2 py-1 border border-gray-200 bg-white hover:bg-gray-100 rounded-md">
          <div class="min-w-0 flex-auto">
            <div class="flex items-center gap-x-3 p-2">
              <div :class="[start.background, 'flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg']">
                <component :is="start.icon" class="h-5 w-5 text-white" aria-hidden="true" />
              </div>
              <h2 class="min-w-0 text-sm font-semibold leading-6 text-gray-900">
                <NuxtLink :to="start.to" :class="[start.show ? '' : 'pointer-events-none', 'flex gap-x-2']">
                  <span>{{ start.title }}</span>
                  <span class="absolute inset-0" />
                </NuxtLink>
              </h2>
            </div>
            <div class="ml-2 mb-2 flex items-center gap-x-2.5 text-sm leading-5 text-gray-700">
              <p>{{ start.description }}<span v-if="!start.show">&nbsp;You need to be a subscriber.</span></p>
            </div>
          </div>
          <ChevronRightIcon class="h-5 w-5 flex-none text-gray-900" aria-hidden="true" />
        </li>
      </ul>
    </div>
    </div>
    <div class="px-2 pb-10 lg:px-4 lg:pb-6 max-w-3xl mx-auto">
      <div v-if="appSettings.current.pageState === 'loading'">
        <LoadingCardSkeleton />
      </div>
      <div v-if="appSettings.current.pageState === 'done'">
        <ProjectFilterPanel />
        <div v-if="projectStore.multi.length === 0" class="space-y-2">
          <CommonEmptyCard term="Nothing right now. Create some projects to see them here." />
        </div>
        <ul role="list" class="space-y-2">
          <li v-for="(project, i) in projectStore.multi" :key="`project-${i}`">
            <ProjectCard :project="project" :last-card="i === projectStore.multi.length - 1" />
          </li>
        </ul>
        <CommonPagination />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ArrowUpTrayIcon,
  BeakerIcon,
  BellIcon,
  CalendarIcon,
  ChevronRightIcon,
  FolderPlusIcon,
  SquaresPlusIcon,
  Square3Stack3DIcon,
} from "@heroicons/vue/24/outline"
import { useAuthStore, useSettingStore, useProjectStore } from "@/stores"

const route = useRoute()
const authStore = useAuthStore()
const appSettings = useSettingStore()
const projectStore = useProjectStore()

watch(() => [route.query], async () => {
  await updateMulti()
})

async function updateMulti() {
  if (route.query && route.query.page) projectStore.setPage(route.query.page as string)
  await projectStore.getMulti()
}

onMounted(async () => {
  appSettings.setPageName("Projects")
  updateMulti()
})

onBeforeUnmount(() => {
  const router = useRouter()
  router.replace({ query: {} })
})

const launch = [
  {
    title: "Create a project",
    description: "Create a project to organise tasks or teams, & define who gets to do what.",
    icon: BeakerIcon,
    to: "/projects/edit",
    background: "bg-ochre-500",
    show: true,
  },
  {
    title: "Create a schema",
    description: "Describe a definition to structure tabular data.",
    icon: SquaresPlusIcon,
    to: "/schema/edit",
    background: "bg-eucalyptus-500",
    show: true,
  },
  {
    title: "Create a task",
    description: "Create a repeating process & manage resources created by tasks.",
    icon: Square3Stack3DIcon,
    to: "/tasks/edit",
    background: "bg-cerulean-500",
    show: true,
  },
  {
    title: "Import data",
    description: "Upload tabular data & automatically derive a source schema.",
    icon: ArrowUpTrayIcon,
    to: "/import",
    background: "bg-sienna-500",
    show: authStore.hasExplorerSubscription,
  },
]
</script>
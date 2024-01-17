<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <!-- @vue-ignore -->
    <img :src="avatar" :alt="heading"
      class="relative mt-3 h-6 w-6 flex-none rounded-full bg-gray-50 ring-1 ring-offset-4 ring-ochre-200 text-gray-700"
      aria-hidden="true" />
    <NuxtLink :to="`/tasks/${props.task.id}`" class="flex-auto rounded-lg  py-2 px-3 ring-1 ring-inset ring-gray-200">
      <div class="flex w-full items-center">
        <div class="flex-1">
          <div class="flex justify-between gap-x-4">
            <div class="py-0.5 text-sm leading-5 text-gray-500">
              <h2 class="font-bold text-gray-900">{{ heading }}</h2>
            </div>
            <div class="truncate py-0.5 text-xs text-gray-500 text-right">
              <time :datetime="props.task.modified" class="flex-none py-0.5 text-xs text-gray-500">{{
                readableDate(props.task.modified as string) }}</time>
            </div>
          </div>
        </div>
      </div>
      <p v-if="props.task.description" class="text-sm leading-6 text-gray-500">{{ props.task.description }}</p>
      <div class="flex items-center justify-between">
        <NuxtLink :to="`/import/task/${props.task.id}`"
          class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 font-semibold text-xs items-center">
          <ArrowUpTrayIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
          <span class="hidden lg:block">Import data</span>
        </NuxtLink>
        <ul role="list" class="flex flex-row justify-end text-xs">
          <h3 id="detail-heading" class="sr-only">Project, templates and schema object</h3>
          <li v-if="props.task.project && Object.keys(props.task.project).length !== 0" class="relative">
            <NuxtLink :to="`/projects/${props.task.project.id}`"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <BeakerIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Project</span>
            </NuxtLink>
          </li>
          <li v-if="addProject && (!props.task.project || Object.keys(props.task.project).length === 0)" class="relative">
            <button type="button" @click.prevent="addToProject"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <BeakerIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Project</span>
            </button>
          </li>
          <li class="relative">
            <NuxtLink :to="`/resources/task/${props.task.id}`"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <RectangleGroupIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Resources</span>
              <span v-if="props.task.resources">({{ props.task.resources }})</span>
            </NuxtLink>
          </li>
          <li class="relative">
            <NuxtLink v-if="props.task.schema" :to="`/schema/${props.task.schema.id}`"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <Squares2X2Icon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Schema</span>
            </NuxtLink>
            <button v-else type="button" @click.prevent="schemaRedirect"
              class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <SquaresPlusIcon class="text-sienna-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Schema</span>
            </button>
          </li>
        </ul>
      </div>
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
import { ArrowsRightLeftIcon, BeakerIcon, RectangleGroupIcon, Squares2X2Icon, SquaresPlusIcon, ArrowUpTrayIcon } from "@heroicons/vue/24/outline"
import { readableDate, getAvatar } from "@/utilities"
import { ITask, IReferenceFilters } from "@/interfaces"
import { useReferenceStore, useTaskStore, useProjectStore } from "@/stores"

const route = useRoute()
const referenceStore = useReferenceStore()
const avatar = shallowRef("")
const heading = ref("")
const addProject = ref(false)

const props = defineProps<{
  task: ITask,
  lastCard: Boolean
}>()

async function addToProject() {
  if (route.params.id && props.task.id) {
    const projectStore = useProjectStore()
    await projectStore.addTask(route.params.id as string, props.task.id)
    const taskStore = useTaskStore()
    await taskStore.getMultiByProject(route.params.id as string)
  }
}

async function schemaRedirect() {
  let filters: IReferenceFilters = { ...referenceStore.filters }
  filters.reference_type = "SCHEMA"
  referenceStore.resetFilters()
  referenceStore.setFilters(filters)
  await navigateTo(`/references/task/${props.task.id}`)
}

onMounted(async () => {
  if (route.path.includes("/project/")) addProject.value = true
  avatar.value = await getAvatar(props.task.id as string)
  if (props.task.title) heading.value = props.task.title
  else heading.value = props.task.name
})
</script>
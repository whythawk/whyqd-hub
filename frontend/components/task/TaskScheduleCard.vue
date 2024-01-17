<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <!-- @vue-ignore -->
    <img :src="avatar" :alt="heading"
      class="relative mt-3 h-6 w-6 flex-none rounded-full bg-gray-50 ring-1 ring-offset-4 ring-ochre-200 text-gray-700"
      aria-hidden="true" />
    <div class="flex-auto rounded-lg  py-2 px-3 ring-1 ring-inset ring-gray-200">
      <NuxtLink :to="`/tasks/${props.task.id}`"  class="flex w-full items-center">
        <div class="flex-1">
          <div class="flex justify-between gap-x-4 items-center">
            <div class="py-0.5 text-sm leading-5 text-gray-500">
              <h2 class="font-bold text-gray-900 hover:text-ochre-600 ">{{ heading }}</h2>
            </div>
            <div class="truncate py-0.5 text-xs text-gray-500 text-right">
              <span v-if="props.task.accrualPriority">Priority: {{ props.task.accrualPriority }}</span>
              <span v-else>Priority: none</span>
              <span class="text-sm text-gray-400 px-2">&middot;</span>
              <span>Update: </span>
              <span v-if="props.task.accrualPolicy">{{ props.task.accrualPolicy.toLowerCase() }}, </span>
              <span v-if="props.task.accrualPeriodicity">{{ props.task.accrualPeriodicity }}</span>
              <span v-else>never</span>
              <time v-if="props.task.latestResource" :datetime="props.task.modified"
                class="flex-none py-0.5 text-xs text-gray-500">
                <span class="text-sm text-gray-400 px-2">&middot;</span>
                {{ readableDate(props.task.latestResource.modified as string) }}
              </time>
            </div>
          </div>
        </div>
      </NuxtLink>
      <p v-if="props.task.description" class="text-sm leading-6 text-gray-500">{{ props.task.description }}</p>
      <div class="flex items-center justify-between">
        <ul role="list" class="flex flex-row justify-start text-xs">
          <h3 id="action-heading" class="sr-only">Import, source link, and latest resource state</h3>
          <li class="relative">
            <NuxtLink :to="`/import/task/${props.task.id}`"
              class="text-cerulean-700 hover:text-ochre-600 group flex gap-x-1 p-2 pl-0 font-semibold text-xs items-center">
              <ArrowUpTrayIcon class="text-cerulean-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span>Import data</span>
            </NuxtLink>
          </li>
          <li v-if="props.task.source && isValidHttpUrl(props.task.source)" class="relative">
            <a :href="props.task.source" target="_blank"
              class="text-cerulean-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold text-xs items-center z-50">
              <LinkIcon class="text-cerulean-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span>Source</span>
            </a>
          </li>
        </ul>
        <ul role="list" class="flex flex-row justify-end text-xs">
          <h3 id="detail-heading" class="sr-only">Project, resources and latest resource state</h3>
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
          <li class="flex flex-row items-center relative">
            <NuxtLink :to="`/resources/task/${props.task.id}`"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 pr-1 font-semibold">
              <RectangleGroupIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Resources</span>
              <span v-if="props.task.resources">({{ props.task.resources }})</span>
            </NuxtLink>
            <span v-if="props.task.latestResource" class="text-sm text-gray-400">&middot;</span>
            <NuxtLink v-if="props.task.latestResource" :to="`/resources/${props.task.latestResource.id}`"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 pl-1 font-semibold">
              <span>{{ props.task.latestResource.state }}</span>
            </NuxtLink>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { BeakerIcon, RectangleGroupIcon, ArrowUpTrayIcon, LinkIcon } from "@heroicons/vue/24/outline"
import { readableDate, getAvatar, isValidHttpUrl } from "@/utilities"
import { IScheduledTask } from "@/interfaces"
import { useTaskStore, useProjectStore } from "@/stores"

const route = useRoute()
const avatar = shallowRef("")
const heading = ref("")
const addProject = ref(false)

const props = defineProps<{
  task: IScheduledTask,
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

onMounted(async () => {
  if (route.path.includes("/project/")) addProject.value = true
  avatar.value = await getAvatar(props.task.id as string)
  if (props.task.title) heading.value = props.task.title
  else heading.value = props.task.name
})
</script>
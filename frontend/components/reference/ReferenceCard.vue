<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <!-- @vue-ignore -->
    <component :is="icons[props.reference.model_type]"
      class="relative mt-3 h-6 w-6 flex-none rounded-full bg-gray-50 ring-1 ring-offset-4 ring-ochre-200 text-gray-700"
      aria-hidden="true" />
    <NuxtLink class="flex-auto rounded-lg  py-2 px-3 ring-1 ring-inset ring-gray-200"
      :to="`/${props.reference.model_type.toLowerCase()}/${props.reference.id}`" v-slot="{ navigate }">
      <button class="flex-auto w-full" :disabled="['DATA', 'TRANSFORM'].includes(props.reference.model_type)"
        @click="navigate">
        <div class="flex w-full items-center justify-between">
          <img class="h-10 w-10 flex-shrink-0 rounded-lg" :src="avatar" :alt="props.reference.name" />
          <div class="flex-1">
            <div class="flex justify-between gap-x-4">
              <div class="py-0.5 text-sm leading-5 text-gray-500 pl-3">
                <h2 v-if="props.reference.title" class="font-bold text-gray-900">{{
                  props.reference.title }}</h2>
                <h2 v-else class="font-bold text-gray-900">{{ props.reference.name }}</h2>
              </div>
              <div class="truncate py-0.5 text-xs text-gray-500 text-right">
                <div class="truncate py-0.5 text-xs text-gray-500">
                  <span class="truncate font-medium text-gray-900">{{ props.reference.model_type }}</span>
                  <span v-if="props.reference.mime_type" class="truncate font-bold text-gray-900">
                    .{{ props.reference.mime_type }}
                  </span>
                </div>
                <div class="truncate py-0.5">
                  <time :datetime="props.reference.created" class="flex-none py-0.5 text-xs text-gray-500">{{
                    readableDate(props.reference.created) }}</time>
                </div>
              </div>
            </div>
          </div>
        </div>
        <p v-if="props.reference.description" class="text-sm leading-6 text-gray-500">{{ props.reference.description }}
        </p>
        <div class="flex justify-between">
          <div class="flex items-center">
            <h4 id="process-heading" class="sr-only">Download data and definitions, or reprocess</h4>
            <ul role="list" class="flex flex-row text-xs">
              <li>
                <CommonDownloadDefinitionButton :reference="props.reference" />
              </li>
            </ul>
          </div>
          <div v-if="addReference" class="flex items-center justify-end">
            <button type="button" @click.prevent="addToReference(addReference)"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 text-xs font-semibold">
              <!-- @vue-ignore -->
              <component :is="addIcons[addReference]" class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0"
                aria-hidden="true" />
              <span class="hidden lg:block">Add to {{ addReference.toLowerCase() }}</span>
            </button>
          </div>
        </div>
      </button>
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
import {
  ArrowsRightLeftIcon,
  BeakerIcon,
  CubeIcon,
  RectangleGroupIcon,
  Square3Stack3DIcon,
  Squares2X2Icon,
  TableCellsIcon,
} from "@heroicons/vue/24/outline"
import { readableDate, getAvatar } from "@/utilities"
import { IReference } from "@/interfaces"
import { useProjectStore, useTaskStore, useResourceStore } from "@/stores"

const route = useRoute()
const avatar = shallowRef("")
const icons = {
  DATA: TableCellsIcon,
  SCHEMA: Squares2X2Icon,
  CROSSWALK: ArrowsRightLeftIcon,
  TRANSFORM: CubeIcon,
}
const addIncludes = {
  RESOURCE: ["SCHEMA", "CROSSWALK"],
  TASK: ["SCHEMA"],
  PROJECT: ["SCHEMA"]
}
const addIcons = {
  RESOURCE: RectangleGroupIcon,
  TASK: Square3Stack3DIcon,
  PROJECT: BeakerIcon
}
const addReference = ref("")

const props = defineProps<{
  reference: IReference,
  lastCard: Boolean
}>()

async function addToReference(addTo: string) {
  switch (addTo) {
    case "PROJECT":
      const projectStore = useProjectStore()
      await projectStore.addSchema(route.params.id as string, props.reference.id)
      break
    case "TASK":
      const taskStore = useTaskStore()
      await taskStore.addTemplate(route.params.id as string, props.reference.id)
      break
    case "RESOURCE":
      const resourceStore = useResourceStore()
      await resourceStore.addSchemaObject(route.params.id as string, props.reference.id)
      break
  }
  await navigateTo(`/${addReference.value.toLowerCase()}s/${route.params.id}`)
}

onMounted(async () => {
  if (route.path.includes("/project/") && addIncludes["PROJECT"].includes(props.reference.model_type))
    addReference.value = "PROJECT"
  if (route.path.includes("/task/") && addIncludes["TASK"].includes(props.reference.model_type))
    addReference.value = "TASK"
  if (route.path.includes("/resource/") && addIncludes["RESOURCE"].includes(props.reference.model_type))
    addReference.value = "RESOURCE"
  avatar.value = await getAvatar(props.reference.model as string)
})
</script>
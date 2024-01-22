<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <!-- @vue-ignore -->
    <img :src="avatar" :alt="props.resource.name"
      class="relative mt-3 h-6 w-6 flex-none rounded-full bg-gray-50 ring-1 ring-offset-4 ring-ochre-200 text-gray-700"
      aria-hidden="true" />
    <div class="flex-auto rounded-lg py-2 px-3 ring-1 ring-inset ring-gray-200">
      <NuxtLink :to="`/resources/${props.resource.id}`" class="flex w-full items-center">
        <div class="flex-1">
          <div class="flex justify-between gap-x-4">
            <div class="py-0.5 text-sm leading-5 text-gray-500">
              <h2 v-if="props.resource.title" class="font-bold text-gray-900 hover:text-ochre-600">
                {{ props.resource.title }}
              </h2>
              <h2 v-else class="font-bold text-gray-900 hover:text-ochre-600">{{ props.resource.name }}</h2>
            </div>
            <div class="truncate py-0.5 text-xs text-gray-500 text-right">
              <time :datetime="props.resource.latest_activity.created" class="flex-none py-0.5 text-xs text-gray-500">
                {{ readableDate(props.resource!.latest_activity.created as string) }}
              </time>
              <BellIcon v-if="props.resource.latest_activity.alert" class="inline-flex h-5 w-5 text-sienna-500 pl-1" />
              <BoltIcon v-if="props.resource.latest_activity.custodiansOnly" class="inline-flex h-5 w-5 text-cerulean-500 pl-1" />
            </div>
          </div>
        </div>
      </NuxtLink>
      <p v-if="props.resource.latest_activity.message" class="text-sm leading-6 text-gray-500">{{ props.resource.latest_activity.message }}</p>
      <div class="flex items-center justify-between pt-2">
        <div class="group flex flex-row text-xs font-medium text-gray-700">
          <MapPinIcon class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
          <span class="ml-1">
            {{ stateValue[props.resource.state] }}
          </span>
        </div>
        <ul role="list" class="flex flex-row justify-end text-xs">
          <h3 id="detail-heading" class="sr-only">Project, resources and latest resource state</h3>
          <li v-if="props.resource.project_id" class="relative">
            <NuxtLink :to="`/activity/project/${props.resource.project_id}`"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 font-semibold text-xs items-center">
              <BeakerIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Project</span>
            </NuxtLink>
          </li>
          <li v-if="props.resource.task_id" class="relative">
            <NuxtLink :to="`/activity/task/${props.resource.task_id}`"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 pl-2 font-semibold text-xs items-center">
              <Square3Stack3DIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Task</span>
            </NuxtLink>
          </li>
          <li v-if="props.resource.sourceURL && isValidHttpUrl(props.resource.sourceURL)" class="relative">
            <a :href="props.resource.sourceURL" target="_blank"
              class="text-cerulean-700 hover:text-ochre-600 group flex gap-x-1 pl-2 font-semibold text-xs items-center">
              <LinkIcon class="text-cerulean-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span>Source</span>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { BeakerIcon, MapPinIcon, Square3Stack3DIcon, BellIcon, BoltIcon, LinkIcon  } from "@heroicons/vue/24/outline"
import { readableDate, getAvatar, isValidHttpUrl } from "@/utilities"
import { IResourceActivitySummary } from "@/interfaces"

const avatar = shallowRef("")
const stateValue = {
  BUSY: "Busy",
  READY: "Ready",
  DATA_READY: "Data Ready",
  SCHEMA_READY: "Schema Ready",
  CROSSWALK_READY: "Crosswalk Ready",
  TRANSFORM_READY: "Transform Ready",
  IMPORT_ERROR: "Import Ready",
  DATA_ERROR: "Data Error",
  SCHEMA_ERROR: "Schema Error",
  CROSSWALK_ERROR: "Crosswalk Error",
  TRANSFORM_ERROR: "Transform Error",
  ERROR: "Error",
  COMPLETE: "Complete"
}

const props = defineProps<{
  resource: IResourceActivitySummary,
  lastCard: Boolean
}>()

onMounted(async () => {
  avatar.value = await getAvatar(props.resource.id as string)
})
</script>
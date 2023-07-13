<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <!-- @vue-ignore -->
    <img :src="avatar" :alt="props.resource.name"
      class="relative mt-3 h-6 w-6 flex-none rounded-full bg-gray-50 ring-1 ring-offset-4 ring-ochre-200 text-gray-700"
      aria-hidden="true" />
    <NuxtLink :to="`/resources/${props.resource.id}`"
      class="flex-auto rounded-lg  py-2 px-3 ring-1 ring-inset ring-gray-200">
      <div class="flex w-full items-center">
        <div class="flex-1">
          <div class="flex justify-between gap-x-4">
            <div class="py-0.5 text-sm leading-5 text-gray-500">
              <h2 v-if="props.resource.title" class="font-bold text-gray-900">{{
                props.resource.title }}</h2>
              <h2 v-else class="font-bold text-gray-900">{{ props.resource.name }}</h2>
            </div>
            <div class="truncate py-0.5 text-xs text-gray-500 text-right">
              <time :datetime="props.resource.modified" class="flex-none py-0.5 text-xs text-gray-500">{{
                readableDate(props.resource!.modified as string) }}</time>
            </div>
          </div>
        </div>
      </div>
      <p v-if="props.resource.description" class="text-sm leading-6 text-gray-500">{{ props.resource.description }}</p>
      <div class="flex items-center justify-between">
        <div class="group flex flex-row text-xs font-medium text-gray-700">
          <MapPinIcon class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
          <span class="ml-1">
            {{ props.resource.state }}
          </span>
        </div>
        <NuxtLink v-if="props.resource.task" :to="`/resources/task/${props.resource.task.id}`"
          class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 font-semibold text-xs items-center">
          <Square3Stack3DIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
          <span class="hidden lg:block">Task</span>
        </NuxtLink>
      </div>
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
import { MapPinIcon, Square3Stack3DIcon } from "@heroicons/vue/24/outline"
import { readableDate, getAvatar } from "@/utilities"
import { IResource } from "@/interfaces"

const avatar = shallowRef("")

const props = defineProps<{
  resource: IResource,
  lastCard: Boolean
}>()

onMounted(async () => {
  avatar.value = await getAvatar(props.resource.id as string)
})
</script>
<template>
  <div class="flex w-full items-center justify-between">
    <div class="flex-1">
      <div class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold text-sm">
        <img v-if="showAvatar" class="h-8 w-8 flex-shrink-0 rounded-lg" :src="avatar" :alt="heading" />
        <component v-else :is="icons[props.showIcon.toUpperCase()]"
          class="h-5 w-5 flex-shrink-0 rounded-lg text-gray-700 group-hover:text-ochre-600" aria-hidden="true" />
        <span>{{ heading }}</span>
      </div>
    </div>
    <div v-if="showState" class="py-0.5 text-sm leading-5 text-gray-500">
      {{ props.summary.state }}
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ArrowsRightLeftIcon, BeakerIcon, CubeIcon, Squares2X2Icon, Square3Stack3DIcon, TableCellsIcon
} from "@heroicons/vue/24/outline"
import { getAvatar } from "@/utilities"
import type { IModelSummary, IKeyable } from "@/interfaces"

const props = defineProps<{
  summary: IModelSummary,
  showState: boolean,
  showIcon: string,
}>()
const avatar = shallowRef("")
const showAvatar = ref(true)
const heading = ref("")
const icons: IKeyable = {
  DATA: TableCellsIcon,
  SCHEMA: Squares2X2Icon,
  CROSSWALK: ArrowsRightLeftIcon,
  TRANSFORM: CubeIcon,
  PROJECT: BeakerIcon,
  TASK: Square3Stack3DIcon,
}

onMounted(async () => {
  if (props.summary.name) heading.value = props.summary.name
  if (props.summary.title) heading.value = props.summary.title
  avatar.value = await getAvatar(props.summary.id as string)
  if (props.showIcon) showAvatar.value = false
})
</script>
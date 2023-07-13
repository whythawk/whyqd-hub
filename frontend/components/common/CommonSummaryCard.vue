<template>
  <div class="flex w-full items-center justify-between">
    <img class="h-8 w-8 flex-shrink-0 rounded-lg" :src="avatar" :alt="heading" />
    <div class="flex-1">
      <div class="flex justify-between gap-x-4">
        <div class="py-0.5 text-sm leading-5 text-gray-500 pl-3">
          <h2 class="font-bold text-gray-900">{{ heading }}</h2>
        </div>
      </div>
    </div>
    <div v-if="showState" class="py-0.5 text-sm leading-5 text-gray-500">
      {{ props.summary.state }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { getAvatar } from "@/utilities"
import { IModelSummary } from "@/interfaces"

const props = defineProps<{
  summary: IModelSummary
  showState: boolean
}>()
const avatar = shallowRef("")
const heading = ref("")

onMounted(async () => {
  if (props.summary.title) heading.value = props.summary.title
  else heading.value = props.summary.name
  avatar.value = await getAvatar(props.summary.id as string)
})
</script>
<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <div class="relative flex h-6 w-6 flex-none items-center justify-center bg-white">
      <div class="h-1.5 w-1.5 rounded-full bg-gray-100 ring-1 ring-gray-300" />
    </div>
    <p class="flex-auto py-0.5 text-xs leading-5 text-gray-500">
      <span class="font-medium text-gray-900">{{ version.name }}</span> {{ version.description }}
    </p>
    <time v-if="version.updated" 
      :datetime="version.updated.toLocaleDateString('en-GB')" 
      class="flex-none py-0.5 text-xs leading-5 text-gray-500">
      {{ readableDate(version.updated) }}
    </time>
  </div>
</template>

<script setup lang="ts">
import { readableDate } from "@/utilities"
import type { IVersion } from "@/interfaces"

const props = defineProps<{
  version: IVersion,
  lastCard: Boolean
}>()
</script>
<template>
  <div class="relative cursor-default">
    <span v-if="truncated" class="block truncate mr-4">{{ props.term }}</span>
    <span v-else class="block mr-3">{{ props.term }}</span>
    <button @click.prevent="truncated = !truncated"
      class="transition ease-in-out delay-150 absolute inset-y-0 right-0 -mr-2 flex items-center">
      <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
    </button>
  </div>
</template>

<script setup lang="ts">
import { ChevronUpDownIcon } from "@heroicons/vue/24/outline"

const truncated = ref(true)

const props = defineProps<{
  term: String
}>()
</script>
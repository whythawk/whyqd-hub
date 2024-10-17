<template>
  <div>
    <h3 class="text-sm font-bold">Citation</h3>
    <div v-if="props.citation">
      <p class="text-xs mt-1 mx-5">
        {{ props.citation.author }}. <span class="italic">{{ props.citation.title }}</span>
        {{ props.citation.institution }}. {{ props.citation.publisher }}. {{ props.citation.month }}
        {{ props.citation.year }}.
        <span v-if="props.citation.doi">{{ props.citation.doi }}</span>
        <span v-if="!props.citation.doi && props.citation.url">{{ props.citation.url }}</span>
      </p>
      <p class="text-sm mt-1 mx-5">Licenced under: <span class="italic">{{ props.citation.licence }}</span></p>
    </div>
    <div v-else>
      <p class="text-sm mt-1 mx-5 italic">No citation provided.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ICitation } from "@/interfaces"

const props = defineProps<{
  citation?: ICitation
}>()
</script>
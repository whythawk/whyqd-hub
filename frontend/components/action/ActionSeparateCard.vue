<template>
  <div class="flex items-center">
    <img src="/img/bracket-open.svg" class="h-5 mr-1" />
    <span class="text-ochre-600 font-semibold">{{ props.action.action.split('_').join('&#x202F;') }}</span>
    <img src="/img/bracket-destination.svg" class="h-5 mx-1" />
    <span class="text-cerulean-600 font-semibold">
      <!-- @vue-ignore -->
      <CommonExpanderSlot :term="props.action.destinationField.join(', ')" class="w-40" />
    </span>
    <img src="/img/bracket-source.svg" class="h-5 mx-1" />
    <span class="text-eucalyptus-600">'{{ props.action.sourceTerm }}'</span>
    <img src="/img/bracket-divider.svg" class="h-5 mx-1" />
    <span class="text-eucalyptus-600 font-semibold">{{ props.action.sourceField }}</span>
    <img src="/img/bracket-close.svg" class="h-5 ml-1" />
  </div>
</template>

<script setup lang="ts">
import type { IActionModel } from "@/interfaces"

const props = defineProps<{
  action: IActionModel
}>()
</script>
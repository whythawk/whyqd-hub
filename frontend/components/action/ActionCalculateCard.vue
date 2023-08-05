<template>
  <div class="flex items-center">
    <img src="/img/bracket-open.svg" class="h-5 mr-1" />
    <span class="text-ochre-600 font-semibold">{{ props.action.action.split('_').join('&#x202F;') }}</span>
    <img src="/img/bracket-destination.svg" class="h-5 mx-1" />
    <span class="text-cerulean-600 font-semibold">{{ props.action.destinationField }}</span>
    <img src="/img/bracket-source.svg" class="h-5 mx-1" />
    <span class="text-eucalyptus-600 font-semibold">
      <CommonExpanderSlot :term="sourceField" class="w-40" />
    </span>
    <img src="/img/bracket-close.svg" class="h-5 ml-1" />
  </div>
</template>

<script setup lang="ts">
import { IActionModel } from "@/interfaces"

const props = defineProps<{
  action: IActionModel
}>()
const sourceField = ref("")

onMounted(async () => {
  if (props.action.sourceField && props.action.sourceField.length !== 0) {
    sourceField.value = props.action.sourceField.map((x: any) => `${x[0]} ${x[1]}`).join(', ')
  }
})
</script>
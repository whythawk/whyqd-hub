<template>
  <div class="flex items-center">
    <img src="/img/bracket-open.svg" class="h-5 mr-1" />
    <span class="text-ochre-600 font-semibold cursor-move">{{ props.action.action.split('_').join('&#x202F;') }}</span>
    <img src="/img/bracket-close.svg" class="h-5 ml-1" />
  </div>
</template>

<script setup lang="ts">
import { IActionModel, ISocketRequest } from "@/interfaces"

const props = defineProps<{
  action: IActionModel
}>()
const emit = defineEmits<{ setRequest: [request: ISocketRequest] }>()

onMounted(async () => {
  if (props.action.uuid === "") {
    const data = { ...props.action }
    const request: ISocketRequest = {
      state: "addAction",
      data
    }
    emit("setRequest", request)
  }
})
</script>
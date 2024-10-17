<template>
  <div class="flex items-center">
    <img src="/img/bracket-open.svg" class="h-5 mr-1" />
    <span class="text-ochre-600 font-semibold cursor-move">{{ props.action.action.split('_').join('&#x202F;') }}</span>
    <img src="/img/bracket-source.svg" class="h-5 mx-1" />
    <CrosswalkInputWildCard :wildTerm="props.action.rows" :is-list="true" @set-wild="watchNewRows" />
    <img src="/img/bracket-close.svg" class="h-5 ml-1" />
  </div>
</template>

<script setup lang="ts">
import type { IKeyable, IActionModel, ISocketRequest } from "@/interfaces"

const props = defineProps<{
  action: IActionModel
}>()
const emit = defineEmits<{ setRequest: [request: ISocketRequest] }>()
let newRows = [] as number[]

function watchNewRows(request: IKeyable) {
  if (request.term && request.term.length) newRows = request.term
  submitRequest()
}

function submitRequest() {
  if (
    newRows && newRows.length
    && newRows.every((t) => !isNaN(t))
  ) {
    let state = "addAction"
    if (props.action.uuid !== "") state = "updateAction"
    let data = { ...props.action }
    data.rows = newRows
    const request: ISocketRequest = {
      state: state,
      data
    }
    emit("setRequest", request)
  }
}

</script>
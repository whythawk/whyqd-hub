<template>
  <div class="flex items-center">
    <img src="/img/bracket-open.svg" class="h-5 mr-1" />
    <span class="text-ochre-600 font-semibold cursor-move">{{ props.action.action.split('_').join('&#x202F;') }}</span>
    <img src="/img/bracket-destination.svg" class="h-5 mx-1" />
    <CrosswalkSingleCombobox :current-field="selectedDestinationField" :schema="props.schemaObject" :subject="false"
      @set-selection="watchSelection" />
    <img src="/img/bracket-source.svg" class="h-5 mx-1" />
    <CrosswalkInputWildCard :wildTerm="props.action.sourceTerm" :is-list="false" @set-wild="watchSourceTerm" />
    <img src="/img/bracket-close.svg" class="h-5 ml-1" />
  </div>
</template>

<script setup lang="ts">
import { IActionModel, IKeyable, IResourceSchemaReference, ISocketRequest } from "@/interfaces"

const props = defineProps<{
  action: IActionModel
  schemaObject: IResourceSchemaReference
}>()
const emit = defineEmits<{ setRequest: [request: ISocketRequest] }>()
const selectedDestinationField = ref("")
const newSourceTerm = ref("")

function watchSourceTerm(request: IKeyable) {
  newSourceTerm.value = request.term
  submitRequest()
}
watch(() => [selectedDestinationField.value], () => {
  submitRequest()
})

function watchSelection(selection: IKeyable) {
  if (selection && Object.keys(selection).length && !selection.subject) {
    selectedDestinationField.value = selection.choice
  }
}

function submitRequest() {
  if (
    selectedDestinationField.value
    && newSourceTerm.value
    && (
      newSourceTerm.value !== props.action.sourceTerm
      || selectedDestinationField.value !== props.action.destinationField
    )
  ) {
    let state = "addAction"
    if (props.action.uuid !== "") state = "updateAction"
    let data = { ...props.action }
    data.destinationField = selectedDestinationField.value
    data.sourceTerm = newSourceTerm.value
    const request: ISocketRequest = {
      state: state,
      data
    }
    emit("setRequest", request)
  }
}

onMounted(async () => {
  if (props.action.uuid !== "") {
    selectedDestinationField.value = props.action.destinationField as string
    newSourceTerm.value = props.action.sourceTerm as string
  }
})
</script>
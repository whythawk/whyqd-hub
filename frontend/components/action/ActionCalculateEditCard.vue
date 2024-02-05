<template>
  <div class="flex items-center">
    <img src="/img/bracket-open.svg" class="h-5 mr-1" />
    <span class="text-ochre-600 font-semibold cursor-move">{{ props.action.action.split('_').join('&#x202F;') }}</span>
    <img src="/img/bracket-destination.svg" class="h-5 mx-1" />
    <CrosswalkSingleCombobox :current-field="selectedDestinationField" :schema="props.schemaObject" :subject="false"
      @set-selection="watchDestinationSelection" />
    <img src="/img/bracket-source.svg" class="h-5 mx-1" />
    <CrosswalkCombinationPopover :action="props.action" :schema-subject="props.schemaSubject" :is-select="false"
      @set-selection="watchSourceSelection" />
    <img src="/img/bracket-close.svg" class="h-5 ml-1" />
  </div>
</template>

<script setup lang="ts">
import { IActionModel, IActionModifierType, IKeyable, IResourceSchemaReference, ISocketRequest } from "@/interfaces"

const props = defineProps<{
  action: IActionModel
  schemaSubject: IResourceSchemaReference,
  schemaObject: IResourceSchemaReference
}>()
const emit = defineEmits<{ setRequest: [request: ISocketRequest] }>()
const selectedDestinationField = ref("")
const selectedSourceField = ref<[IActionModifierType, string][]>([])

function watchDestinationSelection(selection: IKeyable) {
  if (selection && Object.keys(selection).length) {
    selectedDestinationField.value = selection.choice
    submitRequest()
  }
}
function watchSourceSelection(selection: IKeyable) {
  if (selection && Object.keys(selection).length) {
    selectedSourceField.value = selection.choice
    submitRequest()
  }
}

function submitRequest() {
  if (
    selectedDestinationField.value !== props.action.destinationField
    && selectedSourceField.value.length
  ) {
    let state = "addAction"
    if (props.action.uuid !== "") state = "updateAction"
    let data = { ...props.action }
    data.destinationField = selectedDestinationField.value
    data.sourceField = [...selectedSourceField.value]
    const request: ISocketRequest = {
      state: state,
      data
    }
    emit("setRequest", request)
  }
}

onMounted(async () => {
  if (props.action.uuid !== "") {
    if (props.action.destinationField) selectedDestinationField.value = props.action.destinationField as string
  }
})
</script>
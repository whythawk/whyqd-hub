<template>
  <div class="flex items-center">
    <img src="/img/bracket-open.svg" class="h-5 mr-1" />
    <span class="text-ochre-600 font-semibold cursor-move">{{ props.action.action.split('_').join('&#x202F;') }}</span>
    <img src="/img/bracket-destination.svg" class="h-5 mx-1" />
    <CrosswalkSingleCombobox :current-field="selectedDestinationNameField" :schema="props.schemaObject" :subject="false"
      @set-selection="watchSelectionName" />
    <img src="/img/bracket-divider.svg" class="h-5 mx-1" />
    <CrosswalkSingleCombobox :current-field="selectedDestinationValueField" :schema="props.schemaObject" :subject="false"
      @set-selection="watchSelectionValue" />
    <img src="/img/bracket-source.svg" class="h-5 mx-1" />
    <CrosswalkMultiCombobox :current-fields="selectedSourceField" :schema="props.schemaSubject" :subject="true"
      @set-selection="watchSelection" />
    <img src="/img/bracket-close.svg" class="h-5 ml-1" />
  </div>
</template>

<script setup lang="ts">
import type { IActionModel, IKeyable, IResourceSchemaReference, ISocketRequest } from "@/interfaces"

const props = defineProps<{
  action: IActionModel
  schemaSubject: IResourceSchemaReference,
  schemaObject: IResourceSchemaReference
}>()
const emit = defineEmits<{ setRequest: [request: ISocketRequest] }>()
const selectedDestinationNameField = ref("")
const selectedDestinationValueField = ref("")
const selectedDestinationField = ref<string[]>([])
const selectedSourceField = ref<string[]>([])

watch(() => [selectedDestinationNameField.value, selectedDestinationValueField.value, selectedSourceField.value], () => {
  submitRequest()
})

function watchSelectionName(selection: IKeyable) {
  if (selection && Object.keys(selection).length) {
    selectedDestinationNameField.value = selection.choice
  }
}
function watchSelectionValue(selection: IKeyable) {
  if (selection && Object.keys(selection).length) {
    selectedDestinationValueField.value = selection.choice
  }
}
function watchSelection(selection: IKeyable) {
  if (selection && Object.keys(selection).length) {
    if (selection.subject) selectedSourceField.value = selection.choice
    else selectedDestinationField.value = selection.choice
  }
}

function submitRequest() {
  if (
    selectedDestinationNameField.value
    && selectedDestinationValueField.value
    && selectedSourceField.value.length
    && selectedSourceField.value !== props.action.sourceField
  ) {
    let state = "addAction"
    if (props.action.uuid !== "") state = "updateAction"
    let data = { ...props.action }
    data.destinationField = [selectedDestinationNameField.value, selectedDestinationValueField.value]
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
    if (props.action.destinationField && props.action.destinationField.length === 2) {
      selectedDestinationNameField.value = props.action.destinationField[0]
      selectedDestinationValueField.value = props.action.destinationField[1]
    }
    selectedSourceField.value = props.action.sourceField as string[]
  }
})
</script>
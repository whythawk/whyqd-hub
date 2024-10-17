<template>
  <div>
    <div class="flex items-center">
      <img src="/img/bracket-open.svg" class="h-5 mr-1" />
      <span class="text-ochre-600 font-semibold cursor-move">{{ props.action.action.split('_').join('&#x202F;') }}</span>
      <img src="/img/bracket-destination.svg" class="h-5 mx-1" />
      <CrosswalkSingleCombobox :current-field="selectedDestinationField" :schema="props.schemaObject" :subject="false"
        @set-selection="watchSelection" />
      <img src="/img/bracket-source.svg" class="h-5 mx-1" />
      <CrosswalkMultiCombobox :current-fields="selectedSourceField" :schema="props.schemaSubject" :subject="true"
        @set-selection="watchSelection" />
      <img src="/img/bracket-close.svg" class="h-5 ml-1" />
    </div>
    <div>
      <div class="mx-auto py-1 flex items-center">
        <h3 class="text-sm text-eucalyptus-600 font-semibold">
          Source order
        </h3>
        <div aria-hidden="true" class="h-5 w-px bg-gray-300 ml-4" />
        <CrosswalkMultiOrderbox :current-fields="selectedSourceField" @set-selection="watchOrderSelection" />
      </div>
    </div>
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
const selectedDestinationField = ref("")
const selectedSourceField = ref<string[]>([])

watch(() => [selectedDestinationField.value, selectedSourceField.value], () => {
  submitRequest()
})

function watchSelection(selection: IKeyable) {
  if (selection && Object.keys(selection).length) {
    if (selection.subject) selectedSourceField.value = selection.choice
    else selectedDestinationField.value = selection.choice
  }
}

function watchOrderSelection(selection: string[]) {
  selectedSourceField.value = selection
}

function submitRequest() {
  if (
    selectedDestinationField.value
    && selectedSourceField.value.length
    && (selectedDestinationField.value !== props.action.destinationField
      || selectedSourceField.value !== props.action.sourceField)
  ) {
    let state = "addAction"
    if (props.action.uuid !== "") state = "updateAction"
    let data = { ...props.action }
    data.destinationField = selectedDestinationField.value
    data.sourceField = selectedSourceField.value
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
    selectedSourceField.value = props.action.sourceField as string[]
  }
})
</script>
<template>
  <div>
    <div class="flex items-center">
      <img src="/img/bracket-open.svg" class="h-5 mr-1" />
      <span class="text-ochre-600 font-semibold cursor-move">{{ props.action.action.split('_').join('&#x202F;') }}</span>
      <img src="/img/bracket-destination.svg" class="h-5 mx-1" />
      <CrosswalkMultiCombobox :current-fields="selectedDestinationField" :schema="props.schemaObject" :subject="false"
        @set-selection="watchSelection" />
      <img src="/img/bracket-source.svg" class="h-5 mx-1" />
      <CrosswalkInputWildCard :wildTerm="props.action.sourceTerm" :is-list="false" excluded="::" @set-wild="watchByTerm" />
      <img src="/img/bracket-divider.svg" class="h-5 mx-1" />
      <CrosswalkSingleCombobox :current-field="selectedSourceField" :schema="props.schemaSubject" :subject="true"
        @set-selection="watchSelection" />
      <img src="/img/bracket-close.svg" class="h-5 ml-1" />
    </div>
    <div>
      <div class="mx-auto py-1 flex items-center">
        <h3 class="text-sm text-eucalyptus-600 font-semibold">
          Destination order
        </h3>
        <div aria-hidden="true" class="h-5 w-px bg-gray-300 ml-4" />
        <CrosswalkMultiOrderbox :current-fields="selectedDestinationField" @set-selection="watchOrderSelection" />
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
const selectedDestinationField = ref<string[]>([])
const selectedSourceField = ref("")
const byTerm = ref("")
const excluded = "::"

function watchByTerm(request: IKeyable) {
  if (request.term !== excluded) byTerm.value = request.term
}

watch(() => [selectedDestinationField.value, selectedSourceField.value, byTerm.value], () => {
  submitRequest()
})

function watchSelection(selection: IKeyable) {
  if (selection && Object.keys(selection).length) {
    if (selection.subject) selectedSourceField.value = selection.choice
    else selectedDestinationField.value = selection.choice
  }
}

function watchOrderSelection(selection: string[]) {
  selectedDestinationField.value = selection
}

function submitRequest() {
  if (
    selectedSourceField.value
    && selectedDestinationField.value.length
    && byTerm.value !== excluded
  ) {
    let state = "addAction"
    if (props.action.uuid !== "") state = "updateAction"
    let data = { ...props.action }
    data.destinationField = selectedDestinationField.value
    data.sourceField = selectedSourceField.value
    data.sourceTerm = byTerm.value
    const request: ISocketRequest = {
      state: state,
      data
    }
    emit("setRequest", request)
  }
}

onMounted(async () => {
  if (props.action.uuid !== "") {
    selectedDestinationField.value = props.action.destinationField as string[]
    selectedSourceField.value = props.action.sourceField as string
    byTerm.value = props.action.sourceTerm ? props.action.sourceTerm as string : ""
  }
})
</script>
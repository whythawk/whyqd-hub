<template>
  <div class="flex items-center">
    <img src="/img/bracket-open.svg" class="h-5 mr-1" />
    <span class="text-ochre-600 font-semibold">{{ props.action.action.split('_').join('&#x202F;') }}</span>
    <img src="/img/bracket-destination.svg" class="h-5 mx-1" />
    <CrosswalkSingleCombobox :current-field="selectedDestinationField" :schema="props.schemaObject" :subject="false"
      @set-selection="watchSelection" />
    <img src="/img/bracket-divider.svg" class="h-5 mx-1" />
    <CrosswalkCategorySingleCombobox id="category-object-selection" :current-term="selectedDestinationTerm"
      :terms="getSelectedDestinationTerms()" :subject="false" @set-selection="watchSelectionTerm" />
    <img src="/img/bracket-source.svg" class="h-5 mx-1" />
    <CrosswalkSingleCombobox :current-field="selectedSourceField" :schema="props.schemaSubject" :subject="true"
      @set-selection="watchSelection" />
    <img src="/img/bracket-divider.svg" class="h-5 mx-1" />
    <CrosswalkCategoryMultiCombobox id="category-subject-selection" :current-terms="selectedSourceTerms"
      :terms="getSelectedSourceTerms()" :subject="true" @set-selection="watchSelectionTerm" />
    <img src="/img/bracket-close.svg" class="h-5 ml-1" />
  </div>
</template>

<script setup lang="ts">
import { IActionModel, IKeyable, IResourceSchemaReference, ISocketRequest } from "@/interfaces"

const props = defineProps<{
  action: IActionModel
  schemaSubject: IResourceSchemaReference,
  schemaObject: IResourceSchemaReference
}>()
const emit = defineEmits<{ setRequest: [request: ISocketRequest] }>()
const selectedDestinationField = ref("")
const selectedDestinationTerm = ref("")
const selectedSourceTerms = ref<string[]>([])
const selectedSourceField = ref("")

watch(() => [selectedDestinationField.value, selectedSourceField.value, selectedDestinationTerm.value, selectedSourceTerms.value], () => {
  submitRequest()
})

function getSelectedDestinationTerms() {
  let availableTerms
  if (selectedDestinationField.value) {
    availableTerms = props.schemaObject.fields?.find((field) => field.name === selectedDestinationField.value
      && field.constraints && field.constraints.enum && field.constraints.enum.length)
  }
  if (availableTerms && availableTerms.constraints) return availableTerms.constraints.enum as IKeyable[]
  else return [] as IKeyable[]
}
function getSelectedSourceTerms() {
  let availableTerms
  if (selectedSourceField.value) {
    availableTerms = props.schemaSubject.fields?.find((field) => field.name === selectedSourceField.value
      && field.constraints && field.constraints.enum && field.constraints.enum.length)
  }
  if (availableTerms && availableTerms.constraints) return availableTerms.constraints.enum as IKeyable[]
  else return [] as IKeyable[]
}

function watchSelection(selection: IKeyable) {
  if (selection && Object.keys(selection).length) {
    if (selection.subject) selectedSourceField.value = selection.choice
    else selectedDestinationField.value = selection.choice
  }
}
function watchSelectionTerm(selection: IKeyable) {
  if (selection && Object.keys(selection).length) {
    if (selection.subject) selectedSourceTerms.value = [...selection.choice]
    else selectedDestinationTerm.value = selection.choice
  }
}

function submitRequest() {
  let state = "addAction"
  if (props.action.uuid !== "") state = "updateAction"
  let data = { ...props.action }
  data.destinationField = selectedDestinationField.value
  data.sourceField = [selectedSourceField.value]
  data.destinationTerm = selectedDestinationTerm.value
  data.sourceTerm = selectedSourceTerms.value
  const request: ISocketRequest = {
    state: state,
    data
  }
  emit("setRequest", request)
}


onMounted(async () => {
  if (props.action.uuid !== "") {
    selectedDestinationField.value = props.action.destinationField as string
    selectedDestinationTerm.value = props.action.destinationTerm as string
    selectedSourceField.value = props.action.sourceField as string
    selectedSourceTerms.value = props.action.sourceTerm as string[]
  }
})
</script>
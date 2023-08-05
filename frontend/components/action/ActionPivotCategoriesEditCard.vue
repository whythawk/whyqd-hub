<template>
  <div class="flex items-center">
    <img src="/img/bracket-open.svg" class="h-5 mr-1" />
    <span class="text-ochre-600 font-semibold cursor-move">{{ props.action.action.split('_').join('&#x202F;') }}</span>
    <img src="/img/bracket-destination.svg" class="h-5 mx-1" />
    <CrosswalkSingleCombobox :current-field="selectedDestinationField" :schema="props.schemaObject" :subject="false"
      @set-selection="watchSelection" />
    <img src="/img/bracket-source.svg" class="h-5 mx-1" />
    <CrosswalkSingleCombobox :current-field="selectedSourceField" :schema="props.schemaSubject" :subject="true"
      @set-selection="watchSelection" />
    <img src="/img/bracket-divider.svg" class="h-5 mx-1" />
    <CrosswalkInputWildCard :wildTerm="props.action.rows" :is-list="true" @set-wild="watchNewRows" />
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
const selectedDestinationField = ref("Select ...")
const selectedSourceField = ref("Select ...")
let newRows = [] as number[]

function watchNewRows(request: IKeyable) {
  if (request.term && request.term.length) newRows = request.term
  submitRequest()
}
watch(() => [selectedDestinationField.value, selectedSourceField.value], () => {
  submitRequest()
})

function watchSelection(selection: IKeyable) {
  if (selection && Object.keys(selection).length) {
    if (selection.subject) selectedSourceField.value = selection.choice
    else selectedDestinationField.value = selection.choice
  }
}

function submitRequest() {
  if (
    newRows && newRows.length
    && newRows.every((t) => !isNaN(t))
    && (selectedDestinationField.value !== "Select ..."
      && selectedSourceField.value !== "Select ...")
    && (selectedDestinationField.value !== props.action.destinationField
      || selectedSourceField.value !== props.action.sourceField
      || newRows.sort().join(",") !== props.action.rows!.sort().join(",")
    )
  ) {
    let state = "addAction"
    if (props.action.uuid !== "") state = "updateAction"
    let data = { ...props.action }
    data.destinationField = selectedDestinationField.value
    data.sourceField = selectedSourceField.value
    data.rows = newRows
    const request: ISocketRequest = {
      state: state,
      data
    }
    emit("setRequest", request)
  }
}

onMounted(async () => {
  console.log("pivot", props.action.sourceField)
  if (props.action.uuid !== "") {
    selectedDestinationField.value = props.action.destinationField as string
    selectedSourceField.value = props.action.sourceField as string
  }
})
</script>
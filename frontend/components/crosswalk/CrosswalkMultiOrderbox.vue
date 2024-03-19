<template>
    <div class="ml-4 mt-0">
      <div class="-m-1 flex flex-wrap items-center">
        <span v-for="selectedField in selectedFields" 
          :key="selectedField.key" :id="selectedField.key" :draggable="true"
          @dragstart="handleDragStart" @dragenter="handleDragEnter" @dragover="handleDragOver"
          @dragleave="handleDragLeave" @drop="handleDrop" @dragend="handleDragEnd"
          class="m-1 inline-flex items-center rounded-full border border-gray-200 bg-white py-1.5 pl-3 pr-2 text-sm font-medium text-gray-900 cursor-move">
          <button type="button" @click.prevent="duplicateOrderSelection(selectedField.key)"
            class="mr-1 inline-flex flex-shrink-0 rounded-full text-gray-400 hover:bg-gray-200 hover:text-gray-600">
            <span class="sr-only">Duplicate term for {{ selectedField.id }}</span>
            <PlusIcon class="h-4 w-4" aria-hidden="true" />
          </button>
          <span>{{ selectedField.value }}</span>
          <button type="button" @click.prevent="removeOrderSelection(selectedField.key)"
            class="ml-1 inline-flex flex-shrink-0 rounded-full text-gray-400 hover:bg-gray-200 hover:text-gray-600">
            <span class="sr-only">Remove term for {{ selectedField.value }}</span>
            <XMarkIcon class="h-4 w-4" aria-hidden="true" />
          </button>
        </span>
      </div>
    </div>
</template>

<script setup lang="ts">
import { PlusIcon, XMarkIcon } from "@heroicons/vue/24/outline"
import { IKeyable } from "@/interfaces"

const props = defineProps<{
  currentFields: String[],
}>()
const emit = defineEmits<{ setSelection: [selection: string[]] }>()
const selectedFields = ref<IKeyable[]>([])
const dragID = ref("" as string)
const draggedFields = ref<IKeyable[]>([])

watch(() => props.currentFields, () => {
  resetSelectedFields()
})

function duplicateOrderSelection(key: string) {
  let idx = selectedFields.value.findIndex(selected => selected.key === key)
  if (idx !== -1) {
    let value = selectedFields.value[idx].value
    selectedFields.value.splice(
      idx + 1,
      0,
      { key: "id" + Math.random().toString(16).slice(4), value }
    )
    emitSelectedFields()
  }
}

function removeOrderSelection(key: string) {
  selectedFields.value = selectedFields.value.filter((selected) => selected.key !== key)
  emitSelectedFields()
}

function emitSelectedFields() {
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map
  emit("setSelection", selectedFields.value.map((x) => x.value))
}

function resetSelectedFields() {
  // NOTE: currently only does this for the '~' modifier, but can be extended
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map
  // https://stackoverflow.com/a/19842865
  // const modifiers: String[] = ["~"]
  selectedFields.value = []
  if (props.currentFields && props.currentFields.length)
    selectedFields.value = props.currentFields.map((x) => (
      { key: "id" + Math.random().toString(16).slice(4), value: x })
    )
}

onMounted(async () => {
  resetSelectedFields()
})

// DRAG N DROP
// https://web.dev/drag-and-drop/
function handleDragStart(e: any) {
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-white",
    "bg-cerulean-100"
  )
  if (e.currentTarget.id) {
    dragID.value = e.currentTarget.id
    e.dataTransfer.effectAllowed = "move"
    e.dataTransfer.setData("id", dragID.value)
  }
}

function handleDragEnter(e: any) {
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-white",
    "bg-cerulean-100"
  )
}

function handleDragOver(e: any) {
  if (e.preventDefault) {
    e.preventDefault() // Necessary. Allows us to drop.
  }
  if (e.target.id !== e.currentTarget.id) return false
  e.dataTransfer.dropEffect = "move"
  return false
}

function handleDragLeave(e: any) {
  e.stopPropagation()
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "bg-white"
  )
}

function handleDrop(e: any) {
  e.stopPropagation()
  e.preventDefault()
  const dropID = e.currentTarget.id
  if (dragID.value !== dropID) {
    draggedFields.value = [...selectedFields.value]
    const frIdx = draggedFields.value.findIndex(
      (field) => field.key === dragID.value
    )
    const toIdx = draggedFields.value.findIndex(
      (field) => field.key === dropID
    )
    // Because TypeScript, in its infinite wisdom, has no concept of `-1`
    const dragged = { ...draggedFields.value.slice(frIdx)[0] }
    draggedFields.value.splice(frIdx, 1)
    draggedFields.value.splice(toIdx, 0, dragged)
    selectedFields.value = [...draggedFields.value]
    emitSelectedFields()
  }
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "bg-white"
  )
  return false
}

function handleDragEnd(e: any) {
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "bg-white"
  )
}
</script>
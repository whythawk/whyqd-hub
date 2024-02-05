<template>
    <div class="ml-4 mt-0">
      <div class="-m-1 flex flex-wrap items-center">
        <span v-for="selectedField in selectedFields" 
          :key="selectedField" :id="selectedField" :draggable="true"
          @dragstart="handleDragStart" @dragenter="handleDragEnter" @dragover="handleDragOver"
          @dragleave="handleDragLeave" @drop="handleDrop" @dragend="handleDragEnd"
          class="m-1 inline-flex items-center rounded-full border border-gray-200 bg-white py-1.5 pl-3 pr-2 text-sm font-medium text-gray-900 cursor-move">
          <span>{{ selectedField }}</span>
          <button type="button" @click.prevent="removeOrderSelection(selectedField)"
            class="ml-1 inline-flex h-4 w-4 flex-shrink-0 rounded-full p-1 text-gray-400 hover:bg-gray-200 hover:text-gray-500">
            <span class="sr-only">Remove filter for {{ selectedField }}</span>
            <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
              <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
            </svg>
          </button>
        </span>
      </div>
    </div>
</template>

<script setup lang="ts">

const props = defineProps<{
  currentFields: String[],
}>()
const emit = defineEmits<{ setSelection: [selection: string[]] }>()
const selectedFields = ref<string[]>([])
const dragID = ref("" as string)
const draggedFields = ref<string[]>([])

watch(() => props.currentFields, () => {
  if (props.currentFields && props.currentFields.length) selectedFields.value = props.currentFields as string[]
  else selectedFields.value = []
})

watch(() => selectedFields.value, () => {
  if (selectedFields.value.length || props.currentFields.length) {
    emit("setSelection", selectedFields.value)
  }
})

function removeOrderSelection(item: string) {
  selectedFields.value = selectedFields.value.filter((selected) => selected !== item)
}

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
      (field) => field === dragID.value
    )
    const toIdx = draggedFields.value.findIndex(
      (field) => field === dropID
    )
    // Because TypeScript, in its infinite wisdom, has no concept of `-1`
    const dragged = draggedFields.value.slice(frIdx)[0]
    draggedFields.value.splice(frIdx, 1)
    draggedFields.value.splice(toIdx, 0, dragged)
    selectedFields.value = [...draggedFields.value]
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

onMounted(async () => {
  if (props.currentFields && props.currentFields.length) selectedFields.value = props.currentFields as string[]
})
</script>
<template>
  <div @click.prevent="fileClickHandler" @dragover="handleDragOver" @drop="handleDrop"
    class="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10">
    <div class="text-center">
      <!-- @vue-ignore -->
      <component :is="importer[props.reference].icon" class="mx-auto h-12 w-12 text-gray-300" aria-hidden="true" />
      <div class="mt-4 flex text-sm leading-6 text-gray-600">
        <label for="file-upload"
          class="relative cursor-pointer rounded-md bg-white font-semibold text-ochre-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-ochre-600 focus-within:ring-offset-2 hover:text-ochre-500">
          <span>Upload <span v-if="props.reference !== 'DATA'">a</span> {{ props.reference.toLowerCase() }}</span>
          <input id="file-upload" name="file-upload" type="file" class="sr-only" />
        </label>
        <p v-if="dragndrop" class="pl-1">or drag and drop</p>
      </div>
      <p v-if="props.reference === 'DATA'" class="text-xs leading-5 text-gray-600">
        CSV, XLS/X, PARQUET or FEATHER file
      </p>
      <p v-else class="text-xs leading-5 text-gray-600">JSON or {{ props.reference }} file</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { fileOpen } from "browser-fs-access"
import { ArrowsRightLeftIcon, CubeIcon, Squares2X2Icon, TableCellsIcon, } from "@heroicons/vue/24/outline"
import { useToastStore } from "@/stores"
import type { IKeyable } from "@/interfaces"

const toast = useToastStore()
const importer: IKeyable = {
  DATA: {
    icon: TableCellsIcon,
    mimeTypes: [
      "text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "application/vnd.apache.parquet", "application/vnd.apache.feather"
    ],
    extensions: [".csv", ".xls", ".xlsx", ".parquet", ".prq", ".feather", ".ftr"],
    multiple: true
  },
  SCHEMA: {
    icon: Squares2X2Icon,
    mimeTypes: ["application/json"],
    extensions: [".json", ".schema"],
    multiple: false
  },
  CROSSWALK: {
    icon: ArrowsRightLeftIcon,
    mimeTypes: ["application/json"],
    extensions: [".json", ".crosswalk"],
    multiple: false
  },
  TRANSFORM: {
    icon: CubeIcon,
    mimeTypes: ["application/json"],
    extensions: [".json", ".transform"],
    multiple: false
  },
}
const dragndrop = ref(false)
const props = defineProps<{
  reference: string
}>()
const emit = defineEmits<{ setImport: [response: any] }>()

onMounted(async () => {
  dragndrop.value = determineDragAndDropCapable()
})

// UTILITIES
async function fileClickHandler() {
  try {
    let response: any[] | any = await fileOpen({
      mimeTypes: importer[props.reference].mimeTypes,
      extensions: importer[props.reference].extensions,
      multiple: importer[props.reference].multiple,
    })
    if (props.reference !== "DATA") response = await getJSONfromBlob(response)
    emit("setImport", response)
  } catch (error: any) {
    if (error.name !== "AbortError") {
      toast.addNotice({
        title: "Import error",
        content: `Error: ${error}`,
        icon: "error"
      })
    }
  }
}

async function handleDrop(event: DragEvent) {
  event.stopPropagation()
  event.preventDefault()
  try {
    if (event.dataTransfer && event.dataTransfer.files.length) {
      let response: any[] = []
      for (const blob of Array.from(event.dataTransfer.files)) {
        if (!importer[props.reference].mimeTypes.includes(blob.type))
          throw new Error("Not an allowed mimetype.")
        if (props.reference !== "DATA") {
          const altblob = await getJSONfromBlob(blob)
          response.push(altblob)
        }
      }
      if (props.reference !== "DATA") emit("setImport", response)
      else emit("setImport", event.dataTransfer.files)
    }
  } catch (error: any) {
    if (error.name !== "AbortError") {
      toast.addNotice({
        title: "Import error",
        content: `Error: ${error}`,
        icon: "error"
      })
    }
  }
}

function handleDragOver(event: DragEvent) {
  event.preventDefault()
}

async function getJSONfromBlob(payload: any): Promise<any> {
  let response = await payload.text()
  return JSON.parse(response)
}

function determineDragAndDropCapable() {
  // Complete guide to drag and drop files
  // https://serversideup.net/drag-and-drop-file-uploads-with-vuejs-and-axios/
  const div = document.createElement("div")
  return (
    ("draggable" in div || ("ondragstart" in div && "ondrop" in div)) &&
    "FormData" in window &&
    "FileReader" in window
  )
}
</script>
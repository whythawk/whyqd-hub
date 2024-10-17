<template>
  <div class="flex-auto rounded-lg py-2 px-3 ring-1 ring-inset ring-gray-200 text-xs bg-gray-50/75">
    <h3 class="flex border-b border-gray-200 text-xs items-center py-2 px-1 font-medium">
      <CursorArrowRippleIcon class="-ml-0.5 h-5 w-5 text-gray-400" aria-hidden="true" />
      <span class="mx-1 text-gray-500">Actions</span>
    </h3>
    <ul class="flex flex-row md:flex-col flex-wrap mt-2">
      <li v-for="axn in actionCore" :key="`action-template-${axn}`" :id="axn" draggable="true"
        class="relative min-w-full p-2 hover:bg-gray-100 hover:rounded-md cursor-move" @dragstart="handleAddDragStart"
        @dragenter="handleAddDragEnter" @dragover="handleAddDragOver" @dragleave="handleAddDragLeave"
        @drop="handleAddDrop" @dragend="handleAddDragEnd">
        <div class="flex flex-row max-w-full items-center">
          <img src="/img/bracket-open.svg" class="h-5 mr-1" />
          <span class="text-ochre-600 font-semibold">{{ axn.split('_').join('&#x202F;') }}</span>
          <img src="/img/bracket-close.svg" class="h-5 ml-1" />
        </div>
      </li>
    </ul>
    <div class="col-span-full align-bottom">
      <div class="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 bg-gray-100 p-6"
        @dragstart="handleRemoveDragStart" @dragenter="handleRemoveDragEnter" @dragover="handleRemoveDragOver"
        @dragleave="handleRemoveDragLeave" @drop="handleRemoveDrop" @dragend="handleRemoveDragEnd">
        <div class="text-center">
          <TrashIcon class="mx-auto h-6 w-6 text-ochre-300" aria-hidden="true" />
          <div class="mt-4 flex text-sm leading-6 text-gray-600">
            <div class="relative rounded-md font-semibold text-ochre-600">
              Drag here to remove
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CursorArrowRippleIcon, TrashIcon } from "@heroicons/vue/24/outline"
import type { ISocketRequest } from "@/interfaces"

const actionCore = [
  "CALCULATE",
  "CATEGORISE",
  "COLLATE",
  "DEBLANK",
  "DEDUPE",
  "DELETE_ROWS",
  "NEW",
  "PIVOT_CATEGORIES",
  "PIVOT_LONGER",
  "RENAME",
  "SELECT",
  "SELECT_NEWEST",
  "SELECT_OLDEST",
  "SEPARATE",
  "UNITE",
]
const emit = defineEmits<{ setRequest: [request: ISocketRequest] }>()

// DRAG N DROP - ADD
function handleAddDragStart(e: any) {
  e.currentTarget.className = e.currentTarget.className.replace(
    "hover:bg-gray-100",
    "bg-cerulean-100"
  )
  e.dataTransfer.effectAllowed = "move"
  e.dataTransfer.setData("id", "ADD_ACTION")
  e.dataTransfer.setData("addAction", e.currentTarget.id)
}

function handleAddDragEnter(e: any) {
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "hover:bg-gray-100",
    "bg-cerulean-100"
  )
}

function handleAddDragOver(e: any) {
  if (e.preventDefault) {
    e.preventDefault() // Necessary. Allows us to drop.
  }
  e.dataTransfer.dropEffect = "move"
  e.currentTarget.className = e.currentTarget.className.replace(
    "hover:bg-gray-100",
    "bg-cerulean-100"
  )
}

function handleAddDragLeave(e: any) {
  e.stopPropagation()
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "hover:bg-gray-100"
  )
}

function handleAddDrop(e: any) {
  e.stopPropagation()
  e.preventDefault()
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "hover:bg-gray-100"
  )
}

function handleAddDragEnd(e: any) {
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "hover:bg-gray-100"
  )
}

// DRAG N DROP - REMOVE
// https://web.dev/drag-and-drop/
function handleRemoveDragStart(e: any) {
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-gray-100",
    "bg-cerulean-100"
  )
  e.dataTransfer.effectAllowed = "move"
}

function handleRemoveDragEnter(e: any) {
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-gray-100",
    "bg-cerulean-100"
  )
}

function handleRemoveDragOver(e: any) {
  if (e.preventDefault) {
    e.preventDefault() // Necessary. Allows us to drop.
  }
  e.dataTransfer.dropEffect = "move"
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-gray-100",
    "bg-cerulean-100"
  )
}

function handleRemoveDragLeave(e: any) {
  e.stopPropagation()
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "bg-gray-100"
  )
}

function handleRemoveDrop(e: any) {
  e.stopPropagation()
  e.preventDefault()
  const dropID = e.dataTransfer.getData("id")
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "bg-gray-100"
  )
  if (dropID) {
    const request: ISocketRequest = {
      state: "removeAction",
      data: {
        name: dropID
      }
    }
    emit("setRequest", request)
  }
}

function handleRemoveDragEnd(e: any) {
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "bg-gray-100"
  )
}
</script>
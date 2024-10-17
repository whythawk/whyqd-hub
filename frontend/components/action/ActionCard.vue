<template>
  <div class="relative flex hover:bg-gray-100 hover:rounded-md">
    <!-- <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <div class="relative flex h-6 w-6 flex-none items-center justify-center rounded-full">
      <div class="h-1.5 w-1.5 mt-4 rounded-full bg-gray-100 ring-1 ring-gray-300" />
    </div> -->
    <div class="text-sm text-gray-500 p-2 flex items-center gap-x-2">
      <div :class="[props.canEdit ? 'cursor-move' : 'cursor-default']">
        <ActionCalculateCard v-if="props.action.action === 'CALCULATE'" :action="props.action" />
        <ActionCategoriseCard v-if="props.action.action === 'CATEGORISE'" :action="props.action" />
        <ActionCollateCard v-if="props.action.action === 'COLLATE'" :action="props.action" />
        <ActionDeblankCard v-if="props.action.action === 'DEBLANK'" :action="props.action" />
        <ActionDedupeCard v-if="props.action.action === 'DEDUPE'" :action="props.action" />
        <ActionDeleteRowsCard v-if="props.action.action === 'DELETE_ROWS'" :action="props.action" />
        <ActionNewCard v-if="props.action.action === 'NEW'" :action="props.action" />
        <ActionPivotCategoriesCard v-if="props.action.action === 'PIVOT_CATEGORIES'" :action="props.action" />
        <ActionPivotLongerCard v-if="props.action.action === 'PIVOT_LONGER'" :action="props.action" />
        <ActionRenameCard v-if="props.action.action === 'RENAME'" :action="props.action" />
        <ActionSelectCard v-if="props.action.action === 'SELECT'" :action="props.action" />
        <ActionSelectNewestCard v-if="props.action.action === 'SELECT_NEWEST'" :action="props.action" />
        <ActionSelectOldestCard v-if="props.action.action === 'SELECT_OLDEST'" :action="props.action" />
        <ActionSeparateCard v-if="props.action.action === 'SEPARATE'" :action="props.action" />
        <ActionUniteCard v-if="props.action.action === 'UNITE'" :action="props.action" />
      </div>
      <button
        v-if="props.canEdit"
        @click.prevent="editAction(props.action.uuid as string)"
        class="mx-1 text-cerulean-600 group flex font-semibold items-center justify-center absolute right-0 rounded-full bg-white">
        <PlusCircleIcon class="rounded-full hover:bg-cerulean-100 h-6 w-6 shrink-0" aria-hidden="true" />
        <span class="sr-only">Edit</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PlusCircleIcon } from "@heroicons/vue/24/outline"
import type { IActionModel } from "@/interfaces"

const props = defineProps<{
  action: IActionModel,
  lastCard?: boolean
  canEdit?: boolean
}>()
const emit = defineEmits<{ editRequest: [request: string] }>()

async function editAction(id: string) {
  emit("editRequest", id)
}
</script>
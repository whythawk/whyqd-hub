<template>
  <div class="relative flex">
    <div class="text-sm text-gray-500 my-1 min-w-full hover:bg-gray-100 hover:rounded-lg rounded-lg border border-dashed border-gray-900/25 p-2">
      <div>
        <ActionCalculateEditCard v-if="props.edit.action === 'CALCULATE'" :action="props.edit"
          :schema-subject="schemaSubject" :schema-object="schemaObject" @set-request="watchRequestSocket" />
        <ActionCategoriseEditCard v-if="props.edit.action === 'CATEGORISE'" :action="props.edit"
          :schema-subject="schemaSubject" :schema-object="schemaObject" @set-request="watchRequestSocket" />
        <ActionCollateEditCard v-if="props.edit.action === 'COLLATE'" :action="props.edit" :schema-subject="schemaSubject"
          :schema-object="schemaObject" @set-request="watchRequestSocket" />
        <ActionDeblankEditCard v-if="props.edit.action === 'DEBLANK'" :action="props.edit"
          @set-request="watchRequestSocket" />
        <ActionDedupeEditCard v-if="props.edit.action === 'DEDUPE'" :action="props.edit"
          @set-request="watchRequestSocket" />
        <ActionDeleteRowsEditCard v-if="props.edit.action === 'DELETE_ROWS'" :action="props.edit"
          @set-request="watchRequestSocket" />
        <ActionNewEditCard v-if="props.edit.action === 'NEW'" :action="props.edit" :schema-object="schemaObject"
          @set-request="watchRequestSocket" />
        <ActionPivotCategoriesEditCard v-if="props.edit.action === 'PIVOT_CATEGORIES'" :action="props.edit"
          :schema-subject="schemaSubject" :schema-object="schemaObject" @set-request="watchRequestSocket" />
        <ActionPivotLongerEditCard v-if="props.edit.action === 'PIVOT_LONGER'" :action="props.edit"
          :schema-subject="schemaSubject" :schema-object="schemaObject" @set-request="watchRequestSocket" />
        <ActionRenameEditCard v-if="props.edit.action === 'RENAME'" :action="props.edit" :schema-subject="schemaSubject"
          :schema-object="schemaObject" @set-request="watchRequestSocket" />
        <ActionSelectEditCard v-if="props.edit.action === 'SELECT'" :action="props.edit" :schema-subject="schemaSubject"
          :schema-object="schemaObject" @set-request="watchRequestSocket" />
        <ActionSelectNewestEditCard v-if="props.edit.action === 'SELECT_NEWEST'" :action="props.edit"
          :schema-subject="schemaSubject" :schema-object="schemaObject" @set-request="watchRequestSocket" />
        <ActionSelectOldestEditCard v-if="props.edit.action === 'SELECT_OLDEST'" :action="props.edit"
          :schema-subject="schemaSubject" :schema-object="schemaObject" @set-request="watchRequestSocket" />
        <ActionSeparateEditCard v-if="props.edit.action === 'SEPARATE'" :action="props.edit" :schema-subject="schemaSubject"
          :schema-object="schemaObject" @set-request="watchRequestSocket" />
        <ActionUniteEditCard v-if="props.edit.action === 'UNITE'" :action="props.edit" :schema-subject="schemaSubject"
          :schema-object="schemaObject" @set-request="watchRequestSocket" />
      </div>
      <!-- Separator -->
      <div class="my-2 h-px w-full bg-gray-900/10" aria-hidden="true" />
      <div class="flex flex-row-reverse gap-x-2">
        <button @click.prevent="acceptRequest"
          class="text-eucalyptus-600 group flex font-semibold">
          <CheckCircleIcon class="hover:bg-eucalyptus-100 rounded-full h-6 w-6 shrink-0" aria-hidden="true" />
          <span class="sr-only">Accept</span>
        </button>
        <button @click.prevent="rejectRequest"
          class="text-sienna-600 group flex font-semibold">
          <XCircleIcon class="hover:bg-sienna-100 rounded-full h-6 w-6 shrink-0" aria-hidden="true" />
          <span class="sr-only">Reject</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CheckCircleIcon, XCircleIcon } from "@heroicons/vue/24/outline"
import { IActionModel, IResourceSchemaReference, ISocketRequest } from "@/interfaces"

const props = defineProps<{
  edit: IActionModel,
  schemaSubject: IResourceSchemaReference,
  schemaObject: IResourceSchemaReference
}>()
const emit = defineEmits<{
  setRequest: [request: ISocketRequest],
  rejectRequest: [request: string]
}>()
const changeRequest = ref<ISocketRequest>({} as ISocketRequest)
const changeRequested = ref(false)

async function acceptRequest() {
  if (!changeRequested.value) rejectRequest()
  else emit("setRequest", changeRequest.value)
}

async function rejectRequest() {
  emit("rejectRequest", "")
}

async function watchRequestSocket(request: ISocketRequest) {
  changeRequest.value = request
  changeRequested.value = true
  console.log("acceptRequest", changeRequest.value)
}
</script>
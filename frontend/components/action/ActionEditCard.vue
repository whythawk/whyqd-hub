<template>
  <div class="relative flex gap-x-2 min-w-full">
    <div class="text-sm text-gray-500 p-1 min-w-full hover:bg-gray-100 hover:rounded-md">
      <ActionCalculateEditCard v-if="props.edit.action === 'CALCULATE'" :action="props.edit"
        :schema-subject="schemaSubject" :schema-object="schemaObject" @set-request="watchRequestSocket" />
      <ActionCategoriseEditCard v-if="props.edit.action === 'CATEGORISE'" :action="props.edit"
        :schema-subject="schemaSubject" :schema-object="schemaObject" @set-request="watchRequestSocket" />
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
  </div>
</template>

<script setup lang="ts">
import { IActionModel, IResourceSchemaReference, ISocketRequest } from "@/interfaces"

const props = defineProps<{
  edit: IActionModel,
  schemaSubject: IResourceSchemaReference,
  schemaObject: IResourceSchemaReference
}>()
const emit = defineEmits<{ setRequest: [request: ISocketRequest] }>()

async function watchRequestSocket(request: ISocketRequest) {
  emit("setRequest", request)
}
</script>
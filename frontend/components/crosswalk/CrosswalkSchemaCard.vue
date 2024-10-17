<template>
  <div class="relative flex gap-x-4">
    <div class="flex-auto py-0.5 text-xs leading-5 text-gray-500 pb-2 border-b border-gray-200">
      <div v-if="props.reference && props.reference.fields && props.reference.fields.length" class="space-y-2 mx-2">
        <h4 class="text-sm font-semibold leading-7 text-gray-500 pt-2">Fields</h4>
        <ul role="list">
          <li v-for="(field, fIdx) in props.reference.fields" :key="`field-${field.uuid}`">
            <CrosswalkSchemaFieldCard :resource-id="(props.reference.id as string)" :field="field"
              :subject="props.subject" :action="getActionModel(field.name)"
              :last-card="fIdx === props.reference.fields.length - 1" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { IResourceSchemaReference, IActionModel } from "@/interfaces"

function getActionModel(key: string): IActionModel {
  let axn
  if (!props.subject) axn = props.actions.find(
    (action) => action.destinationField
      && (action.destinationField.length
        ? action.destinationField.includes(key)
        : action.destinationField === key
      ))
  else axn = props.actions.find(
    (action) => action.sourceField
      && action.sourceField.length
      // @ts-ignore
      && [].concat(...action.sourceField).includes(key)
  )
  if (axn) return axn
  else return {} as IActionModel
}

const props = defineProps<{
  reference?: IResourceSchemaReference,
  actions: IActionModel[],
  subject: Boolean
}>()
</script>
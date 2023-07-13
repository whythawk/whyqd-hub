<template>
  <div class="relative flex gap-x-2">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <div class="relative flex h-6 w-6 flex-none items-center justify-center rounded-full">
      <div class="h-1.5 w-1.5 mt-4 rounded-full bg-gray-100 ring-1 ring-gray-300" />
    </div>
    <div class="flex-auto text-xs leading-5 text-gray-500 p-2 hover:bg-gray-100 hover:rounded-md">
      <div class="flex w-full justify-between items-center rounded-lg text-base font-semibold text-gray-900">
        <h3 v-if="props.field.title" class="text-sm font-semibold text-gray-900">{{ props.field.title }}</h3>
        <h3 v-else class="text-sm font-semibold text-gray-900">{{ props.field.name }}</h3>
      </div>
      <div class="flex items-center">
        <h4 id="detail-heading" class="sr-only">Overview</h4>
        <ul role="list" class="flex flex-row text-xs">
          <li class="text-gray-700 p-2">
            Type: {{ capitalizeFirst(props.field.type) }}
          </li>
          <li v-if="props.field.constraints && props.field.constraints.enum && props.field.constraints.enum.length"
            class="text-gray-700 p-2">
            <span class="flex">Categories:
              <CommonExpanderSlot
                :term="props.field.constraints.enum.map((category: ICategoryCreate) => category.name).join(', ')"
                class="ml-2 w-64" />
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { IFieldCreate, ICategoryCreate } from "@/interfaces"
import { capitalizeFirst } from "@/utilities"

const props = defineProps<{
  resourceId: string,
  field: IFieldCreate,
  lastCard: Boolean
}>()
</script>
<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <div class="relative flex h-6 w-6 flex-none items-center justify-center bg-white">
      <div class="h-1.5 w-1.5 rounded-full bg-gray-100 ring-1 ring-gray-300" />
    </div>
    <Disclosure as="div" class="flex-auto py-0.5 text-xs leading-5 text-gray-500" v-slot="{ open }">
      <DisclosureButton class="flex w-full justify-between items-center rounded-lg text-base font-semibold text-gray-900">
        <h3 v-if="props.field.title" class="text-sm font-semibold text-gray-900">{{ props.field.title }}</h3>
        <h3 v-else class="text-sm font-semibold text-gray-900">{{ props.field.name }}</h3>
        <ChevronUpIcon :class="open ? 'rotate-180 transform' : ''" class="h-5 w-5" />
      </DisclosureButton>
      <DisclosurePanel class="px-4 pt-2 pb-2 text-sm text-gray-500">
        <div class="border-t border-gray-100">
          <dl class="divide-y divide-gray-100">
            <div class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Name</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ props.field.name }}</dd>
            </div>
            <div v-if="props.field.title" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Title</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ props.field.title }}</dd>
            </div>
            <div v-if="props.field.description" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Description</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ props.field.description }}</dd>
            </div>
            <div v-if="props.field.type" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Data type</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ capitalizeFirst(props.field.type) }}
              </dd>
            </div>
            <div v-if="props.field.example" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Example</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ props.field.example }}</dd>
            </div>
            <div v-if="props.field.constraints" class="px-4 py-2 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Constraints</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700">
                <div class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Required</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                <span v-if="props.field.constraints.required">True</span>
                <span v-else>False</span>
              </dd>
            </div>
            <div class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Unique</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                <span v-if="props.field.constraints.unique">True</span>
                <span v-else>False</span>
              </dd>
            </div>
            <div v-if="props.field.constraints.minimum" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Minimum</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ props.field.constraints.minimum }}
              </dd>
            </div>
            <div v-if="props.field.constraints.maximum" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Maximum</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ props.field.constraints.maximum }}
              </dd>
            </div>
            <div v-if="props.field.constraints.enum && props.field.constraints.enum.length"
              class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Categories</dt>
              <dd class="mt-2 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                <ul role="list" class="divide-y divide-gray-100">
                  <li v-for="(category, i) in props.field.constraints.enum"
                    :key="`field-${props.field.uuid}-category-${i}`"
                    class="flex items-center justify-between p-2 text-sm">
                    <div class="flex w-0 flex-1 items-center">
                      <div class="flex min-w-0 flex-1 gap-2">
                        <span class="font-medium">{{ category.name }}</span>
                        <span class="flex-shrink-0 text-gray-400">{{ category.description }}</span>
                      </div>
                    </div>
                  </li>
                </ul>
              </dd>
            </div>
            <div v-if="props.field.constraints.default" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Default category</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ props.field.constraints.default }}
              </dd>
            </div>
            </dd>
        </div>
        </dl>
  </div>
  </DisclosurePanel>
  </Disclosure>
  </div>
</template>

<script setup lang="ts">
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import { ChevronUpIcon } from "@heroicons/vue/20/solid"
import { IFieldCreate } from "@/interfaces"
import { capitalizeFirst } from "@/utilities"

const props = defineProps<{
  field: IFieldCreate,
  lastCard: Boolean
}>()
</script>
<template>
  <Form class="flex-auto rounded-lg p-3 ring-1 ring-inset ring-gray-200">
    <Disclosure v-slot="{ open }">
      <DisclosureButton class="flex w-full justify-between items-center rounded-lg text-base font-semibold text-gray-900">
        <h3 v-if="draft.title" class="text-base font-semibold text-gray-900">{{ draft.title }}</h3>
        <h3 v-else class="text-base font-semibold text-gray-900">{{ draft.name }}</h3>
        <EllipsisVerticalIcon :class="open ? 'rotate-90 transform' : ''" class="h-5 w-5" />
      </DisclosureButton>
      <DisclosurePanel class="px-4 pt-2 pb-2 text-sm text-gray-500">
        <div class="border-t border-gray-100">
          <dl class="divide-y divide-gray-100">
            <div class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Name</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ draft.name }}</dd>
            </div>
            <div v-if="draft.title" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Title</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ draft.title }}</dd>
            </div>
            <div v-if="draft.description" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Description</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ draft.description }}</dd>
            </div>
            <div v-if="draft.type" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Data type</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ capitalizeFirst(draft.type) }}
              </dd>
            </div>
            <div v-if="draft.example" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Example</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ draft.example }}</dd>
            </div>
            <div v-if="draft.constraints" class="px-4 py-2 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Constraints</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700">
                <div class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Required</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                <span v-if="draft.constraints.required">True</span>
                <span v-else>False</span>
              </dd>
            </div>
            <div class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Unique</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                <span v-if="draft.constraints.unique">True</span>
                <span v-else>False</span>
              </dd>
            </div>
            <div v-if="draft.constraints.minimum" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Minimum</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ draft.constraints.minimum }}
              </dd>
            </div>
            <div v-if="draft.constraints.maximum" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Maximum</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ draft.constraints.maximum }}
              </dd>
            </div>
            <div v-if="draft.constraints.enum && draft.constraints.enum.length"
              class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Categories</dt>
              <dd class="mt-2 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                <ul role="list" class="divide-y divide-gray-100">
                  <li v-for="(category, i) in draft.constraints.enum" :key="`field-${draft.uuid}-category-${i}`"
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
            <div v-if="draft.constraints.default" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt class="text-sm font-medium text-gray-900">Default category</dt>
              <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                {{ draft.constraints.default }}
              </dd>
            </div>
            </dd>
        </div>
        </dl>
        </div>
      </DisclosurePanel>
    </Disclosure>
  </Form>
</template>

<script setup lang="ts">
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import { EllipsisVerticalIcon, CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/20/solid"
import { PlusCircleIcon, MinusCircleIcon, PaperClipIcon } from "@heroicons/vue/24/outline"
import { IFieldCreate } from "@/interfaces"
import { capitalizeFirst } from "@/utilities"

const emit = defineEmits<{ setRequest: [request: string] }>()
const props = defineProps<{
  edit: IFieldCreate,
}>()
const draft = ref({} as IFieldCreate)

// function submitRequest() {
//   if (checkConstraints()) {
//     const request: ISocketRequest = {
//       state: props.state,
//       data: { ...draft.value }
//     }
//     emit("setRequest", request)
//     resetForm()
//   } else toasts.addNotice({
//     title: "Field add error",
//     content: "Please check required terms, including field name, and constraints.",
//     icon: "error"
//   })
// }

watch(() => props.edit, () => {
  resetCard()
})

function resetCard() {
  draft.value = { ...props.edit }
}

onMounted(async () => {
  resetCard()
})
</script>
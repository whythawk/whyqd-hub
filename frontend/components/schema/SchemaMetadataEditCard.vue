<template>
  <form class="flex-auto rounded-lg p-3 ring-1 ring-inset ring-gray-200">
    <Disclosure v-slot="{ open }">
      <DisclosureButton class="flex w-full justify-between items-center rounded-lg text-base font-semibold text-gray-900">
        <h2 class="text-base font-semibold text-gray-900">Details</h2>
        <ChevronUpIcon :class="open ? 'rotate-180 transform' : ''" class="h-5 w-5" />
      </DisclosureButton>
      <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
        <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
          <div class="col-span-full">
            <label for="schema-title" class="block text-sm font-semibold leading-6 text-gray-900">Title</label>
            <div class="mt-2">
              <input type="text" name="schema-title" id="schema-title" v-model="draft.title"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
            </div>
            <p v-if="draft.name" class="mt-2 text-xs leading-6 text-gray-500">
              <span class="font-bold">Machine-readable name: </span>{{ draft.name }}
            </p>
          </div>

          <div class="col-span-full">
            <label for="description" class="block text-sm font-semibold leading-6 text-gray-900">Description</label>
            <div class="mt-2">
              <textarea id="description" name="description" rows="3" v-model="draft.description"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
            </div>
            <p class="mt-2 text-sm leading-6 text-gray-600">A complete description of the schema. Try and be as helpful as
              possible to 'future-you'.</p>
          </div>

          <div class="col-span-full">
            <label for="schema-missing-values" class="block text-sm font-semibold leading-6 text-gray-900">Missing
              values</label>
            <div class="mt-2">
              <input type="text" name="schema-missing-values" id="schema-missing-values" v-model="missing"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
            </div>
            <p class="mt-2 text-sm leading-6 text-gray-500">Indicates which string values in your tabular data should
              be treated as null values. There could be a variety of these, such as
              `<span class="font-mono font-semibold">..</span>`,
              or `<span class="font-mono font-semibold">-</span>` Write them exactly as they would appear, separated with
              commas.
            </p>
          </div>
        </div>
        <div class="mt-6 flex items-center justify-end gap-x-6">
          <button type="button" @click.prevent="resetForm"
            class="text-sm font-semibold leading-6 text-gray-900">Reset</button>
          <button type="submit" @click.prevent="submitRequest"
            class="rounded-md bg-ochre-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-ochre-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ochre-600">
            Set
          </button>
        </div>
      </DisclosurePanel>
    </Disclosure>
  </form>
</template>

<script setup lang="ts">
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import { ChevronUpIcon } from "@heroicons/vue/20/solid"
import { storeToRefs } from "pinia"
import { ISocketRequest, ISchemaCreate } from "@/interfaces"
import { useSchemaStore } from "@/stores"
import { nameSpace } from "@/utilities"

const schemaStore = useSchemaStore()
const { edit } = storeToRefs(schemaStore)
const draft = ref({} as ISchemaCreate)
const missing = ref("")
const emit = defineEmits<{ setRequest: [request: ISocketRequest] }>()
const props = defineProps<{
  state: string,
}>()

watch(
  () => draft.value!.title, (newTitle, oldTitle) => {
    if (newTitle && newTitle !== oldTitle) draft.value.name = nameSpace(newTitle)
  }, { immediate: true })

function submitRequest() {
  // https://stackoverflow.com/a/38201551/295606
  if (missing.value) draft.value.missingValues = missing.value.split(",").map((item: string) => item.trim())
  emit("setRequest", {
    state: props.state,
    data: { ...draft.value }
  })
}

watch(() => edit.value, () => {
  resetForm()
})

function resetForm() {
  draft.value = { ...edit.value }
  if (draft.value.title) draft.value.name = nameSpace(draft.value.title)
}

onMounted(async () => {
  resetForm()
})
</script>
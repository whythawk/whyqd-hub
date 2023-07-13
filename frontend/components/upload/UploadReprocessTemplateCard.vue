<template>
  <div class="relative flex gap-x-4">
    <div class="h-6 absolute left-0 top-0 flex w-6 justify-center">
      <div class="w-px bg-gray-200" />
    </div>
    <TableCellsIcon
      class="relative mt-3 h-6 w-6 flex-none rounded-full bg-gray-50 ring-1 ring-offset-4 ring-ochre-200 text-gray-700"
      aria-hidden="true" />
    <form class="flex-auto rounded-lg  py-2 px-3 ring-1 ring-inset ring-gray-200">
      <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
        <div class="col-span-full">
          <label for="datasource-name" class="block text-sm font-semibold leading-6 text-gray-900">Name *</label>
          <div class="mt-2">
            <input type="text" name="datasource-name" id="datasource-name" v-model="datasource.name"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-1 focus:ring-none focus:ring-gray-300 sm:text-sm sm:leading-6"
              readonly />
          </div>
        </div>
        <div class="col-span-full">
          <label for="datasource-mime" class="block text-sm font-semibold leading-6 text-gray-900">
            Mime / file type *
          </label>
          <div class="mt-2">
            <Listbox v-model="datasource.mime">
              <div class="relative mt-1">
                <ListboxButton
                  :class="[mimeError ? 'shadow-sienna-500' : '', 'relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-ochre-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-ochre-300 sm:text-sm']">
                  <span v-if="datasource.mime" class="block truncate">{{ datasource.mime }}</span>
                  <span v-else class="block truncate">Select...</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </span>
                </ListboxButton>
                <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                  leave-to-class="opacity-0">
                  <ListboxOptions
                    class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-md ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption v-slot="{ active, selected }" v-for="mtype in parameters.mimeType"
                      :key="`mtype-${mtype.value}`" :value="mtype.value" as="template">
                      <li :class="[
                        active ? 'bg-ochre-100 text-ochre-900' : 'text-gray-900',
                        'relative cursor-default select-none py-2 pl-10 pr-4',
                      ]">
                        <span :class="[
                          selected ? 'font-medium' : 'font-normal',
                          'block truncate',
                        ]">{{ mtype.value }}</span>
                        <span v-if="selected" class="absolute inset-y-0 left-0 flex items-center pl-3 text-ochre-600">
                          <CheckIcon class="h-5 w-5" aria-hidden="true" />
                        </span>
                      </li>
                    </ListboxOption>
                  </ListboxOptions>
                </transition>
              </div>
            </Listbox>
          </div>
        </div>
        <Disclosure as="section" aria-labelledby="detail-heading" v-slot="{ open }" class="col-span-full">
          <DisclosureButton
            class="group flex flex-row items-center text-sm font-medium text-gray-500 hover:text-ochre-500">
            Extra attributes
            <ChevronDownIcon :class="open ? 'rotate-180 transform' : ''" class="-mr-1 ml-1 h-4 w-4 flex-shrink-0"
              aria-hidden="true" />
          </DisclosureButton>
          <DisclosurePanel class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
            <div class="col-span-full mt-2">
              <label for="datasource-title" class="block text-sm font-semibold leading-6 text-gray-900">Title</label>
              <div class="mt-2">
                <input type="text" name="datasource-title" id="datasource-title" v-model="datasource.title"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
              </div>
            </div>
            <div class="col-span-full">
              <label for="description" class="block text-sm font-semibold leading-6 text-gray-900">Description</label>
              <div class="mt-2">
                <textarea id="description" name="description" rows="3" v-model="datasource.description"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
              </div>
            </div>
            <div class="col-span-full">
              <label for="datasource-path" class="block text-sm font-semibold leading-6 text-gray-900">
                URL or web-based file path
              </label>
              <div class="mt-2">
                <input type="text" name="datasource-path" id="datasource-path" v-model="datasource.path"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
              </div>
            </div>
            <div class="col-span-full">
              <label for="datasource-header" class="block text-sm font-semibold leading-6 text-gray-900">
                Header
              </label>
              <div class="mt-2">
                <input type="text" name="datasource-header" id="datasource-header" v-model="header"
                  :class="[headerError ? 'shadow-sienna-500 shadow-md' : '', 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6']" />
              </div>
              <p :class="[headerError ? 'text-sienna-500 font-bold' : 'text-gray-500', 'mt-2 text-sm leading-6']">
                Row (0-indexed) to use for the column labels of the parsed DataFrame. Must be a number or - in the case of
                multi-sheet Excel files - a list of numbers indicating the header row in each sheet. You can
                <span class="font-bold">leave this blank</span> if the column labels are in the top row of your source.
              </p>
            </div>
            <div class="col-span-full">
              <label for="datasource-attributes" class="block text-sm font-semibold leading-6 text-gray-900">
                Attributes, key-value
              </label>
              <div class="mt-2">
                <textarea name="datasource-attributes" id="datasource-attributes" v-model="attributes"
                  :class="[attributesError ? 'shadow-sienna-500 shadow-md' : '', 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6']" />
              </div>
              <p :class="[attributesError ? 'text-sienna-500 font-bold' : 'text-gray-500', 'mt-2 text-sm leading-6']">
                Optional open dictionary for reader-specific attributes for Pandas' API. E.g. 'quoting' for the CSV
                library. Only use this if you know what you are doing. Must be in JSON dictionary format.
              </p>
            </div>
          </DisclosurePanel>
        </Disclosure>
      </div>
      <div class="flex items-center justify-between">
        <button @click.prevent="isOpen = true"
          class="text-gray-700 hover:text-ochre-600 text-xs group flex gap-x-1 p-2 font-semibold">
          <TableCellsIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
          <span class="hidden lg:block">Show summary</span>
        </button>
        <TransitionRoot as="template" :show="isOpen">
          <Dialog as="div" class="relative z-50" @close="isOpen = false">
            <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100"
              leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
              <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
            </TransitionChild>
            <div class="fixed inset-0 z-10 overflow-y-auto">
              <div class="flex min-h-full items-end justify-center text-center sm:items-center">
                <TransitionChild as="template" enter="ease-out duration-300"
                  enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                  enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200"
                  leave-from="opacity-100 translate-y-0 sm:scale-100"
                  leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
                  <DialogPanel
                    class="flex flex-col sm:rounded-lg bg-white p-2 text-left shadow-xl transition-all max-w-[100%] sm:max-w-[90%] max-h-screen sm:max-h-[800px]">
                    <CommonDataTable :table-headers="props.reference.summarykeys" :table-rows="props.reference.summary" />
                    <div class="flex flex-row justify-end mt-4">
                      <button type="button"
                        class="mt-3 inline-flex justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 w-auto"
                        @click="isOpen = false">Close</button>
                    </div>
                  </DialogPanel>
                </TransitionChild>
              </div>
            </div>
          </Dialog>
        </TransitionRoot>
        <button type="submit" @click.prevent="submitRequest"
          class="rounded-md bg-ochre-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-ochre-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ochre-600">
          Reprocess
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  Listbox,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
  Dialog,
  DialogPanel,
  TransitionChild,
  TransitionRoot
} from "@headlessui/vue"
import { CheckIcon, ChevronUpDownIcon, ChevronDownIcon } from "@heroicons/vue/20/solid"
import { TableCellsIcon } from "@heroicons/vue/24/outline"
import { useResourceStore } from "@/stores"
import { IDataSourceTemplate, IResourceDataReference } from "@/interfaces"

const route = useRoute()
const resourceStore = useResourceStore()
const datasource = ref({} as IDataSourceTemplate)
const header = ref("")
const attributes = ref("")
const headerError = ref(false)
const mimeError = ref(false)
const attributesError = ref(false)
const isOpen = ref(false)

const props = defineProps<{
  source: IDataSourceTemplate,
  reference: IResourceDataReference,
}>()

const parameters = {
  mimeType: [
    { value: "CSV" },
    { value: "XLS" },
    { value: "XLSX" },
    { value: "PARQUET" },
    { value: "FEATHER" },
  ],
}

function onlyNumbers(payload: any[]): boolean {
  return payload.every(element => {
    return typeof element === "number" && !isNaN(element)
  })
}

function validateTemplate(): boolean {
  if (attributes.value && attributesError.value) return false
  if (
    datasource.value.header
    && Array.isArray(datasource.value.header)
    && datasource.value.header.length
    && !onlyNumbers(datasource.value.header)) {
    headerError.value = true
    return false
  }
  if (!datasource.value.mime) {
    mimeError.value = true
    return false
  }
  headerError.value = false
  mimeError.value = false
  return true
}

async function submitRequest() {
  delete datasource.value.header
  delete datasource.value.attributes
  attributesError.value = false
  headerError.value = false
  if (header.value) {
    try {
      datasource.value.header = header.value.split(",").map((item: string) => parseInt(item.trim()))
    } catch {
      headerError.value = true
    }
  }
  if (attributes.value) {
    try {
      datasource.value.attributes = JSON.parse(attributes.value)
    } catch {
      attributesError.value = true
    }
  }
  // UPLOAD
  if (validateTemplate()) {
    if (datasource.value.header && datasource.value.header.length === 1)
      datasource.value.header = datasource.value.header[0]
    // force this
    datasource.value.name = props.source.name
  }
}

function initialiseTemplate() {
  datasource.value = { ...props.source }
}

onMounted(async () => {
  initialiseTemplate()
})
</script>
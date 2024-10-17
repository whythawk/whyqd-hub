<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <TableCellsIcon
      class="relative mt-3 h-6 w-6 flex-none rounded-full bg-gray-50 ring-1 ring-offset-4 ring-ochre-200 text-gray-700"
      aria-hidden="true" />
    <Form
      @submit="submitRequest"
      :validation-schema="formSchema" :initial-values="formValues"
      class="flex-auto rounded-lg  py-2 px-3 ring-1 ring-inset ring-gray-200">
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
        <div class="col-span-full">
          <label for="datasourcePath" class="block text-sm font-semibold leading-6 text-gray-900">
            URL or web-based file path
          </label>
          <div class="mt-2 group relative inline-block w-full">
            <Field type="text" name="datasourcePath" id="datasourcePath"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
            <ErrorMessage name="datasourcePath"
              class="absolute left-5 top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700" />
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
      <div class="flex items-center justify-end">
        <button type="submit"
          class="rounded-md bg-ochre-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-ochre-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ochre-600">
          Upload
        </button>
      </div>
    </Form>
  </div>
</template>

<script setup lang="ts">
import { Disclosure, DisclosureButton, DisclosurePanel, Listbox, ListboxButton, ListboxOptions, ListboxOption, } from "@headlessui/vue"
import { CheckIcon, ChevronUpDownIcon, ChevronDownIcon } from "@heroicons/vue/20/solid"
import { TableCellsIcon } from "@heroicons/vue/24/outline"
import type { IDataSourceTemplate, IKeyable } from "@/interfaces"
import { useTokenStore, useToastStore } from "@/stores"
import { apiData } from "@/api"
import { isValidHttpUrl } from "@/utilities"

const tokenStore = useTokenStore()
const toasts = useToastStore()
const route = useRoute()
const datasource = ref({} as IDataSourceTemplate)
const header = ref("")
const attributes = ref("")
const headerError = ref(false)
const mimeError = ref(false)
const attributesError = ref(false)
let formData: FormData = new FormData()

const props = defineProps<{
  source: File,
  sourceUrl: string,
  idx: number,
  lastCard: Boolean
}>()
const emit = defineEmits<{ popRequest: [request: number] }>()

const parameters = {
  mimeType: [
    { value: "CSV" },
    { value: "XLS" },
    { value: "XLSX" },
    { value: "PARQUET" },
    { value: "FEATHER" },
  ],
}
const formSchema = {
  datasourcePath: { url: true, required: false },
}
const formValues = ref<IKeyable>({ datasourcePath: '' })

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

async function submitRequest(values: any) {
  if (values.datasourcePath && isValidHttpUrl(values.datasourcePath)) {
    datasource.value.path = values.datasourcePath
  } 
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
    formData.append("data", JSON.stringify(datasource.value))
    await tokenStore.refreshTokens()
    try {
      let msg: string = ""
      if (route.path.includes("/task/") && route.params.id) {
        // task-based source
        const { data: response } = await apiData.postUploadForTask(tokenStore.token, route.params.id as string, formData)
        if (response.value) msg = response.value.msg
      } else {
        // wild source
        const { data: response } = await apiData.postUpload(tokenStore.token, formData)
        if (response.value) msg = response.value.msg
      }
      if (msg) {
        toasts.addNotice({
          title: "Import processing",
          content: msg,
        })
      }
      emit("popRequest", props.idx)
    } catch (error) {
      toasts.addNotice({
        title: "Import error",
        content: error as string,
        icon: "error"
      })
    }
  }
}

function initialiseTemplate() {
  datasource.value.name = props.source.name
  if (props.sourceUrl && isValidHttpUrl(props.sourceUrl)) {
    datasource.value.path = props.sourceUrl
    formValues.value = {
      datasourcePath: props.sourceUrl
    }
  } 
  formData.append("files", props.source, props.source.name)
}

onMounted(async () => {
  initialiseTemplate()
})
</script>
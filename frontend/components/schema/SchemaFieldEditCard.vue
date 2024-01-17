<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <div class="relative flex h-6 w-6 flex-none items-center justify-center bg-white">
      <div class="h-1.5 w-1.5 rounded-full bg-gray-100 ring-1 ring-gray-300" />
    </div>
    <Form
      :class="[props.state === 'addField' ? 'bg-cerulean-100' : '', 'flex-auto rounded-lg p-3 ring-1 ring-inset ring-gray-200']">
      <Disclosure v-slot="{ open, close }">
        <DisclosureButton
          @click="disclosureWatcher(open)"
          class="flex w-full justify-between items-center rounded-lg text-base font-semibold text-gray-900">
          <h2 v-if="props.state === 'addField'" class="text-base font-semibold text-gray-900">Add field</h2>
          <h2 v-else class="text-base font-semibold text-gray-900">Field: {{ props.edit.name }}</h2>
          <EllipsisVerticalIcon :class="open ? 'rotate-90 transform' : ''" class="h-5 w-5" />
        </DisclosureButton>
        <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-500">
          <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
            <div class="col-span-full">
              <label for="field-name" class="block text-sm font-semibold leading-6 text-gray-900">Name *</label>
              <div class="mt-2">
                <Field type="text" name="field-name" id="field-name" v-model="draft.name" rules="required"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
                <ErrorMessage name="field-name" />
              </div>
              <p class="mt-2 text-sm leading-6 text-gray-600">Defined <span class="font-bold">exactly</span> as it is
                appears in use, including UTF8-formatting. By convention, it should be machine-readable, but your terms
                may
                be different.</p>
            </div>
            <div class="col-span-full">
              <label for="field-title" class="block text-sm font-semibold leading-6 text-gray-900">Title</label>
              <div class="mt-2">
                <input type="text" name="field-title" id="field-title" v-model="draft.title"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
              </div>
              <p class="mt-2 text-sm leading-6 text-gray-600">A human-readable version of the field name.</p>
            </div>
            <div class="col-span-full">
              <label for="description" class="block text-sm font-semibold leading-6 text-gray-900">Description</label>
              <div class="mt-2">
                <textarea id="description" name="description" rows="3" v-model="draft.description"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
              </div>
              <p class="mt-2 text-sm leading-6 text-gray-600">A description for the field.</p>
            </div>
            <div class="col-span-full">
              <label for="type" class="block text-sm font-semibold leading-6 text-gray-900">Field value type</label>
              <div class="mt-2">
                <Listbox v-model="draft.type">
                  <div class="relative mt-1">
                    <ListboxButton
                      class="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-ochre-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-ochre-300 sm:text-sm">
                      <span class="block truncate">{{ capitalizeFirst(draft.type) }}</span>
                      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                      </span>
                    </ListboxButton>
                    <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                      leave-to-class="opacity-0">
                      <ListboxOptions
                        class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                        <ListboxOption v-slot="{ active, selected }" v-for="dtype in parameters.dtypes"
                          :key="`dtype-${dtype.value}`" :value="dtype.value" as="template">
                          <li :class="[
                            active ? 'bg-ochre-100 text-ochre-900' : 'text-gray-900',
                            'relative cursor-default select-none py-2 pl-10 pr-4',
                          ]">
                            <span :class="[
                              selected ? 'font-medium' : 'font-normal',
                              'block truncate',
                            ]">{{ capitalizeFirst(dtype.value) }}</span>
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
              <p class="mt-2 text-sm leading-6 text-gray-600">A field must contain values of a specific type.</p>
            </div>
            <div class="col-span-full">
              <legend class="block text-sm font-semibold leading-6 text-gray-900">Constraints</legend>
              <div class="grid grid-cols-2 gap-x-3 pt-2">
                <div class="relative flex gap-x-3">
                  <div class="flex h-6 items-center">
                    <input id="field-constraints-required" name="field-constraints-required" type="checkbox"
                      v-model="draft!.constraints!.required"
                      class="h-4 w-4 rounded border-gray-300 text-ochre-600 focus:ring-ochre-600" />
                  </div>
                  <div class="text-sm leading-6">
                    <label for="field-constraints-required" class="font-medium text-gray-900">Required</label>
                    <p class="text-gray-500">A field must have a value for each instance.</p>
                  </div>
                </div>
                <div class="relative flex gap-x-3">
                  <div class="flex h-6 items-center">
                    <input id="field-constraints-unique" name="field-constraints-unique" type="checkbox"
                      v-model="draft!.constraints!.unique"
                      class="h-4 w-4 rounded border-gray-300 text-ochre-600 focus:ring-ochre-600" />
                  </div>
                  <div class="text-sm leading-6">
                    <label for="field-constraints-unique" class="font-medium text-gray-900">Unique</label>
                    <p class="text-gray-500">Each value must be unique.</p>
                  </div>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-x-3 pt-2">
                <div>
                  <label for="field-constraints-minimum"
                    class="block text-sm font-medium leading-6 text-gray-900">Minimum</label>
                  <div class="mt-2">
                    <Field name="field-constraints-minimum" id="field-constraints-minimum" type="text" rules="numeric"
                      v-model="draft!.constraints!.minimum"
                      class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
                    <ErrorMessage name="field-constraints-minimum" />
                  </div>
                </div>
                <div>
                  <label for="field-constraints-maximum"
                    class="block text-sm font-medium leading-6 text-gray-900">Maximum</label>
                  <div class="mt-2">
                    <Field type="text" name="field-constraints-maximum" id="field-constraints-maximum"
                      rules="numeric|numericRange:field-constraints-minimum" v-model="draft!.constraints!.maximum"
                      class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
                    <ErrorMessage name="field-constraints-maximum" />
                  </div>
                </div>
              </div>
              <div>
                <div class="table w-full border-collapse border-0 mt-2 text-sm font-medium text-gray-900">
                  <div class="table-header-group">
                    <div class="table-row border-transparent">
                      <div class="table-cell border-0">
                        <span v-if="draft.constraints && draft.constraints.enum && draft.constraints.enum.length">
                          Category name
                        </span>
                        <span v-else>Add category constraints</span>
                      </div>
                      <div v-if="draft.constraints && draft.constraints.enum && draft.constraints.enum.length"
                        class="table-cell border-0">
                        Description
                      </div>
                      <div class="table-cell border-0 text-right align-middle">
                        <button @click.prevent="addCategory" class="hover:text-ochre-600">
                          <PlusCircleIcon class="h-5 w-5" />
                        </button>
                      </div>
                    </div>
                  </div>
                  <div v-if="draft.constraints && draft.constraints.enum" class="table-row-group">
                    <div v-for="(category, cIdx) in draft.constraints.enum" :key="`constraints-category-${cIdx}`"
                      class="table-row border-transparent">
                      <div class="table-cell border-0 p-1">
                        <label :for="`constraints-category-name-${cIdx}`" class="sr-only">Category name</label>
                        <input :id="`constraints-category-name-${cIdx}`" v-model="draft.constraints.enum[cIdx].name"
                          :name="`constraints-category-name-${cIdx}`" type="text" placeholder="Category name" required
                          class="focus:ring-transparent focus:border-gray-300 block w-full sm:text-sm rounded-md border-gray-300" />
                      </div>
                      <div class="table-cell border-0">
                        <label for="constraints-category-description" class="sr-only">Category description</label>
                        <input :id="`constraints-category-description-${cIdx}`"
                          v-model="draft.constraints.enum[cIdx].description" type="text"
                          placeholder="Category description"
                          class="focus:ring-transparent focus:border-gray-300 block w-full sm:text-sm rounded-md border-gray-300" />
                      </div>
                      <div class="table-cell border-0 text-right align-middle">
                        <button v-show="draft.constraints.enum.length > 0" @click.prevent="removeCategory(cIdx)"
                          class="hover:text-sienna-600">
                          <MinusCircleIcon class="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="col-span-full">
              <label for="field-example" class="block text-sm font-semibold leading-6 text-gray-900">Example
                values</label>
              <div class="mt-2">
                <input type="text" name="field-example" id="field-example" v-model="draft!.example"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
              </div>
              <p class="mt-2 text-sm leading-6 text-gray-600">An example value, as a string, for the field.</p>
            </div>
          </div>
          <div class="mt-6 flex items-center justify-between gap-x-6">
            <button v-if="draft.uuid" type="button" @click.prevent="removeField(draft.uuid)"
              class="text-sm font-semibold leading-6 text-gray-900 rounded-lg px-3 py-2 ring-1 ring-inset ring-sienna-200 hover:bg-sienna-200">
              Delete
            </button>
            <div class="flex justify-end gap-x-6">
              <button type="button" @click.prevent="resetForm"
                class="text-sm font-semibold leading-6 text-gray-900">Reset</button>
              <button type="submit" @click.prevent="submitRequest(close)"
                class="rounded-md bg-ochre-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-ochre-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ochre-600">
                <span v-if="props.state === 'addField'">Create</span>
                <span v-else>Update</span>
              </button>
            </div>
          </div>
        </DisclosurePanel>
      </Disclosure>
    </Form>
  </div>
</template>

<script setup lang="ts">
import {
  Disclosure, DisclosureButton, DisclosurePanel, Listbox, ListboxButton, ListboxOptions, ListboxOption,
} from "@headlessui/vue"
import { CheckIcon, ChevronUpDownIcon, EllipsisVerticalIcon } from "@heroicons/vue/20/solid"
import { MinusCircleIcon, PlusCircleIcon } from "@heroicons/vue/24/outline"
import { ISocketRequest, IFieldCreate, IConstraintsCreate, ICategoryCreate } from "@/interfaces"
import { useToastStore } from "@/stores"
import { capitalizeFirst, generateUUID } from "@/utilities"

const toasts = useToastStore()
const draft = ref({} as IFieldCreate)
const emit = defineEmits<{
  setRequest: [request: ISocketRequest],
  setDraggable: [isDraggable: boolean]
}>()
const props = defineProps<{
  state: string,
  edit: IFieldCreate,
  lastCard: Boolean
}>()

const parameters = {
  dtypes: [
    { value: "string" },
    { value: "number" },
    { value: "integer" },
    { value: "boolean" },
    { value: "array" },
    { value: "date" },
    { value: "datetime" },
    { value: "month" },
    { value: "quarter" },
    { value: "year" },
    { value: "any" },
  ],
}


// WATCHERS
function disclosureWatcher(open: boolean) {
    // `open` seems to be false if open and true of closed ...
  emit("setDraggable", open)
}

// SETTERS
function checkUnique(objArray: ICategoryCreate[]): boolean {
  if (!objArray || !objArray.length) return true
  let nameList = objArray.map(({ name }) => name)
  const listLength = nameList.length
  const setLength = Array.from(new Set(nameList)).length
  return listLength === setLength
}

function checkConstraints(): boolean {
  if (!draft.value.name) return false
  if (!draft.value.constraints) return true
  if (draft.value.constraints && Object.keys(draft.value.constraints).length !== 0) {
    if (
      (draft.value.constraints.minimum || draft.value.constraints.maximum)
      && !["number", "integer"].includes(draft.value.type)
    ) return false
    if (
      draft.value.constraints.minimum
      && draft.value.constraints.maximum
      && +draft.value.constraints.minimum > +draft.value.constraints.maximum
    ) return false
    if (draft.value.constraints.enum) return checkUnique(draft.value.constraints.enum)
  }
  return true
}

function addCategory(): void {
  if (!draft.value.constraints) draft.value.constraints = {} as IConstraintsCreate
  if (!draft.value.constraints!.enum) draft.value.constraints!.enum = [] as ICategoryCreate[]
  const newCat: ICategoryCreate = {
    uuid: generateUUID(),
    name: "",
    description: "",
  }
  draft.value.constraints!.enum.splice(draft.value.constraints!.enum.length, 1, newCat)
}

function removeCategory(category: number): void {
  if (draft.value.constraints && draft.value.constraints.enum?.length) draft.value.constraints!.enum.splice(category, 1)
}

function removeField(uuid: string) {
  const request: ISocketRequest = {
    state: "removeField",
    data: { name: uuid }
  }
  emit("setDraggable", true)
  emit("setRequest", request)
  resetForm()
}

function submitRequest(close: any) {
  if (checkConstraints()) {
    const request: ISocketRequest = {
      state: props.state,
      data: { ...draft.value }
    }
    emit("setDraggable", true)
    emit("setRequest", request)
    resetForm()
    close()
  } else toasts.addNotice({
    title: "Field add error",
    content: "Please check required terms, including field name, and constraints.",
    icon: "error"
  })
}

watch(() => props.edit, () => {
  resetForm()
})


function resetForm() {
  draft.value = { ...props.edit }
  if (!draft.value.type) draft.value.type = "string"
  if (!draft.value.constraints) draft.value.constraints = {} as IConstraintsCreate
}

onMounted(async () => {
  resetForm()
})
</script>
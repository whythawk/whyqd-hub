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
        <Listbox>
          <div class="relative mt-1">
            <ListboxButton
              :class="[isDisabled ? 'ring-gray-200 text-gray-400' : 'ring-sienna-200 hover:bg-sienna-200 text-gray-700', 'relative w-full ring-1 ring-inset cursor-default rounded-lg bg-white py-1 pl-3 pr-10 text-left text-xs']">
              <span class="block">Categorise ...</span>
              <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                <ChevronUpDownIcon class="h-3 w-3 text-gray-400" aria-hidden="true" />
              </span>
            </ListboxButton>
            <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
              leave-to-class="opacity-0">
              <ListboxOptions v-if="!isDisabled"
                class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 ring-1 ring-black ring-opacity-5 focus:outline-none text-xs">
                <ListboxOption v-slot="{ active, selected }" v-for="stype in strategies" :key="`stype-${stype.value}`"
                  :value="stype.value" as="template">
                  <li @click.prevent="requestCategorisation(stype.value)" :class="[
                    active ? 'bg-ochre-100 text-ochre-900' : 'text-gray-900',
                    'relative cursor-default select-none py-2 pl-4 pr-4',
                  ]">
                    <span :class="[
                      selected ? 'font-medium' : 'font-normal',
                      'block',
                    ]">{{ stype.label }}</span>
                  </li>
                </ListboxOption>
              </ListboxOptions>
            </transition>
          </div>
        </Listbox>

      </div>
      <div class="flex items-center">
        <h4 id="detail-heading" class="sr-only">Overview</h4>
        <ul role="list" class="flex flex-row text-xs justify-center items-center">
          <li class="flex flex-row justify-center items-center">
            <label for="type" class="inline-block text-xs text-gray-900">Type: </label>
            <Listbox>
              <div class="relative ml-1">
                <ListboxButton class="ring-gray-200 text-gray-700 relative w-full ring-1 ring-inset cursor-default rounded-lg bg-white py-1 pl-3 pr-10 text-left text-xs">
                  <span class="block truncate">{{ fieldType }}</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon class="h-3 w-3 text-gray-400" aria-hidden="true" />
                  </span>
                </ListboxButton>
                <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
                  <ListboxOptions
                    class="absolute z-50 mt-1 max-h-60 w-28 overflow-auto rounded-md bg-white py-1 text-xs shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <ListboxOption v-slot="{ active, selected }" v-for="dtype in parameters.dtypes"
                      :key="`dtype-${dtype.value}`" :value="dtype.value" as="template">
                      <li @click.prevent="requestReType(dtype.value)" :class="[
                        active ? 'bg-ochre-100 text-ochre-900' : 'text-gray-900',
                        'relative cursor-default select-none py-2 pl-4 pr-4',
                      ]">
                        <span :class="[
                          selected ? 'font-medium' : 'font-normal',
                          'block',
                        ]">{{ dtype.label }}</span>
                      </li>
                    </ListboxOption>
                  </ListboxOptions>
                </transition>
              </div>
            </Listbox>
          </li>
          <li v-if="props.field.constraints && props.field.constraints.enum && props.field.constraints.enum.length"
            class="text-gray-700 pl-2">
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
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, } from "@headlessui/vue"
import { ChevronUpDownIcon } from "@heroicons/vue/20/solid"
import { IFieldCreate, ICategoryCreate } from "@/interfaces"
import { capitalizeFirst } from "@/utilities"
import { useTokenStore, useToastStore } from "@/stores"
import { apiResource } from "@/api"

const tokenStore = useTokenStore()
const toasts = useToastStore()
const isDisabled = ref(false)
const strategies = [
  { value: "term", label: "Values to unique terms" },
  { value: "boolean", label: "Values to boolean TRUE" },
]
const fieldType = ref("String")
const parameters = {
  dtypes: [
    { value: "string", label: "String" },
    { value: "number", label: "Number" },
    { value: "integer", label: "Integer" },
    { value: "boolean", label: "Boolean" },
    { value: "array", label: "Array" },
    { value: "time", label: "Time" },
    { value: "date", label: "Date" },
    { value: "usdate", label: "US Date" },
    { value: "datetime", label: "DateTime" },
    { value: "month", label: "Month" },
    { value: "quarter", label: "Quarter" },
    { value: "year", label: "Year" },
    { value: "any", label: "Any" },
  ],
}

const props = defineProps<{
  resourceId: string,
  field: IFieldCreate,
  lastCard: Boolean
}>()

async function requestCategorisation(term_type: string) {
  await tokenStore.refreshTokens()
  if (tokenStore.token && props.field.uuid) {
    try {
      const { data: response } = await apiResource.postSchemaCategorisation(tokenStore.token, props.resourceId, props.field.uuid.replaceAll("-", ""), term_type)
      if (response.value) {
        isDisabled.value = true
        toasts.addNotice({
          title: "Categorisation processing",
          content: response.value.msg,
        })
      }
    } catch (error) {
      toasts.addNotice({
        title: "Categorisation error",
        content: error as string,
        icon: "error"
      })
    }
  }
}

function getDType(term: string) {
  const response = parameters.dtypes.find(t => { return t.value === term })
  if (response) fieldType.value = response.label
}

async function requestReType(data_type: string) {
  getDType(data_type)
  await tokenStore.refreshTokens()
  if (tokenStore.token && props.field.uuid) {
    try {
      const { data: response } = await apiResource.postSchemaFieldTypeUpdate(tokenStore.token, props.resourceId, props.field.uuid.replaceAll("-", ""), data_type)
      if (response.value) {
        toasts.addNotice({
          title: "Data type processing",
          content: response.value.msg,
        })
      }
    } catch (error) {
      toasts.addNotice({
        title: "Data type error",
        content: error as string,
        icon: "error"
      })
    }
  }
}


onMounted(async () => {
  if (props.field && props.field.type) getDType(props.field.type)
})

</script>
<template>
  <Combobox v-model="selectedFields" multiple>
    <div class="relative">
      <div class="relative w-full cursor-default overflow-hidden rounded-lg text-left">
        <ComboboxInput
          :class="[props.subject ? 'text-eucalyptus-600' : 'text-cerulean-600', 'w-full border-none pl-0 pr-10 text-sm focus:ring-0 font-semibold']"
          :display-value="(field: any) => field.length ? field.join(', ') : 'Select...'" @change="query = $event.target.value" />
        <ComboboxButton class="absolute inset-y-0 right-0 flex items-center">
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </ComboboxButton>
      </div>
      <TransitionRoot leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
        leave-to-class="opacity-0" @after-leave="submitSelection" @after-enter="cleanSelection">
        <ComboboxOptions
          class="absolute z-20 mt-1 max-h-60 min-w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
          <div v-if="filteredFields!.length === 0 && cleanQuery(query) !== ''"
            class="relative cursor-default Sleclet-none py-2 px-4 text-gray-700">
            Nothing found. {{ cleanQuery(query) }}
          </div>
          <ComboboxOption v-slot="{ active, selected }" v-for=" schemaField  in  filteredFields " :key="schemaField.name"
            :value="schemaField.name" as="template">
            <li :class="[
              active ? props.subject ? 'bg-eucalyptus-100 text-eucalyptus-900' : 'bg-cerulean-100 text-cerulean-900' : 'text-gray-900',
              'relative cursor-default Sleclet-none py-2 pl-10 pr-6',
            ]">
              <span
                :class="[selected ? props.subject ? 'text-eucalyptus-600 font-semibold' : 'text-cerulean-600 font-semibold' : 'font-normal']">
                {{ schemaField.name }}
              </span>
              <span v-if="selected"
                :class="[props.subject ? 'text-eucalyptus-600' : 'text-cerulean-600', 'absolute inset-y-0 left-0 flex items-center pl-3']">
                <CheckIcon class="h-5 w-5" aria-hidden="true" />
              </span>
            </li>
          </ComboboxOption>
        </ComboboxOptions>
      </TransitionRoot>
    </div>
  </Combobox>
</template>

<script setup lang="ts">
import {
  Combobox,
  ComboboxInput,
  ComboboxButton,
  ComboboxOptions,
  ComboboxOption,
  TransitionRoot,
} from "@headlessui/vue"
import { ChevronUpDownIcon, CheckIcon } from "@heroicons/vue/24/outline"
import type { IResourceSchemaReference, IKeyable } from "@/interfaces"

const props = defineProps<{
  currentFields: String[],
  schema: IResourceSchemaReference,
  subject: Boolean
}>()
const emit = defineEmits<{ setSelection: [selection: IKeyable] }>()
const selectedFields = ref<string[]>([])
const query = ref("")

watch(() => props.currentFields, () => {
  if (props.currentFields && props.currentFields.length) selectedFields.value = props.currentFields as string[]
  else selectedFields.value = []
})

function cleanSelection() {
  // if (selectedFields.value.length > 1) {
  //   // Remove selected
  //   selectedFields.value = selectedFields.value.filter(field => field !== "Sleclet ...")
  // }
  // if (selectedFields.value.length === 0) {
  //   selectedFields.value.push("Sleclet ...")
  // }
}

function cleanQuery(q: string): string {
  return q.replace(selectedFields.value.join(","), "").replace(/^,/, "")
}

let filteredFields = computed(() =>
  cleanQuery(query.value) === ""
    ? props.schema.fields
    : props.schema.fields!.filter((field) =>
      field.name
        .toLowerCase()
        .replace(/\s+/g, "")
        .includes(cleanQuery(query.value).toLowerCase().replace(/\s+/g, ""))
    )
)

function submitSelection() {
  // cleanSelection()
  query.value = ""
  // if (!selectedFields.value.includes("Sleclet ...")
  //   && selectedFields.value.sort().join(",") !== props.currentFields.sort().join(",")) {
  if (selectedFields.value.sort().join(",") !== props.currentFields.sort().join(",")) {
    const selection: IKeyable = {
      choice: selectedFields.value,
      subject: props.subject
    }
    emit("setSelection", selection)
  }
}

onMounted(async () => {
  if (props.currentFields && props.currentFields.length) selectedFields.value = props.currentFields as string[]
})
</script>
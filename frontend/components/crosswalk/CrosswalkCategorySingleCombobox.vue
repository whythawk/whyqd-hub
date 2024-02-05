<template>
  <Combobox v-model="selectedTerm">
    <div class="relative">
      <div class="relative w-full cursor-default overflow-hidden rounded-lg text-left">
        <ComboboxInput
          :class="[props.subject ? 'text-eucalyptus-600' : 'text-cerulean-600', 'w-full border-none pl-0 pr-10 text-sm focus:ring-0 font-normal']"
          :display-value="(field: any) => field" @change="query = $event.target.value" />
        <ComboboxButton class="absolute inset-y-0 right-0 flex items-center">
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </ComboboxButton>
      </div>
      <TransitionRoot leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
        leave-to-class="opacity-0" @after-leave="query = ''">
        <ComboboxOptions
          class="absolute z-20 mt-1 max-h-60 min-w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
          <div v-if="filteredTerms!.length === 0 && query !== ''"
            class="relative cursor-default select-none py-2 px-4 text-gray-700">
            Nothing found.
          </div>
          <ComboboxOption v-slot="{ active, selected }" v-for="term in filteredTerms" :key="`single-option-${term}`"
            :value="term" as="template">
            <li :class="[
              active ? props.subject ? 'bg-eucalyptus-100 text-eucalyptus-900' : 'bg-cerulean-100 text-cerulean-900' : 'text-gray-900',
              'relative cursor-default select-none py-2 pl-10 pr-6',
            ]">
              <span :class="[selected ? props.subject ? 'text-eucalyptus-600' : 'text-cerulean-600' : 'text-gray-900']">
                {{ term }}
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
import { IKeyable } from "@/interfaces"

const props = defineProps<{
  currentTerm?: String,
  terms?: IKeyable[],
  subject: Boolean,
}>()
const emit = defineEmits<{ setSelection: [selection: IKeyable] }>()
const availableTerms = ref<string[]>([])
const selectedTerm = ref("")
const query = ref("")

function refreshTerms() {
  availableTerms.value = []
  selectedTerm.value = ""
  if (props.terms && props.terms.length) availableTerms.value = props.terms.map(({ name }) => name)
  if (props.currentTerm && props.currentTerm !== "") selectedTerm.value = props.currentTerm as string
}

watch(() => [props.currentTerm, props.terms], () => {
  refreshTerms()
})

watch(() => selectedTerm.value, () => {
  submitSelection()
})

let filteredTerms = computed(() =>
  query.value === ""
    ? availableTerms.value
    : availableTerms.value.filter((tm) =>
      tm
        .toLowerCase()
        .replace(/\s+/g, "")
        .includes(query.value.toLowerCase().replace(/\s+/g, ""))
    )
)

function submitSelection() {
  if (selectedTerm.value && selectedTerm.value !== props.currentTerm) {
    const selection: IKeyable = {
      choice: selectedTerm.value,
      subject: props.subject
    }
    emit("setSelection", selection)
  }
}

onMounted(async () => {
  refreshTerms()
})
</script>
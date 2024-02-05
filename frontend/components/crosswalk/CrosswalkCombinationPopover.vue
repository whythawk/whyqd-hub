<template>
  <Popover class="relative">
    <PopoverButton
      class="flex justify-between items-center text-eucalyptus-600 w-full border-none pl-0 text-sm focus:ring-0 font-semibold">
      <span v-if="selectedTerms.length">Selected terms ({{ selectedTerms.length }})</span>
      <span v-else>Select ...</span>
      <ChevronDownIcon class="ml-2 h-5 w-5 text-gray-400 transition duration-150 ease-in-out group-hover:text-opacity-80"
        aria-hidden="true" />
    </PopoverButton>
    <TransitionRoot enter-active-class="transition duration-200 ease-out" enter-from-class="translate-y-1 opacity-0"
      enter-to-class="translate-y-0 opacity-100" leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100" leave-to-class="translate-y-1 opacity-0"
      @after-leave="submitSelection">
      <PopoverPanel class="absolute z-20 -translate-x-1/2 transform">
        <div class="w-96 bg-white rounded-lg shadow-lg ring-1 mt-2 ring-black ring-opacity-5">
          <button @click.prevent="addTerm"
            class="flex w-full justify-between items-center p-2 border-b border-gray-200 bg-gray-100 hover:text-ochre-600">
            <span class="font-semibold">Add term</span>
            <PlusCircleIcon class="h-5 w-5" />
          </button>
          <div class="relative">
            <ul v-for="(term, tIdx) in selectedTerms" :key="`combination-term-${tIdx}`"
              class="flex items-center rounded-lg p-2 hover:bg-gray-50 focus:outline-none focus-visible:ring focus-visible:ring-eucalyptus-500 focus-visible:ring-opacity-50">
              <li class="flex justify-between items-center w-full">
                <div v-if="props.isSelect" class="flex justify-between items-center w-full">
                  <CrosswalkSingleCombobox :current-field="term[0]" :schema="props.schemaSubject" :subject="true"
                    :extra="tIdx" @set-selection="watchSelectionName" />
                  <img src="/img/bracket-divider.svg" class="h-5 mx-1" />
                  <CrosswalkSingleCombobox :current-field="(term[2] as string)" :schema="props.schemaSubject" :subject="true"
                    :extra="tIdx" @set-selection="watchSelectionDate" />
                </div>
                <div v-else class="flex justify-between items-center w-full">
                  <Listbox as="div" v-model="term[0]">
                    <ListboxButton
                      class="relative flex justify-between items-center w-20 border-none pl-0 pr-10 text-sm focus:ring-0">
                      <span :class="[term[0] === 'Set ...' ? 'text-sm' : 'font-bold text-lg', 'text-eucalyptus-600']">{{
                        term[0] }}</span>
                      <span class="absolute inset-y-0 right-0 flex items-center pr-2">
                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                      </span>
                    </ListboxButton>
                    <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                      leave-to-class="opacity-0">
                      <ListboxOptions
                        class="absolute z-30 mt-1 max-h-60 w-20 rounded-md bg-white py-1 text-md font-bold shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                        <ListboxOption as="template" v-for="(m, mIdx) in modifiers" :key="`modifier-${tIdx}-${mIdx}`"
                          :value="m" v-slot="{ active, selected }">
                          <div
                            :class="[active ? 'bg-eucalyptus-100 text-eucalyptus-900' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-10 pr-4']">
                            <span :class="[selected ? 'text-eucalyptus-600' : 'text-gray-900']">{{ m }}</span>
                            <span v-if="selected"
                              class="absolute inset-y-0 left-0 flex items-center pl-3 text-eucalyptus-600">
                              <CheckIcon class="h-5 w-5" aria-hidden="true" />
                            </span>
                          </div>
                        </ListboxOption>
                      </ListboxOptions>
                    </transition>
                  </Listbox>
                  <img src="/img/bracket-divider.svg" class="h-5 mx-1" />
                  <CrosswalkSingleCombobox :current-field="term[1]" :schema="props.schemaSubject" :subject="true"
                    :extra="tIdx" @set-selection="watchSelectionTerm" />
                </div>
                <button @click.prevent="removeTerm(tIdx)" class="hover:text-sienna-600">
                  <MinusCircleIcon class="ml-10 w-5 h-5" />
                </button>
              </li>
            </ul>
          </div>
        </div>
      </PopoverPanel>
    </TransitionRoot>
  </Popover>
</template>

<script setup lang="ts">
import {
  Listbox, ListboxButton, ListboxOptions, ListboxOption, Popover, PopoverButton, PopoverPanel, TransitionRoot
} from "@headlessui/vue"
import { CheckIcon, ChevronDownIcon, ChevronUpDownIcon, MinusCircleIcon, PlusCircleIcon } from "@heroicons/vue/20/solid"
import { IActionModel, IKeyable, IResourceSchemaReference, IActionModifierType } from "@/interfaces"

const props = defineProps<{
  action: IActionModel,
  schemaSubject: IResourceSchemaReference,
  isSelect: boolean
}>()
const emit = defineEmits<{ setSelection: [selection: IKeyable] }>()
const selectedTerms = ref<[IActionModifierType, string][] | [string, IActionModifierType, string][]>([])
const modifiers: IActionModifierType[] = ["+", "-"]

function watchSelectionName(selection: IKeyable) {
  // isSelected
  if (selection && Object.keys(selection).length) {
    if (selection.extra !== null && props.isSelect) {
      selectedTerms.value[selection.extra][0] = selection.choice
    }
  }
}
function watchSelectionDate(selection: IKeyable) {
  // isSelected
  if (selection && Object.keys(selection).length) {
    if (selection.extra !== null && props.isSelect) {
      selectedTerms.value[selection.extra][2] = selection.choice
    }
  }
}
function watchSelectionTerm(selection: IKeyable) {
  if (selection && Object.keys(selection).length) {
    if (selection.extra !== null && !props.isSelect) {
      selectedTerms.value[selection.extra][1] = selection.choice
    }
  }
}

function validateSelectTerms() {
  if (!selectedTerms.value || selectedTerms.value.length === 0) return false
  let valid = true
  for (const term of selectedTerms.value) {
    if (
      !(term.length === 3
        && term[0]
        && term[1] === "+"
        && term[2])
    ) valid = false
  }
  return valid
}
function validateNonSelectTerms() {
  if (!selectedTerms.value || selectedTerms.value.length === 0) return false
  let valid = true
  for (const term of selectedTerms.value) {
    if (
      !(term.length === 2
        && modifiers.includes(term[0])
        && term[1])
    ) valid = false
  }
  return valid
}

function submitSelection() {
  if (
    (props.isSelect && validateSelectTerms())
    || validateNonSelectTerms()
  ) {
    let selection: IKeyable = {
      choice: selectedTerms.value,
      isSelect: props.isSelect
    }
    emit("setSelection", selection)
  }
}

function addTerm(): void {
  if (!selectedTerms.value) selectedTerms.value = [] as [IActionModifierType, string][] | [string, IActionModifierType, string][]
  let newTerm
  if (props.isSelect) newTerm = ["", "+", ""]
  else newTerm = ["", ""]
  selectedTerms.value.splice(selectedTerms.value.length, 1, newTerm)
}

function removeTerm(term: number): void {
  if (selectedTerms.value && selectedTerms.value.length) selectedTerms.value.splice(term, 1)
}

onMounted(async () => {
  if (props.action.uuid !== "") {
    if (props.isSelect) selectedTerms.value = props.action.sourceField as [string, IActionModifierType, string][]
    else selectedTerms.value = props.action.sourceField as [IActionModifierType, string][]
  }
})
</script>

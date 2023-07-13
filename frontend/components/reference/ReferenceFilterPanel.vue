<template>
  <Disclosure as="section" aria-labelledby="filter-heading" class="grid items-center my-2">
    <h2 id="filter-heading" class="sr-only">Filters</h2>
    <div class="col-start-1 row-start-1 py-4">
      <div class="relative flex justify-between items-center sm:ml-6 px-4 text-xs sm:px-6">
        <div class="items-center flex max-w-7xl space-x-3 divide-x divide-gray-200">
          <DisclosureButton class="group flex items-center font-medium text-gray-700 hover:text-ochre-600">
            <FunnelIcon class="mr-2 h-5 w-5 flex-none text-gray-400 group-hover:text-ochre-600" aria-hidden="true" />
            Filters
          </DisclosureButton>
          <div class="pl-3">
            <span class="sr-only">Reset filters</span>
            <button type="button" @click="resetFilters" class="text-gray-500 hover:text-ochre-600">Clear</button>
          </div>
        </div>
        <div class="flex items-center justify-center sm:mx-4 px-2 w-full">
          <div class="w-full">
            <label for="search" class="sr-only">Search</label>
            <div class="relative">
              <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
              </div>
              <input id="search" name="search"
                class="block w-full rounded-md border-0 bg-white py-1.5 pl-10 pr-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6"
                placeholder="Search" type="search" />
            </div>
          </div>
        </div>
        <button type="button" @click="refreshReferences" class="group inline-flex justify-center">
          <ArrowPathIcon class="-mr-1 ml-1 mt-1 h-5 w-5 flex-shrink-0 text-gray-400 group-hover:text-ochre-600"
            aria-hidden="true" />
          <span class="sr-only">Refresh activites</span>
        </button>
      </div>
    </div>
    <DisclosurePanel class="border-t border-gray-200 py-5">
      <div class="mx-auto text-xs sm:text-sm px-8 space-y-4">
        <fieldset>
          <legend class="block font-bold">Reference type</legend>
          <div class="space-y-4 pt-4">
            <div class="grid auto-rows-min grid-cols-4 gap-y-2 md:gap-x-3">
              <div v-for="(option, optionIdx) in options.reference" :key="option.value" class="flex items-center">
                <input :id="`reference-${optionIdx}`" name="reference" :value="option.value" type="radio"
                  v-model="filters.reference_type"
                  class="h-4 w-4 flex-shrink-0 rounded-full border-gray-300 text-ochre-600 focus:ring-ochre-500"
                  :checked="option.value === filters.reference_type" />
                <label :for="`reference-${optionIdx}`" class="ml-3 min-w-0 flex-1 text-gray-600">{{
                  capitalizeFirst(option.value) }}</label>
              </div>
            </div>
          </div>
        </fieldset>
        <fieldset>
          <legend class="block font-bold">Data file type</legend>
          <div class="space-y-4 pt-4">
            <div class="grid auto-rows-min grid-cols-3 gap-y-2 md:grid-cols-5 md:gap-x-3">
              <div v-for="(option, optionIdx) in options.mime" :key="option.value" class="flex items-center">
                <input :id="`mime-${optionIdx}`" name="mime" :value="option.value" type="radio"
                  v-model="filters.mime_type"
                  class="h-4 w-4 flex-shrink-0 rounded-full border-gray-300 text-ochre-600 focus:ring-ochre-500"
                  :checked="option.value === filters.mime_type" />
                <label :for="`mime-${optionIdx}`" class="ml-3 min-w-0 flex-1 text-gray-600">{{
                  option.value }}</label>
              </div>
            </div>
          </div>
        </fieldset>
        <fieldset>
          <legend class="block font-bold pb-4">Date range</legend>
          <div class="flex space-x-4 items-center">
            <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateFrom" />
            <span class="text-gray-600">to</span>
            <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateTo" />
          </div>
        </fieldset>
        <fieldset>
          <legend class="block font-bold">Research responsbility</legend>
          <div class="space-y-4 pt-4">
            <div class="grid auto-rows-min grid-cols-4 gap-y-2 md:gap-x-3">
              <div v-for="(option, optionIdx) in options.responsibility" :key="option.value" class="flex items-center">
                <input :id="`responsibility-${optionIdx}`" name="responsibility" :value="option.value" type="radio"
                  v-model="filters.responsibility"
                  class="h-4 w-4 flex-shrink-0 rounded-full border-gray-300 text-ochre-600 focus:ring-ochre-500"
                  :checked="option.value === filters.responsibility" />
                <label :for="`reference-${optionIdx}`" class="ml-3 min-w-0 flex-1 text-gray-600">{{
                  capitalizeFirst(option.value) }}</label>
              </div>
            </div>
          </div>
        </fieldset>
      </div>
      <div class="flex flex-row justify-end pt-4">
        <button type="submit" @click="refreshReferences"
          class="w-20 justify-center rounded-md border border-transparent bg-ochre-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-ochre-700 focus:outline-none focus:ring-2 focus:ring-ochre-600 focus:ring-offset-2">
          Filter
        </button>
      </div>
    </DisclosurePanel>
  </Disclosure>
</template>

<script setup lang="ts">
import VueTailwindDatepicker from "vue-tailwind-datepicker"
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import { ArrowPathIcon, FunnelIcon, MagnifyingGlassIcon } from "@heroicons/vue/24/outline"
import { capitalizeFirst } from "@/utilities"
import { useReferenceStore } from "@/stores"
import { IReferenceFilters } from "@/interfaces"

const referenceStore = useReferenceStore()
const filters = ref({} as IReferenceFilters)
const dateFrom = ref("")
const dateTo = ref("")
const formatter = ref({
  date: "YYYY-MM-DD",
  month: "MMM"
})
const options = {
  reference: [
    { value: "DATA" },
    { value: "SCHEMA" },
    { value: "CROSSWALK" },
    { value: "TRANSFORM" },
  ],
  responsibility: [
    { value: "SEEKER" },
    { value: "WRANGLER" },
    { value: "CURATOR" },
    { value: "CUSTODIAN" },
  ],
  mime: [
    { value: "CSV" },
    { value: "XLS" },
    { value: "XLSX" },
    { value: "PARQUET" },
    { value: "FEATHER" },
  ]
}

async function refreshReferences() {
  if (dateFrom.value && dateTo.value && dateFrom.value >= dateTo.value) dateTo.value = ""
  if (dateFrom.value) filters.value.date_from = dateFrom.value
  if (dateTo.value) filters.value.date_to = dateTo.value
  referenceStore.setFilters(filters.value)
  getFilters()
  await referenceStore.getMulti()
}

function getFilters() {
  filters.value = { ...referenceStore.filters }
  dateFrom.value = ""
  dateTo.value = ""
  if (filters.value.date_from) dateFrom.value = filters.value.date_from
  if (filters.value.date_to) dateTo.value = filters.value.date_to
}

async function resetFilters() {
  referenceStore.resetFilters()
  getFilters()
  await refreshReferences()
}

onMounted(async () => {
  getFilters()
})

</script>
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
        <button type="button" @click="refreshResources" class="group inline-flex justify-center">
          <ArrowPathIcon class="-mr-1 ml-1 mt-1 h-5 w-5 flex-shrink-0 text-gray-400 group-hover:text-ochre-600"
            aria-hidden="true" />
          <span class="sr-only">Refresh activites</span>
        </button>
      </div>
    </div>
    <DisclosurePanel class="border-t border-gray-200 py-5">
      <div class="mx-auto text-xs sm:text-sm px-8 space-y-4">
        <fieldset>
          <legend class="block font-bold">State</legend>
          <div class="space-y-4 pt-4">
            <!-- <div class="mx-auto grid max-w-7xl grid-cols-4 gap-x-4 px-4 text-sm sm:px-6 md:gap-x-6 lg:px-8"> -->
            <div class="grid auto-rows-min grid-cols-3 gap-y-2 md:grid-cols-4 md:gap-x-3">
              <div v-for="(option, optionIdx) in options.state" :key="option.value" class="flex items-center">
                <input :id="`state-${optionIdx}`" name="state" :value="option.value" type="radio" v-model="filters.state"
                  class="h-4 w-4 flex-shrink-0 rounded-full border-gray-300 text-ochre-600 focus:ring-ochre-500"
                  :checked="option.value === filters.state" />
                <label :for="`state-${optionIdx}`" class="ml-3 min-w-0 flex-1 text-gray-600">{{ option.label }}</label>
              </div>
            </div>
          </div>
        </fieldset>
        <fieldset>
          <legend class="block font-bold pb-4">Date range</legend>
          <div class="flex space-x-4 items-center pb-4">
            <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateFrom" />
            <span class="text-gray-600">to</span>
            <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateTo" />
          </div>
        </fieldset>
      </div>
      <div class="flex flex-row justify-end">
        <button type="submit" @click="refreshResources"
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
import { useResourceStore } from "@/stores"
import { IResourceFilters } from "@/interfaces"

const resourceStore = useResourceStore()
const filters = ref({} as IResourceFilters)
const dateFrom = ref("")
const dateTo = ref("")
const formatter = ref({
  date: "YYYY-MM-DD",
  month: "MMM"
})
const options = {
  state: [
    { value: "BUSY", label: "Busy" },
    { value: "READY", label: "Ready" },
    { value: "DATA_READY", label: "Data Ready" },
    { value: "SCHEMA_READY", label: "Schema Ready" },
    { value: "CROSSWALK_READY", label: "Crosswalk Ready" },
    { value: "TRANSFORM_READY", label: "Transform Ready" },
    { value: "IMPORT_ERROR", label: "Import Ready" },
    { value: "DATA_ERROR", label: "Data Error" },
    { value: "SCHEMA_ERROR", label: "Schema Error" },
    { value: "CROSSWALK_ERROR", label: "Crosswalk Error" },
    { value: "TRANSFORM_ERROR", label: "Transform Error" },
    { value: "ERROR", label: "Error" },
    { value: "COMPLETE", label: "Complete" },
  ],
}

async function refreshResources() {
  if (dateFrom.value && dateTo.value && dateFrom.value >= dateTo.value) dateTo.value = ""
  if (dateFrom.value) filters.value.date_from = dateFrom.value
  if (dateTo.value) filters.value.date_to = dateTo.value
  resourceStore.setFilters(filters.value)
  getFilters()
  await resourceStore.getMulti()
}

function getFilters() {
  filters.value = { ...resourceStore.filters }
  dateFrom.value = ""
  dateTo.value = ""
  if (filters.value.date_from) dateFrom.value = filters.value.date_from
  if (filters.value.date_to) dateTo.value = filters.value.date_to
}

async function resetFilters() {
  resourceStore.resetFilters()
  getFilters()
  await refreshResources()
}

onMounted(async () => {
  getFilters()
})

</script>
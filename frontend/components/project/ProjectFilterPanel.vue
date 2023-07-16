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
              <input id="search" name="search" v-model="searchTerm" @keydown="watchSearchTerm"
                class="block w-full rounded-md border-0 bg-white py-1.5 pl-10 pr-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6"
                placeholder="Search" type="search" />
            </div>
          </div>
        </div>
        <button type="button" @click="refreshProjects" class="group inline-flex justify-center">
          <ArrowPathIcon class="-mr-1 ml-1 mt-1 h-5 w-5 flex-shrink-0 text-gray-400 group-hover:text-ochre-600"
            aria-hidden="true" />
          <span class="sr-only">Refresh projects</span>
        </button>
      </div>
    </div>
    <DisclosurePanel class="border-t border-gray-200 py-5">
      <div class="mx-auto text-xs sm:text-sm px-8 space-y-4">
        <fieldset>
          <legend class="block font-bold pb-4">Date range</legend>
          <div class="flex space-x-4 items-center">
            <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateFrom" />
            <span class="text-gray-600">to</span>
            <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateTo" />
          </div>
        </fieldset>
      </div>
      <div class="flex flex-row justify-end pt-4">
        <button type="submit" @click="refreshProjects"
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
import { useProjectStore } from "@/stores"
import { IProjectFilters } from "@/interfaces"

const projectStore = useProjectStore()
const filters = ref({} as IProjectFilters)
const searchTerm = ref("")
const dateFrom = ref("")
const dateTo = ref("")
const formatter = ref({
  date: "YYYY-MM-DD",
  month: "MMM"
})

function watchSearchTerm(event: any) {
  if (event.key === "Enter") refreshProjects()
}

async function refreshProjects() {
  filters.value.match = searchTerm.value
  if (dateFrom.value && dateTo.value && dateFrom.value >= dateTo.value) dateTo.value = ""
  if (dateFrom.value) filters.value.date_from = dateFrom.value
  if (dateTo.value) filters.value.date_to = dateTo.value
  projectStore.setFilters(filters.value)
  getFilters()
  await projectStore.getMulti()
}

function getFilters() {
  filters.value = { ...projectStore.filters }
  dateFrom.value = ""
  dateTo.value = ""
  if (filters.value.date_from) dateFrom.value = filters.value.date_from
  if (filters.value.date_to) dateTo.value = filters.value.date_to
  if (filters.value.match) searchTerm.value = filters.value.match
}

async function resetFilters() {
  projectStore.resetFilters()
  getFilters()
  await refreshProjects()
}

onMounted(async () => {
  getFilters()
})

</script>
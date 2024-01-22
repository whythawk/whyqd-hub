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
        <button type="button" @click="refreshActivities" class="group inline-flex justify-center">
          <ArrowPathIcon class="-mr-1 ml-1 mt-1 h-5 w-5 flex-shrink-0 text-gray-400 group-hover:text-ochre-600"
            aria-hidden="true" />
          <span class="sr-only">Refresh tasks</span>
        </button>
      </div>
    </div>
    <DisclosurePanel class="border-t border-gray-200 py-5">
      <div class="mx-auto text-xs sm:text-sm px-8 space-y-4">
        <div class="grid auto-rows-min grid-cols-1 gap-y-10 md:grid-cols-2 md:gap-x-6">
          <fieldset>
            <legend class="block font-bold">Accrual policy</legend>
            <div class="space-y-4 pt-1">
              <Listbox v-model="filters.accrualPolicy">
                <div class="relative mt-1">
                  <ListboxButton
                  class="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-500 sm:text-sm">
                  <span v-if="filters.accrualPolicy" class="block truncate">{{ getSelectedLabel(options.accrualPolicy, filters.accrualPolicy as string) }}</span>
                  <span v-else class="block truncate">Select...</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                      <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </span>
                  </ListboxButton>
                  <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                  leave-to-class="opacity-0">
                  <ListboxOptions
                      class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption v-slot="{ active, selected }" v-for="(option, optionIdx) in options.accrualPolicy"
                    :key="`accrual-policy-${optionIdx}`" :value="option.value" as="template">
                      <li :class="[
                          active ? 'bg-ochre-100 text-ochre-900' : 'text-gray-900',
                          'relative cursor-default select-none py-2 pl-10 pr-4',
                      ]">
                          <span :class="[
                          selected ? 'font-medium' : 'font-normal',
                          'block truncate',
                          ]">{{ option.label }}</span>
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
          </fieldset>
          <fieldset>
            <legend class="block font-bold">Accrual periodicity</legend>
            <div class="space-y-4 pt-1">
              <Listbox v-model="filters.accrualPeriodicity">
                <div class="relative mt-1">
                  <ListboxButton
                  class="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-500 sm:text-sm">
                  <span v-if="filters.accrualPeriodicity" class="block truncate">{{ getSelectedLabel(options.accrualPeriodicity, filters.accrualPeriodicity as string) }}</span>
                  <span v-else class="block truncate">Select...</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                      <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </span>
                  </ListboxButton>
                  <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                  leave-to-class="opacity-0">
                  <ListboxOptions
                      class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption v-slot="{ active, selected }" v-for="(option, optionIdx) in options.accrualPeriodicity"
                    :key="`accrual-policy-${optionIdx}`" :value="option.value" as="template">
                      <li :class="[
                          active ? 'bg-ochre-100 text-ochre-900' : 'text-gray-900',
                          'relative cursor-default select-none py-2 pl-10 pr-4',
                      ]">
                          <span :class="[
                          selected ? 'font-medium' : 'font-normal',
                          'block truncate',
                          ]">{{ option.label }}</span>
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
          </fieldset>
        </div>
        <fieldset>
            <legend class="block font-bold pb-2">Date range</legend>
            <div class="flex space-x-4 items-center">
                <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateFrom" />
                <span class="text-gray-600">to</span>
                <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateTo" />
            </div>
        </fieldset>
        <fieldset>
          <legend class="block font-bold">Schedule flags</legend>
          <div class="flex space-x-16">
            <div class="relative flex items-start pt-4">
              <div class="flex h-6 items-center">
                <input id="alerts" name="alerts" type="checkbox" v-model="filters.scheduled"
                  class="h-4 w-4 rounded border-gray-300 text-ochre-600 focus:ring-ochre-600" />
              </div>
              <div class="ml-3 leading-6">
                <label for="alerts" class="font-medium text-gray-600">Scheduled only</label>
              </div>
            </div>
            <div class="relative flex items-start pt-4">
              <div class="flex h-6 items-center">
                <input id="alerts" name="alerts" type="checkbox" v-model="filters.prioritised"
                  class="h-4 w-4 rounded border-gray-300 text-ochre-600 focus:ring-ochre-600" />
              </div>
              <div class="ml-3 leading-6">
                <label for="alerts" class="font-medium text-gray-600">Prioritised</label>
              </div>
            </div>
          </div>
        </fieldset>
      </div>
      <div class="flex flex-row justify-end pt-4">
        <button type="submit" @click="refreshActivities"
          class="w-20 justify-center rounded-md border border-transparent bg-ochre-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-ochre-700 focus:outline-none focus:ring-2 focus:ring-ochre-600 focus:ring-offset-2">
          Filter
        </button>
      </div>
    </DisclosurePanel>
  </Disclosure>
</template>

<script setup lang="ts">
import VueTailwindDatepicker from "vue-tailwind-datepicker"
import { Disclosure, DisclosureButton, DisclosurePanel, Listbox, ListboxButton, ListboxOptions, ListboxOption, Switch } from "@headlessui/vue"
import { ArrowPathIcon, FunnelIcon, MagnifyingGlassIcon, CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/24/outline"
import { useTaskStore } from "@/stores"
import { ITaskFilters, IKeyable } from "@/interfaces"

const route = useRoute()
const taskStore = useTaskStore()
const filters = ref({} as ITaskFilters)
const appropriateMulti = ref("TASK")
const searchTerm = ref("")
const dateFrom = ref("")
const dateTo = ref("")
const formatter = ref({
  date: "YYYY-MM-DD",
  month: "MMM"
})

const options: IKeyable = {
accrualPolicy: [
  { value: "closed", label: "Closed" },
  { value: "passive", label: "Passive" },
  { value: "active", label: "Active" },
  { value: "partial", label: "Partial" },
],
accrualPeriodicity: [
  { value: "continuous", label: "Continuous" },
  { value: "daily", label: "Daily" },
  { value: "weekly", label: "Weekly" },
  { value: "threeTimesAWeek", label: "Three times a week" },
  { value: "semiweekly", label: "Semi-weekly" },
  { value: "biweekly", label: "Bi-weekly" },
  { value: "monthly", label: "Monthly" },
  { value: "threeTimesAMonth", label: "Three times a month" },
  { value: "semimonthly", label: "Semi-monthly" },
  { value: "annual", label: "Annual" },
  { value: "semiannual", label: "Semi-annual" },
  { value: "threeTimesAYear", label: "Three times a year" },
  { value: "bimonthly", label: "Bi-monthly" },
  { value: "quarterly", label: "Quarterly" },
  { value: "biennial", label: "Biennial" },
  { value: "triennial", label: "Triennial" },
  { value: "irregular", label: "Irregular" },
]
}

function watchSearchTerm(event: any) {
  if (event.key === "Enter") refreshActivities()
}

async function getAppropriateMulti() {
  switch (appropriateMulti.value) {
    case "SCHEDULE":
      await taskStore.getScheduledMulti()
      break
    case "SCHEDULEPROJECT":
      await taskStore.getScheduledMultiByProject(route.params.id as string)
      break
  }
}

async function refreshActivities() {
  filters.value.match = searchTerm.value
  if (dateFrom.value && dateTo.value && dateFrom.value >= dateTo.value) dateTo.value = ""
  if (dateFrom.value) filters.value.date_from = dateFrom.value
  if (dateTo.value) filters.value.date_to = dateTo.value
  taskStore.setFilters(filters.value)
  getFilters()
  await getAppropriateMulti()
}

function getFilters() {
  filters.value = { ...taskStore.filters }
  if (typeof filters.value.prioritised === "undefined") filters.value.prioritised = true
  dateFrom.value = ""
  dateTo.value = ""
  if (filters.value.date_from) dateFrom.value = filters.value.date_from
  if (filters.value.date_to) dateTo.value = filters.value.date_to
  if (filters.value.match) searchTerm.value = filters.value.match
}

async function resetFilters() {
  searchTerm.value = ""
  taskStore.resetFilters()
  getFilters()
  await refreshActivities()
}

function getSelectedLabel(optionList: IKeyable[], selected: string) {
  const selection = optionList.find(o => { return o.value === selected })
  if (selection) return selection.label
  else return "Select ..."
}

onMounted(async () => {
  if (route.path.includes("/schedule")) appropriateMulti.value = "SCHEDULE"
  if (route.path.includes("/schedule/project/")) appropriateMulti.value = "SCHEDULEPROJECT"
  getFilters()
})

</script>
<template>
  <div v-if="draft" class="mx-auto min-w-full">
    <CommonHeadingEditView v-if="projectStore.term.name" purpose="Project" :name="projectStore.draft.name"
      :title="projectStore.draft.title" :approach="saveApproach" @set-edit-request="watchEditHeadingRequest" />
    <form class="flex-auto rounded-lg p-3">
      <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
        <div class="col-span-full">
          <label for="project-title" class="block text-sm font-semibold leading-6 text-gray-900">Title</label>
          <div class="mt-2">
            <input type="text" name="project-title" id="project-title" v-model="draft.title"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p v-if="draft.name" class="mt-2 text-xs leading-6 text-gray-500">
            <span class="font-bold">Machine-readable name: </span>{{ draft.name }}
          </p>
        </div>
        <div class="col-span-full">
          <label for="description" class="block text-sm font-semibold leading-6 text-gray-900">Description</label>
          <div class="mt-2">
            <textarea id="description" name="description" rows="3" v-model="draft.description"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">A complete description of the project. Try and be as helpful as
            possible to 'future-you'.</p>
        </div>
        <div class="col-span-full">
          <label for="project-subject-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Subjects
          </label>
          <div class="mt-2">
            <input type="text" name="project-subject-values" id="project-subject-values" v-model="subjects"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">A list of topics of the project. Comma-separated.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-frequency-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Frequency
          </label>
          <div class="mt-2">
            <input type="text" name="project-frequency-values" id="project-frequency-values" v-model="draft.frequency"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            The temporal frequency of update of the project.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-spatial-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Spatial
          </label>
          <div class="mt-2">
            <input type="text" name="project-spatial-values" id="project-spatial-values" v-model="draft.spatial"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            Spatial characteristics of the project.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-temporal-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Temporal range
          </label>
          <div class="mt-2">
            <div class="flex space-x-4 items-center">
              <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateFrom" />
              <span class="text-gray-600">to</span>
              <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateTo" />
            </div>
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            Temporal range of the project.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-language-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Language
          </label>
          <div class="mt-2">
            <input type="text" name="project-language-values" id="project-language-values" v-model="draft.language"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            Specify the language of the creative work. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-creator-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Creator
          </label>
          <div class="mt-2">
            <input type="text" name="project-creator-values" id="project-creator-values" v-model="draft.creator"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            An entity primarily responsible for making the project.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-contributor-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Contributor
          </label>
          <div class="mt-2">
            <input type="text" name="project-contributor-values" id="project-contributor-values"
              v-model="draft.contributor"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            An entity responsible for making contributions to the project.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-publisher-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Publisher
          </label>
          <div class="mt-2">
            <input type="text" name="project-publisher-values" id="project-publisher-values" v-model="draft.publisher"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            An entity responsible for making the resource available.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-rights-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Rights
          </label>
          <div class="mt-2">
            <input type="text" name="project-rights-values" id="project-rights-values" v-model="draft.rights"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            Information about rights held in and over the project.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-source-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Source
          </label>
          <div class="mt-2">
            <input type="text" name="project-source-values" id="project-source-values" v-model="draft.source"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            A related resource from which the described resource is derived.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-access-rights-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Access rights
          </label>
          <div class="mt-2">
            <input type="text" name="project-access-rights-values" id="project-access-rights-values"
              v-model="draft.accessRights"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            Information about who may access the resource or an indication of its security status.
          </p>
        </div>

        <div class="col-span-full">
          <label for="project-accrual-method-values" class="block text-sm font-semibold leading-6 text-gray-900">Accrual
            method</label>
          <div class="mt-2">
            <Listbox v-model="draft.accrualMethod">
              <div class="relative mt-1">
                <ListboxButton
                  class="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-ochre-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-ochre-300 sm:text-sm">
                  <span v-if="draft.accrualMethod" class="block truncate">{{ capitalizeFirst(draft.accrualMethod)
                  }}</span>
                  <span v-else class="block truncate">Select...</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </span>
                </ListboxButton>
                <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                  leave-to-class="opacity-0">
                  <ListboxOptions
                    class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption v-slot="{ active, selected }" v-for="mtype in parameters.accrualType"
                      :key="`mtype-${mtype.value}`" :value="mtype.value" as="template">
                      <li :class="[
                        active ? 'bg-ochre-100 text-ochre-900' : 'text-gray-900',
                        'relative cursor-default select-none py-2 pl-10 pr-4',
                      ]">
                        <span :class="[
                          selected ? 'font-medium' : 'font-normal',
                          'block truncate',
                        ]">{{ capitalizeFirst(mtype.value) }}</span>
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
          <p class="mt-2 text-sm leading-6 text-gray-600">
            The method by which items are added to a resource.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-accrual-periodicity-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Accrual periodicity
          </label>
          <div class="mt-2">
            <Listbox v-model="draft.accrualPeriodicity">
              <div class="relative mt-1">
                <ListboxButton
                  class="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-ochre-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-ochre-300 sm:text-sm">
                  <span v-if="draft.accrualPeriodicity" class="block truncate">{{
                    capitalizeFirst(draft.accrualPeriodicity)
                  }}</span>
                  <span v-else class="block truncate">Select...</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </span>
                </ListboxButton>
                <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                  leave-to-class="opacity-0">
                  <ListboxOptions
                    class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption v-slot="{ active, selected }" v-for="ftype in parameters.frequencyType"
                      :key="`ftype-${ftype.value}`" :value="ftype.value" as="template">
                      <li :class="[
                        active ? 'bg-ochre-100 text-ochre-900' : 'text-gray-900',
                        'relative cursor-default select-none py-2 pl-10 pr-4',
                      ]">
                        <span :class="[
                          selected ? 'font-medium' : 'font-normal',
                          'block truncate',
                        ]">{{ capitalizeFirst(ftype.value) }}</span>
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
          <p class="mt-2 text-sm leading-6 text-gray-600">
            The frequency with which items are added to a resource.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-accrual-policy-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Accrual policy
          </label>
          <div class="mt-2">
            <Listbox v-model="draft.accrualPolicy">
              <div class="relative mt-1">
                <ListboxButton
                  class="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-ochre-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-ochre-300 sm:text-sm">
                  <span v-if="draft.accrualPolicy" class="block truncate">{{ capitalizeFirst(draft.accrualPolicy)
                  }}</span>
                  <span v-else class="block truncate">Select...</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </span>
                </ListboxButton>
                <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                  leave-to-class="opacity-0">
                  <ListboxOptions
                    class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption v-slot="{ active, selected }" v-for="ptype in parameters.accrualPolicyType"
                      :key="`ptype-${ptype.value}`" :value="ptype.value" as="template">
                      <li :class="[
                        active ? 'bg-ochre-100 text-ochre-900' : 'text-gray-900',
                        'relative cursor-default select-none py-2 pl-10 pr-4',
                      ]">
                        <span :class="[
                          selected ? 'font-medium' : 'font-normal',
                          'block truncate',
                        ]">{{ capitalizeFirst(ptype.value) }}</span>
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
          <p class="mt-2 text-sm leading-6 text-gray-600">
            The policy governing the addition of items to a resource.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-bibliographic-citation-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Bibliographic citation
          </label>
          <div class="mt-2">
            <input type="text" name="project-bibliographic-citation-values" id="project-bibliographic-citation-values"
              v-model="draft.bibliographicCitation"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            A bibliographic reference for the project.
          </p>
        </div>
        <div class="col-span-full">
          <label for="project-conforms-to-values" class="block text-sm font-semibold leading-6 text-gray-900">
            Conforms to
          </label>
          <div class="mt-2">
            <input type="text" name="project-conforms-to-values" id="project-conforms-to-values"
              v-model="draft.conformsTo"
              class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:text-sm sm:leading-6" />
          </div>
          <p class="mt-2 text-sm leading-6 text-gray-500">
            An established standard to which the described resource conforms.
          </p>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import VueTailwindDatepicker from "vue-tailwind-datepicker"
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, } from "@headlessui/vue"
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/20/solid"
import { nameSpace, capitalizeFirst } from "@/utilities"
import { IProject } from "@/interfaces"
import { useProjectStore } from "@/stores"
import * as dayjs from "dayjs"

const route = useRoute()
const projectStore = useProjectStore()
const draft = ref({} as IProject)
const saveApproach = ref("Create")
const subjects = ref("")
const dateFrom = ref("")
const dateTo = ref("")
const formatter = ref({
  date: "YYYY-MM-DD",
  month: "MMM"
})

const parameters = {
  accrualPolicyType: [
    { value: "closed" },
    { value: "passive" },
    { value: "active" },
    { value: "partial" },
  ],
  accrualType: [
    { value: "deposit" },
    { value: "donation" },
    { value: "purchase" },
    { value: "loan" },
    { value: "license" },
    { value: "itemCreation" },
  ],
  frequencyType: [
    { value: "triennial" },
    { value: "biennial" },
    { value: "annual" },
    { value: "semiannual" },
    { value: "threeTimesAYear" },
    { value: "quarterly" },
    { value: "bimonthly" },
    { value: "monthly" },
    { value: "semimonthly" },
    { value: "biweekly" },
    { value: "threeTimesAMonth" },
    { value: "weekly" },
    { value: "semiweekly" },
    { value: "threeTimesAWeek" },
    { value: "daily" },
    { value: "continuous" },
    { value: "irregular" },
  ]
}

async function watchEditHeadingRequest(request: string) {
  switch (request) {
    case "reset":
      resetForm()
      break
    case "save":
      submitRequest()
      break
    case "cancel":
      return await navigateTo(`/projects/${route.params.id}`)
  }
}

function resetDraft() {
  draft.value = { ...projectStore.draft }
  dateFrom.value = ""
  dateTo.value = ""
  if (draft.value.temporalStart) dateFrom.value = draft.value.temporalStart.split("T")[0]
  if (draft.value.temporalEnd) dateTo.value = draft.value.temporalEnd.split("T")[0]
  if (draft.value.subjects && draft.value.subjects.length) subjects.value = draft.value.subjects.join(", ")
  if (draft.value.title) draft.value.name = nameSpace(draft.value.title)
}

function resetForm() {
  if (saveApproach.value === "Update") projectStore.setDraft({ ...projectStore.term })
  resetDraft()
}

async function submitRequest() {
  // https://stackoverflow.com/a/38201551/295606
  if (subjects.value) draft.value.subjects = subjects.value.split(",").map((item: string) => item.trim())
  if (dateFrom.value && dateTo.value && dateFrom.value >= dateTo.value) dateTo.value = ""
  if (dateFrom.value) draft.value.temporalStart = dayjs(dateFrom.value).format()
  if (dateTo.value) draft.value.temporalEnd = dayjs(dateTo.value).format()
  if (draft.value.title) draft.value.name = nameSpace(draft.value.title)
  projectStore.setDraft(draft.value)
  if (saveApproach.value === "Update" && draft.value.id)
    await projectStore.updateTerm(draft.value.id)
  else await projectStore.createTerm()
  return await navigateTo(`/projects/${projectStore.term.id}`)
}

onMounted(async () => {
  if (route.params.id !== "create") saveApproach.value = "Update"
  if (projectStore.draft && Object.keys(projectStore.draft).length !== 0) resetDraft()
  else resetForm()
})

onBeforeRouteLeave((to, from, next) => {
  projectStore.setDraft(draft.value)
  next()
})
</script>
<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <CommonHeadingView v-if="taskStore.term.name" purpose="Task" :name="taskStore.term.name"
        :title="taskStore.term.title" @set-edit-request="watchHeadingRequest" />
      <dl class="divide-y divide-gray-100">
        <div class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Name</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.name }}</dd>
        </div>
        <div v-if="taskStore.term.title" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Title</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.title }}</dd>
        </div>
        <div v-if="taskStore.term.description" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Description</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.description }}
          </dd>
        </div>
        <div v-if="taskStore.term.frequency" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Frequency</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.frequency }}
          </dd>
        </div>
        <div v-if="taskStore.term.spatial" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Spatial characteristics</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.spatial }}
          </dd>
        </div>
        <div v-if="taskStore.term.temporalStart || taskStore.term.temporalEnd"
          class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Temporal range</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
            <span v-if="taskStore.term.temporalStart">{{ readableDate(taskStore.term.temporalStart) }}</span>
            &mdash;
            <span v-if="taskStore.term.temporalEnd">{{ readableDate(taskStore.term.temporalEnd) }}</span>
          </dd>
        </div>
        <div v-if="taskStore.term.language" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Language</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.language }}
          </dd>
        </div>
        <div v-if="taskStore.term.creator" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Primary creator</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.creator }}
          </dd>
        </div>
        <div v-if="taskStore.term.contributor" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Contributor</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.contributor }}
          </dd>
        </div>
        <div v-if="taskStore.term.publisher" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Publisher</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.publisher }}
          </dd>
        </div>
        <div v-if="taskStore.term.rights" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Rights held</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.rights }}
          </dd>
        </div>
        <div v-if="taskStore.term.source" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Source</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.source }}
          </dd>
        </div>
        <div v-if="taskStore.term.accessRights" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Access and security</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.accessRights }}
          </dd>
        </div>
        <div v-if="taskStore.term.accrualMethod" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Accrual method</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.accrualMethod }}
          </dd>
        </div>
        <div v-if="taskStore.term.accrualPeriodicity" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Accrual periodicity</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
            {{ taskStore.term.accrualPeriodicity }}
          </dd>
        </div>
        <div v-if="taskStore.term.accrualPolicy" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Accrual policy</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.accrualPolicy }}
          </dd>
        </div>
        <div v-if="taskStore.term.bibliographicCitation" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Bibliographic reference</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
            {{ taskStore.term.bibliographicCitation }}
          </dd>
        </div>
        <div v-if="taskStore.term.conformsTo" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-900">Standard conforms to</dt>
          <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ taskStore.term.conformsTo }}
          </dd>
        </div>
      </dl>
    </div>
    <div class="space-y-2 mx-2">
      <h2 class="text-sm font-semibold leading-7 text-gray-900 pt-2">Project, resources, templates and schema object
      </h2>
      <div v-if="taskStore.term.project && Object.keys(taskStore.term.project).length !== 0" class="space-y-6">
        <NuxtLink :to="`/projects/${taskStore.term.project.id}`">
          <CommonSummaryCard :summary="taskStore.term.project" :show-state="false" />
        </NuxtLink>
      </div>
      <div v-else class="space-y-6">
        <NuxtLink to="/projects"
          class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold text-sm">
          <BeakerIcon class="text-sienna-700 group-hover:text-ochre-600 h-5 w-5 shrink-0" aria-hidden="true" />
          <span class="hidden lg:block">Add to project</span>
        </NuxtLink>
      </div>
      <NuxtLink :to="`/resources/task/${taskStore.term.id}`"
        class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold text-sm">
        <RectangleGroupIcon class="text-gray-700 group-hover:text-ochre-600 h-5 w-5 shrink-0" aria-hidden="true" />
        <span class="hidden lg:block">Resources</span>
      </NuxtLink>
      <div v-if="taskStore.term.datasource && Object.keys(taskStore.term.datasource).length !== 0" class="space-y-6">
        <NuxtLink :to="`/datasource/${taskStore.term.datasource.id}`">
          <CommonSummaryCard :summary="taskStore.term.datasource" :show-state="false" />
        </NuxtLink>
      </div>
      <div v-else class="space-y-6">
        <button class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold text-sm">
          <TableCellsIcon class="text-sienna-700 group-hover:text-ochre-600 h-5 w-5 shrink-0" aria-hidden="true" />
          <span class="hidden lg:block">Add data source template</span>
        </button>
      </div>
      <div v-if="taskStore.term.crosswalk && Object.keys(taskStore.term.crosswalk).length !== 0" class="space-y-6">
        <NuxtLink :to="`/crosswalk/${taskStore.term.crosswalk.id}`">
          <CommonSummaryCard :summary="taskStore.term.crosswalk" :show-state="false" />
        </NuxtLink>
      </div>
      <div v-else class="space-y-6">
        <button class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold text-sm">
          <ArrowsRightLeftIcon class="text-sienna-700 group-hover:text-ochre-600 h-5 w-5 shrink-0" aria-hidden="true" />
          <span class="hidden lg:block">Add crosswalk template</span>
        </button>
      </div>
      <div v-if="taskStore.term.schema && Object.keys(taskStore.term.schema).length !== 0" class="space-y-6">
        <div class="flex flex-row justify-between items-center">
          <NuxtLink :to="`/schema/${taskStore.term.schema.id}`">
            <CommonSummaryCard :summary="taskStore.term.schema" :show-state="false" />
          </NuxtLink>
          <button type="button" @click.prevent="removeSchema"
            class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold text-sm">
            <TrashIcon class="text-sienna-700 group-hover:text-ochre-600 h-5 w-5 shrink-0" aria-hidden="true" />
            <span class="hidden lg:block">Remove schema</span>
          </button>
        </div>
      </div>
      <div v-else class="space-y-6">
        <button type="button" @click.prevent="schemaRedirect"
          class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold text-sm">
          <SquaresPlusIcon class="text-sienna-700 group-hover:text-ochre-600 h-5 w-5 shrink-0" aria-hidden="true" />
          <span class="hidden lg:block">Add schema</span>
        </button>
      </div>
    </div>
    <div v-if="citation && Object.keys(citation).length !== 0" class="space-y-2 mx-2">
      <CommonCitationCard :citation="citation" />
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ArrowsRightLeftIcon,
  BeakerIcon,
  RectangleGroupIcon,
  SquaresPlusIcon,
  TableCellsIcon,
  TrashIcon
} from "@heroicons/vue/24/outline"
import { readableDate } from "@/utilities"
import { ICitation, IReferenceFilters } from "@/interfaces"
import { useSettingStore, useTaskStore, useReferenceStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const appSettings = useSettingStore()
const route = useRoute()
const taskStore = useTaskStore()
const citation = ref({} as ICitation)

async function watchHeadingRequest(request: string) {
  switch (request) {
    case "remove":
      await taskStore.removeTerm(route.params.id as string)
      return await navigateTo("/tasks")
    case "edit":
      return await navigateTo(`/tasks/edit/${route.params.id}`)
  }
}

function setCitation() {
  if (
    taskStore.term
    && Object.keys(taskStore.term).length !== 0
    && taskStore.term.title
    && taskStore.term.creator
  )
    citation.value = {
      author: taskStore.term.creator,
      title: taskStore.term.title,
      url: taskStore.term.source,
      publisher: taskStore.term.publisher,
      licence: taskStore.term.rights,
    }
}

async function schemaRedirect() {
  const referenceStore = useReferenceStore()
  let filters: IReferenceFilters = { ...referenceStore.filters }
  filters.reference_type = "SCHEMA"
  referenceStore.resetFilters()
  referenceStore.setFilters(filters)
  await navigateTo(`/references/task/${taskStore.term.id}`)
}

async function removeSchema() {
  if (taskStore.term.id && taskStore.term.schema && taskStore.term.schema.id)
    await taskStore.removeTemplate(taskStore.term.id, taskStore.term.schema.id)
}

onMounted(async () => {
  await taskStore.getTerm(route.params.id as string)
  if (!taskStore.term || Object.keys(taskStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  appSettings.setPageName("Tasks")
  setCitation()
})

// METADATA - START
// https://nuxt.com/docs/getting-started/seo-meta
const title = ref("whyqd.com — more research, less wrangling")
const description = ref("Perform schema-to-schema transforms for interoperability and data reuse. Transform messy data into structured schemas using readable, auditable methods.")
useHead({
  title,
  meta: [{
    name: "description",
    content: description
  }]
})
useServerSeoMeta({
  title,
  ogTitle: title,
  description: description,
  ogDescription: description,
  ogImage: "https://whyqd.com/img/ugly-data.png"
})
// METADATA - END
</script>
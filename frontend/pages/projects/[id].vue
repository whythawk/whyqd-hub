<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done' && projectStore.term && projectStore.term.name">
      <CommonHeadingView purpose="Project" :name="projectStore.term.name" :title="projectStore.term.title"
        @set-edit-request="watchHeadingRequest" />
      <TabGroup>
        <TabList class="flex space-x-8 border-b border-gray-200 text-xs">
          <Tab v-for="tab in navigation" :key="`tab-${tab.id}`" as="template" v-slot="{ selected }">
            <button
              :class="[selected ? 'border-ochre-500 text-ochre-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700', 'group inline-flex items-center border-b-2 py-4 px-1 font-medium']">
              <component :is="tab.icon"
                :class="[selected ? 'text-ochre-500' : 'text-gray-400 group-hover:text-gray-500', '-ml-0.5 mr-2 h-5 w-5']"
                aria-hidden="true" />
              <span>{{ tab.name }}</span>
            </button>
          </Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <dl class="divide-y divide-gray-100">
              <div class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Name</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.name }}</dd>
              </div>
              <div v-if="projectStore.term.title" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Title</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.title }}</dd>
              </div>
              <div v-if="projectStore.term.description" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Description</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.description }}
                </dd>
              </div>
              <div v-if="projectStore.term.subjects && projectStore.term.subjects.length"
                class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Subjects</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                  {{ projectStore.term.subjects.join(", ") }}
                </dd>
              </div>
              <div v-if="projectStore.term.frequency" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Frequency</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.frequency }}
                </dd>
              </div>
              <div v-if="projectStore.term.spatial" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Spatial characteristics</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.spatial }}
                </dd>
              </div>
              <div v-if="projectStore.term.temporalStart || projectStore.term.temporalEnd"
                class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Temporal range</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                  <span v-if="projectStore.term.temporalStart">{{ readableDate(projectStore.term.temporalStart) }}</span>
                  &mdash;
                  <span v-if="projectStore.term.temporalEnd">{{ readableDate(projectStore.term.temporalEnd) }}</span>
                </dd>
              </div>
              <div v-if="projectStore.term.language" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Language</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.language }}
                </dd>
              </div>
              <div v-if="projectStore.term.creator" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Primary creator</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.creator }}
                </dd>
              </div>
              <div v-if="projectStore.term.contributor" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Contributor</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.contributor }}
                </dd>
              </div>
              <div v-if="projectStore.term.publisher" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Publisher</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.publisher }}
                </dd>
              </div>
              <div v-if="projectStore.term.rights" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Rights held</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.rights }}
                </dd>
              </div>
              <div v-if="projectStore.term.source" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Source</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.source }}
                </dd>
              </div>
              <div v-if="projectStore.term.accessRights" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Access and security</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.accessRights
                }}
                </dd>
              </div>
              <div v-if="projectStore.term.accrualMethod" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Accrual method</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.accrualMethod
                }}
                </dd>
              </div>
              <div v-if="projectStore.term.accrualPeriodicity" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Accrual periodicity</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                  {{ projectStore.term.accrualPeriodicity }}
                </dd>
              </div>
              <div v-if="projectStore.term.accrualPolicy" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Accrual policy</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.accrualPolicy
                }}
                </dd>
              </div>
              <div v-if="projectStore.term.bibliographicCitation"
                class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Bibliographic reference</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                  {{ projectStore.term.bibliographicCitation }}
                </dd>
              </div>
              <div v-if="projectStore.term.conformsTo" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-900">Standard conforms to</dt>
                <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{ projectStore.term.conformsTo }}
                </dd>
              </div>
            </dl>
            <div class="space-y-2 mx-2">
              <h2 class="text-sm font-semibold leading-7 text-gray-900 pt-2">Tasks and schema object</h2>
              <NuxtLink :to="`/tasks/project/${projectStore.term.id}`"
                class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold text-sm">
                <Square3Stack3DIcon class="text-gray-700 group-hover:text-ochre-600 h-5 w-5 shrink-0"
                  aria-hidden="true" />
                <span class="hidden lg:block">Tasks</span>
              </NuxtLink>
              <div v-if="projectStore.term.schema && Object.keys(projectStore.term.schema).length !== 0"
                class="space-y-6">
                <div class="flex flex-row justify-between items-center">
                  <NuxtLink :to="`/schema/${projectStore.term.schema.id}`">
                    <CommonSummaryCard :summary="projectStore.term.schema" :show-state="false" show-icon="SCHEMA" />
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
                  <SquaresPlusIcon class="text-sienna-700 group-hover:text-ochre-600 h-5 w-5 shrink-0"
                    aria-hidden="true" />
                  <span class="hidden lg:block">Add schema</span>
                </button>
              </div>
            </div>
            <div v-if="citation && Object.keys(citation).length !== 0" class="space-y-2 mx-2">
              <CommonCitationCard :citation="citation" />
            </div>
          </TabPanel>
          <TabPanel>
            <ProjectMembersCard :project="(route.params.id as string)" />
          </TabPanel>
          <TabPanel>
            <ProjectInvitationsCard :project="(route.params.id as string)" />
          </TabPanel>
        </TabPanels>
      </TabGroup>
    </div>
  </div>
</template>

<script setup lang="ts">
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue"
import { BeakerIcon, EnvelopeIcon, Square3Stack3DIcon, SquaresPlusIcon, TrashIcon, UserGroupIcon } from "@heroicons/vue/24/outline"
import { readableDate } from "@/utilities"
import { ICitation, IReferenceFilters } from "@/interfaces"
import { useSettingStore, useProjectStore, useReferenceStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const appSettings = useSettingStore()
const route = useRoute()
const projectStore = useProjectStore()
const citation = ref({} as ICitation)
let navigation = [
  { name: "Metadata", id: "METADATA", icon: BeakerIcon },
  { name: "Members", id: "MEMBERS", icon: UserGroupIcon },
]

async function watchHeadingRequest(request: string) {
  switch (request) {
    case "remove":
      await projectStore.removeTerm(route.params.id as string)
      return await navigateTo("/projects")
    case "edit":
      return await navigateTo(`/projects/edit/${route.params.id}`)
  }
}

function setCitation() {
  if (
    projectStore.term
    && Object.keys(projectStore.term).length !== 0
    && projectStore.term.title
    && projectStore.term.creator
  )
    citation.value = {
      author: projectStore.term.creator,
      title: projectStore.term.title,
      url: projectStore.term.source,
      publisher: projectStore.term.publisher,
      licence: projectStore.term.rights,
    }
}

async function schemaRedirect() {
  const referenceStore = useReferenceStore()
  let filters: IReferenceFilters = { ...referenceStore.filters }
  filters.reference_type = "SCHEMA"
  referenceStore.resetFilters()
  referenceStore.setFilters(filters)
  await navigateTo(`/references/project/${projectStore.term.id}`)
}

async function removeSchema() {
  if (projectStore.term.id && projectStore.term.schema && projectStore.term.schema.id)
    await projectStore.removeSchema(projectStore.term.id, projectStore.term.schema.id)
}

onMounted(async () => {
  appSettings.setPageName("Projects")
  await projectStore.getTerm(route.params.id as string)
  if (!projectStore.term || Object.keys(projectStore.term).length === 0)
    throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
  if (projectStore.isCustodian)
    navigation.push({ name: "Invitations", id: "INVITATIONS", icon: EnvelopeIcon })
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
  ogImage: "https://whyqd.com/img/crosswalk.jpg"
})
// METADATA - END
</script>
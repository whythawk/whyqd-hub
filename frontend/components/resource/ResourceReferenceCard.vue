<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-8' : '-bottom-8', 'absolute left-0 top-0 flex w-8 justify-center']">
      <div class="w-px bg-gray-100" />
    </div>
    <div class="flex h-8 w-8 z-10 items-center justify-center rounded-full bg-gray-100 ring-3 ring-gray-100">
      <component :is="modelTypes[props.modelType].icon" class="h-5 w-5 text-gray-500" aria-hidden="true" />
    </div>
    <div class="flex-auto py-0.5 text-xs leading-5 text-gray-500 pb-2 border-b border-gray-200">
      <div class="flex w-full justify-between items-center rounded-lg text-base font-semibold text-gray-900">
        <NuxtLink v-if="props.reference"
          :to="props.modelType === 'CROSSWALK' ? `/${props.modelType.toLowerCase()}/${resourceId}` : `/${props.modelType.toLowerCase()}/${props.reference.id}`">
          <h3 class="text-sm font-semibold text-gray-900 hover:text-ochre-600">{{ heading }}</h3>
        </NuxtLink>
        <h3 v-else class="text-sm font-semibold text-gray-900">{{ heading }}</h3>
      </div>
      <div v-if="props.reference" class="flex items-center">
        <h4 id="detail-heading" class="sr-only">Overview</h4>
        <ul role="list" class="flex flex-row text-xs">
          <li v-if="props.reference.created" class="text-gray-700 p-2">
            <time :datetime="props.reference.created" class="flex-none py-0.5 text-xs text-gray-500">
              Created: {{ readableDate(props.reference.created) }}</time>
          </li>
        </ul>
      </div>
      <div class="flex justify-between">
        <div v-if="props.reference" class="flex items-center">
          <h4 id="process-heading" class="sr-only">Download data and definitions, or reprocess</h4>
          <ul role="list" class="flex flex-row text-xs">
            <li>
              <button @click.prevent="getDownload(props.reference.id as string, props.modelType)"
                class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
                <ArrowDownOnSquareStackIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0"
                  aria-hidden="true" />
                <span class="hidden lg:block">Download definition</span>
              </button>
            </li>
          </ul>
        </div>
        <div v-if="props.reference && ['SCHEMA', 'CROSSWALK'].includes(props.modelType)" class="flex items-center">
          <h4 id="process-heading" class="sr-only">Remove {{ props.modelType.toLowerCase() }}</h4>
          <ul role="list" class="flex flex-row text-xs">
            <li>
              <button @click.prevent="removeReference"
                class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
                <TrashIcon class="text-sienna-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="hidden lg:block">Delete</span>
              </button>
            </li>
          </ul>
        </div>
        <div v-if="!props.reference && props.modelType === 'SCHEMA'" class="flex items-center">
          <h4 id="process-heading" class="sr-only">Add or create {{ props.modelType.toLowerCase() }}</h4>
          <ul role="list" class="flex flex-row text-xs">
            <li class="relative">
              <button type="button" @click.prevent="createReferenceRedirect(props.modelType)"
                class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
                <BoltIcon class="text-sienna-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="hidden lg:block">Create {{ modelTypes[props.modelType].title }}</span>
              </button>
            </li>
            <li class="relative">
              <button type="button" @click.prevent="addReferenceRedirect(props.modelType)"
                class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
                <PlusCircleIcon class="text-sienna-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="hidden lg:block">Add {{ modelTypes[props.modelType].title }}</span>
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ArrowDownOnSquareStackIcon,
  ArrowsRightLeftIcon,
  BoltIcon,
  CubeIcon,
  PlusCircleIcon,
  Squares2X2Icon,
  TrashIcon,
} from "@heroicons/vue/24/outline"
import type { IStatusType, IModelSummary, IKeyable, IReferenceType, IResourceManager, IReferenceFilters } from "@/interfaces"
import { readableDate } from "@/utilities"
import { useTokenStore, useToastStore, useReferenceStore, useResourceStore } from "@/stores"
import { apiData, apiResource } from "@/api"

const tokenStore = useTokenStore()
const referenceStore = useReferenceStore()
const toasts = useToastStore()
const heading = ref("")
const modelTypes: IKeyable = {
  SCHEMA: {
    title: "Schema object",
    icon: Squares2X2Icon,
    to: "/data/download/data/",
  },
  CROSSWALK: {
    title: "Crosswalk",
    icon: ArrowsRightLeftIcon,
    to: "/data/download/data/",
  },
  TRANSFORM: {
    title: "Transform",
    icon: CubeIcon,
    to: "/data/download/data/",
  },
}

const props = defineProps<{
  resourceId?: string,
  modelType: IReferenceType,
  reference?: IModelSummary,
  state?: IStatusType,
  lastCard?: boolean
}>()

function returnDownload(response: any, fileName: string, contentType: string) {
  // https://stackoverflow.com/a/18197341/295606
  const a = document.createElement("a")
  a.href = `data:${contentType},${encodeURIComponent(JSON.stringify(response))}`
  a.download = fileName
  a.type = contentType
  a.style.display = "none"
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

async function getDownload(key: string, download: string) {
  // `${linkTypes[item.model_type].to}${item.id}`
  if (props.reference && props.reference.id && props.reference.name) {
    await tokenStore.refreshTokens()
    if (tokenStore.token) {
      try {
        const { data: response } = await apiData.getModelDownload(tokenStore.token, key)
        if (response.value) {
          return returnDownload(response.value, `${props.reference.name}.${download}`, "application/json")
        }
      } catch (error) {
        toasts.addNotice({
          title: "Download error",
          content: error as string,
          icon: "error"
        })
      }
    }
  }
}

async function addReferenceRedirect(reference_type: IReferenceType) {
  let filters: IReferenceFilters = {}
  filters.reference_type = reference_type
  referenceStore.resetFilters()
  referenceStore.setFilters(filters)
  await navigateTo(`/references/resource/${props.resourceId}`)
}

async function createReferenceRedirect(reference_type: IReferenceType) {
  if (reference_type === "SCHEMA") await navigateTo("/schema/edit")
  else await navigateTo(`/references/resource/${props.resourceId}`)
}

async function removeReference() {
  if (
    props.reference
    && props.reference.id
    && props.resourceId
    && props.modelType
    && ["SCHEMA", "CROSSWALK"].includes(props.modelType)
  ) {
    await tokenStore.refreshTokens()
    if (tokenStore.token) {
      let responseData: IResourceManager = {} as IResourceManager
      try {
        if (props.modelType == "SCHEMA") {
          const { data: response } = await apiResource.removeTermSchemaObject(tokenStore.token, props.resourceId as string)
          if (response.value) responseData = response.value
        }
        if (props.modelType == "CROSSWALK") {
          const { data: response } = await apiResource.removeTermCrosswalk(tokenStore.token, props.resourceId as string)
          if (response.value) responseData = response.value
        }
        if (responseData && Object.keys(responseData).length) {
          const resourceStore = useResourceStore()
          resourceStore.setTerm(responseData)
        }
      } catch (error) {
        toasts.addNotice({
          title: "Remove error",
          content: error as string,
          icon: "error"
        })
      }
    }
  }
}

onMounted(async () => {
  let prehead = modelTypes[props.modelType].title
  if (props.reference && props.reference.name) {
    heading.value = `${prehead}: ${props.reference.name}`
    if (props.reference.title) heading.value = `${prehead}: ${props.reference.title}`
  } else heading.value = `${prehead}: unavailable`
})
</script>
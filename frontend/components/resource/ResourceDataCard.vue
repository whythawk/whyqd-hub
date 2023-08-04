<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-8' : '-bottom-8', 'absolute left-0 top-0 flex w-8 justify-center']">
      <div class="w-px bg-gray-100" />
    </div>
    <div class="flex h-8 w-8 z-10 items-center justify-center rounded-full bg-gray-100 ring-3 ring-gray-100">
      <component :is="props.lastCard ? CubeIcon : TableCellsIcon" class="h-5 w-5 text-gray-500" aria-hidden="true" />
    </div>
    <div class="flex-auto py-0.5 text-xs leading-5 text-gray-500 pb-2 border-b border-gray-200">
      <div class="flex w-full justify-between items-center rounded-lg text-base font-semibold text-gray-900">
        <h3 class="text-sm font-semibold text-gray-900">
          <span v-if="props.lastCard">Transform</span>
          <span v-else>Data</span>: {{ heading }}
        </h3>
        <div
          v-if="!props.reference && props.state === 'TRANSFORM_READY' && props.lastCard && authStore.hasExplorerSubscription"
          class="flex items-center justify-end">
          <h4 id="process-heading" class="sr-only">Process transform</h4>
          <ul role="list" class="flex flex-row text-xs">
            <li v-if="isTransforming">
              <div class="text-eucalyptus-700 group flex gap-x-1 p-2 font-semibold">
                <CubeTransparentIcon class="text-eucalyptus-700 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="hidden lg:block">Processing ...</span>
              </div>
            </li>
            <li v-else>
              <Listbox>
                <div class="relative -mt-1">
                  <ListboxButton
                    class="relative w-full cursor-default rounded-lg bg-white pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-ochre-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-ochre-300 sm:text-sm">
                    <span
                      class="text-eucalyptus-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold items-center">
                      <CubeTransparentIcon class="text-eucalyptus-700 group-hover:text-ochre-600 h-4 w-4 shrink-0"
                        aria-hidden="true" /><span class="hidden lg:block">Run Transform</span>
                    </span>
                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                      <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                    </span>
                  </ListboxButton>
                  <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                    leave-to-class="opacity-0">
                    <ListboxOptions
                      class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-md ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                      <ListboxOption v-slot="{ active, selected }" v-for="mtype in parameters.mimeType"
                        :key="`mtype-${mtype.value}`" :value="mtype.value" as="template">
            <li :class="[
              active ? 'bg-eucalyptus-100 text-eucalyptus-900' : 'text-gray-900',
              'relative cursor-default select-none py-2 pl-10 pr-4',
            ]" @click.prevent="processTransform(mtype.value)">
              <span :class="[
                selected ? 'font-medium' : 'font-normal',
                'block truncate',
              ]">{{ mtype.value }}</span>
              <span v-if="selected" class="absolute inset-y-0 left-0 flex items-center pl-3 text-eucalyptus-600">
                <CheckIcon class="h-5 w-5" aria-hidden="true" />
              </span>
            </li>
            </ListboxOption>
            </ListboxOptions>
            </transition>
        </div>
        </Listbox>
        </li>
        </ul>
      </div>
      <div
        v-if="!props.reference && props.state === 'TRANSFORM_READY' && props.lastCard && !authStore.hasExplorerSubscription"
        class="flex items-center justify-end">
        <NuxtLink to="/pricing"
          class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm font-normal text-white bg-ochre-600 hover:bg-ochre-700">
          <CreditCardIcon class="sm:-ml-0.5 h-4 w-4 text-white" aria-hidden="true" />
          <span class="hidden sm:block">Subscribe</span>
        </NuxtLink>
      </div>
    </div>
    <div v-if="props.reference" class="flex items-center">
      <h4 id="detail-heading" class="sr-only">Overview</h4>
      <ul role="list" class="flex flex-row text-xs">
        <li v-if="props.reference.created" class="text-gray-700 p-2">
          <time :datetime="props.reference.created" class="flex-none py-0.5 text-xs text-gray-500">
            Created: {{ readableDate(props.reference.created) }}</time>
        </li>
        <li v-if="props.reference.sheet_name" class="text-gray-700 p-2">
          Sheet: {{ props.reference.sheet_name }}
        </li>
        <li v-if="props.reference.mime_type" class="text-gray-700 p-2">
          Mimetype: {{ getMimeType(props.reference.mime_type) }}
        </li>
        <li class="text-gray-700 p-2">
          Rows: {{ props.reference.index }}
        </li>
      </ul>
    </div>
    <div class="flex justify-between">
      <div v-if="props.reference" class="flex items-center">
        <h4 id="process-heading" class="sr-only">Download data and definitions, or reprocess</h4>
        <ul role="list" class="flex flex-row text-xs">
          <li v-if="props.reference.summary && props.reference.summarykeys">
            <button @click="isOpen = true"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <TableCellsIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Show summary</span>
            </button>
            <TransitionRoot as="template" :show="isOpen">
              <Dialog as="div" class="relative z-50" @close="isOpen = false">
                <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100"
                  leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
                  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
                </TransitionChild>
                <div class="fixed inset-0 z-10 overflow-y-auto">
                  <div class="flex min-h-full items-end justify-center text-center sm:items-center">
                    <TransitionChild as="template" enter="ease-out duration-300"
                      enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                      enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200"
                      leave-from="opacity-100 translate-y-0 sm:scale-100"
                      leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
                      <DialogPanel
                        class="flex flex-col sm:rounded-lg bg-white p-2 text-left shadow-xl transition-all max-w-[100%] sm:max-w-[90%] max-h-screen sm:max-h-[800px]">
                        <CommonDataTable :table-headers="props.reference.summarykeys"
                          :table-rows="props.reference.summary" />
                        <div class="flex flex-row justify-end mt-4">
                          <button type="button"
                            class="mt-3 inline-flex justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 w-auto"
                            @click="isOpen = false">Close</button>
                        </div>
                      </DialogPanel>
                    </TransitionChild>
                  </div>
                </div>
              </Dialog>
            </TransitionRoot>
          </li>
          <li v-for="item in props.reference.links" :key="`data-link-${item.id}`">
            <button @click.prevent="getDownload(item.id, item.model_type)"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <component :is="linkTypes[item.model_type].icon"
                class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">{{ linkTypes[item.model_type].title }}</span>
            </button>
          </li>
        </ul>
      </div>
      <div v-if="props.reference && props.state === 'COMPLETE' && props.lastCard" class="flex items-center">
        <h4 id="process-heading" class="sr-only">Remove transform</h4>
        <ul role="list" class="flex flex-row text-xs">
          <li>
            <button @click.prevent="removeTransform"
              class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <TrashIcon class="text-sienna-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Delete</span>
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
  Dialog,
  DialogPanel,
  TransitionChild,
  TransitionRoot,
  Listbox,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
} from "@headlessui/vue"
import {
  ArrowDownTrayIcon,
  ArrowDownOnSquareStackIcon,
  CheckIcon,
  ChevronUpDownIcon,
  CreditCardIcon,
  CubeIcon,
  CubeTransparentIcon,
  TableCellsIcon,
  TrashIcon,
} from "@heroicons/vue/24/outline"
import { IStatusType, IResourceDataReference, IKeyable } from "@/interfaces"
import { readableDate, getMimeType } from "@/utilities"
import { useTokenStore, useToastStore, useResourceStore, useAuthStore } from "@/stores"
import { apiData, apiResource } from "@/api"

const tokenStore = useTokenStore()
const authStore = useAuthStore()
const toasts = useToastStore()
const heading = ref("")
const isOpen = ref(false)
const isTransforming = ref(false)

const linkTypes: IKeyable = {
  DATA: {
    title: "Download definition",
    icon: ArrowDownOnSquareStackIcon,
    to: "/data/download/model/",
  },
  DATASOURCE: {
    title: "Download data",
    icon: ArrowDownTrayIcon,
    to: "/data/download/source/",
  },
  TRANSFORM: {
    title: "Download definition",
    icon: ArrowDownOnSquareStackIcon,
    to: "/data/download/model/",
  },
}
const parameters = {
  mimeType: [
    { value: "CSV" },
    { value: "XLS" },
    { value: "XLSX" },
    { value: "PARQUET" },
    { value: "FEATHER" },
  ],
}


const props = defineProps<{
  resourceId?: String,
  reference?: IResourceDataReference,
  state?: IStatusType,
  lastCard?: Boolean
}>()

function getEncodedResponse(mime: string, response: any) {
  switch (mime) {
    case "application/json":
      return `data:${mime},${encodeURIComponent(JSON.stringify(response))}`
    case "text/csv":
      return `data:${mime},${encodeURIComponent(response)}`
    default:
      // it's a blob ...
      return URL.createObjectURL(response)
  }
}

function returnDownload(response: any, fileName: string, contentType: string) {
  // https://stackoverflow.com/a/18197341/295606
  const a = document.createElement("a")
  const data = getEncodedResponse(contentType, response)
  a.href = data
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
        if (["DATA", "TRANSFORM"].includes(download)) {
          const { data: response } = await apiData.getModelDownload(tokenStore.token, key)
          if (response.value) {
            return returnDownload(response.value, `${props.reference.name}.${download}`, "application/json")
          }
        } else {
          const { data: response } = await apiData.getSourceDownload(tokenStore.token, key)
          if (response.value && props.reference.mime_type) {
            return returnDownload(response.value, props.reference.name, props.reference.mime_type)
          }
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

async function removeTransform() {
  if (props.reference && props.reference.id && props.resourceId) {
    await tokenStore.refreshTokens()
    if (tokenStore.token) {
      try {
        const { data: response } = await apiResource.removeTermTransform(tokenStore.token, props.resourceId as string)
        if (response.value) {
          const resourceStore = useResourceStore()
          resourceStore.setTerm(response.value)
        }
      } catch (error) {
        toasts.addNotice({
          title: "Transform remove error",
          content: error as string,
          icon: "error"
        })
      }
    }
  }
}

async function processTransform(mimetype: string) {
  if (!props.reference && props.resourceId) {
    await tokenStore.refreshTokens()
    if (tokenStore.token) {
      try {
        const { data: response } = await apiResource.postProcessTransform(tokenStore.token, props.resourceId as string, mimetype)
        if (response.value) {
          isTransforming.value = true
          toasts.addNotice({
            title: "Transform processing",
            content: response.value.msg,
          })
        }
      } catch (error) {
        toasts.addNotice({
          title: "Transform remove error",
          content: error as string,
          icon: "error"
        })
      }
    }
  }
}

onMounted(async () => {
  if (props.reference && props.reference.name) {
    heading.value = props.reference.name
    if (props.reference.title) heading.value = props.reference.title
  } else heading.value = "unavailable"
})
</script>
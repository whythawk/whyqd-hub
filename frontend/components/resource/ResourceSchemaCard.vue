<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-8' : '-bottom-8', 'absolute left-0 top-0 flex w-8 justify-center']">
      <div class="w-px bg-gray-100" />
    </div>
    <div class="flex h-8 w-8 z-10 items-center justify-center rounded-full bg-gray-100 ring-3 ring-gray-100">
      <Squares2X2Icon class="h-5 w-5 text-gray-500" aria-hidden="true" />
    </div>
    <div class="flex-auto py-0.5 text-xs leading-5 text-gray-500 pb-2 border-b border-gray-200">
      <div class="flex w-full justify-between items-center rounded-lg text-base font-semibold text-gray-900">
        <NuxtLink v-if="props.reference" :to="`/schema/${props.reference.id}`">
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
      <div v-if="props.reference" class="flex items-center">
        <h4 id="process-heading" class="sr-only">Download data and definitions, or reprocess</h4>
        <ul role="list" class="flex flex-row text-xs">
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
      <div v-if="props.reference && props.reference.fields && props.reference.fields.length" class="space-y-2 mx-2">
        <Disclosure as="div" v-slot="{ open }">
          <DisclosureButton class="flex w-full items-start justify-between text-left">
            <h4 class="text-sm font-semibold leading-7 text-gray-500 pt-2">
              Fields
            </h4>
            <ChevronDownIcon :class="[open ? 'rotate-180 transform' : '', 'h-5 w-5']" aria-hidden="true" />
          </DisclosureButton>
          <DisclosurePanel>
            <ul role="list">
              <li v-for="(field, fIdx) in props.reference.fields" :key="`field-${field.uuid}`">
                <ResourceSchemaFieldCard :resource-id="(props.resourceId as string)" :field="field"
                  :last-card="fIdx === props.reference.fields.length - 1" />
              </li>
            </ul>
          </DisclosurePanel>
        </Disclosure>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Disclosure, DisclosureButton, DisclosurePanel, } from "@headlessui/vue"
import { ArrowDownOnSquareStackIcon, ChevronDownIcon, Squares2X2Icon, } from "@heroicons/vue/24/outline"
import type { IStatusType, IResourceSchemaReference, IKeyable } from "@/interfaces"
import { readableDate } from "@/utilities"
import { useTokenStore, useToastStore } from "@/stores"
import { apiData } from "@/api"

const tokenStore = useTokenStore()
const toasts = useToastStore()
const heading = ref("")
const linkTypes: IKeyable = {
  SCHEMA: {
    title: "Download definition",
    icon: ArrowDownOnSquareStackIcon,
    to: "/data/download/model/",
  },
}

const props = defineProps<{
  resourceId?: string,
  reference?: IResourceSchemaReference,
  schemaHead?: string,
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

onMounted(async () => {
  let prehead
  if (props.schemaHead) prehead = `Schema ${props.schemaHead}`
  else prehead = "Schema subject"
  if (props.reference && props.reference.name) {
    heading.value = `${prehead}: ${props.reference.name}`
    if (props.reference.title) heading.value = `${prehead}: ${props.reference.title}`
  } else heading.value = `${prehead}: unavailable`
})
</script>
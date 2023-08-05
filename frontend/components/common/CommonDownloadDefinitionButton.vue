<template>
  <div class="flex justify-left items-center">
    <button @click.prevent="getDownload(props.reference.id as string, props.reference.model_type, false)"
      class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
      <ArrowDownOnSquareStackIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
      <span class="hidden lg:block">Download definition</span>
    </button>
    <button v-if="props.reference.model_type == 'DATA'"
      @click.prevent="getDownload(props.reference.id as string, props.reference.model_type, true)"
      class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
      <ArrowDownTrayIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
      <span class="hidden lg:block">Download data</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ArrowDownOnSquareStackIcon, ArrowDownTrayIcon } from "@heroicons/vue/24/outline"
import { IReference } from "@/interfaces"
import { useTokenStore, useToastStore } from "@/stores"
import { apiData } from "@/api"

const tokenStore = useTokenStore()
const toasts = useToastStore()
const IMimeReference: { [key: string]: string } = {
  CSV: "text/csv",
  XLS: "application/vnd.ms-excel",
  XLSX: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  PARQUET: "application/octet-stream",
  FEATHER: "application/octet-stream"
}

const props = defineProps<{
  reference: IReference
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

async function getDownload(key: string, download: string, datasource: boolean) {
  // `${linkTypes[item.model_type].to}${item.id}`
  if (props.reference && props.reference.id && props.reference.name) {
    await tokenStore.refreshTokens()
    if (tokenStore.token) {
      try {
        if (!datasource) {
          const { data: response } = await apiData.getModelDownload(tokenStore.token, key)
          if (response.value) {
            return returnDownload(response.value, `${props.reference.name}.${download}`, "application/json")
          }
        } else {
          const { data: response } = await apiData.getSourceDownload(tokenStore.token, key)
          console.log(response.value, IMimeReference[props.reference.mime_type])
          if (response.value && props.reference.mime_type) {
            return returnDownload(response.value, props.reference.name, IMimeReference[props.reference.mime_type])
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
</script>
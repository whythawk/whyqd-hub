<template>
  <div>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
      <CommonHeadingEditView purpose="Schema" :name="schemaStore.draft.name" :title="schemaStore.draft.title"
        :approach="saveApproach" @set-edit-request="watchEditHeadingRequest" />
      <div class="space-y-4">
        <p class="text-sm leading-6 text-gray-600 pt-2">A whyqd (/wɪkɪd/) schema definition describes the
          structural
          organisation of tabular data. Each column is identified by a field name and defined by conformance to
          technical specifications. These, along with field constraints and sensible defaults, ensure interoperability.
        </p>
        <div class="flex items-center justify-end gap-x-3">
          <button @click.prevent="showImport = true">
            <ArrowUpTrayIcon
              :class="[showImport ? 'text-cerulean-600' : 'text-gray-500', 'h-5 w-5  hover:text-ochre-600']" />
          </button>
          <button @click.prevent="showImport = false">
            <PencilSquareIcon
              :class="[showImport ? 'text-gray-500' : 'text-cerulean-600', 'h-5 w-5  hover:text-ochre-600']" />
          </button>
        </div>
        <CommonImportCard v-if="showImport" reference="SCHEMA" @set-import="watchSetImport" />
        <div v-else class="space-y-4">
          <SchemaMetadataEditCard state="setMetadata" @set-request="watchRequestSocket" />
          <div v-if="schemaStore.draft.fields" class="border-t border-gray-900/10 space-y-4">
            <div>
              <div class="flex justify-between items-center">
                <h2 class="text-base font-semibold leading-7 text-gray-900 pt-2">Fields</h2>
                <button @click.prevent="showAddField = !showAddField">
                  <PlusCircleIcon v-if="!showAddField" class="h-6 w-6 text-cerulean-600 hover:text-ochre-600" />
                  <MinusCircleIcon v-else class="h-6 w-6 text-sienna-600 hover:text-ochre-600" />
                </button>
              </div>
              <p class="text-sm text-gray-500">Drag to reorder.</p>
            </div>
            <SchemaFieldEditCard v-if="showAddField" state="addField" :edit="{} as IFieldCreate" :last-card="false"
              @set-request="watchRequestSocket" @set-draggable="watchDraggableState" />
            <div v-for="(field, fIdx) in schemaStore.draft.fields" :key="`field-${field.uuid}`"
              :id="`field-${field.uuid}`" :draggable="isDraggable" class="bg-white rounded-lg" @dragstart="handleDragStart"
              @dragenter="handleDragEnter" @dragover="handleDragOver" @dragleave="handleDragLeave" @drop="handleDrop"
              @dragend="handleDragEnd">
              <!-- <SchemaFieldCard :edit="field" /> -->
              <SchemaFieldEditCard state="updateField" :edit="field"
                :last-card="fIdx === schemaStore.draft.fields.length - 1" 
                @set-request="watchRequestSocket" @set-draggable="watchDraggableState" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import WebSocketAsPromised from "websocket-as-promised"
import { storeToRefs } from "pinia"
import { ArrowUpTrayIcon, ExclamationCircleIcon, MinusCircleIcon, PencilSquareIcon, PlusCircleIcon, Squares2X2Icon } from "@heroicons/vue/24/outline"
import { ISchemaCreate, IFieldCreate, IKeyable, ISocketRequest, ISocketResponse, } from "@/interfaces"
import { apiSchema } from "@/api"
import { useSettingStore, useSchemaStore, useToastStore } from "@/stores"
import { getAvatar } from "@/utilities"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const schemaStore = useSchemaStore()
const { edit } = storeToRefs(schemaStore)
const toast = useToastStore()
const appSettings = useSettingStore()
const streaming = ref(false)
let draftFields = [] as IFieldCreate[]
const dragID = ref("" as string)
let wsp = {} as WebSocketAsPromised
const heading = ref("")
const avatar = ref("")
const saveApproach = ref("Create")
const showAddField = ref(false)
const showReset = ref(false)
const referenceID = ref("" as string)
const showImport = ref(false)
const isDraggable = ref(false)

onMounted(async () => {
  if (route.params.id !== "create" || schemaStore.term.uuid === schemaStore.draft.uuid) {
    if (route.params.id !== "create") avatar.value = await getAvatar(route.params.id as string)
    saveApproach.value = "Update"
  }
  appSettings.setPageName("Edit schema")
  await schemaStore.authTokens.refreshTokens()
  await initialiseSocket()
  resetFields()
})

async function watchEditHeadingRequest(request: string) {
  switch (request) {
    case "reset":
      await resetSchema()
      break
    case "save":
      saveSchema()
      break
    case "cancel":
      const link = route.params.id !== 'create' ? `/schema/${route.params.id}` : '/'
      return await navigateTo(link)
  }
}

async function watchDraggableState(draggable: boolean) {
  isDraggable.value = draggable
}

onBeforeRouteLeave((to, from, next) => {
  closeSocket()
  next()
})

function resetFields() {
  if (schemaStore.draft.fields && schemaStore.draft.fields.length) draftFields = [...schemaStore.draft.fields]
}

watch(() => edit, () => {
  resetFields()
})

async function newSchema() {
  schemaStore.resetDraft()
  await schemaStore.authTokens.refreshTokens()
  await initialiseSocket()
  resetFields()
  showReset.value = false
  if (route.params.id !== "create") return await navigateTo("/schema/edit")
}

async function resetSchema() {
  if (route.params.id !== 'create' && referenceID.value) resetFields() // return await navigateTo(`/schema/edit/${referenceID.value}`)
  else {
    await newSchema()
  }
}

async function saveSchema() {
  watchRequestSocket({
    state: "save",
    data: {}
  })
}

// WEBSOCKETS
async function watchResponseSocket(response: ISocketResponse) {
  let saveDraft = true
  // response: { state, data, error }
  console.log("response: ", response.state, response.data)
  switch (response.state) {
    case "initialised":
      // if have a legitimate parameter id, load from server
      // note: also means that a previously edited, but existing, schema isn't reloaded
      if (route.params.id !== "create") await watchRequestSocket({
        state: "loadSchema",
        data: { id: route.params.id }
      })
      else {
        // if already have a saved draft, reload it
        if (
          schemaStore.draft
          && Object.keys(schemaStore.draft).length !== 0
          && (
            !schemaStore.term
            || (
              Object.keys(schemaStore.term).length !== 0
              && schemaStore.term.uuid === schemaStore.draft.uuid
            )
          )
        ) await watchRequestSocket({
          state: "initialiseSchema",
          data: schemaStore.draft
        })
        else {
          await watchRequestSocket({
            state: "initialiseSchema",
            data: {}
          })
        }
      }
      await watchRequestSocket({
        state: "getReference",
        data: {}
      })
      saveDraft = false
      break
    case "addField":
      // Hide the add panel and switch the buttons
      showAddField.value = false
      saveDraft = true
      break
    case "getReference":
      // Used to check if need to reload a reference for reset
      if (response.data && response.data.id) referenceID.value = response.data.id
      response.data = {} as ISchemaCreate
      saveDraft = false
      break
    case "save":
      // backend closes the socket itself
      // redirect to the schema page
      if (response.data && response.data.id) {
        streaming.value = false
        schemaStore.resetDraft()
        return await navigateTo(`/schema/${response.data.id}`)
      }
      saveDraft = false
      break
    case "error":
      if (!schemaStore.draft || Object.keys(schemaStore.draft).length === 0)
        throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
      toast.addNotice({
        title: "Schema error",
        content: `Error: ${response.error}`,
        icon: "error"
      })
      saveDraft = false
      break
  }
  if (response.data && saveDraft) {
    schemaStore.setDraft(response.data as ISchemaCreate)
    if (schemaStore.draft.title) heading.value = schemaStore.draft.title
    else heading.value = schemaStore.draft.name
  }
}

async function watchRequestSocket(request: ISocketRequest) {
  // request: { state, data }
  console.log("request: ", request.state, request.data)
  sendSocketRequest(request.state, request.data)
  // switch (request.state) {
  //   case "save":
  //     // Three situations: 
  //     //   1. route.params.id so updating an existing where have the reference
  //     //   2. create, but existing, so updating where have NO reference
  //     //   3. create a new schema
  //     // Fortunately, this is done on the backend
  //     break
  //   default:
  //     sendSocketRequest(request.state, request.data)
  // }
}

function sendSocketRequest(state: string, data: IKeyable) {
  try {
    const payload: ISocketRequest = {
      state,
      data
    }
    wsp.sendPacked(payload)
  } catch (e) {
    console.log(e)
    // closeSocket()
  }
}

async function initialiseSocket() {
  wsp = apiSchema.socketEdit()
  await wsp.open()
  wsp.onUnpackedMessage.addListener((data) => watchResponseSocket(data))
  const jsonData: IKeyable = {
    token: schemaStore.authTokens.token
  }
  wsp.sendPacked(jsonData)
  streaming.value = true
}

function closeSocket() {
  wsp.onUnpackedMessage.removeListener((data) => watchResponseSocket(data))
  if (streaming.value) {
    wsp.close()
    streaming.value = false
  }
}

// JSON IMPORTER
async function watchSetImport(payload: any) {
  await watchRequestSocket({
    state: "initialiseSchema",
    data: payload
  })
  showImport.value = false
}

// DRAG N DROP
// https://web.dev/drag-and-drop/
function getFieldID(text: string): string {
  return [...text.split("-")].slice(-5).join("-") as string
}

function handleDragStart(e: any) {
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-white",
    "bg-cerulean-100"
  )
  dragID.value = getFieldID(e.currentTarget.id)
  e.dataTransfer.effectAllowed = "move"
}

function handleDragEnter(e: any) {
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-white",
    "bg-cerulean-100"
  )
}

function handleDragOver(e: any) {
  if (e.preventDefault) {
    e.preventDefault() // Necessary. Allows us to drop.
  }
  if (e.target.id !== e.currentTarget.id) return false
  e.dataTransfer.dropEffect = "move"
  return false
}

function handleDragLeave(e: any) {
  e.stopPropagation()
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "bg-white"
  )
}

function handleDrop(e: any) {
  e.stopPropagation()
  e.preventDefault()
  resetFields()
  const dropID = getFieldID(e.currentTarget.id)
  if (dragID.value !== dropID) {
    const frIdx = draftFields.findIndex(
      (field) => field.uuid === dragID.value
    )
    const toIdx = draftFields.findIndex(
      (field) => field.uuid === dropID
    )
    // Because TypeScript, in its infinite wisdom, has no concept of `-1`
    const dragged = { ...draftFields.slice(frIdx)[0] }
    draftFields.splice(frIdx, 1)
    draftFields.splice(toIdx, 0, dragged)
    watchRequestSocket({
      state: "reorderFields",
      data: draftFields.map(({ uuid }) => uuid)
    })
  }
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "bg-white"
  )
  return false
}

function handleDragEnd(e: any) {
  if (e.target.id !== e.currentTarget.id) return false
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-cerulean-100",
    "bg-white"
  )
}

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
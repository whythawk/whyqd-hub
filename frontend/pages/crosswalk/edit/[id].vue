<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 min-w-full min-h-full mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-if="appSettings.current.pageState === 'done' && crosswalkStore.term && crosswalkStore.term.name">
      <div class="mx-auto min-w-full px-2 sm:px-3 lg:px-6">
        <CommonHeadingEditView purpose="Crosswalk" :name="crosswalkStore.draft.name" :title="crosswalkStore.draft.title"
          :approach="saveApproach" @set-edit-request="watchEditHeadingRequest" />
        <!-- Main three-panel grid -->
        <div class="isolate grid grid-cols-1 items-start gap-2 2xl:grid-cols-10">
          <!-- Action column -->
          <div class="isolate grid grid-cols-1 gap-1 2xl:col-span-5">
            <section aria-labelledby="section-1-title">
              <h2 class="sr-only" id="section-1-title">Action area</h2>
              <div class="pt-2">
                <!-- Action panel grid -->
                <div class="grid grid-cols-1 gap-2 md:grid-cols-4">
                  <!-- Action list column -->
                  <ActionTemplateCard @set-request="watchRequestSocket" />
                  <!-- Action workspace column -->
                  <div class="md:col-span-3 rounded-lg py-2 px-3 ring-1 ring-inset ring-gray-200">
                    <h2 class="flex border-b border-gray-200 text-xs items-center py-2 px-1 font-medium">
                      <BoltIcon class="-ml-0.5 h-5 w-5 text-gray-400" aria-hidden="true" />
                      <span class="mx-1 text-gray-500">Workspace</span>
                    </h2>
                    <div class="space-y-4 max-h-[650px] 2xl:max-h-[1100px] min-h-full overflow-y-auto mt-2">
                      <div class="mx-2 min-h-full" @dragstart="handleDragStart" @dragenter="handleDragEnter"
                        @dragover="handleDragOver" @dragleave="handleDragLeave" @drop="handleDrop"
                        @dragend="handleDragEnd">
                        <div
                          class="my-1 flex justify-center rounded-lg border border-dashed border-gray-900/25 bg-gray-100 p-2">
                          <div class="text-center">
                            <div class="mt-2 flex text-sm leading-6 text-gray-600">
                              <BoltIcon class="mx-auto h-6 w-6 text-ochre-300" aria-hidden="true" />
                              <div class="relative rounded-md font-semibold text-ochre-600 ml-1">
                                Drop zone
                              </div>
                            </div>
                          </div>
                        </div>
                        <ul v-if="draftActions && draftActions.length" role="list">
                          <li v-for="(action, aIdx) in draftActions"
                            :key="`action-${action.uuid ? action.uuid : 'add-' + aIdx}`"
                            :id="`action-${action.uuid ? action.uuid : 'add-' + aIdx}`" draggable="true"
                            class="bg-white rounded-lg" @dragstart="handleDragStart" @dragenter="handleDragEnter"
                            @dragover="handleDragOver" @dragleave="handleDragLeave" @drop="handleDrop"
                            @dragend="handleDragEnd">
                            <ActionEditCard :edit="action" :schema-subject="crosswalkStore.draft.schema_subject"
                              :schema-object="crosswalkStore.draft.schema_object" @set-request="watchRequestSocket" />
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
          <!-- Information column -->
          <div class="grid grid-cols-1 gap-1 2xl:col-span-5">
            <section aria-labelledby="section-2-title">
              <h2 class="sr-only" id="section-2-title">Information and schemas</h2>
              <div class="w-full flex-auto rounded-lg  py-2 px-3 ring-1 ring-inset ring-gray-200 mt-2">
                <TabGroup>
                  <TabList class="flex space-x-8 border-b border-gray-200 text-xs focus:ring-0 focus:ring-offset-0">
                    <!-- Use the `selected` state to conditionally style the selected tab. -->
                    <Tab v-for="tab in tabs" :key="`tab-${tab.name}`" as="template" v-slot="{ selected }"
                      class="focus:ring-0 focus:ring-offset-0">
                      <button
                        :class="[selected ? 'border-ochre-500 text-ochre-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700', 'group inline-flex items-center border-b-2 py-4 px-1 font-medium focus:ring-0 focus:ring-offset-0']">
                        <component :is="tab.icon"
                          :class="[selected ? 'text-ochre-500' : 'text-gray-400 group-hover:text-gray-500', '-ml-0.5 mr-2 h-5 w-5']"
                          aria-hidden="true" />
                        <span>{{ tab.name }}</span>
                      </button>
                    </Tab>
                  </TabList>
                  <TabPanels>
                    <TabPanel>
                      <div class="overflow-y-auto">
                        <div
                          class="flex flex-col p-2 text-left transition-all max-w-[100%] max-h-[800px] 2xl:max-h-[1100px]">
                          <CommonDataTable
                            v-if="crosswalkStore.draft.data && crosswalkStore.draft.data.summary && crosswalkStore.draft.data.summarykeys"
                            :table-headers="crosswalkStore.draft.data.summarykeys"
                            :table-rows="crosswalkStore.draft.data.summary" />
                          <CommonEmptyCard v-else term="This crosswalk has no source data." />
                        </div>
                      </div>
                    </TabPanel>
                    <TabPanel>
                      <div class="overflow-y-auto">
                        <div
                          class="flex flex-col p-2 text-left transition-all max-w-[100%] max-h-[800px] 2xl:max-h-[1100px]">
                          <CrosswalkSchemaCard :reference="crosswalkStore.draft.schema_subject" :actions="draftActions"
                            :subject="true" />
                        </div>
                      </div>
                    </TabPanel>
                    <TabPanel>
                      <div class="overflow-y-auto">
                        <div
                          class="flex flex-col p-2 text-left transition-all max-w-[100%] max-h-[800px] 2xl:max-h-[1100px]">
                          <CrosswalkSchemaCard :reference="crosswalkStore.draft.schema_object" :actions="draftActions"
                            :subject="false" />
                        </div>
                      </div>
                    </TabPanel>
                    <TabPanel>
                      <div class="overflow-y-auto">
                        <div
                          class="flex flex-col p-2 text-left transition-all max-w-[100%] max-h-[800px] 2xl:max-h-[1100px]">
                          <CrosswalkMetadataEditCard state="setMetadata" @set-request="watchRequestSocket" />
                        </div>
                      </div>
                    </TabPanel>
                    <TabPanel>
                      <div class="overflow-y-auto">
                        <div
                          class="flex flex-col p-2 text-left transition-all max-w-[100%] max-h-[800px] 2xl:max-h-[1100px]">
                          <p class="text-sm mb-2 leading-6 text-gray-600">Whyqd (/wɪkɪd/) crosswalks are mappings of the
                            relationships between
                            fields defined between a schema subject and a schema object. Ideally, these are one-to-one,
                            where a field in
                            the subject has an exact match in the object. In practice, it's more complicated than that.
                          </p>
                          <CommonEmptyCard term="Contextual helps is still being written. Sorry." />
                        </div>
                      </div>
                    </TabPanel>
                  </TabPanels>
                </TabGroup>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import WebSocketAsPromised from "websocket-as-promised"
import { storeToRefs } from "pinia"
import { Menu, MenuButton, MenuItems, MenuItem, TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue"
import {
  ArrowsRightLeftIcon, ArrowPathIcon, ArrowUpTrayIcon, Bars3BottomLeftIcon, BoltIcon, ChevronDownIcon,
  ExclamationCircleIcon, QuestionMarkCircleIcon, Squares2X2Icon, TableCellsIcon, XMarkIcon
} from "@heroicons/vue/24/outline"
import { IResourceCrosswalkManager, IActionModel, IActionType, IKeyable, ISocketRequest, ISocketResponse, } from "@/interfaces"
import { apiCrosswalk } from "@/api"
import { useSettingStore, useToastStore, useCrosswalkStore } from "@/stores"
import { getAvatar, convertActionModelList, convertActionModelToScript } from "@/utilities"

definePageMeta({
  layout: "crosswork",
  middleware: ["authenticated"],
});

const route = useRoute()
const crosswalkStore = useCrosswalkStore()
const { scripts } = storeToRefs(crosswalkStore)
const toast = useToastStore()
const appSettings = useSettingStore()
const streaming = ref(false)
const draftActions = ref<IActionModel[]>([] as IActionModel[])
const dragID = ref("" as string)
let wsp = {} as WebSocketAsPromised
const heading = ref("")
const avatar = ref("")
const saveApproach = ref("Update")
const showAddAction = ref(false)
const tabs = [
  { name: "Data source", icon: TableCellsIcon },
  { name: "Schema subject", icon: Squares2X2Icon },
  { name: "Schema object", icon: Squares2X2Icon },
  { name: "Metadata", icon: Bars3BottomLeftIcon },
  { name: "Help", icon: QuestionMarkCircleIcon },
]

onMounted(async () => {
  appSettings.setPageState("loading")
  avatar.value = await getAvatar(route.params.id as string)
  appSettings.setPageName("Edit crosswalk")
  await crosswalkStore.authTokens.refreshTokens()
  await initialiseSocket()
  resetActions()
})

onBeforeRouteLeave((to, from, next) => {
  closeSocket()
  next()
})

async function initialiseDraft(data: IKeyable = {}) {
  if (data && Object.keys(data).length !== 0)
    crosswalkStore.setDraft(data as IResourceCrosswalkManager)
  if (crosswalkStore.draft.title) heading.value = crosswalkStore.draft.title
  else heading.value = crosswalkStore.draft.name
  if (route.params.id === crosswalkStore.draft.id) {
    saveApproach.value = "Create"
    appSettings.setPageName("Create crosswalk")
  }
}

async function watchEditHeadingRequest(request: string) {
  switch (request) {
    case "reset":
      crosswalkStore.resetDraft()
      await watchRequestSocket({
        state: "initialiseCrosswalk",
        data: {}
      })
      break
    case "save":
      await watchRequestSocket({
        state: "save",
        data: {}
      })
      break
    case "cancel":
      let link = `/crosswalk/${route.params.id}`
      if (saveApproach.value === 'Create') link = `/resources/${route.params.id}`
      return await navigateTo(link)
  }
}

function resetActions() {
  draftActions.value = []
  if (scripts.value && scripts.value.length)
    draftActions.value = [...scripts.value]
}

watch(() => scripts.value, () => {
  resetActions()
})

// WEBSOCKETS
async function watchResponseSocket(response: ISocketResponse) {
  let saveDraft = true
  // response: { state, data, error }
  console.log("response: ", response.state, response.data)
  switch (response.state) {
    case "initialised":
      // response.data contains the IResourceCrosswalkManager
      if (
        crosswalkStore.draft
        && Object.keys(crosswalkStore.draft).length !== 0
        && response.data
        && [crosswalkStore.draft.id, crosswalkStore.draft.crosswalk.id].includes(response.data.id as string)
      ) {
        // if already have a saved draft, & response.data.
        initialiseDraft()
        const data = {
          metadata: {
            name: crosswalkStore.draft.crosswalk.name,
            title: crosswalkStore.draft.crosswalk.title,
            description: crosswalkStore.draft.crosswalk.description,
          },
          actions: [] as string[]
        }
        if (crosswalkStore.draft.crosswalk.actions && crosswalkStore.draft.crosswalk.actions.length)
          data.actions = convertActionModelList(crosswalkStore.draft.crosswalk.actions)
        await watchRequestSocket({
          state: "loadCrosswalk",
          data
        })
      } else {
        initialiseDraft(response.data)
        await watchRequestSocket({
          state: "initialiseCrosswalk",
          data: {}
        })
      }
      appSettings.setPageState("done")
      break
    case "setMetadata":
      if (response.data && response.data.metadata) {
        crosswalkStore.setDraftMetadata(response.data.metadata)
        saveDraft = false
      }
      break
    case "addAction":
      // Hide the add panel and switch the buttons
      showAddAction.value = false
      break
    case "save":
      // backend closes the socket itself
      // redirect to the crosswalk page
      if (response.data && response.data.id) {
        streaming.value = false
        closeSocket()
        crosswalkStore.resetDraft()
        return await navigateTo(`/crosswalk/${response.data.id}`)
      }
      saveDraft = false
      break
    case "error":
      if (!crosswalkStore.draft || Object.keys(crosswalkStore.draft).length === 0)
        throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
      toast.addNotice({
        title: "Crosswalk error",
        content: `Error: ${response.error}`,
        icon: "error"
      })
      saveDraft = false
      break
  }
  if (response.data && saveDraft) {
    if (response.data.actions && response.data.actions.length)
      crosswalkStore.setActionDraft(response.data.actions as IActionModel[])
    else crosswalkStore.resetActionDraft()
  }
}

async function watchRequestSocket(request: ISocketRequest) {
  // request: { state, data }
  console.log("request: ", request.state, request.data)
  let data
  switch (request.state) {
    case "addAction":
      data = convertActionModelToScript(request.data as IActionModel)
      if (data) request.data = { script: data }
      else request.state = "error"
      break
    case "updateAction":
      data = convertActionModelToScript(request.data as IActionModel)
      if (data) request.data = {
        uuid: request.data.uuid,
        script: data
      }
      else request.state = "error"
      break
    case "removeAction":
      if (request.data.name.startsWith("action-add")) {
        request.state = "error"
        const frIdx = [...request.data.name.split("-")].slice(-1)[0]
        draftActions.value.splice(frIdx, 1)
      }
      break
  }
  if (request.state !== "error") sendSocketRequest(request.state, request.data)
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
  wsp = apiCrosswalk.socketEdit(route.params.id as string)
  await wsp.open()
  wsp.onUnpackedMessage.addListener((data) => watchResponseSocket(data))
  const jsonData: IKeyable = {
    token: crosswalkStore.authTokens.token
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

// DRAG N DROP
// https://web.dev/drag-and-drop/
function getActionID(text: string): string {
  return [...text.split("-")].slice(-5).join("-") as string
}

function handleDragStart(e: any) {
  e.currentTarget.className = e.currentTarget.className.replace(
    "bg-white",
    "bg-cerulean-100"
  )
  dragID.value = getActionID(e.currentTarget.id)
  e.dataTransfer.effectAllowed = "move"
  e.dataTransfer.setData("id", dragID.value)
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
  const hasData = e.dataTransfer.getData("id")
  if (hasData === "ADD_ACTION") {
    // Initialise a new ACTION
    const addAction: IActionModel = {
      uuid: "",
      action: e.dataTransfer.getData("addAction") as IActionType
    }
    draftActions.value.unshift(addAction)
  } else {
    resetActions()
    const dropID = getActionID(e.currentTarget.id)
    if (dragID.value !== dropID) {
      const frIdx = draftActions.value.findIndex(
        (action) => action.uuid === dragID.value
      )
      const toIdx = draftActions.value.findIndex(
        (action) => action.uuid === dropID
      )
      // Because TypeScript, in its infinite wisdom, has no concept of `-1`
      const dragged = { ...draftActions.value.slice(frIdx)[0] }
      draftActions.value.splice(frIdx, 1)
      draftActions.value.splice(toIdx, 0, dragged)
      watchRequestSocket({
        state: "reorderActions",
        data: draftActions.value.map(({ uuid }) => uuid)
      })
    }
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
<template>
  <form class="flex-auto p-3">
    <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
      <div class="col-span-full">
        <label for="crosswalk-title" class="block text-sm font-semibold leading-6 text-gray-900">Title</label>
        <div class="mt-2">
          <input type="text" name="crosswalk-title" id="crosswalk-title" v-model="draft.title"
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
        <p class="mt-2 text-sm leading-6 text-gray-600">A complete description of the crosswalk. Try and be as helpful
          as
          possible to 'future-you'.</p>
      </div>
    </div>
    <div class="mt-6 flex items-center justify-end gap-x-6">
      <button type="button" @click.prevent="resetForm"
        class="text-sm font-semibold leading-6 text-gray-900">Reset</button>
      <button type="submit" @click.prevent="submitRequest"
        class="rounded-md bg-ochre-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-ochre-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ochre-600">
        Set
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia"
import type { ISocketRequest, IKeyable } from "@/interfaces"
import { useCrosswalkStore } from "@/stores"
import { nameSpace } from "@/utilities"

const crosswalkStore = useCrosswalkStore()
const { edit } = storeToRefs(crosswalkStore)
const draft = ref({} as IKeyable)
const emit = defineEmits<{ setRequest: [request: ISocketRequest] }>()
const props = defineProps<{
  state: string,
}>()

watch(
  () => draft.value.title, (newTitle, oldTitle) => {
    if (newTitle && newTitle !== oldTitle) draft.value.name = nameSpace(newTitle)
  }, { immediate: true })

function submitRequest() {
  const data = {
    name: draft.value.name,
    title: draft.value.title,
    description: draft.value.description,
  }
  emit("setRequest", {
    state: props.state,
    data
  })
}

watch(() => edit.value, () => {
  resetForm()
})

function resetForm() {
  draft.value = {
    name: edit.value.crosswalk.name,
    title: edit.value.crosswalk.title,
    description: edit.value.crosswalk.description
  }
  if (draft.value.title) draft.value.name = nameSpace(draft.value.title)
}

onMounted(async () => {
  resetForm()
})
</script>
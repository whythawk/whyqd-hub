<template>
  <div class="relative">
    <input type="text" v-model="newWildTerm" placeholder="Set ..." @keydown="watchWildTerm"
      class="block w-full rounded-md border-0 pl-1 pr-10 text-eucalyptus-600 placeholder:text-eucalyptus-600 focus:ring-1 focus:ring-inset focus:ring-eucalyptus-600 text-sm" />
    <button @click.prevent="submitWildTerm" class="absolute inset-y-0 right-0 pr-1 flex items-center">
      <ArrowRightCircleIcon 
        :class="[hasChanged ? 'text-sienna-600 hover:bg-sienna-50 rounded-full' : 'text-gray-400', 'h-5 w-5']" 
        aria-hidden="true" />
    </button>
  </div>
</template>

<script setup lang="ts">
import { IKeyable } from "@/interfaces"
import { ArrowRightCircleIcon } from "@heroicons/vue/24/outline"

const props = defineProps<{
  wildTerm?: string | number[] | string[],
  isList: boolean,
  exclude?: string
}>()
const emit = defineEmits<{ setWild: [request: IKeyable] }>()
const newWildTerm = ref("")
const hasChanged = ref(false)

// watch(() => newWildTerm.value, () => {
//   if (newWildTerm.value !== props.wildTerm) selectedFields.value = props.currentFields as string[]
//   else selectedFields.value = []
// })

function refreshWildTerm() {
  if (props.wildTerm) {
    if (props.isList && typeof props.wildTerm !== "string" && props.wildTerm.length)
      newWildTerm.value = props.wildTerm.join(", ") as string
    else newWildTerm.value = props.wildTerm as string
  }
}

function watchWildTerm(event: any) {
  hasChanged.value = true
  if (event.key === "Enter") submitWildTerm()
}

function submitWildTerm() {
  let request: IKeyable = {
    term: newWildTerm.value ? newWildTerm.value : ""
  }
  if (
    // Can be "", i.e. empty
    (
      // Check isList of numbers
      props.isList
      && newWildTerm.value.split(",").every((t) => !isNaN(+t))
    )
    || (
      props.exclude && newWildTerm.value !== props.exclude
    )
  ) {
    request = {
      term: props.isList ? newWildTerm.value.split(",").map((t) => +t) : newWildTerm.value ? newWildTerm.value : ""
    }
  }
  hasChanged.value = false
  emit("setWild", request)
}

onMounted(async () => {
  refreshWildTerm()
})
</script>
<template>
  <div class="relative">
    <input type="text" v-model="newWildTerm" @keydown="watchWildTerm"
      class="block w-full rounded-md border-0 pl-0 pr-10 text-eucalyptus-600  focus:ring-1 focus:ring-inset focus:ring-eucalyptus-600 text-sm" />
    <button @click.prevent="submitWildTerm" class="absolute inset-y-0 right-0 flex items-center">
      <ArrowRightCircleIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
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
const newWildTerm = ref("Set ...")

watch(() => [props.wildTerm], () => {
  refreshWildTerm()
})
function refreshWildTerm() {
  if (props.wildTerm) {
    if (props.isList && typeof props.wildTerm !== "string" && props.wildTerm.length)
      newWildTerm.value = props.wildTerm.join(", ") as string
    else newWildTerm.value = props.wildTerm as string
  }
}
function watchWildTerm(event: any) {
  if (event.key === "Enter") submitWildTerm()
}

function submitWildTerm() {
  if (!newWildTerm.value) newWildTerm.value = "Set ..."
  if (
    newWildTerm.value !== "Set ..."
    || (
      // Check isList of numbers
      props.isList
      && newWildTerm.value.split(",").every((t) => !isNaN(+t))
    )
    || (
      props.exclude && newWildTerm.value !== props.exclude
    )
  ) {
    const request: IKeyable = {
      term: props.isList ? newWildTerm.value.split(",").map((t) => +t) : newWildTerm.value
    }
    emit("setWild", request)
  }
}

onMounted(async () => {
  refreshWildTerm()
})
</script>
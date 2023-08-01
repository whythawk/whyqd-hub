<template>
  <div class="relative flex-none">
    <img class="h-10 w-10" :src="avatar" :alt="props.alt" aria-hidden="true" />
  </div>
</template>

<script setup lang="ts">
import { getAvatar } from "@/utilities"
const avatar = ref("")

const props = defineProps<{
  seed: string,
  alt: string
}>()

onMounted(async () => {
  avatar.value = await getAvatar(props.seed)
})
</script>
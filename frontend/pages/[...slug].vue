<template>
  <main class="max-w-none mx-auto sm:w-3/5 prose px-4 pt-10 pb-20 sm:px-6">
    <ContentRenderer v-if="data" :value="data" />
  </main>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ["refresh"],
})

const { path } = useRoute()
const { data, error } = await useAsyncData(`content-${path}`, () => {
  return queryContent().where({ _path: path }).findOne();
})
if (error.value) {
  throw createError({ statusCode: 404, statusMessage: "Page Not Found" })
}

</script>
  
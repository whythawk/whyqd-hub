<template>
  <main class="max-w-none mx-auto sm:w-3/5 prose px-4 pt-10 pb-20 sm:px-6">
    <ContentDoc />
  </main>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ["refresh"],
});
</script>
  
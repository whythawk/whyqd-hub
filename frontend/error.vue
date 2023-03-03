<template>
  <main class="min-h-screen bg-cover bg-top sm:bg-top bg-whyqd-lost">
    <div class="max-w-7xl mx-auto px-4 py-10 text-center sm:px-6 sm:py-16 lg:px-8 lg:py-20">
      <p v-show="props.error?.statusCode === 404" class="text-sm font-semibold text-ochre-500 uppercase tracking-wide">
        404 error
      </p>
      <h1 class="mt-6 text-4xl font-extrabold text-black tracking-tight sm:text-5xl">
        Look, we're not proud, but ...
      </h1>
      <p class="mt-4 text-3xl font-medium text-ochre-500 bg-indigo-500">
        some places just aren't meant to found.
      </p>
      <div class="mt-12">
        <button @click="handleError"
          class="mx-auto flex justify-center rounded-md border border-transparent bg-ochre-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-ochre-700 focus:outline-none focus:ring-2 focus:ring-ochre-600 focus:ring-offset-2">
          Go back home
        </button>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
const props = defineProps({
  error: Object
})
const handleError = () => clearError({ redirect: "/" })
</script>

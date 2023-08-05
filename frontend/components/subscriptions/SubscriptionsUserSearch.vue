<template>
  <form class="my-3 mx-auto sm:flex sm:max-w-md">
    <label for="email-address" class="sr-only">Email address</label>
    <input type="email" name="email-address" id="email-address" autocomplete="email" v-model="email"
      class="w-full min-w-0 appearance-none rounded-md border-0 bg-white px-3 py-1.5 text-base text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-ochre-600 sm:w-64 sm:text-sm sm:leading-6 xl:w-full"
      placeholder="Find user by email" />
    <div class="mt-4 sm:ml-4 sm:mt-0 sm:flex-shrink-0">
      <button type="submit" @click.prevent="submit"
        class="flex w-full items-center justify-center rounded-md bg-ochre-600 px-3 py-2 text-sm text-white shadow-sm hover:bg-ochre-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ochre-600">Find</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { useSubscriptionsStore } from "@/stores"

const subscriptionStore = useSubscriptionsStore()
const email = ref("")
const emit = defineEmits<{ setRequest: [request: boolean] }>()

async function submit() {
  if (email.value !== "") await subscriptionStore.getSubscriber(email.value)
  if (subscriptionStore.subscriberProfile && Object.keys(subscriptionStore.subscriberProfile).length)
    emit("setRequest", true)
}
</script>
<template>
  <main class="flex min-h-full">
    <div class="flex flex-1 flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div>
          <img class="h-12 w-auto" src="/img/mark.svg" alt="Whyqd.com" />
          <h2 class="mt-6 text-3xl font-bold tracking-tight text-gray-900">Two-factor authentication</h2>
          <p class="text-sm font-medium text-ochre-500 hover:text-ochre-600 mt-6">
            Enter the 6-digit verification code from your app.
          </p>
        </div>

        <div class="mt-8">
          <div class="mt-6">
            <Form @submit="submit" :validation-schema="schema" class="space-y-6">
              <div>
                <label for="claim" class="block text-sm font-medium text-gray-700">Verification code</label>
                <div class="mt-1 group relative inline-block w-full">
                  <Field id="claim" name="claim" type="text" autocomplete="off"
                    class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-ochre-600 focus:outline-none focus:ring-ochre-600 sm:text-sm" />
                </div>
              </div>

              <div>
                <button type="submit"
                  class="flex w-full justify-center rounded-md border border-transparent bg-ochre-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-ochre-700 focus:outline-none focus:ring-2 focus:ring-ochre-600 focus:ring-offset-2">
                  Submit
                </button>
              </div>
            </Form>
          </div>
        </div>
      </div>
    </div>
    <div class="relative hidden w-0 flex-1 lg:block">
      <svg
        class="absolute inset-0 -z-10 h-full w-full stroke-gray-200 [mask-image:radial-gradient(100%_100%_at_top_right,white,transparent)]"
        aria-hidden="true">
        <defs>
          <pattern id="0787a7c5-978c-4f66-83c7-11c213f99cb7" width="90" height="30" x="50%" y="-1"
            patternUnits="userSpaceOnUse">
            <path d="M.5 200V.5H200" fill="none" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" stroke-width="0" fill="url(#0787a7c5-978c-4f66-83c7-11c213f99cb7)" />
      </svg>
    </div>
  </main>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores"
import { tokenIsTOTP } from "@/utilities"

definePageMeta({
  layout: "authentication",
  middleware: ["anonymous"],
});

const route = useRoute()
const auth = useAuthStore()
const redirectRoute = "/settings"
const subscriptionRoute = "/pricing"
let query = ""
const schema = {
  claim: { required: true, min: 6, max: 7 }
}

async function submit(values: any) {
  await auth.totpLogin(values.claim)
  if (auth.loggedIn) {
    if (query && route.query.subscription) return await navigateTo(subscriptionRoute + query)
    else return await navigateTo(redirectRoute + query)
  }
}

onMounted(async () => {
  if (
    route.query &&
    Object.keys(route.query).length !== 0 &&
    route.query.constructor === Object
  ) {
    query = "?" + Object.keys(route.query).map((key) => key + "=" + route.query[key]).join("&")
  }
  // Check if token exists
  if (!auth.authTokens.token || !tokenIsTOTP(auth.authTokens.token))
    return await navigateTo("/login" + query)
})
</script>
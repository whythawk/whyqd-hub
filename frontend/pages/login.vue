<template>
  <main class="flex min-h-full">
    <div class="flex flex-1 flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div>
          <img class="h-12 w-auto" src="/img/mark.svg" alt="Whyqd.com" />
          <h2 class="mt-6 text-3xl font-bold tracking-tight text-gray-900">
            <span v-if="!oauth">Login with email</span>
            <span v-else>Login with password</span>
          </h2>
          <p v-if="!oauth" class="text-sm font-medium text-ochre-500 hover:text-ochre-600 mt-6">
            We'll check if you have an account, and create one if you don't.
          </p>
        </div>

        <div class="mt-6">
          <Form @submit="submit" :validation-schema="schema" class="space-y-6">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
              <div class="mt-1 group relative inline-block w-full">
                <Field id="email" name="email" type="email" autocomplete="email"
                  class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-ochre-600 focus:outline-none focus:ring-ochre-600 sm:text-sm" />
                <ErrorMessage name="email"
                  class="absolute left-5 top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700" />
              </div>
            </div>

            <div v-if="oauth" class="space-y-1">
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <div class="mt-1 group relative inline-block w-full">
                <Field id="password" name="password" type="password" autocomplete="password"
                  class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-ochre-600 focus:outline-none focus:ring-ochre-600 sm:text-sm" />
                <ErrorMessage name="password"
                  class="absolute left-5 top-0 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700" />
              </div>
              <div class="text-sm text-right">
                <NuxtLink to="/recover-password" class="font-medium text-ochre-500 hover:text-ochre-600">Forgot your
                  password?</NuxtLink>
              </div>
            </div>

            <div role="status">
              <button type="submit"
                :class="[loadState ? 'pointer-none' : '', 'flex w-full justify-center items-center rounded-md border border-transparent bg-ochre-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-ochre-700 focus:outline-none focus:ring-2 focus:ring-ochre-600 focus:ring-offset-2']"
                :disabled="loadState">
                <svg v-if="loadState" aria-hidden="true" class="w-5 h-5 mr-2 text-ochre-200 animate-spin fill-white"
                  viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor" />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill" />
                </svg>
                <span v-if="loadState">Processing...</span>
                <span v-else>Submit</span>
              </button>
            </div>
          </Form>
        </div>

        <div class="mt-8 flex items-center justify-between">
          <p class="text-sm text-ochre-500 align-middle">
            If you prefer, use your password & don't email.
          </p>
          <Switch v-model="oauth"
            class="group relative inline-flex h-5 w-10 flex-shrink-0 cursor-pointer items-center justify-center rounded-full focus:outline-none focus:ring-2 focus:ring-ochre-600 focus:ring-offset-2">
            <span class="sr-only">Use setting</span>
            <span aria-hidden="true" class="pointer-events-none absolute h-full w-full rounded-md bg-white" />
            <span aria-hidden="true"
              :class="[oauth ? 'bg-ochre-500' : 'bg-gray-200', 'pointer-events-none absolute mx-auto h-4 w-9 rounded-full transition-colors duration-200 ease-in-out']" />
            <span aria-hidden="true"
              :class="[oauth ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none absolute left-0 inline-block h-5 w-5 transform rounded-full border border-gray-200 bg-white shadow ring-0 transition-transform duration-200 ease-in-out']" />
          </Switch>
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
import { Switch } from '@headlessui/vue'
import { useAuthStore } from "@/stores"
import { tokenParser, tokenIsTOTP } from "@/utilities"

definePageMeta({
  layout: "authentication",
  middleware: ["anonymous"],
});

const route = useRoute()
const auth = useAuthStore()
const redirectAfterLogin = "/"
const redirectAfterMagic = "/magic"
const redirectTOTP = "/totp"
const subscriptionRoute = "/pricing"
const loadState = ref(false)
let query = ""

const oauth = ref(false)
const schema = {
  email: { email: true, required: true },
  password: { min: 8, max: 64 },
}

async function submit(values: any) {
  loadState.value = true
  let payload = { username: values.email, password: values.password, query: "" }
  if (query && route.query.subscription) payload = { username: values.email, password: values.password, query: route.query.subscription as string }
  await auth.logIn(payload)
  loadState.value = false
  if (auth.loggedIn) {
    if (query && route.query.subscription) return await navigateTo(subscriptionRoute + query)
    else return await navigateTo(redirectAfterLogin + query)
  }
  if (auth.authTokens.token && tokenIsTOTP(auth.authTokens.token))
    return await navigateTo(redirectTOTP + query)
  if (auth.authTokens.token &&
    tokenParser(auth.authTokens.token).hasOwnProperty("fingerprint"))
    return await navigateTo(redirectAfterMagic + query)
}

onMounted(async () => {
  // Check if password requested
  if (route.query && route.query.oauth) oauth.value = true
  if (
    route.query &&
    Object.keys(route.query).length !== 0 &&
    route.query.constructor === Object
  ) {
    query = "?" + Object.keys(route.query).map((key) => key + "=" + route.query[key]).join("&")
  }
})
</script>
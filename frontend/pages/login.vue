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

            <div>
              <button type="submit"
                class="flex w-full justify-center rounded-md border border-transparent bg-ochre-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-ochre-700 focus:outline-none focus:ring-2 focus:ring-ochre-600 focus:ring-offset-2">
                Submit
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

const oauth = ref(false)
const schema = {
  email: { email: true, required: true },
  password: { min: 8, max: 64 },
}

async function submit(values: any) {
  await auth.logIn({ username: values.email, password: values.password })
  if (auth.loggedIn) return await navigateTo(redirectAfterLogin)
  if (auth.authTokens.token && tokenIsTOTP(auth.authTokens.token))
    return await navigateTo(redirectTOTP)
  if (auth.authTokens.token &&
    tokenParser(auth.authTokens.token).hasOwnProperty("fingerprint"))
    return await navigateTo(redirectAfterMagic)
}

onMounted(async () => {
  // Check if password requested
  if (route.query && route.query.oauth) oauth.value = true
})
</script>
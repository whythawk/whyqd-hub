<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <CommonLaunchCard />
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <ActivityFilterPanel />
      <ul role="list" class="space-y-6">
        <li v-for="(activity, i) in activityStore.multi" :key="`activity-${i}`">
          <ActivityCard :activity="activity" :last-card="i === activityStore.multi.length - 1" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingStore, useAuthStore, useActivityStore } from "@/stores"
import { tokenIsTOTP } from "@/utilities"

const appSettings = useSettingStore()
const auth = useAuthStore()
const activityStore = useActivityStore()

definePageMeta({
  layout: "home",
});

const redirectTOTP = "/totp"
const redirectAfterLogin = "/"

onMounted(async () => {
  // Check if email is being validated
  const route = useRoute()
  if (route.query && route.query.magic) {
    // No idea: https://stackoverflow.com/q/74759799/295606
    await new Promise((resolve) => {
      setTimeout(() => {
        resolve(true)
      }, 100)
    })
    if (!auth.loggedIn) await auth.magicLogin(route.query.magic as string)
    if (tokenIsTOTP(auth.authTokens.token)) await navigateTo(redirectTOTP)
    else await navigateTo(redirectAfterLogin)
  }
  appSettings.setPageName("Home")
  await activityStore.getMulti()
})

// METADATA - START
// https://nuxt.com/docs/getting-started/seo-meta
const title = ref("whyqd.com — more research, less wrangling")
const description = ref("Perform schema-to-schema transforms for interoperability and data reuse. Transform messy data into structured schemas using readable, auditable methods.")
useHead({
  title,
  meta: [{
    name: "description",
    content: description
  }]
})
useServerSeoMeta({
  title,
  ogTitle: title,
  description: description,
  ogDescription: description,
  ogImage: "https://whyqd.com/img/ugly-data.png"
})
// METADATA - END
</script>
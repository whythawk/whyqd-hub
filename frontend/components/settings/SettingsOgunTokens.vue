<template>
  <div class="flex-auto p-3">
    <div class="shadow rounded-md">
      <div class="space-y-6 bg-white py-6 px-4 sm:p-6">
        <div>
          <h3 class="text-lg font-medium leading-6 text-gray-900">{{ title }}</h3>
          <p class="mt-1 text-sm text-gray-500">{{ description }}</p>
        </div>
        <div v-if="!authStore.password">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <ExclamationTriangleIcon class="h-6 w-6 text-sienna-400" aria-hidden="true" />
            </div>
            <div class="ml-3 w-0 flex-1 pt-0.5">
              <p class="text-sm font-medium text-gray-900">You don't have a password!</p>
              <p class="mt-1 text-sm text-gray-500">You'll need to fully secure your account before you can create and
                manage API access.</p>
            </div>
          </div>
        </div>
        <div v-else>
          <SettingsOgunCreateModal />
          <ul v-if="ogunStore.multi && ogunStore.multi.length" role="list" class="divide-y divide-gray-100">
            <li v-for="ogun in ogunStore.multi " :key="ogun.id" class="flex justify-between gap-x-6 py-5">
              <div class="flex gap-x-4">
                <CommonAvatarIcon :seed="ogun.access_key" :alt="`Ogun ${ogun.responsibility}`" />
                <div class="min-w-0 flex-auto">
                  <p class="text-sm font-semibold leading-6 text-gray-900">{{ ogun.responsibility }}</p>
                  <p class="mt-1 truncate text-xs leading-5 text-gray-500">Key: {{ ogun.access_key }}</p>
                </div>
              </div>
              <div class="hidden sm:flex sm:flex-col sm:items-end">
                <button type="button" @click="removeOgun(ogun.access_key)">
                  <TrashIcon class="mx-auto h-6 w-6 text-sienna-500 hover:text-sienna-300" aria-hidden="true" />
                </button>
                <p class="mt-1 text-xs leading-5 text-gray-500">
                  Created <time :datetime="ogun.created">{{ readableDate(ogun.created) }}</time>
                </p>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <CommonPagination />
  </div>
</template>

<script setup lang="ts">
import { ExclamationTriangleIcon, TrashIcon } from "@heroicons/vue/24/outline"
import { useSettingStore, useAuthStore, useOgunStore } from "@/stores"
import { readableDate } from "@/utilities"

const route = useRoute()
const authStore = useAuthStore()
const appSettings = useSettingStore()
const ogunStore = useOgunStore()
const title = "API settings"
const description = "Manage your API users and keys for programmatic access to the Whyqd (/wɪkɪd/) Hub."

watch(() => [route.query], async () => {
  await updateMulti()
})

async function updateMulti() {
  if (route.query && route.query.page) ogunStore.setPage(route.query.page as string)
  await ogunStore.getMulti()
}

onMounted(async () => {
  appSettings.setPageName("Settings")
  await updateMulti()
})

async function removeOgun(key: string) {
  await ogunStore.removeTerm(key)
}

onBeforeUnmount(() => {
  const router = useRouter()
  router.replace({ query: {} })
})
</script>
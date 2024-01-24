<template>
  <div class="flex-auto p-3">
    <div class="shadow sm:overflow-hidden sm:rounded-md">
      <ModerationClearWorkingDirectory />
      <table class="min-w-full divide-y divide-gray-300">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">Name</th>
            <th scope="col" class="hidden px-3 py-3.5 text-left text-sm font-semibold text-gray-900 lg:table-cell">Email
            </th>
            <th scope="col" class="hidden px-3 py-3.5 text-left text-sm font-semibold text-gray-900 lg:table-cell">
              Validated
            </th>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Active</th>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Moderator</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 bg-white">
          <tr v-for="person in userProfiles" :key="person.id">
            <td class="w-full max-w-0 py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:w-auto sm:max-w-none sm:pl-6">
              {{ person.full_name }}
              <dl class="font-normal lg:hidden">
                <dt class="sr-only">Email</dt>
                <dd class="mt-1 truncate text-gray-700">{{ person.email }}</dd>
                <dt class="sr-only sm:hidden">Validated</dt>
                <dd class="mt-1 truncate sm:hidden">
                  <ModerationCheckState :check="person.email_validated" />
                </dd>
              </dl>
            </td>
            <td class="hidden px-3 py-4 text-sm text-gray-500 lg:table-cell">{{ person.email }}</td>
            <td class="hidden px-3 py-4 text-sm lg:table-cell">
              <ModerationCheckState :check="person.email_validated" />
            </td>
            <td class="px-3 py-4 text-sm text-gray-500">
              <ModerationToggleActive :check="person.is_active" :email="person.email" />
            </td>
            <td class="px-3 py-4 text-sm text-gray-500">
              <ModerationToggleMod :check="person.is_superuser" :email="person.email" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <CommonPagination />
  </div>
</template>

<script setup lang="ts">
import { apiAuth } from "@/api"
import { useTokenStore, useSettingStore } from "@/stores"
import { IOgunFilters, IUserProfile } from "@/interfaces"

const route = useRoute()
const router = useRouter()
const settingStore = useSettingStore()
const tokenStore = useTokenStore()
const userProfiles = ref([] as IUserProfile[])
const payload = ref<IOgunFilters>({} as IOgunFilters)

watch(() => [route.query], async () => {
  await getAllUsers()
})

async function getAllUsers() {
  if (route.query && route.query.page && !isNaN(+route.query.page)) payload.value = { page: +route.query.page }
  await tokenStore.refreshTokens()
  const { data: response } = await apiAuth.getAllUsers(tokenStore.token, payload.value)
  if (response.value && response.value.length) {
    userProfiles.value = response.value
    settingStore.setPageNext(true)
  } else {
    settingStore.setPageNext(false)
  }
}

onMounted(async () => {
  await getAllUsers()
})

onBeforeUnmount(() => {
  router.replace({ query: {} })
})
</script>
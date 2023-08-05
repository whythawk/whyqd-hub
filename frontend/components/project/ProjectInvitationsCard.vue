<template>
  <div class="flex-auto p-3">
    <div class="shadow sm:overflow-hidden sm:rounded-md min-w-max">
      <table class="min-w-full divide-y divide-gray-300">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Invited</th>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Email</th>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Response</th>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">By</th>
            <th scope="col" class="px-3 py-3.5 text-center text-sm font-semibold text-gray-900"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 bg-white">
          <tr v-for="invite in projectStore.invitations" :key="invite.id">
            <td class="px-3 py-3.5 text-left text-sm text-gray-900">
              <time :datetime="invite.created">{{ readableDate(invite.created as string) }}</time>
            </td>
            <td class="px-3 py-3.5 text-left text-sm text-gray-900">
              {{ invite.email }}
            </td>
            <td class="px-3 py-3.5 text-left text-sm  text-gray-900">{{ invite.response }}</td>
            <td class="px-3 py-3.5 text-left text-sm text-gray-900">{{ invite.sender.email }}</td>
            <td class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
              <button @click.prevent="removeInvitation(invite.id)"
                class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
                <TrashIcon class="text-sienna-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="sr-only">Delete</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <CommonPagination />
  </div>
</template>

<script setup lang="ts">
import { TrashIcon } from "@heroicons/vue/24/outline"
import { useProjectStore } from "@/stores"
import { IOgunFilters } from "@/interfaces"
import { readableDate } from "@/utilities"

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()
const payload = ref<IOgunFilters>({} as IOgunFilters)
const props = defineProps<{
  project: string
}>()

watch(() => [route.query], async () => {
  await getAllInvitations()
})

function setPage() {
  if (route.query && route.query.page && !isNaN(+route.query.page)) payload.value = { page: +route.query.page }
}

async function removeInvitation(inviteKey: string) {
  setPage()
  await projectStore.removeInvitation(props.project, inviteKey, payload.value)
}

async function getAllInvitations() {
  setPage()
  await projectStore.getInvitations(props.project, payload.value)
}

onMounted(async () => {
  await getAllInvitations()
})

onBeforeUnmount(() => {
  router.replace({ query: {} })
})
</script>
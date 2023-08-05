<template>
  <div class="flex-auto p-3">
    <div class="shadow sm:overflow-hidden sm:rounded-md min-w-max">
      <table class="min-w-full divide-y divide-gray-300">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Invited</th>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">For</th>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">By</th>
            <th scope="col" class="px-3 py-3.5 text-center text-sm font-semibold text-gray-900"></th>
            <th scope="col" class="px-3 py-3.5 text-center text-sm font-semibold text-gray-900"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 bg-white">
          <tr v-for="invite in projectStore.invitations" :key="invite.id">
            <td class="px-3 py-3.5 text-left text-sm text-gray-900">
              <time :datetime="invite.created">{{ readableDate(invite.created as string) }}</time>
            </td>
            <td class="px-3 py-3.5 text-left text-sm truncate text-gray-900">{{ getProjectName(invite.project) }}</td>
            <td class="px-3 py-3.5 text-left text-sm text-gray-900">{{ invite.sender.email }}</td>
            <td class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
              <button @click.prevent="acceptInvitation(invite.id)"
                class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
                <CheckIcon class="text-eucalyptus-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="sr-only">Accept</span>
              </button>
            </td>
            <td class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
              <button @click.prevent="rejectInvitation(invite.id)"
                class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
                <TrashIcon class="text-sienna-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="sr-only">Reject</span>
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
import { CheckIcon, TrashIcon } from "@heroicons/vue/24/outline"
import { useProjectStore } from "@/stores"
import { IOgunFilters, IModelSummary } from "@/interfaces"
import { readableDate } from "@/utilities"

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()
const payload = ref<IOgunFilters>({} as IOgunFilters)

watch(() => [route.query], async () => {
  await getAllInvitations()
})

function getProjectName(project: IModelSummary) {
  if (project.title) return project.title
  return project.name
}

function setPage() {
  if (route.query && route.query.page && !isNaN(+route.query.page)) payload.value = { page: +route.query.page }
}

async function rejectInvitation(inviteKey: string) {
  setPage()
  await projectStore.rejectInvitation(inviteKey, payload.value)
}

async function acceptInvitation(inviteKey: string) {
  setPage()
  await projectStore.acceptInvitation(inviteKey, payload.value)
}

async function getAllInvitations() {
  setPage()
  await projectStore.getMembershipInvitations(payload.value)
}

onMounted(async () => {
  await getAllInvitations()
})

onBeforeUnmount(() => {
  router.replace({ query: {} })
})
</script>
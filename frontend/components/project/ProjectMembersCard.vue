<template>
  <div class="flex-auto p-3">
    <div class="shadow sm:rounded-md min-w-max">
      <ProjectInvitationPanel v-if="projectStore.isCustodian" :project="props.project" />
      <table class="min-w-full divide-y divide-gray-300">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Since</th>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Name</th>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Email</th>
            <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
              Responsibility
            </th>
            <th scope="col" class="px-3 py-3.5 text-center text-sm font-semibold text-gray-900"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 bg-white">
          <tr v-for="member in projectStore.members" :key="member.id">
            <td class="px-3 py-3.5 text-left text-sm text-gray-900">
              <time :datetime="member.created">{{ readableDate(member.created as string) }}</time>
            </td>
            <td class="px-3 py-3.5 text-left text-sm text-gray-900">
              {{ member.researcher.full_name }}
            </td>
            <td class="px-3 py-3.5 text-left text-sm text-gray-900">{{ member.researcher.email }}</td>
            <td v-if="projectStore.isCustodian && member.researcher.email !== authStore.email"
              class="pr-3 py-3.5 text-left text-sm  text-gray-900">
              <Listbox>
                <div class="relative">
                  <ListboxButton
                    class="relative w-full cursor-default rounded-lg bg-white py-1 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-ochre-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-ochre-300 sm:text-sm">
                    <span class="block truncate">{{ member.responsibility }}</span>
                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                      <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                    </span>
                  </ListboxButton>
                  <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                    leave-to-class="opacity-0">
                    <ListboxOptions
                      class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-md ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                      <ListboxOption v-slot="{ active, selected }" v-for="rtype in parameters.role"
                        :key="`rtype-${rtype.value}`" :value="rtype.value" as="template">
                        <li :class="[
                          active ? 'bg-ochre-100 text-ochre-900' : 'text-gray-900',
                          'relative cursor-default select-none py-2 pl-10 pr-4',
                        ]" @click="updateMemberRole(member.id, rtype.value as IResearcherRoleType)">
                          <span :class="[
                            selected ? 'font-medium' : 'font-normal',
                            'block truncate',
                          ]">{{ rtype.value }}</span>
                          <span v-if="selected" class="absolute inset-y-0 left-0 flex items-center pl-3 text-ochre-600">
                            <CheckIcon class="h-5 w-5" aria-hidden="true" />
                          </span>
                        </li>
                      </ListboxOption>
                    </ListboxOptions>
                  </transition>
                </div>
              </Listbox>
            </td>
            <td v-else class="px-3 py-3.5 text-left text-sm  text-gray-900">{{ member.responsibility }}</td>
            <td v-if="member.researcher.email === authStore.email"
              class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
              <CheckCircleIcon class="text-eucalyptus-700 h-5 w-5" aria-hidden="true" />
            </td>
            <td v-if="member.researcher.email !== authStore.email && projectStore.isCustodian"
              class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
              <button @click.prevent="removeMember(member.id)"
                class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
                <TrashIcon class="text-sienna-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="sr-only">Remove</span>
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
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, } from "@headlessui/vue"
import { CheckCircleIcon, CheckIcon, ChevronUpDownIcon, TrashIcon } from "@heroicons/vue/24/outline"
import { useProjectStore, useAuthStore } from "@/stores"
import type { IOgunFilters, IResearcherRoleType } from "@/interfaces"
import { readableDate } from "@/utilities"

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()
const authStore = useAuthStore()
const payload = ref<IOgunFilters>({} as IOgunFilters)
const props = defineProps<{
  project: string
}>()
const parameters = {
  role: [
    { value: "SEEKER" },
    { value: "WRANGLER" },
    { value: "CURATOR" },
    { value: "CUSTODIAN" },
  ],
}

watch(() => [route.query], async () => {
  await getAllMembers()
})

async function getAllMembers() {
  if (route.query && route.query.page && !isNaN(+route.query.page)) payload.value = { page: +route.query.page }
  await projectStore.getMembers(props.project, payload.value)
}

async function updateMemberRole(roleID: string, role: IResearcherRoleType) {
  await projectStore.updateMember(props.project, roleID, role, payload.value)
  await getAllMembers()
}

async function removeMember(memberKey: string) {
  await projectStore.removeMember(props.project, memberKey, payload.value)
}

onMounted(async () => {
  await getAllMembers()
})

onBeforeUnmount(() => {
  router.replace({ query: {} })
})
</script>
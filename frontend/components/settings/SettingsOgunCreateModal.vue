<template>
  <div class="flex justify-start">
    <Menu as="div" class="relative text-left">
      <MenuButton
        class="flex items-center justify-start -ml-px gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
        <CommandLineIcon class="-ml-0.5 h-5 w-5 text-gray-400" aria-hidden="true" />
        <span>Create key</span>
        <ChevronDownIcon class="-ml h-5 w-5 text-gray-400" aria-hidden="true" />
      </MenuButton>
      <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
        <MenuItems
          class="absolute right-0 z-10 mt-2 w-72 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
          <div class="justify-start">
            <MenuItem v-for="role in ogunRoles" :key="`ogun-new-${role.name}`" v-slot="{ active }">
            <button type="button" @click.prevent="createOgun(role.name as IResearcherRoleType)"
              :class="['flex cursor-default select-none rounded-md p-3', active && 'bg-gray-100']">
              <CommonAvatarIcon :seed="role.name" :alt="`Ogun ${role.name}`" />
              <div class="ml-4 text-start">
                <p :class="['text-sm font-medium', active ? 'text-gray-900' : 'text-gray-700']">
                  {{ role.name }}
                </p>
                <p :class="['text-sm', active ? 'text-gray-700' : 'text-gray-500']">
                  {{ role.description }}
                </p>
              </div>
            </button>
            </MenuItem>
          </div>
        </MenuItems>
      </transition>
    </Menu>
    <TransitionRoot appear :show="isOpen" as="template">
      <Dialog as="div" class="relative z-50">
        <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0" enter-to="opacity-100"
          leave="duration-200 ease-in" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-black bg-opacity-25" />
        </TransitionChild>
        <div class="fixed inset-0">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100" leave="duration-200 ease-in" leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95">
              <DialogPanel
                class="w-full max-w-md transform overflow-hidden rounded-md bg-white p-2 text-left align-middle shadow-xl transition-all">
                <DialogTitle as="h3" class="flex justify-between items-center w-full text-lg font-medium text-gray-900">
                  <div class="flex items-center flex-shrink-0">
                    <CommonAvatarIcon v-if="createResponse.access_key" :seed="createResponse.access_key"
                      :alt="`Ogun ${createResponse.responsibility}`" />
                    <span class="pl-2">SUCCESS - NOW SAVE YOUR KEYS!</span>
                  </div>
                  <div class="mr-2 flex flex-shrink-0">
                    <button type="button" @click="clearOgun"
                      class="inline-flex rounded-md bg-white text-sienna-400 hover:text-sienna-500 focus:outline-none">
                      <span class="sr-only">Close</span>
                      <XMarkIcon class="h-5 w-5" aria-hidden="true" />
                    </button>
                  </div>
                </DialogTitle>
                <div class="flex items-start">
                  <div class="ml-3 w-0 flex-1 pt-0.5 mt-2">
                    <p class="mt-1 text-sm text-gray-600">
                      <span class="font-bold">Access key:</span> {{ createResponse.access_key }}
                    </p>
                    <p class="mt-1 text-sm text-gray-600">
                      <span class="font-bold">Secret key:</span> {{ createResponse.secret_key }}
                    </p>
                    <p class="text-sm font-medium text-center text-gray-900 my-2">Your secret key cannot be recovered.</p>
                  </div>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup lang="ts">
import {
  Menu, MenuButton, MenuItems, MenuItem,
  TransitionRoot, TransitionChild, Dialog,
  DialogPanel, DialogTitle,
} from "@headlessui/vue"
import { CommandLineIcon, ChevronDownIcon, XMarkIcon } from "@heroicons/vue/24/outline"
import { useToastStore, useOgunStore } from "@/stores"
import { apiOgun } from "@/api"
import type { IResearcherRoleType, IOgunCreate } from "@/interfaces"

const ogunStore = useOgunStore()
const toastStore = useToastStore()
const isOpen = ref(false)
const createResponse = shallowRef<IOgunCreate>({} as IOgunCreate)
const ogunRoles = [
  {
    name: "SEEKER",
    description: "View existing work. Full rights over work it creates."
  },
  {
    name: "WRANGLER",
    description: "Edit crosswalks. Full rights over work it creates."
  },
  {
    name: "CURATOR",
    description: "Edit schemas and crosswalks. Full rights over work it creates."
  },
]

function clearOgun() {
  createResponse.value = {} as IOgunCreate
  isOpen.value = false
}

async function createOgun(role: IResearcherRoleType) {
  await ogunStore.authTokens.refreshTokens()
  if (ogunStore.authTokens.token) {
    try {
      const { data: response } = await apiOgun.createTerm(ogunStore.authTokens.token, role)
      if (response.value) {
        createResponse.value = response.value
        await ogunStore.getMulti()
        isOpen.value = true
      }
    } catch (error) {
      toastStore.addNotice({
        title: "API creation error",
        content: error as string,
        icon: "error"
      })
    }
  }
}
</script>

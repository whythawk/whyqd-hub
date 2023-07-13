<template>
  <!-- Profile dropdown -->
  <Menu as="div" class="relative ml-3 pb-8 lg:pl-6 overflow-x-visible">
    <div v-if="!authStore.loggedIn">
      <NuxtLink to="/login"
        class="text-ochre-600 hover:text-ochre-500 focus:outline-none group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold">
        <ArrowLeftOnRectangleIcon class="h-6 w-6 shrink-0" />
        <span class="hidden lg:block">Login</span>
      </NuxtLink>
    </div>
    <div v-else class="flex">
      <NuxtLink to="#" class="hidden lg:group lg:block lg:flex-grow hover:bg-gray-50">
        <div class="flex items-center">
          <div class="rounded-lg bg-gray-200 -mx-2 w-12">
            <img class="h-12 w-12 rounded-full" :src="avatar" alt="authStore.email" />
          </div>
          <div class="ml-3">
            <p class="text-sm font-medium text-gray-700 group-hover:text-gray-900 truncate">{{ authStore.full_name }}</p>
            <p class="text-xs font-medium text-gray-500 group-hover:text-gray-700 truncate">{{ authStore.email }}</p>
          </div>
        </div>
      </NuxtLink>
      <MenuButton class="inline-flex items-center hover:bg-gray-50 rounded-full text-sm focus:outline-none">
        <span class="sr-only">Open user menu</span>
        <EllipsisVerticalIcon class="hidden lg:block h-6 w-6 text-gray-500" />
        <div class="flex items-center lg:hidden">
          <div class="rounded-lg bg-gray-200 w-12">
            <img class="h-12 w-12 rounded-full" :src="avatar" alt="authStore.email" />
          </div>
        </div>
      </MenuButton>
    </div>
    <transition enter-active-class="transition ease-out duration-200" enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
      <MenuItems
        class="-top-4 transform -translate-y-full absolute lg:right-2 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-md ring-1 ring-black ring-opacity-5 focus:outline-none overflow-x-visible">
        <MenuItem v-for="(nav, i) in navigation" :key="`nav-${i}`" v-slot="{ active }">
        <NuxtLink :to="nav.to" :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']">{{
          nav.name }}
        </NuxtLink>
        </MenuItem>
        <MenuItem v-slot="{ active }">
        <a :class="[active ? 'bg-gray-100 cursor-pointer' : '', 'block px-4 py-2 text-sm text-gray-700 cursor-pointer']"
          @click="logout">
          Logout
        </a>
        </MenuItem>
      </MenuItems>
    </transition>
  </Menu>
</template>

  
<script setup lang="ts">
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue"
import { ArrowLeftOnRectangleIcon, EllipsisVerticalIcon } from "@heroicons/vue/24/outline"
import { useAuthStore } from "@/stores"
import { getAvatar } from "@/utilities"

// With credit to DiceBear https://dicebear.com/styles/bottts
// And Pablo Stanley for https://bottts.com/

const authStore = useAuthStore()
const avatar = ref("")

const navigation = [
  { name: "Settings", to: "/settings" },
]
const redirectRoute = "/"

async function logout() {
  authStore.logOut()
  await navigateTo(redirectRoute)
}

onMounted(async () => {
  // Check if user is logged in
  if (authStore.loggedIn)
    avatar.value = await getAvatar(authStore.email as string)
})
</script>
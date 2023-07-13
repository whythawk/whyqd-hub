<template>
  <!-- Profile dropdown -->
  <Menu as="div" class="relative ml-3">
    <div v-if="!authStore.loggedIn">
      <NuxtLink to="/login" class="rounded-full p-1 text-ochre-600 hover:text-ochre-500 focus:outline-none">
        <ArrowLeftOnRectangleIcon class="h-6 w-6 shrink-0" />
      </NuxtLink>
    </div>
    <div v-else class="flex">
      <MenuButton class="inline-flex items-center hover:bg-gray-50 rounded-full text-sm focus:outline-none">
        <span class="sr-only">Open user menu</span>
        <div class="flex items-center">
          <div class="rounded-lg bg-gray-200 w-8">
            <img class="h-8 w-8 rounded-full" :src="avatar" :alt="authStore.email" />
          </div>
        </div>
      </MenuButton>
    </div>
    <transition enter-active-class="transition ease-out duration-200" enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
      <MenuItems
        class="absolute z-10 mt-2 w-48 origin-top-left right-2 md:top-5 md:transform md:-translate-y-full md:right-8 rounded-md bg-white py-1 shadow-md ring-1 ring-black ring-opacity-5 focus:outline-none">
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
import { ArrowLeftOnRectangleIcon } from "@heroicons/vue/24/outline"
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
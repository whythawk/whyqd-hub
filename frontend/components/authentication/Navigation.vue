<template>
  <!-- Profile dropdown -->
  <Menu as="div" class="relative ml-3">
    <div v-if="!auth.loggedIn">
      <NuxtLink to="/login" class="rounded-full p-1 text-ochre-600 hover:text-ochre-500 focus:outline-none">
        <ArrowLeftOnRectangleIcon class="block h-6 w-6" />
      </NuxtLink>
    </div>
    <div v-else>
      <MenuButton class="flex rounded-full bg-white text-sm focus:outline-none">
        <span class="sr-only">Open user menu</span>
        <img class="h-8 w-8 rounded-full" :src="avatar" alt="auth.email" />
      </MenuButton>
    </div>
    <transition enter-active-class="transition ease-out duration-200" enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
      <MenuItems
        class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
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

  
<script setup>
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue"
import { ArrowLeftOnRectangleIcon } from "@heroicons/vue/24/outline"
import { useAuthStore } from "@/stores"
import { createAvatar } from "@dicebear/core"
import * as bottts from "@dicebear/bottts"

// With credit to DiceBear https://dicebear.com/styles/bottts
// And Pablo Stanley for https://bottts.com/

const auth = useAuthStore()
const avatar = ref("")

const navigation = [
  { name: "Settings", to: "/settings" },
]
const redirectRoute = "/"

async function logout() {
  auth.logOut()
  await navigateTo(redirectRoute)
}

onMounted(async () => {
  // Check if user is logged in
  if (auth.loggedIn)
    avatar.value = await createAvatar(bottts, {
      seed: auth.email,
      scale: 90,
      randomiseIds: true,
    }).toDataUri()
})
</script>
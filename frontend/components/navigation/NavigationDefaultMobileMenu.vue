<template>
  <div>
    <!-- TOP BAR -->
    <div class="fixed top-0 z-30 w-full flex items-center gap-x-6 bg-white/90 px-4 py-4 sm:px-6 md:hidden">
      <div v-if="headingTerm && Object.keys(headingTerm).length !== 0"
        class="group inline-flex gap-x-3 flex-1 text-md font-semibold leading-6 text-ochre-600">
        <component :is="headingTerm.icon" class="text-ochre-600 h-6 w-6 shrink-0" aria-hidden="true" />
        {{ headingTerm.name }}
      </div>
      <div v-else class="group inline-flex gap-x-3 flex-1 text-md font-semibold leading-6 text-ochre-600">
        {{ appSettings.current.pageName }}
      </div>
      <AuthenticationNavigation />
    </div>
    <!-- BOTTOM BAR -->
    <Menu as="div" class="z-30 fixed md:hidden inset-x-0 bottom-0 w-full bg-white">
      <div class="max-w-full mx-auto">
        <nav class="relative grid grid-cols-4 gap-4 justify-center py-1" aria-label="Global">
          <NuxtLink v-for="(item, i) in baseNavigation" :key="`basenav-${i}`" :to="item.to" :class="[!(auth.loggedIn || !item.login)
            ? 'pointer-events-none text-gray-500'
            : item.name === appSettings.current.pageName
              ? 'bg-gray-50 text-ochre-600'
              : 'text-gray-700 hover:text-ochre-600 hover:bg-gray-50',
            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
            :disabled="!(auth.loggedIn || !item.login)">
            <component :is="item.icon"
              :class="[item.name === appSettings.current.pageName ? 'text-ochre-600' : 'text-gray-400 group-hover:text-ochre-600', 'h-6 w-6 shrink-0 inline-flex items-center']"
              aria-hidden="true" />
          </NuxtLink>
          <MenuButton class="group flex-col inline-flex items-center gap-x-3 rounded-md p-2 text-sm font-semibold">
            <span class="sr-only">Open user menu</span>
            <EllipsisHorizontalIcon class="block h-6 w-6 text-gray-500" />
          </MenuButton>
        </nav>
      </div>
      <transition enter-active-class="transition ease-out duration-200" enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
        <MenuItems
          class="-top-4 transform -translate-y-full absolute z-10 mt-2 w-full origin-top-right rounded-md bg-white/90 py-1 shadow-md ring-1 ring-black ring-opacity-5 focus:outline-none overflow-x-visible">
          <MenuItem v-for="(item, i) in leadNavigation" :key="`scndrynav-${i}`" v-slot="{ active }">
          <NuxtLink :to="item.to" :class="[!(auth.loggedIn || !item.login)
            ? 'pointer-events-none text-gray-500'
            : item.name === appSettings.current.pageName
              ? 'bg-gray-50 text-ochre-600'
              : 'text-gray-700 hover:text-ochre-600 hover:bg-gray-50',
            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
            :disabled="!(auth.loggedIn || !item.login)">
            <component :is="item.icon"
              :class="[item.name === appSettings.current.pageName || active ? 'text-ochre-600' : 'text-gray-400 group-hover:text-ochre-600', 'h-6 w-6 shrink-0']"
              aria-hidden="true" />
            {{ item.name }}
          </NuxtLink>
          </MenuItem>
          <MenuItem v-for="(item, i) in secondaryNavigation" :key="`scndrynav-${i}`" v-slot="{ active }">
          <NuxtLink :to="item.to" :class="[!(auth.loggedIn || !item.login)
            ? 'pointer-events-none text-gray-500'
            : item.name === appSettings.current.pageName
              ? 'bg-gray-50 text-ochre-600'
              : 'text-gray-700 hover:text-ochre-600 hover:bg-gray-50',
            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
            :disabled="!(auth.loggedIn || !item.login)">
            <component :is="item.icon"
              :class="[item.name === appSettings.current.pageName || active ? 'text-ochre-600' : 'text-gray-400 group-hover:text-ochre-600', 'h-6 w-6 shrink-0']"
              aria-hidden="true" />
            {{ item.name }}
          </NuxtLink>
          </MenuItem>
        </MenuItems>
      </transition>
    </Menu>
  </div>
</template>

<script setup lang="ts">
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue"
import {
  ArrowUpTrayIcon,
  BeakerIcon,
  BellIcon,
  // BookmarkIcon,
  CalendarIcon,
  Cog8ToothIcon,
  DocumentTextIcon,
  EllipsisHorizontalIcon,
  HomeIcon,
  // MagnifyingGlassIcon,
  RectangleGroupIcon,
  Square3Stack3DIcon,
} from "@heroicons/vue/24/outline"
import { useSettingStore, useAuthStore } from "@/stores"

const appSettings = useSettingStore()
const auth = useAuthStore()
const headingTerm = ref({} as INav)

interface INav {
  name: string
  to: string
  icon: any
  login: boolean
}

const baseNavigation: INav[] = [
  { name: "Home", to: "/", icon: HomeIcon, login: false },
  // { name: "Search", to: "/search", icon: MagnifyingGlassIcon },
  { name: "Activity", to: "/activity", icon: BellIcon, login: true },
  { name: "Schedule", to: "/schedule", icon: CalendarIcon, login: true },
]
const leadNavigation: INav[] = [
  { name: "Home", to: "/", icon: HomeIcon, login: false },
  { name: "Activity", to: "/activity", icon: BellIcon, login: true },
  { name: "Schedule", to: "/schedule", icon: CalendarIcon, login: true },
  // { name: "Bookmarks", to: "/bookmarks", icon: BookmarkIcon, login: true  },
]
const secondaryNavigation: INav[] = [
  { name: "Import", to: "/import", icon: ArrowUpTrayIcon, login: true },
  { name: "References", to: "/references", icon: DocumentTextIcon, login: true },
  { name: "Resources", to: "/resources", icon: RectangleGroupIcon, login: true },
  { name: "Tasks", to: "/tasks", icon: Square3Stack3DIcon, login: true },
  { name: "Projects", to: "/projects", icon: BeakerIcon, login: true },
  { name: "Settings", to: "/settings", icon: Cog8ToothIcon, login: true },
]

function getCurrent() {
  const navigationObjects = [...baseNavigation, ...leadNavigation, ...secondaryNavigation]
  const response = navigationObjects.find((item) => item.name === appSettings.current.pageName)
  if (response) return response
  return {} as INav
}

onMounted(() => {
  headingTerm.value = getCurrent()
})
</script>
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
    <Popover as="div" class="z-30 fixed md:hidden inset-x-0 bottom-0 w-full bg-white">
      <div class="max-w-full mx-auto">
        <nav class="relative grid grid-cols-4 gap-4 justify-center py-1" aria-label="Global">
          <NuxtLink v-for="(item, i) in baseNavigation" :key="`basenav-${i}`" :to="item.to" :class="[!(auth.loggedIn || !item.login)
            ? 'pointer-events-none text-gray-500'
            : item.name === appSettings.current.pageName
              ? 'bg-gray-50 text-ochre-600'
              : 'text-gray-700 hover:text-ochre-600 hover:bg-gray-50',
            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold justify-center']"
            :disabled="!(auth.loggedIn || !item.login)">
            <component :is="item.icon"
              :class="[item.name === appSettings.current.pageName ? 'text-ochre-600' : 'text-gray-400 group-hover:text-ochre-600', 'h-6 w-6 shrink-0 inline-flex items-center']"
              aria-hidden="true" />
          </NuxtLink>
          <PopoverButton class="group flex-col inline-flex items-center gap-x-3 rounded-md p-2 text-sm font-semibold">
            <span class="sr-only">Open user menu</span>
            <EllipsisHorizontalIcon class="block h-6 w-6 text-gray-500" />
          </PopoverButton>
        </nav>
      </div>
      <transition enter-active-class="transition ease-out duration-200" enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
        <PopoverPanel
          class="-top-4 transform -translate-y-full absolute z-10 mt-2 w-full origin-top-right rounded-md bg-white/90 pt-1 shadow-md ring-1 ring-black ring-opacity-5 focus:outline-none overflow-x-visible">
          <NuxtLink v-for="(item, i) in leadNavigation" :key="`scndrynav-${i}`" :to="item.to" :class="[!(auth.loggedIn || !item.login)
            ? 'pointer-events-none text-gray-500'
            : item.name === appSettings.current.pageName
              ? 'bg-gray-50 text-ochre-600'
              : 'text-gray-700 hover:text-ochre-600 hover:bg-gray-50',
            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
            :disabled="!(auth.loggedIn || !item.login)">
            <component :is="item.icon"
              :class="[item.name === appSettings.current.pageName ? 'text-ochre-600' : 'text-gray-400 group-hover:text-ochre-600', 'h-6 w-6 shrink-0']"
              aria-hidden="true" />
            {{ item.name }}
          </NuxtLink>
          <NuxtLink v-for="(item, i) in secondaryNavigation" :key="`scndrynav-${i}`" :to="item.to" :class="[!(auth.loggedIn || !item.login)
            ? 'pointer-events-none text-gray-500'
            : item.name === appSettings.current.pageName
              ? 'bg-gray-50 text-ochre-600'
              : 'text-gray-700 hover:text-ochre-600 hover:bg-gray-50',
            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
            :disabled="!(auth.loggedIn || !item.login)">
            <component :is="item.icon"
              :class="[item.name === appSettings.current.pageName ? 'text-ochre-600' : 'text-gray-400 group-hover:text-ochre-600', 'h-6 w-6 shrink-0']"
              aria-hidden="true" />
            {{ item.name }}
          </NuxtLink>
          <div class="flex flex-wrap justify-center bg-gray-50 mt-2 py-3">
            <div v-for="item in footerNavigation" :key="item.name">
              <NuxtLink :to="item.to" class="text-sm text-gray-400 hover:text-gray-300">{{ item.name }}</NuxtLink>
              <span v-show="item.dot" class="text-sm text-gray-400 px-2">&middot;</span>
            </div>
          </div>
        </PopoverPanel>
      </transition>
    </Popover>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia"
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue"
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
  Squares2X2Icon,
} from "@heroicons/vue/24/outline"
import { useSettingStore, useAuthStore } from "@/stores"

const appSettings = useSettingStore()
const { pageName } = storeToRefs(appSettings)
const auth = useAuthStore()
const headingTerm = ref({} as INav)

interface INav {
  name: string
  to: string
  icon: any
  login: boolean
}

watch(() => pageName.value, () => {
  headingTerm.value = getCurrent()
})

const baseNavigation: INav[] = [
  { name: "Home", to: "/", icon: HomeIcon, login: false },
  // { name: "Search", to: "/search", icon: MagnifyingGlassIcon },
  { name: "Schedule", to: "/schedule", icon: CalendarIcon, login: true },
  { name: "Activity", to: "/activity", icon: BellIcon, login: true },
]
const leadNavigation: INav[] = [
  { name: "Home", to: "/", icon: HomeIcon, login: false },
  { name: "Schedule", to: "/schedule", icon: CalendarIcon, login: true },
  { name: "Activity", to: "/activity", icon: BellIcon, login: true },
  { name: "Import", to: "/import", icon: ArrowUpTrayIcon, login: true },
  // { name: "Bookmarks", to: "/bookmarks", icon: BookmarkIcon, login: true  },
]
const secondaryNavigation: INav[] = [
  { name: "Schemas", to: "/schema", icon: Squares2X2Icon, login: true },
  // { name: "Resources", to: "/resources", icon: RectangleGroupIcon, login: true },
  // { name: "Tasks", to: "/tasks", icon: Square3Stack3DIcon, login: true },
  // { name: "Projects", to: "/projects", icon: BeakerIcon, login: true },
  { name: "Settings", to: "/settings", icon: Cog8ToothIcon, login: true },
]
const footerNavigation = [
  { name: "About", to: "/about", dot: true },
  { name: "Pricing", to: "/pricing", dot: true },
  { name: "Developers", to: "https://whyqd.readthedocs.io/", dot: true },
  { name: "Privacy", to: "/privacy", dot: true },
  { name: "Contact", to: "/contact", dot: false },
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
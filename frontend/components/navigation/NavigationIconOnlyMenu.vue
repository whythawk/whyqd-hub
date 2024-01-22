<template>
  <div class="hidden md:fixed md:inset-y-0 md:z-30 md:flex md:flex-col md:w-24">
    <div class="flex grow flex-col gap-y-5 px-6">
      <div class="flex h-16 shrink-0 items-center">
        <img class="block h-8 w-auto lg:hidden" src="/img/mark.svg" alt="Whyqd.com" />
        <img class="hidden h-8 w-auto lg:block" src="/img/mark.svg" alt="Whyqd.com" />
      </div>
      <nav class="flex flex-1 flex-col">
        <ul role="list" class="flex flex-1 flex-col gap-y-7">
          <!-- <li class="block lg:hidden -mx-2 space-y-1">
            <NuxtLink to="#"
              class="text-gray-400 hover:text-ochre-600 hover:bg-gray-50 group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold">
              <MagnifyingGlassIcon class="h-6 w-6 shrink-0" aria-hidden="true" />
            </NuxtLink>
          </li> -->
          <li>
            <ul role="list" class="-mx-2 space-y-1">
              <li v-for="item in leadNavigation" :key="item.name">
                <NuxtLink :to="item.to" :class="[!(auth.loggedIn || !item.login)
                  ? 'pointer-events-none text-gray-500'
                  : item.name === appSettings.current.pageName
                    ? 'bg-gray-50 text-ochre-600'
                    : 'text-gray-700 hover:text-ochre-600 hover:bg-gray-50',
                  'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
                  :disabled="!(auth.loggedIn || !item.login)">
                  <component :is="item.icon"
                    :class="[item.name === appSettings.current.pageName ? 'text-ochre-600' : 'text-gray-400 group-hover:text-ochre-600', 'h-6 w-6 shrink-0']"
                    aria-hidden="true" />
                </NuxtLink>
              </li>
            </ul>
          </li>
          <li>
            <ul role="list" class="-mx-2 mt-2 space-y-1">
              <li v-for="item in secondaryNavigation" :key="item.name">
                <NuxtLink :to="item.to" :class="[!(auth.loggedIn || !item.login)
                  ? 'pointer-events-none text-gray-500'
                  : item.name === appSettings.current.pageName
                    ? 'bg-gray-50 text-ochre-600'
                    : 'text-gray-700 hover:text-ochre-600 hover:bg-gray-50',
                  'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
                  :disabled="!(auth.loggedIn || !item.login)">
                  <component :is="item.icon"
                    :class="[item.name === appSettings.current.pageName ? 'text-ochre-600' : 'text-gray-400 group-hover:text-ochre-600', 'h-6 w-6 shrink-0']"
                    aria-hidden="true" />
                </NuxtLink>
              </li>
            </ul>
          </li>
          <li class="-mx-4 mb-2 mt-auto">
            <AuthenticationNavigation />
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ArrowUpTrayIcon,
  BeakerIcon,
  BellIcon,
  // BookmarkIcon,
  CalendarIcon,
  Cog8ToothIcon,
  DocumentTextIcon,
  HomeIcon,
  // MagnifyingGlassIcon,
  RectangleGroupIcon,
  Square3Stack3DIcon,
  Squares2X2Icon,
} from "@heroicons/vue/24/outline"
import { useSettingStore, useAuthStore } from "@/stores"

const appSettings = useSettingStore()
const auth = useAuthStore()

const leadNavigation = [
  { name: "Home", to: "/", icon: HomeIcon, login: false },
  { name: "Schedule", to: "/schedule", icon: CalendarIcon, login: true },
  { name: "Activity", to: "/activity", icon: BellIcon, login: true },
  // { name: "Bookmarks", to: "/bookmarks", icon: BookmarkIcon, login: true },
  { name: "Import", to: "/import", icon: ArrowUpTrayIcon, login: true },
]

const secondaryNavigation = [
  { name: "Schemas", to: "/schema", icon: Squares2X2Icon, login: true },
  { name: "Settings", to: "/settings", icon: Cog8ToothIcon, login: true },
]
</script>
<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 min-w-full min-h-full mx-auto">
    <div v-if="appSettings.current.pageState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <div class="mx-auto min-w-full px-2 sm:px-3 lg:px-6">


        <div
          class="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
          <button type="button" class="-m-2.5 p-2.5 text-gray-700 lg:hidden" @click="sidebarOpen = true">
            <span class="sr-only">Open sidebar</span>
            <Bars3Icon class="h-6 w-6" aria-hidden="true" />
          </button>

          <!-- Separator -->
          <div class="h-6 w-px bg-gray-900/10 lg:hidden" aria-hidden="true" />

          <div class="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
            <form class="relative flex flex-1" action="#" method="GET">
              <label for="search-field" class="sr-only">Search</label>
              <MagnifyingGlassIcon class="pointer-events-none absolute inset-y-0 left-0 h-full w-5 text-gray-400"
                aria-hidden="true" />
              <input id="search-field"
                class="block h-full w-full border-0 py-0 pl-8 pr-0 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
                placeholder="Search..." type="search" name="search" />
            </form>
            <div class="flex items-center gap-x-4 lg:gap-x-6">
              <!-- Separator -->
              <div class="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-900/10" aria-hidden="true" />
              <Menu as="div" class="relative inline-block text-left">
                <div>
                  <MenuButton
                    class="inline-flex items-center w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm  text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                    <ExclamationCircleIcon class="-ml-0.5 h-5 w-5 text-sienna-600" aria-hidden="true" />
                    Reload
                    <ChevronDownIcon class="-mr-1 h-4 w-4 text-gray-400" aria-hidden="true" />
                  </MenuButton>
                </div>
                <transition enter-active-class="transition ease-out duration-100"
                  enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
                  leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100"
                  leave-to-class="transform opacity-0 scale-95">
                  <MenuItems
                    class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <div class="py-1">
                      <MenuItem v-slot="{ active }">
                      <button type="button"
                        :class="[active ? 'bg-sienna-100 text-gray-900' : 'text-gray-700', 'flex items-center w-full gap-x-1.5 px-4 py-2 text-sm']">
                        <ArrowPathIcon class="-ml-0.5 h-5 w-5 text-gray-400" aria-hidden="true" />
                        Reload
                      </button>
                      </MenuItem>
                    </div>
                  </MenuItems>
                </transition>
              </Menu>
              <NuxtLink to="/resources"
                class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                <XMarkIcon class="-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                Cancel
              </NuxtLink>
              <button type="button"
                class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                <ArrowUpTrayIcon class="-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                Save
              </button>
            </div>
          </div>
        </div>

        <!-- Main 3 column grid -->
        <div class="grid grid-cols-1 items-start gap-2 2xl:grid-cols-7">
          <!-- Left column -->
          <div class="grid grid-cols-1 gap-1 2xl:col-span-3">
            <section aria-labelledby="section-1-title">
              <h2 class="sr-only" id="section-1-title">Section title</h2>
              <div class="overflow-hidden rounded-lg bg-white shadow">
                <div class="p-2">
                  <div class="grid grid-cols-1 items-start gap-2 md:grid-cols-4">
                    <!-- Left column -->
                    <div class="grid grid-cols-1 gap-1 text-xs bg-gray-50">
                      <ActionTemplateCard />
                    </div>
                    <!-- Right column -->
                    <div class="grid grid-cols-1 gap-1 md:col-span-3">
                      Work area
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
          <!-- Right column -->
          <div class="grid grid-cols-1 gap-1 2xl:col-span-4">
            <section aria-labelledby="section-2-title">
              <h2 class="sr-only" id="section-2-title">Section title</h2>
              <div class="w-full rounded-lg bg-white shadow">
                <TabGroup>
                  <TabList class="flex space-x-8 border-b border-gray-200 text-xs">
                    <!-- Use the `selected` state to conditionally style the selected tab. -->
                    <Tab v-for="tab in tabs" :key="`tab-${tab.name}`" as="template" v-slot="{ selected }">
                      <button
                        :class="[selected ? 'border-ochre-500 text-ochre-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700', 'group inline-flex items-center border-b-2 py-4 px-1 font-medium']">
                        <component :is="tab.icon"
                          :class="[selected ? 'text-ochre-500' : 'text-gray-400 group-hover:text-gray-500', '-ml-0.5 mr-2 h-5 w-5']"
                          aria-hidden="true" />
                        <span>{{ tab.name }}</span>
                      </button>
                    </Tab>
                  </TabList>
                  <TabPanels>
                    <TabPanel v-for="tab in tabs" :key="`tab-panel-${tab.name}`">
                      {{ tab }}
                    </TabPanel>

                  </TabPanels>
                </TabGroup>
              </div>
            </section>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Menu, MenuButton, MenuItems, MenuItem, TabGroup, TabList, Tab, TabPanels, TabPanel,
} from "@headlessui/vue"
import {
  ArrowPathIcon,
  ArrowUpTrayIcon,
  Bars3Icon,
  ExclamationCircleIcon,
  BarsArrowUpIcon, ChevronDownIcon, MagnifyingGlassIcon,
  Squares2X2Icon,
  TableCellsIcon,
  XMarkIcon
} from "@heroicons/vue/24/outline"
import { useSettingStore } from "@/stores"

definePageMeta({
  layout: "crosswork",
  middleware: ["authenticated"],
});

const appSettings = useSettingStore()
const tabs = [
  { name: "Data source", icon: TableCellsIcon },
  { name: "Schema subject", icon: Squares2X2Icon },
  { name: "Schema object", icon: Squares2X2Icon },
]

const sidebarOpen = ref(false)



onMounted(async () => {
  appSettings.setPageName("Schedule")
})

// METADATA - START
// https://nuxt.com/docs/getting-started/seo-meta
const title = ref("whyqd.com — more research, less wrangling")
const description = ref("Perform schema-to-schema transforms for interoperability and data reuse. Transform messy data into structured schemas using readable, auditable methods.")
useHead({
  title,
  meta: [{
    name: "description",
    content: description
  }]
})
useServerSeoMeta({
  title,
  ogTitle: title,
  description: description,
  ogDescription: description,
  ogImage: "https://whyqd.com/img/ugly-data.png"
})
// METADATA - END
</script>
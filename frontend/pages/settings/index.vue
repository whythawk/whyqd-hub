<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <TabGroup>
      <TabList class="flex space-x-8 border-b border-gray-200 text-xs">
        <Tab v-for="tab in navigation" :key="`tab-${tab.id}`" as="template" v-slot="{ selected }">
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
        <TabPanel>
          <SettingsProfile />
        </TabPanel>
        <TabPanel>
          <SettingsSecurity />
        </TabPanel>
        <TabPanel>
          <SettingsOgunTokens />
        </TabPanel>
        <TabPanel>
          <ModerationUserTable />
        </TabPanel>
      </TabPanels>
    </TabGroup>
    <!-- <div class="lg:grid lg:grid-cols-12 lg:gap-x-5">
        <aside class="py-6 px-2 sm:px-6 lg:col-span-3 lg:py-0 lg:px-0">
          <nav class="space-y-1" aria-label="tabs">
            <button v-for="item in navigation" :key="`settings-${item.id}`"
              :class="[item.id === selected
                ? 'text-ochre-700 hover:text-ochre-700'
                : 'text-gray-900 hover:text-gray-900', 'group rounded-md px-3 py-2 flex items-center text-sm font-medium']" @click.prevent="changeSelection(item.id)">
              <component :is="item.icon" :class="[item.id === selected
                ? 'text-ochre-700 group-hover:text-ochre-700'
                : 'text-gray-400 group-hover:text-gray-500', 'flex-shrink-0 -ml-1 mr-3 h-6 w-6']" aria-hidden="true" />
              <span class="truncate">{{ item.name }}</span>
            </button>
            <button v-if="auth.is_superuser"
              class="text-gray-900 hover:text-gray-900 group rounded-md px-3 py-2 flex items-center text-sm font-medium cursor-pointer"
              @click.prevent="navigateTo('/moderation')">
              <component :is="UsersIcon" class="text-gray-400 group-hover:text-gray-500 flex-shrink-0 -ml-1 mr-3 h-6 w-6"
                aria-hidden="true" />
              <span class="truncate">Moderation</span>
            </button>
          </nav>
        </aside>
        <div class="space-y-6 ml-3 sm:px-6 lg:col-span-9 min-w-full lg:px-0">
          <div v-if="selected === 'ACCOUNT'">
            <SettingsProfile />
          </div>
          <div v-if="selected === 'SECURITY'">
            <SettingsSecurity />
          </div>
        </div>
      </div> -->
  </div>
</template>

<script setup lang="ts">
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue"
import { CommandLineIcon, KeyIcon, UserCircleIcon, UsersIcon } from "@heroicons/vue/24/outline"
import { useSettingStore, useAuthStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const auth = useAuthStore()
const appSettings = useSettingStore()

let navigation = [
  { name: "Account", id: "ACCOUNT", icon: UserCircleIcon },
  { name: "Security", id: "SECURITY", icon: KeyIcon },
  { name: "API Keys", id: "APIKEYS", icon: CommandLineIcon },
]

onMounted(() => {
  appSettings.setPageName("Settings")
  if (auth.is_superuser) navigation.push({
    name: "Moderation",
    id: "MODERATION",
    icon: UsersIcon
  })
})

// METADATA - START
// https://nuxt.com/docs/getting-started/seo-meta
const title = ref("Settings")
const description = ref("Update your personal settings, or delete your account.")
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
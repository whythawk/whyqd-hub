<template>
  <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
    <div v-if="readyState === 'loading'">
      <LoadingCardSkeleton />
    </div>
    <div v-else>
      <TabGroup>
        <TabList class="flex space-x-8 border-b border-gray-200 text-xs">
          <Tab v-for="tab in navigation" :key="`tab-${tab.id}`" as="template" v-slot="{ selected }">
            <button
              :class="[selected ? 'border-ochre-500 text-ochre-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700', 'group inline-flex items-center border-b-2 py-4 px-1 font-medium']">
              <component :is="tab.icon"
                :class="[selected ? 'text-ochre-500' : 'text-gray-400 group-hover:text-gray-500', '-ml-0.5 mr-2 h-5 w-5']"
                aria-hidden="true" />
              <span class="hidden lg:block">{{ tab.name }}</span>
            </button>
          </Tab>
        </TabList>
        <TabPanels>
          <TabPanel v-if="!auth.isAdmin">
            <SubscriptionsHistoryCard />
          </TabPanel>
          <TabPanel>
            <SettingsInvitationsCard />
          </TabPanel>
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
          <TabPanel>
            <SubscriptionsTable v-if="!manageSubscriber" @set-request="watchSubscriberRequest" />
            <SubscriptionsCreateView v-else @set-request="watchSubscriberRequest" />
          </TabPanel>
          <TabPanel>
            <SubscriptionsCurateProductsCard />
          </TabPanel>
        </TabPanels>
      </TabGroup>
    </div>
  </div>
</template>

<script setup lang="ts">
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue"
import { CommandLineIcon, CreditCardIcon, EnvelopeIcon, KeyIcon, UserCircleIcon, UsersIcon, UserGroupIcon } from "@heroicons/vue/24/outline"
import { useSettingStore, useAuthStore, useToastStore } from "@/stores"

definePageMeta({
  middleware: ["authenticated"],
});

const route = useRoute()
const auth = useAuthStore()
const toastStore = useToastStore()
const appSettings = useSettingStore()
const readyState = ref("loading")
const manageSubscriber = ref(false)

let navigation = [
  { name: "Invitations", id: "INVITATIONS", icon: EnvelopeIcon },
  { name: "Account", id: "ACCOUNT", icon: UserCircleIcon },
  { name: "Security", id: "SECURITY", icon: KeyIcon },
  { name: "API Keys", id: "APIKEYS", icon: CommandLineIcon },
]

onMounted(() => {
  appSettings.setPageName("Settings")
  if (
    route.query &&
    Object.keys(route.query).length !== 0 &&
    route.query.constructor === Object &&
    route.query.session_id
  ) {
    toastStore.addNotice({
      title: "A Whyqd Welcome",
      content: "Thank you for your subscription and welcome to Whyqd.",
    })
  }
  if (auth.is_superuser) {
    navigation.push({
      name: "Moderation",
      id: "MODERATION",
      icon: UsersIcon
    })
    navigation.push({
      name: "Subscribers",
      id: "SUBSCRIBERS",
      icon: UserGroupIcon
    })
    navigation.push({
      name: "Products",
      id: "PRODUCTS",
      icon: CreditCardIcon
    })
  } else {
    navigation.unshift({
      name: "Subscription",
      id: "SUBSCRIPTION",
      icon: CreditCardIcon
    })
  }
  readyState.value = "done"
})


function watchSubscriberRequest(request: boolean) {
  manageSubscriber.value = request
}

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
  ogImage: "https://whyqd.com/img/crosswalk.jpg"
})
// METADATA - END
</script>
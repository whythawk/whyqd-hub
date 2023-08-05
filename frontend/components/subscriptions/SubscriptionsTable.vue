<template>
  <div v-if="appSettings.current.pageState === 'loading'">
    <LoadingCardSkeleton />
  </div>
  <div v-if="appSettings.current.pageState === 'done' && subscriptionStore.multi.length">
    <div class="flex-auto p-3">
      <div class="shadow sm:overflow-hidden sm:rounded-md min-w-max">
        <SubscriptionsUserSearch @set-request="watchSubscriberRequest" />
        <table class="min-w-full divide-y divide-gray-300">
          <thead class="bg-gray-50">
            <tr>
              <th v-for="(th, i) in defaultHeaders" :key="`header-${i}`"
                class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                {{ printableHeaders[th] }}
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 bg-white">
            <tr v-for="(tr, j) in subscriptionStore.multi" :key="`row-${j}`">
              <td v-for="(td, k) in defaultHeaders" :key="`row-${j}-column-${k}`"
                class="w-full max-w-0 py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:w-auto sm:max-w-none sm:pl-6">
                <span v-if="['created', 'ends'].includes(td)">{{
                  readableDate(tr[td as keyof ISubscriptionView] as string)
                }}</span>
                <span v-if="[
                      'subscription_event_type',
                      'subscription_type',
                      'override',
                    ].includes(td)
                    ">{{ tr[td as keyof ISubscriptionView] }}</span>
                <span v-if="['subscriber'].includes(td)"><button class="btn btn-outline btn-xs"
                    @click.prevent="submit(tr[td as keyof ISubscriptionView] as string)">
                    {{ tr[td as keyof ISubscriptionView] }}
                  </button></span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <CommonPagination />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSubscriptionsStore, useSettingStore } from "@/stores"
import { readableDate } from "@/utilities"
import { IKeyable, ISubscriptionView } from "@/interfaces"

const route = useRoute()
const appSettings = useSettingStore()
const subscriptionStore = useSubscriptionsStore()
const defaultHeaders: string[] = [
  "created",
  "subscription_event_type",
  "subscription_type",
  "ends",
  "override",
  "subscriber",
]
const printableHeaders: IKeyable = {
  created: "Created",
  subscription_event_type: "Status",
  subscription_type: "Subscription",
  ends: "Ends",
  override: "Override",
  subscriber: "Subscriber",
}
const emit = defineEmits<{ setRequest: [request: boolean] }>()

watch(() => [route.query], async () => {
  await updateMulti()
})

async function updateMulti() {
  if (route.query && route.query.page) subscriptionStore.setPage(route.query.page as string)
  await subscriptionStore.getMulti()
}

onMounted(async () => {
  updateMulti()
})

function watchSubscriberRequest(request: boolean) {
  emit("setRequest", request)
}

async function submit(email: string) {
  await subscriptionStore.getSubscriber(email)
  if (subscriptionStore.subscriberProfile && Object.keys(subscriptionStore.subscriberProfile).length)
    emit("setRequest", true)
}

onBeforeUnmount(() => {
  const router = useRouter()
  router.replace({ query: {} })
})
</script>

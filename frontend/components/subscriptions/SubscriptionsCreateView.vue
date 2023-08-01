<template>
  <div class="flex-auto p-3">
    <div class="shadow rounded-md">
      <div class="space-y-6 bg-white py-6 px-4 sm:p-6">
        <h3 class="text-lg font-medium leading-6 text-gray-900">Create a subscription</h3>
        <div class="mx-10 text-sm grid grid-cols-2 gap-x-6 mb-5">
          <fieldset>
            <legend class="block text-gray-400 mb-2">Email</legend>
            <div class="flex">
              <p class="text-gray-900 items-center">
                {{ subscription.subscriber }}
              </p>
            </div>
          </fieldset>
          <fieldset>
            <legend class="block text-gray-400 mb-2">
              Admin override
            </legend>
            <div class="flex">
              <div v-for="(state, i) in overrideOptions" :key="`state-${i}`" class="flex mx-2 items-center">
                <input :id="`state-${i}`" v-model="subscription.override" :value="state" type="radio"
                  class="h-4 w-4 border-gray-300 text-ochre-600 focus:ring-ochre-600" />
                <label :for="`state-${i}`" class="ml-3 min-w-0 flex-1 text-gray-600">
                  {{ getTextOverrideState(state) }}
                </label>
              </div>
            </div>
          </fieldset>
        </div>
        <div class="mx-10 text-sm grid grid-cols-2 gap-x-6">
          <fieldset>
            <legend class="block text-gray-400 mb-2">
              Subscription ends
            </legend>
            <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateTo" />
          </fieldset>
          <fieldset>
            <legend class="block text-gray-400 mb-2">
              Subscription type
            </legend>
            <div class="flex">
              <div v-for="(sub, i) in subscriptionOptions" :key="`substate-${i}`" class="flex mx-2 items-center">
                <input :id="`substate-${i}`" v-model="subscription.subscription_type" :value="sub" type="radio"
                  class="h-4 w-4 border-gray-300 text-ochre-600 focus:ring-ochre-600" />
                <label :for="`substate-${i}`" class="ml-3 min-w-0 flex-1 text-gray-600">
                  {{ sub }}
                </label>
              </div>
            </div>
          </fieldset>
        </div>
        <div class="flex justify-end items-center space-x-2 m-4">
          <button type="button" @click.prevent="cancel"
            class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
            Cancel
          </button>
          <button type="submit" @click.prevent="submit"
            class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
            Submit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import VueTailwindDatepicker from "vue-tailwind-datepicker"
import { ISubscriptionAdminCreate, IProductTypes } from "@/interfaces"
import { useSubscriptionsStore } from "@/stores"

const subscriptionStore = useSubscriptionsStore()
const dateTo = ref("")
const formatter = ref({
  date: "YYYY-MM-DD",
  month: "MMM"
})
const emit = defineEmits<{ setRequest: [request: boolean] }>()

const subscription = ref<ISubscriptionAdminCreate>({} as ISubscriptionAdminCreate)
const subscriptionOptions: IProductTypes[] = ["EXPLORER", "RESEARCHER"]
const overrideOptions: boolean[] = [true, false]

function getTextOverrideState(state: boolean): string {
  if (state) return "True"
  else return "False"
}

function cancel() {
  emit("setRequest", false)
}

async function submit() {
  subscription.value.ends = new Date(dateTo.value)
  await subscriptionStore.createSubscription(subscription.value)
  emit("setRequest", false)
}

onMounted(async () => {
  subscription.value = {
    subscription_type: "EXPLORER",
    ends: "",
    override: false,
    subscriber: subscriptionStore.subscriberProfile.email,
  }
})
</script>

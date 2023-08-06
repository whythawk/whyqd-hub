<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <!-- @vue-ignore -->
    <component :is="icons[summaryIcon]"
      class="relative mt-3 h-6 w-6 flex-none rounded-full bg-gray-50 ring-1 ring-offset-4 ring-ochre-200 text-gray-700"
      aria-hidden="true" />
    <div class="flex-auto rounded-lg py-2 px-3 ring-1 ring-inset ring-gray-200">
      <div class="flex w-full items-center justify-between">
        <img class="h-10 w-10 flex-shrink-0 rounded-lg" :src="summaryAvatar" alt="summary.name" />
        <div class="flex-1">
          <div class="flex justify-between gap-x-4">
            <div class="py-0.5 text-sm leading-5 text-gray-500 pl-3">
              <h2 v-if="summary.title" class="font-bold text-gray-900">{{
                summary.title }}</h2>
              <h2 v-else class="font-bold text-gray-900">{{ summary.name }}</h2>
              <p v-if="summary.state" class="mt-1 truncate text-sm text-gray-500">{{ splitWordify(summary.state) }}</p>
            </div>
            <div class="truncate py-0.5 text-xs text-gray-500 text-right">
              <div class="truncate py-0.5">
                <time :datetime="props.activity.created" class="flex-none py-0.5 text-xs text-gray-500">{{
                  readableDate(props.activity.created) }}</time>
                <BellIcon v-if="props.activity.alert" class="inline-flex h-5 w-5 text-sienna-500 pl-1" />
                <BoltIcon v-if="props.activity.custodiansOnly" class="inline-flex h-5 w-5 text-cerulean-500 pl-1" />
              </div>
              <div class="truncate py-0.5 text-xs text-gray-500">
                <span v-if="props.activity.researcher.full_name" class="truncate font-medium text-gray-900">{{
                  props.activity.researcher.full_name }}</span>
                <span v-else class="truncate font-medium text-gray-900">{{ props.activity.researcher.email }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <p class="text-sm leading-6 text-gray-500">{{ props.activity.message }}</p>
      <Disclosure as="section" aria-labelledby="detail-heading" v-slot="{ open }">
        <div class="flex items-center justify-between">
          <DisclosureButton class="group flex flex-row text-xs font-medium text-gray-400">
            Details
            <ChevronDownIcon :class="open ? 'rotate-180 transform' : ''"
              class="-mr-1 ml-1 h-4 w-4 flex-shrink-0 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
          </DisclosureButton>
          <ul role="list" class="flex flex-row justify-end text-xs">
            <h3 id="detail-heading" class="sr-only">Further details and links</h3>
            <li v-for="(term, i) in ['resource', 'task', 'project']" :key="`act-${term}-${i}`" class="relative">
              <NuxtLink
                v-if="props.activity.hasOwnProperty(term) && props.activity[term as keyof IActivity] && Object.keys(props.activity[term as keyof IActivity]).length !== 0"
                :to="`${term}s/${(props.activity[term as keyof IActivity] as IModelSummary).id}`"
                class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
                <!-- @vue-ignore -->
                <component :is="icons[term]" class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0"
                  aria-hidden="true" />
                <span class="hidden lg:block">{{ capitalizeFirst(term) }}</span>
              </NuxtLink>
            </li>
          </ul>
        </div>
        <DisclosurePanel class="border-t border-gray-200 py-1">
          <ul role="list" class="text-xs space-y-2">
            <li v-for="(term, i) in ['project', 'task', 'resource']" :key="`detail-${term}-${i}`">
              <div
                v-if="props.activity.hasOwnProperty(term) && props.activity[term as keyof IActivity] && Object.keys(props.activity[term as keyof IActivity]).length !== 0">
                <span class="font-bold">{{ capitalizeFirst(term) }}: </span>
                <span v-if="(props.activity[term as keyof IActivity] as IModelSummary).title">
                  {{ (props.activity[term as keyof IActivity] as IModelSummary).title }}</span>
                <span v-else>{{ (props.activity[term as keyof IActivity] as IModelSummary).name }}</span>
                <div v-if="(props.activity[term as keyof IActivity] as IModelSummary).description"
                  class="font-medium text-gray-500">
                  {{ (props.activity[term as keyof IActivity] as IModelSummary).description }}
                </div>
              </div>
            </li>
          </ul>
        </DisclosurePanel>
      </Disclosure>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
import { BeakerIcon, BellIcon, BoltIcon, ChevronDownIcon, RectangleGroupIcon, Square3Stack3DIcon, } from "@heroicons/vue/24/outline"
import { readableDate, capitalizeFirst, splitWordify, getAvatar } from "@/utilities"
import { IActivity, IModelSummary } from "@/interfaces"

const summary = shallowRef({} as IModelSummary)
const summaryAvatar = shallowRef("")
const summaryIcon = shallowRef("")
const icons = {
  "resource": RectangleGroupIcon,
  "task": Square3Stack3DIcon,
  "project": BeakerIcon
}

function getModelSummary(): IModelSummary {
  for (const k of ["resource", "task", "project"]) {
    if (props.activity.hasOwnProperty(k) && (props.activity[k as keyof IActivity]) && Object.keys(props.activity[k as keyof IActivity]).length !== 0) {
      summaryIcon.value = k
      return props.activity[k as keyof IActivity] as IModelSummary
    }
  }
  return {} as IModelSummary
}

const props = defineProps<{
  activity: IActivity,
  lastCard: Boolean
}>()

onMounted(async () => {
  summary.value = getModelSummary()
  summaryAvatar.value = await getAvatar(summary.value.id as string)
})
</script>
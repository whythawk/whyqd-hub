<template>
  <div class="max-w-3xl mx-auto">
    <ul role="list" class="mt-6 flex justify-between border-b border-t border-gray-200 py-6 md:px-12">
      <li v-for="(item, itemIdx) in items" :key="itemIdx">
        <NuxtLink :to="item.to"
          :class="[item.show ? '' : 'pointer-events-none', 'flex items-center space-x-2 rounded-lg hover:bg-gray-50 pr-1']">
          <div :class="[item.background, 'flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg']">
            <component :is="item.icon" class="h-6 w-6 text-white" aria-hidden="true" />
          </div>
          <h3 class="text-sm font-bold text-gray-900">
            {{ item.title }}
          </h3>
        </NuxtLink>
      </li>
    </ul>
    <div class="mt-6 md:px-12">
      <h1 class="text-lg font-bold leading-8 my-1">Welcome - let's get started ...</h1>
      <p class="text-sm my-2 mb-3">
        Whyqd (/wɪkɪd/) has a relatively simple workflow, and these quick-links will guide you.
      </p>
      <ul role="list" class="space-y-1">
        <li v-for="(start, startIdx) in launch" :key="startIdx"
          class="relative flex items-center space-x-2 py-1 border border-gray-200 bg-white hover:bg-gray-100 rounded-md">
          <div class="min-w-0 flex-auto">
            <div class="flex items-center gap-x-3 p-2">
              <div :class="[start.background, 'flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg']">
                <component :is="start.icon" class="h-5 w-5 text-white" aria-hidden="true" />
              </div>
              <h2 class="min-w-0 text-sm font-semibold leading-6 text-gray-900">
                <NuxtLink :to="start.to" :class="[start.show ? '' : 'pointer-events-none', 'flex gap-x-2']">
                  <span>{{ start.title }}</span>
                  <span class="absolute inset-0" />
                </NuxtLink>
              </h2>
            </div>
            <div class="ml-2 mb-2 flex items-center gap-x-2.5 text-sm leading-5 text-gray-700">
              <p>{{ start.description }}<span v-if="!start.show">&nbsp;You need to be a subscriber.</span></p>
            </div>
          </div>
          <ChevronRightIcon class="h-5 w-5 flex-none text-gray-900" aria-hidden="true" />
        </li>
      </ul>

    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ArrowUpTrayIcon,
  BeakerIcon,
  BellIcon,
  CalendarIcon,
  ChevronRightIcon,
  FolderPlusIcon,
  SquaresPlusIcon,
  Square3Stack3DIcon,
} from "@heroicons/vue/24/outline"
import { useAuthStore } from "@/stores"

const authStore = useAuthStore()
const items = [
  {
    title: "Import data",
    icon: ArrowUpTrayIcon,
    to: "/import",
    background: "bg-sienna-500",
    show: authStore.hasExplorerSubscription,
  },
  {
    title: "Create a schema",
    icon: SquaresPlusIcon,
    to: "/schema/edit",
    background: "bg-eucalyptus-500",
    show: true,
  },
  {
    title: "Create a task",
    icon: FolderPlusIcon,
    to: "/tasks/edit",
    background: "bg-cerulean-500",
    show: true,
  },
]
const launch = [
  {
    title: "Manage projects",
    description: "Organise tasks or teams. Specify a schema for all tasks to use, & define who gets to do what.",
    icon: BeakerIcon,
    to: "/projects",
    background: "bg-ochre-500",
    show: true,
  },
  {
    title: "See what's new",
    description: "Review the list of recent activities.",
    icon: BellIcon,
    to: "/activity",
    background: "bg-sienna-500",
    show: true,
  },
  {
    title: "Review your schedule",
    description: "See which tasks need to be started or reviewed.",
    icon: CalendarIcon,
    to: "/schedule",
    background: "bg-eucalyptus-500",
    show: true,
  },
  {
    title: "Manage tasks",
    description: "Organise repeating processes & manage resources created by tasks.",
    icon: Square3Stack3DIcon,
    to: "/tasks",
    background: "bg-cerulean-500",
    show: true,
  },
  {
    title: "Organise schemas",
    description: "Describe & structure tabular data. Link two schemas with a crosswalk transform.",
    icon: SquaresPlusIcon,
    to: "/references",
    background: "bg-ochre-500",
    show: true,
  },
  {
    title: "Import data",
    description: "Upload tabular data & automatically derive a source schema.",
    icon: ArrowUpTrayIcon,
    to: "/import",
    background: "bg-sienna-500",
    show: authStore.hasExplorerSubscription,
  },
]
</script>
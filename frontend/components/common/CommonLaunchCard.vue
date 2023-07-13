<template>
  <div>
    <ul role="list" class="mt-6 flex justify-between border-b border-t border-gray-200 py-6 md:px-12">
      <li v-for="(item, itemIdx) in items" :key="itemIdx">
        <NuxtLink :to="item.to" class="flex items-center space-x-2 rounded-lg hover:bg-gray-50 pr-1">
          <div :class="[item.background, 'flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg']">
            <component :is="item.icon" class="h-6 w-6 text-white" aria-hidden="true" />
          </div>
          <h3 class="text-sm font-bold text-gray-900">
            {{ item.title }}
          </h3>
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import {
  ArrowUpTrayIcon,
  FolderPlusIcon,
  SquaresPlusIcon,
} from "@heroicons/vue/24/outline"

const items = [
  {
    title: "Import data",
    icon: ArrowUpTrayIcon,
    to: "/import",
    background: "bg-sienna-500",
  },
  {
    title: "Create a schema",
    icon: SquaresPlusIcon,
    to: "/schema/edit",
    background: "bg-eucalyptus-500",
  },
  {
    title: "Create a task",
    icon: FolderPlusIcon,
    to: "/tasks/edit",
    background: "bg-cerulean-500",
  },
]
</script>
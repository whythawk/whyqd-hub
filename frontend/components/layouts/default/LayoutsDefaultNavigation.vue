<template>
  <header>
    <Disclosure as="nav" v-slot="{ open }">
      <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div class="relative flex h-16 justify-between">
          <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
            <!-- Mobile menu button -->
            <DisclosureButton
              class="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-ochre-500">
              <span class="sr-only">Open main menu</span>
              <Bars3Icon v-if="!open" class="block h-6 w-6" aria-hidden="true" />
              <XMarkIcon v-else class="block h-6 w-6" aria-hidden="true" />
            </DisclosureButton>
          </div>
          <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
            <NuxtLink to="/" class="flex flex-shrink-0 items-center">
              <img class="block h-8 w-auto lg:hidden" src="/img/mark.svg" alt="Whyqd.com" />
              <img class="hidden h-8 w-auto lg:block" src="/img/mark-large.svg" alt="Whyqd.com" />
            </NuxtLink>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <NuxtLink v-for="(nav, i) in navigation" :key="`nav-${i}`" :to="nav.to"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-ochre-500">
                {{ nav.name }}</NuxtLink>
            </div>
          </div>
          <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
            <AuthenticationNavigation />
          </div>
        </div>
      </div>

      <DisclosurePanel class="sm:hidden">
        <div class="space-y-1 pt-2 pb-4">
          <!-- Current: "bg-ochre-50 border-ochre-500 text-ochre-700", Default: "border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700" -->
          <NuxtLink v-for="(nav, i) in navigation" :key="`nav-mobile-${i}`" :to="nav.to"
            class="block hover:border-l-4 hover:border-ochre-500 hover:bg-ochre-50 py-2 pl-3 pr-4 text-base font-medium text-ochre-700">
            {{ nav.name }}
          </NuxtLink>
        </div>
      </DisclosurePanel>
    </Disclosure>
  </header>
</template>
  
<script setup lang="ts">
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import { Bars3Icon, XMarkIcon } from "@heroicons/vue/24/outline"

const navigation = [
  { name: "About", to: "/about" },
  { name: "Developers", to: "https://whyqd.readthedocs.io/" },
  { name: "Blog", to: "/blog" },
]
</script>
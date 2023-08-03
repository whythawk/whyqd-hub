<template>
  <div class="relative flex gap-x-4">
    <div :class="[props.lastCard ? 'h-6' : '-bottom-6', 'absolute left-0 top-0 flex w-6 justify-center']">
      <div class="w-px bg-gray-200" />
    </div>
    <!-- @vue-ignore -->
    <img :src="avatar" :alt="props.project.name"
      class="relative mt-3 h-6 w-6 flex-none rounded-full bg-gray-50 ring-1 ring-offset-4 ring-ochre-200 text-gray-700"
      aria-hidden="true" />
    <NuxtLink :to="`/projects/${props.project.id}`"
      class="flex-auto rounded-lg py-2 px-3 ring-1 ring-inset ring-gray-200">
      <div class="flex w-full items-center">
        <div class="flex-1">
          <div class="flex justify-between gap-x-4">
            <div class="py-0.5 text-sm leading-5 text-gray-500">
              <h2 v-if="props.project.title" class="font-bold text-gray-900">{{
                props.project.title }}</h2>
              <h2 v-else class="font-bold text-gray-900">{{ props.project.name }}</h2>
            </div>
            <ul role="list" class="flex flex-row justify-end text-xs leading-5">
              <li class="truncate py-0.5 text-xs text-gray-500 text-right">
                <time :datetime="props.project.modified" class="flex-none py-0.5 text-xs text-gray-500">{{
                  readableDate(props.project!.modified as string) }}</time>
              </li>
              <li v-if="props.project.auths && props.project.auths.length"
                class="relative group flex flex-row text-xs font-medium text-gray-500 gap-x-1 pl-2">
                <UserGroupIcon class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                {{ props.project.auths.length }}
                <span v-if="props.project.auths.length === 1">member</span>
                <span v-else>members</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <p v-if="props.project.description" class="text-sm leading-6 text-gray-500">{{ props.project.description }}</p>
      <div class="flex items-center justify-between">
        <div class="group flex flex-row text-xs font-medium text-gray-700">
          <TagIcon class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
          <span v-if="props.project.subjects && props.project.subjects.length" class="ml-1">
            {{ props.project.subjects.join(", ") }}
          </span>
          <span v-else class="ml-1">
            untagged
          </span>
        </div>
        <ul role="list" class="flex flex-row justify-end text-xs">
          <h3 id="detail-heading" class="sr-only">Project tasks and schema object</h3>
          <li class="relative">
            <NuxtLink :to="`/schedule/project/${props.project.id}`"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <CalendarIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Schedule</span>
            </NuxtLink>
          </li>
          <li class="relative">
            <NuxtLink :to="`/tasks/project/${props.project.id}`"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <Square3Stack3DIcon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Tasks</span>
            </NuxtLink>
          </li>
          <li v-if="props.project.schema" class="relative">
            <NuxtLink :to="`/schema/${props.project.schema.id}`"
              class="text-gray-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <Squares2X2Icon class="text-gray-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Schema</span>
            </NuxtLink>
          </li>
          <li v-else class="relative">
            <button type="button" @click.prevent="schemaRedirect"
              class="text-sienna-700 hover:text-ochre-600 group flex gap-x-1 p-2 font-semibold">
              <SquaresPlusIcon class="text-sienna-700 group-hover:text-ochre-600 h-4 w-4 shrink-0" aria-hidden="true" />
              <span class="hidden lg:block">Schema</span>
            </button>
          </li>
        </ul>
      </div>
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
import { CalendarIcon, Square3Stack3DIcon, Squares2X2Icon, SquaresPlusIcon, TagIcon, UserGroupIcon } from "@heroicons/vue/24/outline"
import { readableDate, getAvatar } from "@/utilities"
import { IProject, IReferenceFilters } from "@/interfaces"
import { useReferenceStore } from "@/stores"

const referenceStore = useReferenceStore()
const avatar = shallowRef("")

const props = defineProps<{
  project: IProject,
  lastCard: Boolean
}>()

async function schemaRedirect() {
  let filters: IReferenceFilters = { ...referenceStore.filters }
  filters.reference_type = "SCHEMA"
  referenceStore.resetFilters()
  referenceStore.setFilters(filters)
  await navigateTo(`/references/project/${props.project.id}`)
}

onMounted(async () => {
  avatar.value = await getAvatar(props.project.id as string)
})
</script>
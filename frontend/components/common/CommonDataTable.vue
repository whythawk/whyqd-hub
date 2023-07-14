<template>
  <div v-if="tableKeys && tableKeys.length"
    class="flow-root min-h-0 overflow-y-auto overflow-x-auto max-w-screen max-h-screen">
    <div class="inline-block">
      <table class="border-separate border-spacing-0">
        <thead>
          <tr>
            <th scope="col"
              class="sticky top-0 z-10 border-y border-gray-300 bg-opacity-75 px-3 py-3.5 text-left text-sm font-semibold text-gray-900 bg-gray-50 backdrop-blur backdrop-filter table-cell">
              Index
            </th>
            <th v-for="(th, i) in props.tableHeaders" :key="`header-${i}`" scope="col"
              class="sticky top-0 z-10 border-y border-gray-300 bg-white bg-opacity-75 px-3 py-3.5 text-left text-sm font-semibold text-gray-900 backdrop-blur backdrop-filter table-cell">
              {{ th }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(tr, j) in tableRows" :key="`row-${j}`">
            <td class="whitespace-nowrap h-8 py-2 text-sm text-gray-500 table-cell border border-gray-100 bg-gray-50">
              {{ j }}
            </td>
            <td v-for="(td, k) in tableKeys" :key="`row-${j}-column-${k}`"
              class="whitespace-nowrap h-8 py-2 text-sm text-gray-500 table-cell border border-gray-100">
              {{ tr[td] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { IKeyable } from "@/interfaces"

const props = defineProps<{
  tableHeaders: String[]
  tableRows: IKeyable[]
}>()
const tableKeys = ref<string[]>([])

function setTableKeys() {
  if (props.tableRows.length) tableKeys.value = Object.keys(props.tableRows[0])
}

onMounted(async () => {
  setTableKeys()
})

</script>

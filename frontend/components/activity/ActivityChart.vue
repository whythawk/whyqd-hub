<template>
    <div class="mt-2">
      <figure class="mx-auto flex items-center justify-center">
        <svg id="chart" ref="chart"></svg>
      </figure>
    </div>
</template>

<script setup lang="ts">
import type { IActivityReportFilters } from "@/interfaces"
import { useTokenStore } from "@/stores"
import { apiActivity } from "@/api"

const route = useRoute()
const filters = ref({} as IActivityReportFilters)
const barChart = useBarLineChart()
const chart = ref({} as HTMLElement)
const tokenStore = useTokenStore()

async function getReportData() {
  await tokenStore.refreshTokens()
  if (tokenStore.token) {
    try {
      const { data: response } = await apiActivity.getReport(tokenStore.token, filters.value)
      if (
        response.value
        && Object.keys(response.value).length
        && response.value.data
        && Array.isArray(response.value.data)
        && response.value.data.length
      ) {
        barChart.getBarLineChart(response.value.data)
      }
    } catch (error) {
      console.log(error)
    }
  }
}

onMounted(async () => {
  if (route.path.includes("/tasks/")) filters.value.task_id = route.params.id as string
  if (route.path.includes("/projects/")) filters.value.project_id = route.params.id as string
  filters.value.frequency = "QUARTER"
  filters.value.state = "COMPLETE"
  await getReportData()
})
</script>
import type { IResourceActivitySummary, IActivityFilters, IActivityReportFilters, IActivityReport } from "@/interfaces"
import { apiCore } from "./core"

export const apiActivity = {
  // ACTIVITIES
  async getMulti(token: string, payload: IActivityFilters = {}) {
    return await useFetch<IResourceActivitySummary[]>(`${apiCore.url()}/activity/`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getMultiByTask(token: string, task_key: string, payload: IActivityFilters = {}) {
    return await useFetch<IResourceActivitySummary[]>(`${apiCore.url()}/activity/task/${task_key}`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getMultiByProject(token: string, project_key: string, payload: IActivityFilters = {}) {
    return await useFetch<IResourceActivitySummary[]>(`${apiCore.url()}/activity/project/${project_key}`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getReport(token: string, payload: IActivityReportFilters = {}) {
    return await useFetch<IActivityReport>(`${apiCore.url()}/activity/report`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
}
import { IActivity, IActivityFilters } from "@/interfaces"
import { apiCore } from "./core"

export const apiActivity = {
  // ACTIVITIES
  async getMulti(token: string, payload: IActivityFilters = {}) {
    return await useFetch<IActivity[]>(`${apiCore.url()}/activity/`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
}
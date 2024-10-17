import type { IOgunCreate, IOgunUser, IOgunFilters, IMsg, IResearcherRoleType } from "@/interfaces"
import { apiCore } from "./core"

export const apiOgun = {
  async getMulti(token: string, payload: IOgunFilters = {}) {
    return await useFetch<IOgunUser[]>(`${apiCore.url()}/ogun/`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async createTerm(token: string, role: IResearcherRoleType) {
    return await useFetch<IOgunCreate>(`${apiCore.url()}/ogun/create/${role}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<IMsg>(`${apiCore.url()}/ogun/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
}
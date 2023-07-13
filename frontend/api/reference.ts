import { IReference, IReferenceFilters } from "@/interfaces"
import { apiCore } from "./core"

export const apiReference = {
  // REFERENCES
  async getMulti(token: string, payload: IReferenceFilters = {}) {
    return await useFetch<IReference[]>(`${apiCore.url()}/reference`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getTerm(token: string, key: string) {
    return await useFetch<IReference>(`${apiCore.url()}/reference/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<IReference>(`${apiCore.url()}/reference/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
}
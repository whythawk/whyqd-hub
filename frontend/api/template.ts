import type {
  IReferenceTemplate,
  IDataSourceTemplate,
  ICrosswalkTemplate,
  IReferenceFilters,
  IReferenceType,
} from "@/interfaces"
import { apiCore } from "./core"

export const apiTemplate = {
  // REFERENCES
  async getMulti(token: string, payload: IReferenceFilters = {}) {
    return await useFetch<IReferenceTemplate[]>(`${apiCore.url()}/template`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getCrosswalk(token: string, key: string) {
    return await useFetch<ICrosswalkTemplate>(`${apiCore.url()}/template/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async getDataSource(token: string, key: string) {
    return await useFetch<IDataSourceTemplate>(`${apiCore.url()}/template/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async createTerm(token: string, template_type: IReferenceType, payload: IDataSourceTemplate | ICrosswalkTemplate) {
    return await useFetch<IReferenceTemplate>(`${apiCore.url()}/template/${template_type}`, 
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async updateTerm(token: string, key: string, payload: IDataSourceTemplate | ICrosswalkTemplate) {
    return await useFetch<IReferenceTemplate>(`${apiCore.url()}/template/${key}`, 
      {
        method: "PUT",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<IReferenceTemplate>(`${apiCore.url()}/template/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
}
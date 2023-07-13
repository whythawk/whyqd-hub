import { IProject, IProjectFilters } from "@/interfaces"
import { apiCore } from "./core"

export const apiProject = {
  // REFERENCES
  async getMulti(token: string, payload: IProjectFilters = {}) {
    return await useFetch<IProject[]>(`${apiCore.url()}/project`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getTerm(token: string, key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async createTerm(token: string, payload: IProject) {
    return await useFetch<IProject>(`${apiCore.url()}/project`, 
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async updateTerm(token: string, key: string, payload: IProject) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}`, 
      {
        method: "PUT",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async addTask(token: string, key: string, task_key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}/task/${task_key}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTask(token: string, key: string, task_key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}/task/${task_key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async addSchema(token: string, key: string, schema_key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}/schema/${schema_key}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  async removeSchema(token: string, key: string, schema_key: string) {
    return await useFetch<IProject>(`${apiCore.url()}/project/${key}/schema/${schema_key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
}
import { ITask, IScheduledTask, ITaskFilters } from "@/interfaces"
import { apiCore } from "./core"

export const apiTask = {
  // REFERENCES
  async getMulti(token: string, payload: ITaskFilters = {}) {
    return await useFetch<ITask[]>(`${apiCore.url()}/task`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getMultiByProject(token: string, project_key: string, payload: ITaskFilters = {}) {
    return await useFetch<ITask[]>(`${apiCore.url()}/task/project/${project_key}`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getScheduledMulti(token: string, payload: ITaskFilters = {}) {
    return await useFetch<IScheduledTask[]>(`${apiCore.url()}/task/scheduled`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getScheduledMultiByProject(token: string, project_key: string, payload: ITaskFilters = {}) {
    return await useFetch<IScheduledTask[]>(`${apiCore.url()}/task/scheduled/project/${project_key}`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getTerm(token: string, key: string) {
    return await useFetch<ITask>(`${apiCore.url()}/task/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async createTerm(token: string, payload: ITask) {
    return await useFetch<ITask>(`${apiCore.url()}/task`, 
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async updateTerm(token: string, key: string, payload: ITask) {
    return await useFetch<ITask>(`${apiCore.url()}/task/${key}`, 
      {
        method: "PUT",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<ITask>(`${apiCore.url()}/task/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async addTemplate(token: string, key: string, template_key: string) {
    return await useFetch<ITask>(`${apiCore.url()}/task/${key}/template/${template_key}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTemplate(token: string, key: string, template_key: string) {
    return await useFetch<ITask>(`${apiCore.url()}/task/${key}/template/${template_key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async addToProject(token: string, key: string, project_key: string) {
    return await useFetch<ITask>(`${apiCore.url()}/task/${key}/project/${project_key}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  async removeFromProject(token: string, key: string, project_key: string) {
    return await useFetch<ITask>(`${apiCore.url()}/task/${key}/project/${project_key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
}
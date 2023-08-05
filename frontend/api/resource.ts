import { IResource, IResourceManager, IResourceFilters, IDataSourceTemplate, IMsg } from "@/interfaces"
import { apiCore } from "./core"

export const apiResource = {
  async getMulti(token: string, payload: IResourceFilters = {}) {
    return await useFetch<IResource[]>(`${apiCore.url()}/resource`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getMultiByTask(token: string, task_key: string, payload: IResourceFilters = {}) {
    return await useFetch<IResource[]>(`${apiCore.url()}/resource/task/${task_key}`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getTerm(token: string, key: string) {
    return await useFetch<IResourceManager>(`${apiCore.url()}/resource/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async getTermTemplate(token: string, key: string) {
    return await useFetch<IDataSourceTemplate>(`${apiCore.url()}/resource/template/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<IResource>(`${apiCore.url()}/resource/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTermTransform(token: string, key: string) {
    return await useFetch<IResourceManager>(`${apiCore.url()}/resource/transform/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTermCrosswalk(token: string, key: string) {
    return await useFetch<IResourceManager>(`${apiCore.url()}/resource/crosswalk/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async addTermSchemaObject(token: string, key: string, schema_key: string) {
    return await useFetch<IResourceManager>(`${apiCore.url()}/resource/${key}/schema/${schema_key}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTermSchemaObject(token: string, key: string) {
    return await useFetch<IResourceManager>(`${apiCore.url()}/resource/schema/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async postSchemaCategorisation(token: string, key: string, field_name: string, term_type: string) {
    return await useFetch<IMsg>(`${apiCore.url()}/resource/${key}/categorise/${field_name}/${term_type}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  async postProcessTransform(token: string, key: string, mimetype: string) {
    return await useFetch<IMsg>(`${apiCore.url()}/resource/${key}/transform/${mimetype}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
}
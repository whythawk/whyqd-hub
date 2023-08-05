import WebSocketAsPromised from "websocket-as-promised"
import { ISchema, IResourceManager } from "@/interfaces"
import { apiCore } from "./core"

export const apiSchema = {
  async getTerm(token: string, key: string) {
    return await useFetch<ISchema>(`${apiCore.url()}/schema/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async createSchemaCrosswalk(token: string, subject_key: string, object_key: string) {
    return await useFetch<IResourceManager>(`${apiCore.url()}/schema/subject/${subject_key}/object/${object_key}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  async createTaskSchemaCrosswalk(token: string, task_key: string, subject_key: string) {
    return await useFetch<IResourceManager>(`${apiCore.url()}/schema/task/${task_key}/schema/${subject_key}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  // SCHEMA WEBSOCKETS
  socketEdit() {
    return new WebSocketAsPromised(`${apiCore.wsurl()}/schema/edit`, {
      packMessage: (data) => JSON.stringify(data),
      unpackMessage: (data) => JSON.parse(data as string),
    })
  },
}
import type { IMsg, IKeyable } from "@/interfaces"
import { apiCore } from "./core"

export const apiData = {
  async postUpload(token: string, payload: FormData) {
    return await useFetch<IMsg>(`${apiCore.url()}/data/upload`, 
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async postUploadForTask(token: string, key: string, payload: FormData) {
    return await useFetch<IMsg>(`${apiCore.url()}/data/upload/task/${key}`, 
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async getModelDownload(token: string, key: string) {
    return await useFetch<IKeyable>(`${apiCore.url()}/data/download/model/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async getSourceDownload(token: string, key: string) {
    return await useFetch(`${apiCore.url()}/data/download/source/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
}
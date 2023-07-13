import WebSocketAsPromised from "websocket-as-promised"
import { IResourceCrosswalkManager } from "@/interfaces"
import { apiCore } from "./core"

export const apiCrosswalk = {
  async getTerm(token: string, key: string) {
    return await useFetch<IResourceCrosswalkManager>(`${apiCore.url()}/crosswalk/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  // WEBSOCKETS
  socketEdit(key: string) {
    return new WebSocketAsPromised(`${apiCore.wsurl()}/crosswalk/edit/${key}`, {
      packMessage: (data) => JSON.stringify(data),
      unpackMessage: (data) => JSON.parse(data as string),
    })
  },
  socketTemplate(key: string) {
    return new WebSocketAsPromised(`${apiCore.wsurl()}/crosswalk/template/${key}`, {
      packMessage: (data) => JSON.stringify(data),
      unpackMessage: (data) => JSON.parse(data as string),
    })
  },
}
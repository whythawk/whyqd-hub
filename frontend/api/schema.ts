import WebSocketAsPromised from "websocket-as-promised"
import { ISchema } from "@/interfaces"
import { apiCore } from "./core"

export const apiSchema = {
  async getTerm(token: string, key: string) {
    return await useFetch<ISchema>(`${apiCore.url()}/schema/${key}`, 
      {
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
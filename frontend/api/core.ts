export const apiCore = {
  url(): string {
    return useRuntimeConfig().public.apiUrl
  },
  wsurl(): string {
    return useRuntimeConfig().public.apiWS
  },
  headers(token: string) {
    return {
        "Cache-Control": "no-cache",
        Authorization: `Bearer ${token}`
    }
  }
}
import { IOgunUser, IOgunFilters  } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useToastStore } from "./toasts"
import { useSettingStore } from "./settings"
import { apiOgun } from "@/api"

export const useOgunStore = defineStore("ogunStore", {
  state: () => ({
    board: [] as IOgunUser[],
    facets: {} as IOgunFilters,
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    multi: (state) => state.board,
    filters: (state) => state.facets,
    authTokens: () => {
      return ( useTokenStore() )
    },
    settings: () => {
      return ( useSettingStore() )
    },
  },
  actions: {
    async getMulti(facets: IOgunFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiOgun.getMulti(this.authTokens.token, facets)
          if (response.value) {
            if (response.value.length) {
              this.setMulti(response.value)
              this.settings.setPageNext(true)
            } else {
              this.settings.setPageNext(false)
            }
          }
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.board = []
        }
      }
    },
    setMulti(payload: IOgunUser[]) {
      this.board = payload
    },
    async removeTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiOgun.removeTerm(this.authTokens.token, key)
          if (response.value) {
            await this.getMulti()
            const toasts = useToastStore()
            toasts.addNotice({
              title: "Success",
              content: "Your API key was successfully removed.",
            })
          }
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Deletion error",
            content: "Could not remove API key. Please check your details, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    setFilters(payload: IOgunFilters) {
      this.facets = payload
    },
    setPage(payload: string) {
      if (!isNaN(+payload)) {
        this.facets.page = +payload 
      }
    },
    resetFilters() {
      const page = this.facets.page
      this.facets = {}
      this.setPage("" + page)
    },
    // reset state using `$reset`
    resetState () {
      this.$reset()
    }
  }
})
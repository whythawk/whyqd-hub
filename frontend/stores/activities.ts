import { IActivity, IActivityFilters } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { apiActivity } from "@/api"

export const useActivityStore = defineStore("activityStore", {
  state: () => ({
    board: [] as IActivity[],
    facets: {} as IActivityFilters,
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    first: (state) => state.board.length > 0 && state.board[0],
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
    async getMulti() {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setMulti([])
          const { data: response } = await apiActivity.getMulti(this.authTokens.token, this.facets)
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
          this.resetState()
        }
      }
    },
    setMulti(payload: IActivity[]) {
      this.board = payload
    },
    setFilters(payload: IActivityFilters) {
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
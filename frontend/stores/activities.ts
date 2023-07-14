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
          const { data: response } = await apiActivity.getMulti(this.authTokens.token, this.facets)
          if (response.value) this.setMulti(response.value)
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
    resetFilters() {
      this.facets = {}
    },
    // reset state using `$reset`
    resetState () {
      this.$reset()
    }
  }
})
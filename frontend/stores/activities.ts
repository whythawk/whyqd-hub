import { IResourceActivitySummary, IActivityFilters } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { apiActivity } from "@/api"

export const useActivityStore = defineStore("activityStore", {
  state: () => ({
    board: [] as IResourceActivitySummary[],
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
    async getMultiByTask(task_key: string, facets: IActivityFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiActivity.getMultiByTask(this.authTokens.token, task_key, facets)
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
    async getMultiByProject(project_key: string, facets: IActivityFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiActivity.getMultiByProject(this.authTokens.token, project_key, facets)
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
    setMulti(payload: IResourceActivitySummary[]) {
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
      this.facets = {}
    },
    // reset state using `$reset`
    resetState () {
      this.$reset()
    }
  }
})
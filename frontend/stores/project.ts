import {
  IProject, IProjectFilters
} from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { apiProject } from "@/api"

export const useProjectStore = defineStore("projectStore", {
  state: () => ({
    board: [] as IProject[],
    one: {} as IProject,
    edit: {} as IProject,
    facets: {} as IProjectFilters,
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    multi: (state) => state.board,
    term: (state) => state.one,
    draft: (state) => state.edit,
    filters: (state) => state.facets,
    authTokens: () => {
      return ( useTokenStore() )
    },
    settings: () => {
      return ( useSettingStore() )
    },
  },
  actions: {
    async getMulti(facets: IProjectFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiProject.getMulti(this.authTokens.token, facets)
          if (response.value) this.setMulti(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.board = []
        }
      }
    },
    setMulti(payload: IProject[]) {
      this.board = payload
    },
    async getTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        this.setTerm({} as IProject)
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiProject.getTerm(this.authTokens.token, key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
        }
      }
    },
    async createTerm(payload: IProject = {} as IProject) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          if (payload && Object.keys(payload).length !== 0) this.setDraft(payload)
          const { data: response } = await apiProject.createTerm(this.authTokens.token, this.draft)
          if (response.value) {
            this.setTerm(response.value)
            this.resetDraft()
          } 
        } catch (error) {
          this.one = {} as IProject
        }
      }
    },
    async updateTerm(key: string, payload: IProject = {} as IProject) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          if (payload && Object.keys(payload).length !== 0) this.setDraft(payload)
          const { data: response } = await apiProject.updateTerm(this.authTokens.token, key, this.draft)
          if (response.value) {
            this.setTerm(response.value)
            this.resetDraft()
          } 
        } catch (error) {
          this.one = {} as IProject
        }
      }
    },
    setDraft(payload: IProject) {
      this.edit = payload
    },
    resetDraft() {
      this.edit = {} as IProject
    },
    setTerm(payload: IProject) {
      this.one = payload
    },
    async removeTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiProject.removeTerm(this.authTokens.token, key)
          if (response.value) this.setTerm({} as IProject)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Deletion error",
            content: "Could not remove project. Please check your details, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    async addTask(key: string, task_key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiProject.addTask(this.authTokens.token, key, task_key)
          if (response.value) this.setTerm(response.value)
        } catch (error) {
          this.one = {} as IProject
        }
      }
    },
    async removeTask(key: string, task_key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiProject.removeTask(this.authTokens.token, key, task_key)
          if (response.value) this.setTerm(response.value)
        } catch (error) {
          this.one = {} as IProject
        }
      }
    },
    async addSchema(key: string, schema_key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiProject.addSchema(this.authTokens.token, key, schema_key)
          if (response.value) this.setTerm(response.value)
        } catch (error) {
          this.one = {} as IProject
        }
      }
    },
    async removeSchema(key: string, schema_key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiProject.removeSchema(this.authTokens.token, key, schema_key)
          if (response.value) this.setTerm(response.value)
        } catch (error) {
          this.one = {} as IProject
        }
      }
    },
    setFilters(payload: IProjectFilters) {
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
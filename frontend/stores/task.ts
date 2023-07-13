import {
  ITask, ITaskFilters
} from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { apiTask } from "@/api"

export const useTaskStore = defineStore("taskStore", {
  state: () => ({
    board: [] as ITask[],
    one: {} as ITask,
    edit: {} as ITask,
    facets: {} as ITaskFilters,
  }),
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
    async getMulti(facets: ITaskFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiTask.getMulti(this.authTokens.token, facets)
          if (response.value) this.setMulti(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.board = []
        }
      }
    },
    async getMultiByProject(project_key: string, facets: ITaskFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiTask.getMultiByProject(this.authTokens.token, project_key, facets)
          if (response.value) this.setMulti(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.board = []
        }
      }
    },
    setMulti(payload: ITask[]) {
      this.board = payload
    },
    async getTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiTask.getTerm(this.authTokens.token, key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.one = {} as ITask
        }
      }
    },
    async createTerm(payload: ITask = {} as ITask) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          if (payload && Object.keys(payload).length !== 0) this.setDraft(payload)
          const { data: response } = await apiTask.createTerm(this.authTokens.token, this.draft)
          if (response.value) {
            this.setTerm(response.value)
            this.resetDraft()
          } 
        } catch (error) {
          this.one = {} as ITask
        }
      }
    },
    async updateTerm(key: string, payload: ITask = {} as ITask) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          if (payload && Object.keys(payload).length !== 0) this.setDraft(payload)
          const { data: response } = await apiTask.updateTerm(this.authTokens.token, key, this.draft)
          if (response.value) {
            this.setTerm(response.value)
            this.resetDraft()
          } 
        } catch (error) {
          this.one = {} as ITask
        }
      }
    },
    setTerm(payload: ITask) {
      this.one = payload
    },
    setDraft(payload: ITask) {
      this.edit = payload
    },
    resetDraft() {
      this.edit = {} as ITask
    },
    async removeTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiTask.removeTerm(this.authTokens.token, key)
          if (response.value) this.setTerm({} as ITask)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Deletion error",
            content: "Could not remove task. Please check your details, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    async addTemplate(key: string, template_key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiTask.addTemplate(this.authTokens.token, key, template_key)
          if (response.value) this.setTerm(response.value)
        } catch (error) {
          this.one = {} as ITask
        }
      }
    },
    async removeTemplate(key: string, template_key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiTask.removeTemplate(this.authTokens.token, key, template_key)
          if (response.value) this.setTerm(response.value)
        } catch (error) {
          this.one = {} as ITask
        }
      }
    },
    setFilters(payload: ITaskFilters) {
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
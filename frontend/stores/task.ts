import {
  ITask, IScheduledTask, ITaskFilters
} from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { apiTask } from "@/api"

export const useTaskStore = defineStore("taskStore", {
  state: () => ({
    board: [] as ITask[],
    assigned: [] as IScheduledTask[],
    one: {} as ITask,
    edit: {} as ITask,
    facets: {} as ITaskFilters,
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    multi: (state) => state.board,
    scheduled: (state) => state.assigned,
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
          this.setMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiTask.getMulti(this.authTokens.token, facets)
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
    async getMultiByProject(project_key: string, facets: ITaskFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiTask.getMultiByProject(this.authTokens.token, project_key, facets)
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
    setMulti(payload: ITask[]) {
      this.board = payload
    },
    async getScheduledMulti(facets: ITaskFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setScheduledMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiTask.getScheduledMulti(this.authTokens.token, facets)
          if (response.value) {
            if (response.value.length) {
              this.setScheduledMulti(response.value)
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
    async getScheduledMultiByProject(project_key: string, facets: ITaskFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setScheduledMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiTask.getScheduledMultiByProject(this.authTokens.token, project_key, facets)
          if (response.value) {
            if (response.value.length) {
              this.setScheduledMulti(response.value)
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
    setScheduledMulti(payload: IScheduledTask[]) {
      this.assigned = payload
    },
    async getTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setTerm({} as ITask)
          const { data: response } = await apiTask.getTerm(this.authTokens.token, key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
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
    async addToProject(key: string, project_key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiTask.addToProject(this.authTokens.token, key, project_key)
          if (response.value) this.setTerm(response.value)
        } catch (error) {
          this.one = {} as ITask
        }
      }
    },
    async removeFromProject(key: string, project_key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiTask.removeFromProject(this.authTokens.token, key, project_key)
          if (response.value) this.setTerm(response.value)
        } catch (error) {
          this.one = {} as ITask
        }
      }
    },
    setFilters(payload: ITaskFilters) {
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
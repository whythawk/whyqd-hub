import {
  IResource, IResourceManager, IResourceFilters
} from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { apiResource, apiSchema } from "@/api"

export const useResourceStore = defineStore("resourceStore", {
  state: () => ({
    board: [] as IResource[],
    one: {} as IResourceManager,
    edit: {} as IResourceManager,
    facets: {} as IResourceFilters,
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
    async getMulti(facets: IResourceFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiResource.getMulti(this.authTokens.token, facets)
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
    async getMultiByTask(task_key: string, facets: IResourceFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiResource.getMultiByTask(this.authTokens.token, task_key, facets)
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
    setMulti(payload: IResource[]) {
      this.board = payload
    },
    async getTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setTerm({} as IResourceManager)
          const { data: response } = await apiResource.getTerm(this.authTokens.token, key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
        }
      }
    },
    setTerm(payload: IResourceManager) {
      this.one = payload
    },
    setDraft(payload: IResourceManager) {
      this.edit = payload
    },
    resetDraft() {
      this.edit = {} as IResourceManager
    },
    async addSchemaObject(key: string, schema_key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          // this.settings.setPageState("loading")
          const { data: response } = await apiResource.addTermSchemaObject(this.authTokens.token, key, schema_key)
          if (response.value) this.setTerm({} as IResourceManager)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Add schema object error",
            content: "Could not add schema object. Please check your details, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    async createSchemaCrosswalk(subject_key: string, object_key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          // this.settings.setPageState("loading")
          this.setTerm({} as IResourceManager)
          const { data: response } = await apiSchema.createSchemaCrosswalk(this.authTokens.token, subject_key, object_key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Create crosswalk error",
            content: "Could create crosswalk. Please check your details, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    async createTaskSchemaCrosswalk(task_key: string, subject_key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          // this.settings.setPageState("loading")
          this.setTerm({} as IResourceManager)
          const { data: response } = await apiSchema.createTaskSchemaCrosswalk(this.authTokens.token, task_key, subject_key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Create crosswalk error",
            content: "Could create crosswalk. Please check your details, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    async removeTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          // this.settings.setPageState("loading")
          const { data: response } = await apiResource.removeTerm(this.authTokens.token, key)
          if (response.value) this.setTerm({} as IResourceManager)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Deletion error",
            content: "Could not remove resource. Please check your details, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    setFilters(payload: IResourceFilters) {
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
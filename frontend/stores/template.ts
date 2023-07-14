import {
  IReferenceTemplate,
  IDataSourceTemplate,
  ICrosswalkTemplate,
  IReferenceFilters,
  IMimeType,
} from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { apiTemplate } from "@/api"

export const useTemplateStore = defineStore("templateStore", {
  state: () => ({
    board: [] as IReferenceTemplate[],
    one: {} as IDataSourceTemplate | ICrosswalkTemplate,
    edit: {} as IDataSourceTemplate | ICrosswalkTemplate,
    facets: {} as IReferenceFilters,
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
    async getMulti(facets: IReferenceFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiTemplate.getMulti(this.authTokens.token, facets)
          if (response.value) this.setMulti(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.board = []
        }
      }
    },
    setMulti(payload: IReferenceTemplate[]) {
      const IMimeReference: { [key: string]: IMimeType } = {
        "text/csv": "CSV",
        "application/vnd.ms-excel": "XLS",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "XLSX",
        "application/vnd.apache.parquet": "PARQUET",
        "application/vnd.apache.feather": "FEATHER"
      }
      for (const p of payload) {
        if (p.mime_type) p.mime_type = IMimeReference[p.mime_type]
      }
      this.board = payload
    },
    async getCrosswalk(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiTemplate.getCrosswalk(this.authTokens.token, key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.one = {} as ICrosswalkTemplate
        }
      }
    },
    async getDataSource(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiTemplate.getDataSource(this.authTokens.token, key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.one = {} as IDataSourceTemplate
        }
      }
    },
    setTerm(payload: IDataSourceTemplate | ICrosswalkTemplate) {
      this.one = payload
    },
    setDraft(payload: IDataSourceTemplate | ICrosswalkTemplate) {
      this.edit = payload
    },
    resetDraft() {
      this.edit = {} as IDataSourceTemplate | ICrosswalkTemplate
    },
    async removeTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiTemplate.removeTerm(this.authTokens.token, key)
          if (response.value) this.setTerm({} as IDataSourceTemplate | ICrosswalkTemplate)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Deletion error",
            content: "Could not remove template. Please check your details, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    setFilters(payload: IReferenceFilters) {
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
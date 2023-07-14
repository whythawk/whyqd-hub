import { IMimeType, IReference, IReferenceFilters } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { apiReference } from "@/api"

export const useReferenceStore = defineStore("referenceStore", {
  state: () => ({
    board: [] as IReference[],
    one: {} as IReference,
    facets: {} as IReferenceFilters,
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    multi: (state) => state.board,
    term: (state) => state.one,
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
          const { data: response } = await apiReference.getMulti(this.authTokens.token, facets)
          if (response.value) this.setMulti(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.board = []
        }
      }
    },
    setMulti(payload: IReference[]) {
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
    async getTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiReference.getTerm(this.authTokens.token, key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.one = {} as IReference
        }
      }
    },
    setTerm(payload: IReference) {
      this.one = payload
    },
    async removeTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiReference.removeTerm(this.authTokens.token, key)
          if (response.value) this.setTerm({} as IReference)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Deletion error",
            content: "Could not remove reference. Please check your details, or internet connection, and try again.",
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
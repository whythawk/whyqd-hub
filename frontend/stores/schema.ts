import type { IReference, ISchema, ISchemaCreate, IField, IFieldCreate, ICitation, IReferenceFilters } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useReferenceStore } from "./reference"
import { apiSchema, apiReference } from "@/api"

export const useSchemaStore = defineStore("schemaStore", {
  state: () => ({
    board: [] as IReference[],
    one: {} as ISchema,
    edit: {} as ISchemaCreate,
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
    // reference: () => {
    //   return ( useReferenceStore() )
    // },
  },
  actions: {
    async getMulti(facets: IReferenceFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          this.facets.reference_type = "SCHEMA"
          const { data: response } = await apiReference.getMulti(this.authTokens.token, facets)
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
    setMulti(payload: IReference[]) {
      this.board = payload
    },
    async getTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setTerm({} as ISchema)
          const { data: response } = await apiSchema.getTerm(this.authTokens.token, key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
        }
      }
    },
    setTerm(payload: ISchema) {
      this.one = payload
    },
    setDraft(payload: ISchemaCreate) {
      this.edit = payload
    },
    resetDraft() {
      this.edit = {} as ISchemaCreate
    },
    setFilters(payload: IReferenceFilters) {
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
    resetState() {
      this.$reset()
    }
  }
})
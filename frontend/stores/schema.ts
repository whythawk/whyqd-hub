import { IReference, ISchema, ISchemaCreate, IField, IFieldCreate, ICitation,  } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useReferenceStore } from "./reference"
import { apiSchema } from "@/api"

export const useSchemaStore = defineStore("schemaStore", {
  state: () => ({
    board: [] as IReference[],
    one: {} as ISchema,
    edit: {} as ISchemaCreate,
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    multi: (state) => state.board,
    term: (state) => state.one,
    draft: (state) => state.edit,
    authTokens: () => {
      return ( useTokenStore() )
    },
    settings: () => {
      return ( useSettingStore() )
    },
    reference: () => {
      return ( useReferenceStore() )
    },
  },
  actions: {
    async getMulti() {
      this.reference.facets.reference_type = "SCHEMA"
      await this.reference.getMulti()
      if (this.reference.multi) this.setMulti(this.reference.multi)
      else this.setMulti([])
    },
    setMulti(payload: IReference[]) {
      this.board = payload
    },
    async getTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        this.setTerm({} as ISchema)
        try {
          this.settings.setPageState("loading")
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
    resetState() {
      this.$reset()
    }
  }
})
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
    storage: persistedState.cookiesWithOptions({
      // https://prazdevs.github.io/pinia-plugin-persistedstate/frameworks/nuxt-3.html
      // https://nuxt.com/docs/api/composables/use-cookie#options
      // in seconds
      // useRuntimeConfig().public.appCookieExpire,
      path: "/",
      secure: true,
      maxAge: 60 * 60 * 24 * 90,
      expires: new Date(new Date().getTime() + 60 * 60 * 24 * 90),
    }),
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
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiSchema.getTerm(this.authTokens.token, key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.setTerm({} as ISchema)
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
import { IResourceCrosswalkManager, ICrosswalkCreate, IActionModel, IKeyable,  } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { apiCrosswalk } from "@/api"

export const useCrosswalkStore = defineStore("crosswalkStore", {
  state: () => ({
    one: {} as IResourceCrosswalkManager,
    edit: {} as IResourceCrosswalkManager
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    term: (state) => state.one,
    draft: (state) => state.edit,
    scripts: (state) =>
    state.edit && state.edit.crosswalk && state.edit.crosswalk.actions && state.edit.crosswalk.actions.length
      ? state.edit.crosswalk.actions
      : [] as IActionModel[],
    authTokens: () => {
      return ( useTokenStore() )
    },
    settings: () => {
      return ( useSettingStore() )
    },
  },
  actions: {
    async getTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiCrosswalk.getTerm(this.authTokens.token, key)
          if (response.value) this.setTerm(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.setTerm({} as IResourceCrosswalkManager)
        }
      }
    },
    setTerm(payload: IResourceCrosswalkManager) {
      this.one = payload
    },
    setDraft(payload: IResourceCrosswalkManager) {
      this.edit = payload
    },
    setDraftMetadata(payload: IKeyable) {
      if (payload.name) {
        this.edit.crosswalk.name = payload.name
        this.edit.crosswalk.title = payload.title
        this.edit.crosswalk.description = payload.description
      }
    },
    setActionDraft(payload: IActionModel[]) {
      this.edit.crosswalk.actions = payload
    },
    resetActionDraft() {
      this.edit.crosswalk.actions = [] as IActionModel[]
    },
    resetDraft() {
      this.edit = {} as IResourceCrosswalkManager
    },
    resetState() {
      this.$reset()
    }
  }
})
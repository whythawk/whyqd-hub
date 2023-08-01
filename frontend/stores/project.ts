import { IProject, IProjectFilters, IProjectRole, IProjectInvitation, IResearcherRoleType, IOgunFilters } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { useAuthStore } from "./auth"
import { apiProject, apiAuth } from "@/api"

export const useProjectStore = defineStore("projectStore", {
  state: () => ({
    board: [] as IProject[],
    one: {} as IProject,
    edit: {} as IProject,
    invitationships: {} as IProjectInvitation[],
    memberships: {} as IProjectRole[],
    facets: {} as IProjectFilters,
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    multi: (state) => state.board,
    term: (state) => state.one,
    draft: (state) => state.edit,
    invitations: (state) => state.invitationships,
    members: (state) => state.memberships,
    isCustodian: (state) => {
      const authStore = useAuthStore()
      return (
        state.one
        && state.one.auths
        && state.one.auths.length
        && state.one.auths.filter(member =>
          member.researcher.email === authStore.email
          && member.responsibility === "CUSTODIAN").length === 1
      )
    },
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
    async getMembers(key: string, facets: IOgunFilters = {}) {
      // For the project
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiProject.getAllMembers(this.authTokens.token, key, facets)
          if (response.value) {
            if (response.value.length) {
              this.setMembers(response.value)
              this.settings.setPageNext(true)
            } else {
              this.settings.setPageNext(false)
            }
          }
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.memberships = []
        }
      }
    },
    async getProjectRoles(facets: IOgunFilters = {}) {
      // For the user
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiAuth.getAllMemberships(this.authTokens.token, facets)
          if (response.value) {
            if (response.value.length) {
              this.setMembers(response.value)
              this.settings.setPageNext(true)
            } else {
              this.settings.setPageNext(false)
            }
          }
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.memberships = []
        }
      }
    },
    async updateMember(key: string, member_key: string, role_type: IResearcherRoleType, facets: IOgunFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiProject.updateMember(this.authTokens.token, key, member_key, role_type, facets)
          if (response.value) this.setMembers(response.value)
        } catch (error) {
          this.memberships = []
        }
      }
    },
    async removeMember(key: string, member_key: string, facets: IOgunFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiProject.removeMember(this.authTokens.token, key, member_key, facets)
          if (response.value) this.setMembers(response.value)
        } catch (error) {
          this.memberships = []
        }
      }
    },
    setMembers(payload: IProjectRole[]) {
      this.memberships = payload
    },
    async getInvitations(key: string, facets: IOgunFilters = {}) {
      // For project
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiProject.getAllInvitations(this.authTokens.token, key, facets)
          if (response.value) {
            if (response.value.length) {
              this.setInvitations(response.value)
              this.settings.setPageNext(true)
            } else {
              this.settings.setPageNext(false)
            }
          }
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.invitationships = []
        }
      }
    },
    async getMembershipInvitations(facets: IOgunFilters = {}) {
      // For user
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiAuth.getAllInvitations(this.authTokens.token, facets)
          if (response.value) {
            if (response.value.length) {
              this.setInvitations(response.value)
              this.settings.setPageNext(true)
            } else {
              this.settings.setPageNext(false)
            }
          }
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.invitationships = []
        }
      }
    },
    async createInvitation(key: string, email: string, facets: IOgunFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const toasts = useToastStore()
          const { data: response } = await apiProject.createInvitation(this.authTokens.token, key, email, facets)
          if (response.value) {
            this.setInvitations(response.value)
            toasts.addNotice({
              title: "Member invitation",
              content: `Remember to email ${email} to invite them yourself and tell them about this project.`,
            })
          } else toasts.addNotice({
            title: "Invitation error",
            content: `You have already invited ${email}.`,
            icon: "error"
          })
        } catch (error) {
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Invitation error",
            content: error as string,
            icon: "error"
          })
        }
      }
    },
    async removeInvitation(key: string, invitation_key: string, facets: IOgunFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiProject.removeInvitation(this.authTokens.token, key, invitation_key, facets)
          if (response.value) this.setInvitations(response.value)
        } catch (error) {
          this.invitationships = []
        }
      }
    },
    async acceptInvitation(invitation_key: string, facets: IOgunFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiAuth.acceptInvitation(this.authTokens.token, invitation_key, facets)
          if (response.value) this.setInvitations(response.value)
        } catch (error) {
          this.invitationships = []
        }
      }
    },
    async rejectInvitation(invitation_key: string, facets: IOgunFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiAuth.rejectInvitation(this.authTokens.token, invitation_key, facets)
          if (response.value) this.setInvitations(response.value)
        } catch (error) {
          this.invitationships = []
        }
      }
    },
    setInvitations(payload: IProjectInvitation[]) {
      this.invitationships = payload
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
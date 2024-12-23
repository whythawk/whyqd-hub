import type {
  IUserProfile,
  IUserProfileUpdate,
  IUserOpenProfileCreate,
  ISubscriptionProfile,
  IEnableTOTP,
  IWebToken,
} from "@/interfaces"
import { apiAuth } from "@/api"
import { useTokenStore } from "./tokens"
import { useToastStore } from "./toasts"
import { tokenIsTOTP, tokenParser } from "@/utilities"

export const useAuthStore = defineStore("authStore", {
  state: (): IUserProfile => ({
    id: "",
    email: "",
    email_validated: false,
    is_active: false,
    is_superuser: false,
    full_name: "",
    password: false,
    totp: false,
    subscriptions: {} as ISubscriptionProfile
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
    isAdmin: (state) => {
        return (
          state.id &&
          state.is_superuser &&
          state.is_active
        )
    },
    profile: (state) => state,
    loggedIn: (state) => state.id !== "",
    hasExplorerSubscription: (state) => {
      return (
        state.id &&
        state.is_active &&
        (["EXPLORER", "RESEARCHER", "INVESTIGATOR"].includes(state.subscriptions.membership)
          || state.is_superuser)
      )
    },
    hasResearcherSubscription: (state) => {
      return (
        state.id &&
        state.is_active &&
        (["RESEARCHER", "INVESTIGATOR"].includes(state.subscriptions.membership)
          || state.is_superuser)
      )
    },
    subscriptionState: (state) => state.subscriptions,
    authTokens: () => {
      return ( useTokenStore() )
    }
  },
  actions: {
    // AUTHENTICATION
    async logIn(payload: { username: string; password?: string; query?: string }) {
      try {
        await this.authTokens.getTokens(payload)
        if (this.authTokens.token && 
            !tokenIsTOTP(this.authTokens.token)
            ) await this.getUserProfile()
      } catch (error) {
        const toasts = useToastStore()
        toasts.addNotice({
          title: "Login error",
          content: "Please check your details, or internet connection, and try again.",
          icon: "error"
        })
        this.logOut()
      }
    },
    async magicLogin(token: string) {
      try {
        await this.authTokens.validateMagicTokens(token)
        if (this.authTokens.token && 
          !tokenIsTOTP(this.authTokens.token)
          ) await this.getUserProfile()
      } catch (error) {
        const toasts = useToastStore()
        toasts.addNotice({
          title: "Login error",
          content: "Please check your details, or internet connection, and try again.",
          icon: "error"
        })
        this.logOut()
      }
    },
    async totpLogin(claim: string) {
      try {
        await this.authTokens.validateTOTPClaim(claim)
        if (this.authTokens.token && 
          !tokenIsTOTP(this.authTokens.token)
          ) await this.getUserProfile()
      } catch (error) {
        const toasts = useToastStore()
        toasts.addNotice({
          title: "Login error",
          content: "Please check your details, or internet connection, and try again.",
          icon: "error"
        })
        this.logOut()
      }
    },
    // PROFILE MANAGEMENT
    async createUserProfile(payload: IUserOpenProfileCreate) {
      try {
        const { data: response } = await apiAuth.createProfile(payload)
        if (response.value) this.setUserProfile(response.value)
        await this.authTokens.getTokens({ 
          username: this.email, 
          password: payload.password 
        })
      } catch (error) {
        const toasts = useToastStore()
        toasts.addNotice({
          title: "Login creation error",
          content: "Please check your details, or internet connection, and try again.",
          icon: "error"
        })
      }
    },
    async getUserProfile(force: boolean = false) {
      if (!this.loggedIn || force) {
        await this.authTokens.refreshTokens()
        if (this.authTokens.token) {
          try {
            const { data: response } = await apiAuth.getProfile(this.authTokens.token)
            if (response.value) this.setUserProfile(response.value)
          } catch (error) {
            this.logOut()
          }
        }
      }
    },
    async updateUserProfile(payload: IUserProfileUpdate) {
      await this.authTokens.refreshTokens()
      if (this.loggedIn && this.authTokens.token) {
        const toasts = useToastStore()
        try {
          const { data: response } = await apiAuth.updateProfile(this.authTokens.token, payload)
          if (response.value) {
            this.setUserProfile(response.value)
            toasts.addNotice({
              title: "Profile update",
              content: "Your settings have been updated.",
            })
          } else throw "Error"
        } catch (error) {
          toasts.addNotice({
            title: "Profile update error",
            content: "Please check your submission, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    // MANAGING TOTP
    async enableTOTPAuthentication(payload: IEnableTOTP) {
      const toasts = useToastStore()
      await this.authTokens.refreshTokens()
      if (this.loggedIn && this.authTokens.token) {
        try {
          const { data: response } = await apiAuth.enableTOTPAuthentication(this.authTokens.token, payload)
          if (response.value) {
            this.totp = true
            toasts.addNotice({
              title: "Two-factor authentication",
              content: response.value.msg,
            })
          } else throw "Error"
        } catch (error) {
          toasts.addNotice({
            title: "Error enabling two-factor authentication",
            content: "Please check your submission, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    async disableTOTPAuthentication(payload: IUserProfileUpdate) {
      const toasts = useToastStore()
      await this.authTokens.refreshTokens()
      if (this.loggedIn && this.authTokens.token) {
        try {
          const { data: response } = await apiAuth.disableTOTPAuthentication(this.authTokens.token, payload)
          if (response.value) {
            this.totp = false
            toasts.addNotice({
              title: "Two-factor authentication",
              content: response.value.msg,
            })
          } else throw "Error"
        } catch (error) {
          toasts.addNotice({
            title: "Error disabling two-factor authentication",
            content: "Please check your submission, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    // mutations are actions, instead of `state` as first argument use `this`
    setUserProfile (payload: IUserProfile) {
      this.id = payload.id
      this.email = payload.email
      this.email_validated = payload.email_validated
      this.is_active = payload.is_active
      this.is_superuser = payload.is_superuser
      this.full_name = payload.full_name
      this.password = payload.password
      this.totp = payload.totp
      this.subscriptions = payload.subscriptions
    },
    async recoverPassword(email: string) {
      const toasts = useToastStore()
      if (!this.loggedIn) {
        try {
          const { data: response } = await apiAuth.recoverPassword(email)
          if (response.value) {
            if (response.value.hasOwnProperty("claim")) 
              this.authTokens.setMagicToken(response.value as unknown as IWebToken)
            toasts.addNotice({
              title: "Success",
              content: "If that login exists, we'll send you an email to reset your password.",
            })
          } else throw "Error"
        } catch (error) {
          toasts.addNotice({
            title: "Login error",
            content: "Please check your details, or internet connection, and try again.",
            icon: "error"
          })
          this.authTokens.resetState()
        }
      }
    },
    async resetPassword(password: string, token: string) {
      const toasts = useToastStore()
      if (!this.loggedIn) {
        try {
          const claim: string = this.authTokens.token
          // Check the two magic tokens meet basic criteria
          const localClaim = tokenParser(claim)
          const magicClaim = tokenParser(token)
          if (localClaim.hasOwnProperty("fingerprint") 
              && magicClaim.hasOwnProperty("fingerprint")
              && localClaim["fingerprint"] === magicClaim["fingerprint"]) {
            const { data: response } = await apiAuth.resetPassword(password, claim, token)
            if (response.value) toasts.addNotice({
              title: "Success",
              content: response.value.msg,
            })
            else throw "Error"
          }
        } catch (error) {
          toasts.addNotice({
            title: "Login error",
            content: "Ensure you're using the same browser and that the token hasn't expired.",
            icon: "error"
          })
          this.authTokens.resetState()
        }
      }
    },
    // reset state using `$reset`
    logOut () {
      this.authTokens.resetState()
      this.$reset()
    }
  }
})
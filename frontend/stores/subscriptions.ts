import {
  ICode, IOrder, IProduct, IUserProfile, ISubscription, ISubscriptionView, ISubscriptionAdminCreate,
  IStripeCheckoutResponse, IStripeIntent, IStripeCheckoutIntent, IOgunFilters
} from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useToastStore } from "./toasts"
import { useSettingStore } from "./settings"
import { apiSubscriptions } from "@/api"

export const useSubscriptionsStore = defineStore("subscriptionsStore", {
  state: () => ({
    products: [] as IProduct[],
    orders: [] as IOrder[],
    board: [] as ISubscriptionView[],
    subscriber: {} as IUserProfile,
    redirect: "",
    facets: {} as IOgunFilters,
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    subscriptionProducts: (state) => state.products,
    orderHistory: (state) => state.orders,
    multi: (state) => state.board,
    subscriberProfile: (state) => state.subscriber,
    filters: (state) => state.facets,
    stripeRedirect: (state) => state.redirect,
    authTokens: () => {
      return ( useTokenStore() )
    },
    settings: () => {
      return ( useSettingStore() )
    },
  },
  actions: {
    async getMulti(facets: IOgunFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiSubscriptions.getMulti(this.authTokens.token, facets)
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
    setMulti(payload: ISubscriptionView[]) {
      this.board = payload
    },
    async getOrders(facets: IOgunFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiSubscriptions.getOrders(this.authTokens.token, facets)
          if (response.value) {
            if (response.value.length) {
              this.setOrders(response.value)
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
    setOrders(payload: IOrder[]) {
      this.orders = payload
    },
    async getSubscriber(email: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const payload = { email }
          const { data: response } = await apiSubscriptions.getSubscriber(this.authTokens.token, payload)
          if (response.value) this.setSubscriber(response.value)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.board = []
        }
      }
    },
    setSubscriber(payload: IUserProfile) {
      this.subscriber = payload
    },
    async getAllSubscriptionProducts() {
      try {
        this.settings.setPageState("loading")
        const { data: response } = await apiSubscriptions.getAllSubscriptionProducts(
          this.authTokens.token
        )
        if (response.value) {
          this.setSubscriptionProducts(response.value)
        }
        this.settings.setPageState("done")
      } catch (error) {
        this.settings.setPageState("error")
      }
    },
    async updateAllSubscriptionProducts(payload: IProduct[]) {
      try {
        const { data: response } = await apiSubscriptions.updateAllSubscriptionProducts(
          this.authTokens.token,
          payload
        )
        if (response.value) {
          this.setSubscriptionProducts(response.value)
        }
        this.settings.setPageState("done")
      } catch (error) {
        this.settings.setPageState("error")
      }
    },
    setSubscriptionProducts(payload: IProduct[]) {
      this.products = payload
    },
    async createSubscription(payload: ISubscriptionAdminCreate) {
      try {
        const { data: response } = await apiSubscriptions.createSubscription(
          this.authTokens.token,
          payload
        )
        this.settings.setPageState("done")
      } catch (error) {
        this.settings.setPageState("error")
      }
    },
    async removeSubscription(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiSubscriptions.removeSubscription(this.authTokens.token, key)
          if (response.value) this.getMulti()
        } catch (error) {
          this.settings.setPageState("error")
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Deletion error",
            content: "Could not remove subscriber. Please check your details, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    async createStripeCheckout(payload: IStripeCheckoutIntent) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiSubscriptions.createCheckoutSession(
            this.authTokens.token,
            payload
          )
          if (response.value) {
            this.setStripeRedirect(response.value.redirect)
          }
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
        }
      }
    },
    async redirectToStripeAccount() {
      try {
        const { data: response } = await apiSubscriptions.redirectToStripeAccount(this.authTokens.token)
        if (response.value) {
          this.setStripeRedirect(response.value.redirect)
        }
        this.settings.setPageState("done")
      } catch (error) {
        this.settings.setPageState("error")
      }
    },
    setStripeRedirect(payload: string) {
      this.redirect = payload
     },
    setFilters(payload: IOgunFilters) {
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
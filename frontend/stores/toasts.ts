import type { INotification } from "@/interfaces"
import { generateUUID } from "@/utilities"

export const useToastStore = defineStore("toastStore", {
  state: () => ({
    board: [] as INotification[]
  }),
  getters: {
    first: (state) => state.board.length > 0 && state.board[0],
    multi: (state) => state.board
  },
  actions: {
    addNotice (payload: INotification) {
      payload.uid = generateUUID()
      if (!payload.icon) payload.icon = "success"
      this.multi.push(payload)
    },
    removeNotice (payload: INotification) {
      this.board = this.multi.filter(
        (note) => note !== payload
      )
    },
    async timeoutNotice (payload: INotification, timeout: number = 2000) {
      await new Promise((resolve) => {
        setTimeout(() => {
          this.removeNotice(payload)
          resolve(true)
        }, timeout)
      })
    },
    // reset state using `$reset`
    resetState() {
      this.$reset()
    }
  }
})
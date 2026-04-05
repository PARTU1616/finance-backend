import { defineStore } from 'pinia'
import { api } from 'boot/axios'
import { Notify } from 'quasar'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user_id: null,
    email: null,
    role: null,
    isAuthenticated: false
  }),

  getters: {
    isAdmin: (state) => state.role === 'Admin',
    isAnalyst: (state) => state.role === 'Analyst',
    isViewer: (state) => state.role === 'Viewer',
    canWrite: (state) => state.role === 'Admin',
    canViewDashboard: (state) => ['Admin', 'Analyst'].includes(state.role)
  },

  actions: {
    setSession(userData) {
      this.user_id = userData.user_id
      this.email = userData.email
      this.role = userData.role
      this.isAuthenticated = true
    },

    clearSession() {
      this.user_id = null
      this.email = null
      this.role = null
      this.isAuthenticated = false
    },

    async fetchSession() {
      try {
        const response = await api.get('/auth/session/')
        if (response.data.ok) {
          this.setSession(response.data.data)
          return true
        } else {
          this.clearSession()
          return false
        }
      } catch (error) {
        this.clearSession()
        return false
      }
    },

    async login(email, password) {
      try {
        const response = await api.post('/auth/login/', { email, password })

        if (response.data.ok) {
          this.setSession(response.data.data)
          Notify.create({
            type: 'positive',
            message: 'Login successful',
            position: 'top'
          })
          return { success: true }
        } else {
          Notify.create({
            type: 'negative',
            message: response.data.msg || 'Login failed',
            position: 'top'
          })
          return { success: false, error: response.data.error }
        }
      } catch (error) {
        const message = error.response?.data?.msg || 'Login failed'
        Notify.create({
          type: 'negative',
          message,
          position: 'top'
        })
        return { success: false, error: message }
      }
    },

    async logout() {
      try {
        await api.post('/auth/logout/')
        this.clearSession()
        Notify.create({
          type: 'positive',
          message: 'Logged out successfully',
          position: 'top'
        })
        return true
      } catch (error) {
        this.clearSession()
        return true
      }
    }
  }
})

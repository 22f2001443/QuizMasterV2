// stores/authStore.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    roles: [],
    name: null,
    email: null,
  }),
  getters: {
    isAdmin: (state) => state.roles.includes('admin'),
    hasRole: (state) => (role) => state.roles.includes(role),
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    setAuthData({ token, roles, name, email }) {
      this.token = token
      this.roles = roles
      this.name = name
      this.email = email
    },
    logout() {
      this.token = null
      this.roles = []
      this.name = null
      this.email = null
    },
  },
  persist: true // ✅ Auto-persist all state
})
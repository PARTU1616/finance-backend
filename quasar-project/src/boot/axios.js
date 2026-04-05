import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Use live backend API in production, local proxy in development
const baseURL = process.env.NODE_ENV === 'production' 
  ? 'https://finance-backend-1j75.onrender.com/api'
  : '/api'

// Create axios instance
const api = axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default boot(({ app, router }) => {
  // Make axios available globally
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api

  // Response interceptor for handling 401 errors
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        // Redirect to login on 401
        if (router.currentRoute.value.path !== '/login') {
          router.push('/login')
        }
      }
      return Promise.reject(error)
    }
  )
})

export { api }

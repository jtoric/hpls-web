/**
 * Application entry point.
 *
 * Bootstraps the Vue 3 app with Pinia (state) and Vue Router,
 * then validates the stored JWT token before mounting.
 * This ensures the auth state is resolved before any route guard runs.
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Validate the persisted token (if any) before mounting so that
// router guards see the correct authentication state on first load.
const auth = useAuthStore()
auth.checkAuth().then(() => {
  app.mount('#app')
})

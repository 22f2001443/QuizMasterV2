// import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toast from 'vue-toastification'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import 'vue-toastification/dist/index.css'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import 'bootstrap-icons/font/bootstrap-icons.css'

import App from './App.vue'
import router from './routes'

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate) // Register the plugin

app.use(pinia)
app.use(router)
app.use(Toast)

app.mount('#app')
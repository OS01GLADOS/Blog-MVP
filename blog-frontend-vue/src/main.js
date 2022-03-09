import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

var vm = createApp(App).use(router).mount('#app')

export default vm
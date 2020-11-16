import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Job from '../views/Job.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  { path: '/job/:id', component: Job }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

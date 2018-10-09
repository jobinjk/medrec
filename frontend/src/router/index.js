import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Patients from '@/components/Patients'
import Meta from 'vue-meta'

Vue.use(Router)
Vue.use(Meta)

export default new Router({
  routes: [
    {path: '/', redirect: '/patients'},
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        public: true
      }
    },
    {
      path: '/patients',
      name: 'Patients',
      component: Patients,
      meta: {
        permissions: {
        roles: ['user'],
        permissions: ['can_view'],
        redirectTo: '/login'
        },
      }
    },
  ]
})

import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Patients from '@/components/Patients'
import Profile from '@/components/Profile'
import Home from '@/components/Home'
import Meta from 'vue-meta'

Vue.use(Router)
Vue.use(Meta)

export default new Router({
  routes: [
    {path: '/', redirect: '/home'},
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        public: true
      }
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
      meta: {
        permissions: {
        roles: ['user'],
        permissions: ['can_view'],
        redirectTo: '/login'
        },
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
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      props: true,
      meta: {
        permissions: {
          roles: ['user'],
          permissions: ['can_view'],
          redirectTo: '/login'
        }
      }

    }
  ]
})

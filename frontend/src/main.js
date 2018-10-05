// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import axios from 'axios'
import VueAxios from 'vue-axios'
import 'font-awesome/css/font-awesome.min.css'
import Notifications from 'vue-notification'
import VueAuthenticate from 'vue-authenticate'
import VueAuthorize from 'vue-authorize'
import VueMoment from 'vue-moment'
import VueJsonPretty from 'vue-json-pretty'
import countTo from 'vue-count-to'
const baseUrl = process.env.BASE_ORIGIN
// const secureCookie = process.env.SECURE_COOKIE

console.log('Setting Axios baseUrl as :', baseUrl)
var theme = {
  primary: '#259dab',
  secondary: '#424242',
  accent: '#82B1FF',
  error: '#dd4b39',
  info: '#2196F3',
  success: '#4CAF50',
  warning: '#FFC107',
  background: '#898E9E'
}

// Vuetify base theme
Vue.use(Vuetify, {theme: theme})

// Add Vue Plugins
Vue.use(Notifications)
Vue.use(VueMoment)
Vue.use(VueAxios, axios)

// Add Vue additional Components
Vue.component('vue-json-pretty', VueJsonPretty)
Vue.component('v-counter', countTo)

Vue.config.productionTip = false

// For http request handling
axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.baseURL = baseUrl

// JWT Login
Vue.use(VueAuthenticate, {
  tokenName: 'auth_token',
  baseUrl: baseUrl,
  storageType: 'cookieStorage',
  // Secure cookie storage only works on Production and not on localhost
  // cookieStorage: { secure: true },
  providers: {
  }
})
Vue.use(VueAuthorize, {
  roles: {
    user: {
      handler: function () {
        return this.$auth.isAuthenticated()
      },

      permissions: ['can_view']
    }
  },

  permissions: {
    can_view: function () {
      return true
    }
  }
})
router.beforeEach(function (to, from, next) {
  if (to.meta && to.meta.permissions) {
    let roles = to.meta.permissions.roles
    let permissions = to.meta.permissions.permissions

    router.app.$authorize.isAuthorized(roles, permissions).then(function () {
      next()
    }).catch(function () {
      next(to.meta.permissions.redirectTo || '/login')
    })
  } else {
    next()
  }
})
/* eslint-disable no-new */

// MomentJS filters
Vue.filter('humanizeTime', function (value) {
  return Vue.moment(value).fromNow()
})

Vue.filter('calendarTime', function (value) {
  return Vue.moment(value).calendar()
})

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

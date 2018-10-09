<template>
      <v-app id="login" class="secondary">
        <v-content>
          <v-container fluid fill-height>
            <v-layout align-center justify-center>
              <v-flex xs12 sm8 md4 lg4>
                <v-card class="elevation-1 pa-3">
                  <v-form v-model="loginForm" @submit.prevent="doLogin" ref="loginForm">
                    <v-card-text>
                      <div class="layout column align-center">
                        <h1 class="flex my-4 primary--text">MEDREC</h1>
                      </div> 
                      <v-layout row wrap>
                        <v-flex xs12>
                          <v-text-field append-icon="person" name="username" label="Username" type="text" v-model=" username"></v-text-field>
                        </v-flex>
                        
                        <v-flex xs12>
                          <v-text-field append-icon="lock" name="password" label="Password" id="password" type="password" v-model="password"></v-text-field>
                        </v-flex>

                        <v-flex xs12>
                            <v-alert :value="loginErrMsg" color="error" icon="warning" outline>{{loginErrMsg}}</v-alert>
                        </v-flex>
                      </v-layout>               
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn flat color="success" type="submit" :loading="loading">Login</v-btn>
                    </v-card-actions>
                  </v-form>
                </v-card>
              </v-flex>
            </v-layout>
          </v-container>
        </v-content>
      </v-app>
    </template>
    <script>
      export default {
        data () {
          return {
            loading: false,
            valid: true,
            loginForm: true,
            username: '',
            loginErrMsg: '',
            usernameRules: [
              v => !!v || 'Username is required',
              v => (v && v.length >= 5) || 'Username must be greater than 5 characters'
            ],
            e1: false,
            password: '',
            passRules: [
              v => !!v || 'Password is required',
              v => (v && v.length >= 6) || 'Password must be greater than 6 characters'
            ],

            select: null
          }
        },
        metaInfo () {
          return {
            title: 'Login',
            titleTemplate: '%s | MEDREC '
          }
        },
        methods: {
          checkLogin () {
            if (this.$auth.isAuthenticated()) {
              this.$notify({
                title: 'Welcome',
                type: 'success',
                text: 'You are already logged in, please logout to change user'
              })
              this.$router.push('/')
            }
          },
          doLogin () {
            this.checkLogin()
            this.loading = true
            var user = {username: this.username, password: this.password}
            var requestOptions = {
              method: 'POST',
              headers: {'Content-type': 'application/json'}
            }
            this.$auth.login(user, requestOptions).then((response) => {
              if (response.status === 200) {
                this.loading = false
                window.location = '/'
              }
            }, (err) => {
              this.err = true
              if (err.response.status === 404) {
                this.loading = false
                this.loginErrMsg = 'User not found'
              }
              if (err.response.status === 400) {
                this.loading = false
                this.loginErrMsg = err.response.data.msg
              }
            })
          },
          clear () {
            this.$refs.form.reset()
          }
        },
        created () {
          this.checkLogin()
        }
      }
    </script>
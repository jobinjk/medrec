<template>
  <v-container fluid grid-list-lg>
    <v-layout row wrap>
      <v-flex xs12 sm12 md12 lg4>
        <v-card flat>
          <v-card-text class="primary">
            <v-layout column align-center>
              <v-flex xs12>
                <v-avatar :size="75" color="teal lighten-3">
                  <img src="https://randomuser.me/api/portraits/men/42.jpg" alt="user image">
                </v-avatar>
              </v-flex>
              <v-flex xs12 class="text-xs-center">
                <label class="title white--text">{{user.username}}</label>
                <br>
                <label class="caption white--text">{{user.email}}</label>
                <br>
                <v-tooltip left>
                  <label slot="activator" class="caption white--text">{{user.created_on | humanizeTime}}</label>
                  <span>{{ user.created_on | calendarTime}}</span>
                </v-tooltip>
              </v-flex>
            </v-layout>
          </v-card-text>          
        </v-card>
      </v-flex>
      <v-flex xs12 sm12 md12 lg6>
        <v-card>
          <v-card-text>
            <v-form v-model="editUserForm" ref="editUserForm" @submit.prevent="updateProfile" >
              <v-layout row wrap>
                <v-flex xs12>
                  <v-text-field v-model="editUser.username" :rules="usernameRules" label="Enter Username" min="5" max="10" :counter="10" required></v-text-field>
                </v-flex>
                <v-flex xs12>
                  <v-text-field v-model="password_old" :append-icon="e1 ? 'visibility' : 'visibility_off'" @click:append="() => (e1 = !e1)" :type="e1 ? 'password' : 'text'" 
                    :rules="passRules" name="old password" label="Enter Your Old Password" 
                    hint="At least 6 characters" min="6" max="15" :counter="15" required>                      
                  </v-text-field>
                </v-flex>
                
                <v-flex xs12>
                  <v-text-field v-model="password_new" :append-icon="e1 ? 'visibility' : 'visibility_off'" @click:append="() => (e1 = !e1)" :type="e1 ? 'password' : 'text'" 
                    :rules="passRules" name="new password" label="Enter Your New Password" 
                    hint="At least 6 characters" min="6" max="15" :counter="15" required>
                  </v-text-field>
                </v-flex>
                
                <v-flex xs12>
                  <v-alert :value="updateErrMsg" color="error" icon="warning" outline>{{updateErrMsg}}</v-alert>
                </v-flex>
              </v-layout>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="success darken-1" flat type="submit">Update</v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
          
        </v-card>
        
      </v-flex>
    </v-layout>
  </v-container>

</template>
<script>
  export default {
    name: 'Profile',
    data () {
      return {
        oldPassword: false,
        newPassword: false,
        editUserForm: true,
        updateErrMsg: '',
        editUser: {
          username: '',
          password: {
  
          }
        },
        password_old: '',
        password_new: '',
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

        select: null,
        user: {},
        stats: {}
      }
    },
    methods: {
      fetchProfile () {
        var url = '/api/users/profile'
        this.$http.get(url).then(
          (response) => {
            this.user = response.data.profile
            localStorage.user = JSON.stringify(this.user)
          })
      },
      updateProfile () {
        var url = '/api/users/profile'
        this.editUser.password.old = this.password_old
        this.editUser.password.new = this.password_new
        this.$http.put(url, this.editUser).then(
          (response) => {
            this.fetchProfile()
            this.$refs.editUserForm.reset()
            this.updateErrMsg = ''
            this.$notify({
              title: response.statusText,
              type: 'success',
              text: 'Hello, the Profile is editted successfully!!!'
            })
          },
          (err) => {
            this.$notify({
              title: err.response.statusText,
              type: 'error',
              text: 'Profile editting failed error in password, please check the password you have typed'

            })
            this.updateErrMsg = err.response.data.message
          })
      }
    },
    created(){
      try{
      this.user = JSON.parse(localStorage.user)
    }
    catch(err){
      this.fetchProfile()
    }
    }
  }
      </script>
<template>
  <v-card flat>
    <v-card-text class="primary">
      <v-layout column align-center>
        <v-flex xs12>
          <v-avatar :size="75" color="teal lighten-3">
            <img src="https://randomuser.me/api/portraits/men/42.jpg" alt="user image">
          </v-avatar>
        </v-flex>
        <v-flex xs12>
          <label class="subheading white--text">{{user.username}}</label>
        </v-flex>
      </v-layout>
    </v-card-text>
    <v-card-actions>
      <v-btn flat small color="success" @click.native= "$router.push('/profile')">Profile</v-btn>
      <v-spacer></v-spacer>
      <v-btn flat small color="error" @click.native="logout" >Logout</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {

  data () {
    return {
      user: {}
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
    logout () {
      this.$auth.logout()
      window.location.reload()
    }
  },
  created(){
    this.fetchProfile()
  }
}
</script>
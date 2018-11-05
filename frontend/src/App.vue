  <template>
    <div>
    <template v-if="$route.meta.public">
      <router-view/>
    </template>
    <template v-else>
      <v-app>
        <v-navigation-drawer persistent :mini-variant="miniVariant" :clipped="clipped" enable-resize-watcher fixed app  dark class="background">
          <v-list>
            <v-list-tile value="true" v-for="(item, i) in items" :key="i" :href="'#'+item.href">
              <v-list-tile-action class="white--text">
                <v-icon v-html="item.icon" medium></v-icon>
              </v-list-tile-action>
              <v-list-tile-content class="white--text">
                <v-list-tile-title v-text="item.title"></v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-navigation-drawer>
        <v-toolbar app :clipped-left="clipped" dark color="primary">
          <v-btn icon @click.stop="miniVariant = !miniVariant">
            <v-icon>menu</v-icon>
          </v-btn>
          <v-toolbar-title v-text="title"></v-toolbar-title>
          <v-spacer></v-spacer>
          <v-menu open-on-hover offset-y :nudge-bottom="15" close-on-click>
            <v-btn dark icon slot="activator">
              <v-icon medium>fa-user</v-icon>
            </v-btn>      
            <profile-tile></profile-tile>
          </v-menu>
        </v-toolbar>
        <v-content>
          <notifications position="bottom right" animation-name="v-fade-right"/>
          <router-view :key="$route.fullPath"></router-view>
        </v-content>
        <v-footer inset app>
          <v-layout column align-end>
            <span>New ones &copy; 2018</span>
          </v-layout>
        </v-footer>
      </v-app>
    </template>
  </div>
  </template>
  <script>
    import ProfileTile from '@/components/others/ProfileTile'
    export default {
      components: {'profile-tile': ProfileTile},
      data () {
        return {
          clipped: true,
          fixed: false,
          isLoggedIn: false,
          items: [
          {
            icon: 'fa-home',
            title: 'Home',
            href: '/home'
          },
          { 
            icon: 'fa-database',
            title: 'Patients',
            href: '/patients'
          }],
          miniVariant: false,
          title: 'MEDREC'
        }
      },
      methods: {
      },
      created () {
        // this.isLoggedIn = this.$auth.isAuthenticated()
        // console.log('>>>>>>>>>> ashdhsakjdhsajhdh')
      },
      computed: {
        currentRoute () {
          return this.$route.path
        }
      },
      name: 'App'
    }
  </script>

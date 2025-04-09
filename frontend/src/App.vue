<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-app-bar-nav-icon @click="change_drawer_state" />
      </div>

      <v-spacer></v-spacer>
      <v-btn @click="$router.push('/user')" text>
        <!--User Profile-->
        <v-icon>mdi-account</v-icon>
      </v-btn>
    </v-app-bar>
    <Navigator/>
    <v-main>
      <router-view/>
    </v-main>
    <Footer />
  </v-app>
</template>

<script>
import { checkAuthorizaion, loadSessionToken } from '@/utils'
import Footer from './components/FooterPage.vue';
import Navigator from './components/NavigatorPage.vue';
export default {
  name: 'App',

  components: {
    Navigator,
    Footer
  },

  data: () => ({
    //
  }),
  methods: {
    change_drawer_state() {
      console.log('change_drawer_state')
      this.$store.dispatch('toggle_navigator_drawer');
    },
  },
  created() {
    if(checkAuthorizaion()){
      this.$store.dispatch('set_authenticated', true);
      this.$store.dispatch('set_user_token', loadSessionToken());
    }else{
      this.$store.dispatch('set_authenticated', false);
    }
  },
};
</script>
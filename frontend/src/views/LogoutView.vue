<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" sm="8" md="6">
          <v-card>
            <v-card-title class="headline">登出</v-card-title>
            <v-card-text>
              <p>您已登出，将在 {{ countdown }} 秒后返回。</p>
              <v-btn color="error" @click="logoutNow">立即返回</v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import {logout} from '@/utils'
  export default {
    data() {
      return {
        countdown: 5,
        timer: null
      };
    },
    mounted() {
      this.startCountdown();
      logout()
      this.$store.dispatch("set_authenticated", false)
      this.$store.dispatch("set_user_token", null)
      this.$store.dispatch("set_user_info", null)
    },
    methods: {
      startCountdown() {
        this.timer = setInterval(() => {
          if (this.countdown > 0) {
            this.countdown--;
          } else {
            this.signout();
          }
        }, 1000);
      },
      signout() {
        clearInterval(this.timer);
        this.$router.push('/login');
      },
      logoutNow() {
        this.signout();
      }
    },
    beforeDestroy() {
      clearInterval(this.timer);
    },
  };
  </script>
  
  <style scoped>
  </style>
  
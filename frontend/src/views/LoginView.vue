<template>
    <v-container fluid>

      <v-snackbar v-model="snackbar" :timeout="timeout">
        {{ message }}
        <template v-slot:action="{ attrs }">
          <v-btn color="white" text v-bind="attrs" @click="snackbar = false">
            关闭
          </v-btn>
        </template>
      </v-snackbar>

      <v-row justify="center" style="margin-top: 1%;">
        <v-alert type="warning" text prominent border="left" v-if="this.$store.state.authenticated">
            该网站已经登录，可以通过重新登陆来更新用户信息
        </v-alert>
      </v-row>

      <v-row justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="elevation-12">
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title>登录</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field
                  v-model="formData.username"
                  label="邮箱、用户名"
                  :rules="[rules.required]"
                  required
                  prepend-icon="mdi-email"
                ></v-text-field>
                <v-text-field
                  v-model="formData.password"
                  :rules="[rules.minLength]"
                  label="密码"
                  required
                  prepend-icon="mdi-lock"
                  type="password"
                ></v-text-field>
               
                <v-checkbox
                  v-model="rememberMe"
                  label="记住我"
                ></v-checkbox>
              </v-form>

            </v-card-text>
            <v-card-actions>
              <v-btn text color="primary" @click="register">用户注册</v-btn>
              <v-spacer></v-spacer>
              
              <v-btn color="primary" :disabled="!valid" @click="submit">登录</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        
      </v-row>
  
    </v-container>
  </template>
  <script>
  import Cookies from 'js-cookie';
  import http from '@/http'
  import { checkAuthorizaion } from '@/utils';
  export default {
    data: () => ({
      loggedIn: false,
      snackbar: false,
      message: '',
      timeout: 5000,
      valid: true,
      formData:{
        username: '',
        password: '',
      },
      rules: {
        required: value => !!value || '必填项',
        minLength: value => (value && value.length >= 6) || '至少6个字符',
    },
      rememberMe: false,
      role: '',
      roles: [],
      rolesScopes: {},
    }),
    methods: {
      submit() {
        if (this.$refs.form.validate()){
        let formData = new FormData();
        formData.append('username', this.formData.username);
        formData.append('password', this.formData.password);
          
        http.post('/auth/login',formData,
            { headers: { 'Content-Type': 'application/json' } }
          ).then(response => {
            if (response.status == 200) {
              let token = response.data;
              Cookies.set("token", token)
              this.$store.dispatch("set_authenticated", true)
              this.$store.dispatch("set_user_token", token)
              this.$router.push(this.$route.query.redirect || '/')
            } else {
              this.showSnackbar("登录失败"+response.status+" "+response.data);
            }
          }).catch(error => { 
            this.showSnackbar("登录失败"+error); 
          });
          if (this.rememberMe) {
            Cookies.set('username', this.formData.username, { expires: 7 });
          }
        }
      },
      showSnackbar(message = 'Login error', timeout = 5000) {
        this.message = message;
        this.timeout = timeout;
        this.snackbar = true;
      },
      register() {
        this.$router.push('/register');
      },
      autoFillCredentials() {
        const storedUsername = Cookies.get('username');
        if (storedUsername) {
          this.formData.username = storedUsername;
          this.rememberMe = true;
        }
      },
    },
    mounted() {
      this.autoFillCredentials();
      if (checkAuthorizaion()){
        this.loggedIn = true;
      }
    }
  };
  </script>
  
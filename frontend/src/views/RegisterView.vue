<template>
     <v-container fluid>
        
      <v-row justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="elevation-12">
          
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title>{{formType == 'register' ? '用户注册' : '忘记密码'}}</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="form" v-model="valid" lazy-validation>
                <!-- 邮箱字段已移除 -->
                <v-text-field
                  v-if="formType == 'register'"
                  v-model="formData.username"
                  label="用户名"
                  :rules="[rules.required]"
                  required
                  prepend-icon="mdi-account"
                ></v-text-field>
                <v-text-field
                  v-if="formType == 'register'"
                  v-model="formData.password"
                  label="密码"
                  :rules="[rules.required]"
                  required
                  prepend-icon="mdi-lock"
                  type="password"
                ></v-text-field>
                <v-text-field
                  v-if="formType == 'register'"
                  v-model="formData.authCode"
                  label="授权码"
                  :rules="[rules.required]"
                  required
                  prepend-icon="mdi-key"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" :disabled="!valid" @click="submit" block>{{'注册'}}</v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-btn text color="secondary" @click="goToLogin" block>已有账号？去登录</v-btn>
            </v-card-actions>
            <v-alert
                v-if="failedNotify"
                color="error"
                icon="mdi-alert">{{ failedMessage }}</v-alert>
          </v-card>
        </v-col>
      </v-row>
     </v-container>
</template>


<script>
import http from "@/http";
export default {
  name: "RegisterView",
  data() {
    return {
      failedNotify: false,
      failedMessage: "",
      formType: "register", // 默认为注册表单
      formData:{
        // email 字段已移除
        username: "",
        password: "",
        authCode: "", // 添加授权码字段
      },
      valid: false,
      userString: "",
      rules: {
        required: v =>!!v || "必填项不能为空",
      }
    }   
  },
  methods: {
    submit() {
      this.$refs.form.validate()
      if (this.valid) {
        http.post('/auth/register?token='+this.formData.authCode, this.formData)
          .then(response => {
            // 处理注册成功的逻辑
            console.log('注册成功', response.data);
            this.registerSuccess();
          })
          .catch(error => {
            console.error('注册失败', error);
            this.failedNotify = true;
            this.failedMessage = "注册失败"
            setTimeout(() => {
              this.failedNotify = false;
            }, 3000);
          })

      }
    },
    registerSuccess() {
      this.$router.push('/login');
    },
    goToLogin() {
      this.$router.push('/login');
    }
  },
}
</script>
<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-6">
          <v-card-title class="text-h4 text-center">
            服务器资源管理器
          </v-card-title>
          
          <v-card-text class="text-center mt-4">
            <p class="text-subtitle-1">
              版本: {{ commitHash }}
            </p>
            
            <v-divider class="my-4"></v-divider>
            
            <div class="text-body-1 text-left">
              <h3 class="mb-3">版权声明</h3>
              <p>
                Copyright © 2024 服务器资源管理器
              </p>
              <p>
                本软件基于 MIT 许可证发布。您可以自由地使用、修改和分发本软件，但需要在软件的所有副本中包含上述版权声明和本许可声明。
              </p>
              
              <h3 class="mt-6 mb-3">免责声明</h3>
              <p>
                本软件按"原样"提供，不提供任何明示或暗示的保证，包括但不限于适销性和特定用途适用性的保证。在任何情况下，作者或版权持有人均不对任何索赔、损害或其他责任负责。
              </p>
              
              <h3 class="mt-6 mb-3">联系方式</h3>
              <v-list dense>
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>mdi-github</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <a href="https://github.com/phil616/devResMgr" target="_blank" rel="noopener">
                      GitHub 仓库
                    </a>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>mdi-email</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <a href="mailto:phil616@163.com">phil616@163.com</a>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'AboutView',
  data() {
    return {
      commitHash: process.env.CF_PAGES_COMMIT_SHA || '未知版本'
    }
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
  color: inherit;
}
a:hover {
  color: primary;
  text-decoration: underline;
}
</style>
<template>

    <v-navigation-drawer 
        v-model="drawerSwitch"
        app
        temporary
        clipped
        height="100rm"
      >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h6">
            云服务管理
          </v-list-item-title>
          <v-list-item-subtitle>
            个人云服务管理后台
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item-content>
          <v-list-item-title>

            <v-btn @click="drawBack">
              <v-icon>mdi-arrow-left</v-icon>
              收起
            </v-btn>
            
          </v-list-item-title>
        </v-list-item-content>
      <v-divider></v-divider>

      <v-list
        dense
        nav
      >
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title @click="linkto(item.link)">{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    

</template>

<script>
export default {
data: () => ({
    items: [
      { title: '主页', link: '/', icon:'mdi-home' },
      { title: '域名管理', link: '/domain', icon:'mdi-book-open-page-variant'},
      { title: '服务器管理', link: '/instance', icon:'mdi-newspaper' },
      { title: '登录', link: '/login', icon:'mdi-login' },
      { title: '登出', link: '/logout', icon:'mdi-logout' },
      { title: '关于', link: '/about', icon:'mdi-information' },
    ],
  }),
  computed:{
    drawerSwitch : {
      get() {
        return this.$store.state.navigator_drawer;
      },
      set(val) {
        this.$store.dispatch('set_navigator_drawer',val);
      }
    }
  },
  methods: {
    linkto(link) {
      this.$router.replace({path: link});
      this.drawerSwitch = false;
    },
    drawBack() {
      this.$store.dispatch('set_navigator_drawer',false);
    },
    quit() {
        
    }
  }
}
</script>
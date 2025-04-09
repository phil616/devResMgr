import Vue from 'vue';
import Router from 'vue-router';
import store from '@/store';
Vue.use(Router);

const router = new Router({
  mode: 'history',

  routes: [
    {
      path: "/",
      name: "Index",
      redirect: "/home",
    },
    {
      path: "/home",
      name: "Home",
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: "/login",
      name: "Login",
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: "/domain",
      name: "Domain",
      component: () => import('@/views/DomainView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: "/instance",
      name: "Instance",
      component: () => import('@/views/InstanceView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: "/about",
      name: "About",
      component: () => import('@/views/AboutView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: "/logout",
      name: "Logout",
      component: () => import('@/views/LogoutView.vue'),
    },
    {
      path: "/register",
      name: "Register",
      component: () => import('@/views/RegisterView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '*',
      name: 'NotFound',
      component: () => import('@/views/NotFoundView.vue'),
    }
  ]
});



router.beforeEach((to, from, next) => {
  from;
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  // const isAuthenticated = checkAuthorizaion()
  const isAuthenticated = store.state.authenticated
  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next();
  }
})
// 全局后置钩子

router.afterEach((to, from) => {
    to;
    from;
});
export default router;
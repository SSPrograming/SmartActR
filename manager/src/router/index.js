import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'
import Login from '../views/Login.vue'
import Home from '../views/Home'
import Notice from '../views/Notice'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: {name: 'Login'}
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/notice',
    name: 'Notice',
    component: Notice
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  let login = store.state.login
  if (!login) {
    let jwt = localStorage.getItem('jwt')
    if (!jwt) {
      jwt = sessionStorage.getItem('jwt')
    }
    if (jwt) {
      store.commit({
        type: 'login',
        jwt
      })
      login = true
    }
  }
  if (!login && to.name !== 'Login') {
    next({name: 'Login'})
  } else if (login && to.name === 'Login') {
    next({name: 'Home'})
  } else {
    next()
  }
})

export default router

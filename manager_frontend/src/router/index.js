import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'
import Login from '@/views/Login.vue'
import Home from '@/views/Home'
import Notice from '@/views/Notice'
import NotFound from '@/views/NotFound';

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: {name: 'Home'}
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
  },
  {
    path: '/reserve/today',
    name: 'TodayRecord',
    component: NotFound
  },
  {
    path: '/reserve/history',
    name: 'HistoryRecord',
    component: NotFound
  },
  {
    path: '/equipment',
    name: 'Equipment',
    component: NotFound
  },
  {
    path: '/equipment/rules',
    name: 'EquipmentRules',
    component: NotFound
  },
  {
    path: '/instruction',
    name: 'Instruction',
    component: NotFound
  },
  {
    path: '/instruction/editor',
    name: 'InstructionEditor',
    component: NotFound
  },
  {
    path: '/user',
    name: 'User',
    component: NotFound
  },
  {
    path: '/user/feedback',
    name: 'FeedBack',
    component: NotFound
  },
  {
    path: '/404',
    name: 'NotFound',
    component: NotFound
  },
  {
    path: '*',
    redirect: {name: 'NotFound'}
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
  } else {
    next()
  }
})

export default router

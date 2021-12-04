import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    login: false,
    jwt: ''
  },
  mutations: {
    login(state, payload) {
      localStorage.setItem('jwt', payload.jwt)
      sessionStorage.setItem('jwt', payload.jwt)
      state.jwt = payload.jwt
      state.login = true
    },
    logout(state) {
      localStorage.removeItem('jwt')
      sessionStorage.removeItem('jwt')
      state.jwt = ''
      state.login = false
    }
  },
  actions: {},
  modules: {}
})

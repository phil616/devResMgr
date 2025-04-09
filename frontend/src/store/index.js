// store.js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        navigator_drawer: false,  // Navigation drawer state
        authenticated: false,     // Authentication state
        user_info: null,          // User information - load from storage or get from API
        user_token: null          // User token - load from storage or get from API
    },
    mutations: {
        set_user_info(state, value) {
            state.user_info = value
        },
        set_user_token(state, value) {
            state.user_token = value
        },
        set_navigator_drawer(state, value) {
            state.navigator_drawer = value
        },
        set_authenticated(state, value) {
            state.authenticated = value
        },
        toggle_navigator_drawer(state) {
            state.navigator_drawer =!state.navigator_drawer
        }
    },
    actions: {
        set_user_info({ commit }, value) {
            commit('set_user_info', value)
        },
        set_user_token({ commit }, value) {
            commit('set_user_token', value)
        },
        set_navigator_drawer({ commit }, value) {
            commit('set_navigator_drawer', value)
        },
        set_authenticated({ commit }, value) {
            commit('set_authenticated', value)
        },
        toggle_navigator_drawer({ commit }) {
            commit('toggle_navigator_drawer')
        }
    },
    getters: {
        get_navigator_drawer: state => state.navigator_drawer,
        get_authenticated: state => state.authenticated,
        get_user_info: state => state.user_info,
        get_user_token: state => state.user_token
    }
})
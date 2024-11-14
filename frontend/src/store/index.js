// store/index.js
import { createStore } from 'vuex';
import axios from 'axios';
import apiClient from '@/apiClient';

const store = createStore({
  state: {
    user: null,
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },
    SET_TOKENS(state, tokens) {
      state.accessToken = tokens.access_token;
      state.refreshToken = tokens.refresh_token;
      localStorage.setItem('accessToken', tokens.access_token);
      localStorage.setItem('refreshToken', tokens.refresh_token);
    },
    CLEAR_AUTH(state) {
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    },
  },
  actions: {
    fetchUser({ commit }, user) {
      commit('SET_USER', user);
    },
    clearUser({ commit }) {
      commit('CLEAR_USER');
    },
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('/auth/login', credentials);
        commit('SET_TOKENS', response.data);

        // Fetch user data using the access token
        const userResponse = await apiClient.get('/users/me');
        commit('SET_USER', userResponse.data);
      } catch (error) {
        console.error(error);
        throw error;
      }
    },
    logout({ commit }) {
      commit('CLEAR_AUTH');
    },
    async restoreAuth({ commit }) {
      if (localStorage.getItem('accessToken')) {
        try {
          const userResponse = await apiClient.get('/users/me');
          commit('SET_USER', userResponse.data);
        } catch (error) {
          console.error("Failed to restore user session", error);
          commit('CLEAR_AUTH');
        }
      }
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    getUser: (state) => state.user,
  },
});

export default store;

import { login as loginApi } from "@/api/login";
import router from "@/router";
export default {
  namespaced: true,
  state: () => ({
    token: localStorage.getItem("token") || "",
  }),
  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem("token", token);
    },
  },
  actions: {
    login({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        loginApi(userInfo)
          .then((res) => {
            console.log(res.data.token);
            commit("setToken", res.data.token);
            router.replace("/download");
            resolve();
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
    // 退出
    logout({ commit }) {
      commit("setToken", "");
      localStorage.clear();
      router.replace("/login");
    },
  },
};

// import { createStore } from 'vuex'

// export default createStore({
//   state: {
//   },
//   getters: {
//   },
//   mutations: {
//   },
//   actions: {
//   },
//   modules: {
//   }
// })
import { createStore } from "vuex";
import app from "./modules/app";
import getters from "./getters";
export default createStore({
  modules: {
    app,
  },
  getters,
});

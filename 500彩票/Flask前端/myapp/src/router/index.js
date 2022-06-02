import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  {
    path: "/download",
    name: "download",
    component: () => import("../views/DownLoadView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/LoginView.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;

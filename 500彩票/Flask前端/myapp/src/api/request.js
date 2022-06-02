import axios from "axios";
import { ElMessage } from "element-plus";
// 创建请求服务
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 5000,
});

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    if (localStorage.getItem("token"))
      config.headers.Authorization = localStorage.getItem("token");
    return config;
  },
  (error) => {
    return Promise.reject(new Error(error));
  }
);

// 响应请求拦截器
service.interceptors.response.use(
  (response) => {
    const data = response.data[0];
    const meta = response.data[1];
    if (meta.meta[1].statu === "200" || meta.meta[1].statu === "201") {
      return data;
    } else {
      ElMessage.error(meta.meta[0].msg);
      return Promise.reject(new Error(meta.meta[0].msg));
    }
  },
  (error) => {
    error.response && ElMessage.error(error.response.data);
    return Promise.reject(new Error(error.response.data));
  }
);
export default service;

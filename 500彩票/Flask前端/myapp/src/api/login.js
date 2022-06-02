import request from "./request";

export const login = (params) => {
  return request({
    url: "http://localhost:5000/login",
    params,
  });
};

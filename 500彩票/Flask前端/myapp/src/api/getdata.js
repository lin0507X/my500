import request from "./request";

export const getGamesData = (params) => {
  return request({
    url: "http://localhost:5000/index",
    // 参数
    params,
  });
};
export const startSpider = () => {
  return request({
    url: "http://localhost:5000/startspider",
  });
};

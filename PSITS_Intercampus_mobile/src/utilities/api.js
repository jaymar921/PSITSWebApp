import md5 from "md5";

let baseUrl = "http://119.92.196.92:3000";

export const accessKey = md5("PSITS2023");

export const _fetch = (url, method, options) => {
  return fetch(`${baseUrl}${url}`, {
    method: method.toUpperCase(),
    headers: options.headers,
  });
};

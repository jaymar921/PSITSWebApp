import md5 from "md5";

let baseUrl = "API_HERE";
let key = "KEY HERE";
export const accessKey = md5(key);

export const _fetch = (url, method, options) => {
  return fetch(`${baseUrl}${url}`, {
    method: method.toUpperCase(),
    headers: options.headers,
  });
};

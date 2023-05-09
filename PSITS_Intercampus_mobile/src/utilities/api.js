import AsyncStorage from "@react-native-async-storage/async-storage";
import md5 from "md5";

let key = "KEY HERE";
export const accessKey = md5(key);

export const _fetch = async (url, method, options) => {
  const ipadd = await AsyncStorage.getItem("ipadd");
  const port = await AsyncStorage.getItem("port");
  console.log(`${ipadd}:${port}${url}`);
  return fetch(`${ipadd}:${port}${url}`, {
    method: method.toUpperCase(),
    headers: options.headers,
  });
};

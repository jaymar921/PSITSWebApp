import { _fetch } from "../utilities/api";

export default function useLogin() {
  const login = async (idno, pass) => {
    const options = {
      headers: {
        idno: idno,
        pass: pass,
      },
    };

    const res = await _fetch("/api/getacc", "get", options);
    const { message } = await res.json();

    return message === "permitted";
  };

  return { login };
}

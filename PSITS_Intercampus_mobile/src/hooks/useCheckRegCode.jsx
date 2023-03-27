import { accessKey, _fetch } from "../utilities/api";

export default function useCheckRegCode() {
  const checkRegCode = async (code) => {
    const options = {
      headers: {
        "access-key": accessKey,
        regCode: code,
      },
    };
    const res = await (await _fetch("/api/registry", "get", options)).json();

    return res.message === "success" ? res : null;
  };

  return { checkRegCode };
}

import { accessKey, _fetch } from "../utilities/api";

export default function useSendForm() {
  const send = async (info, valueCheck, value) => {
    const flag = valueCheck === "true";

    // check if the same value from before
    if (flag === info.checked && value === info.option) return true;

    const options = {
      headers: {
        "access-key": accessKey,
        regId: info.regId,
        checked: info.checked,
        option: info.option,
      },
    };
    const res = await (await _fetch("/api/registry", "put", options)).json();

    return res.message.toString().includes("success") ? true : false;
  };

  return { send };
}

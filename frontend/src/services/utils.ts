import { toast, TypeOptions } from "react-toastify";

export function generateToast(msg: string, type: TypeOptions) {
  toast(msg, {
    position: toast.POSITION.BOTTOM_CENTER,
    type: type,
  });
}

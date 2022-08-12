import { toast } from "react-toastify";

const TOAST_CONTAINER = {
  position: "top-right",
  autoClose: 5000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  progress: undefined,
  theme: "dark",
};

export const showSuccessNotification = (msg) => {
  toast.success(msg, TOAST_CONTAINER);
};

export const showErrorNotification = (msg) => {
  toast.error(msg, TOAST_CONTAINER);
};

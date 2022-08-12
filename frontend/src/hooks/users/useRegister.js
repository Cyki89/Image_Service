import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import axios from "../../api/axios";

import useAuth from "../useAuth";
import useAxiosFunction from "../axios/useAxiosFunction";

import { showSuccessNotification } from "../../utils/notifications";

const useRegister = () => {
  const [response, error, loading, axiosFetch] = useAxiosFunction();

  const { setUser, csrf, getCsrf } = useAuth();
  const navigate = useNavigate();

  const register = ({ username, password, confirm_password }) => {
    axiosFetch({
      axiosInstance: axios,
      method: "post",
      url: "/auth/register/",
      requestConfig: {
        username,
        password,
        confirm_password,
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf,
        },
      },
    });
  };

  useEffect(() => {
    if (!response) return;

    getCsrf();
    setUser(response);
    navigate("/profile", { replace: true });
    showSuccessNotification(
      "Your account has been created.\nUpdate your profile data"
    );
  }, [response]);

  return [register, error, loading];
};

export default useRegister;

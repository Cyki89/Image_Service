import { useEffect } from "react";
import { axiosPrivate } from "../../api/axios";
import useAuth from "../useAuth";

const useAxiosPrivate = () => {
  const { csrf } = useAuth();

  useEffect(() => {
    const requestIntercept = axiosPrivate.interceptors.request.use(
      async (request) => {
        request.headers["Content-Type"] = "multipart/form-data";
        request.headers["X-CSRFToken"] = csrf;
        return request;
      },
      (error) => {
        Promise.reject(error);
      }
    );

    return () => {
      axiosPrivate.interceptors.request.eject(requestIntercept);
    };
  }, [csrf]);

  return axiosPrivate;
};

export default useAxiosPrivate;

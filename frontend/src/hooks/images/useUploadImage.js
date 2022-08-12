import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import useAxiosFunction from "../axios/useAxiosFunction";
import useAxiosPrivate from "../axios/useAxiosPrivate";

import { showSuccessNotification } from "../../utils/notifications";

const useUploadImage = () => {
  const [response, error, loading, axiosFetch] = useAxiosFunction();
  const axiosPrivate = useAxiosPrivate();

  const navigate = useNavigate();

  const upload = (data) => {
    axiosFetch({
      axiosInstance: axiosPrivate,
      method: "post",
      url: "/images/",
      requestConfig: data,
    });
  };

  useEffect(() => {
    if (!response) return;

    showSuccessNotification("Your image was uploaded");
    navigate("/images");
  }, [response]);

  return [upload, error, loading];
};

export default useUploadImage;

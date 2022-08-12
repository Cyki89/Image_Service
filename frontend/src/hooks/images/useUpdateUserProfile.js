import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import useAuth from "../useAuth";
import useAxiosFunction from "../axios/useAxiosFunction";
import useAxiosPrivate from "../axios/useAxiosPrivate";

import { showSuccessNotification } from "../../utils/notifications";

const useUpdateUserProfile = () => {
  const { user, setUser } = useAuth();
  const [response, error, loading, axiosFetch] = useAxiosFunction();
  const axiosPrivate = useAxiosPrivate();

  const update = (data) => {
    axiosFetch({
      axiosInstance: axiosPrivate,
      method: "put",
      url: `/auth/profile/${user.id}/`,
      requestConfig: data,
    });
  };

  useEffect(() => {
    if (response) {
      setUser(response);
      showSuccessNotification("Your data was updated successfully");
    }
    // eslint-disable-next-line
  }, [response]);

  return [update, error, loading];
};

export default useUpdateUserProfile;

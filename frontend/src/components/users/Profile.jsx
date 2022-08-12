import useAuth from "../../hooks/useAuth";
import useAxios from "../../hooks/axios/useAxios";
import useAxiosPrivate from "../../hooks/axios/useAxiosPrivate";

import ProfileForm from "./ProfileForm";

import LoadingScreen from "../special_screens/LoadingScreen";
import ErrorScreen from "../special_screens/ErrorScreen";

const Profile = () => {
  const { user } = useAuth();
  const axiosPrivate = useAxiosPrivate();

  const [response, error, loading] = useAxios({
    axiosInstance: axiosPrivate,
    method: "get",
    url: `/auth/profile/${user.id}/`,
  });

  const context = () => {
    if (loading) return <LoadingScreen />;
    if (error) return <ErrorScreen>{error.message}</ErrorScreen>;
    return <ProfileForm initialValues={response} />;
  };

  return context();
};

export default Profile;

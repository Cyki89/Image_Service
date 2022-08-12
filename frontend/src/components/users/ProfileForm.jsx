import Form from "../forms/Form";
import useUpdateUserProfile from "../../hooks/images/useUpdateUserProfile";

const INPUTS = [
  {
    title: "Username",
    name: "username",
  },
  {
    title: "First Name",
    name: "first_name",
  },
  {
    title: "Last Name",
    name: "last_name",
  },
  {
    title: "Email",
    name: "email",
  },
];

const ProfileForm = ({ initialValues }) => {
  return (
    <Form
      useFunc={useUpdateUserProfile}
      formData={initialValues}
      formTitle={"User Profile"}
      submitBtnTitle={"Update"}
      inputs={INPUTS}
    />
  );
};

export default ProfileForm;

import Form from "../forms/Form";
import useRegister from "../../hooks/users/useRegister";

const INPUTS = [
  {
    title: "Username",
    name: "username",
  },
  {
    title: "Password",
    name: "password",
    type: "password",
  },

  {
    title: "Confirm Password",
    name: "confirm_password",
    type: "password",
  },
];

const Register = () => {
  return (
    <Form
      useFunc={useRegister}
      formData={{ username: "", password: "", confirm_password: "" }}
      formTitle={"Register Form"}
      submitBtnTitle={"Register"}
      inputs={INPUTS}
    />
  );
};

export default Register;

import Form from "../forms/Form";
import useLogin from "../../hooks/users/useLogin";

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
];

const Login = () => {
  return (
    <Form
      useFunc={useLogin}
      formData={{ username: "", password: "" }}
      formTitle={"Login Form"}
      submitBtnTitle={"Login"}
      inputs={INPUTS}
    />
  );
};

export default Login;

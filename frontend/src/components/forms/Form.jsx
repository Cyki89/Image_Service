import useForm from "./../../hooks/useForm";

import { default as BForm } from "react-bootstrap/Form";

import Input from "../forms/Input";
import SubmitButton from "../forms/SubmitButton";
import ServerErrors from "../forms/ServerErrors";
import NonFieldErrors from "../forms/NonFieldErrors";

const Form = ({ useFunc, formData, formTitle, submitBtnTitle, inputs }) => {
  const [func, error, loading] = useFunc();
  const [data, handleInputChange, handleFileChange] = useForm(formData);

  const handleSubmit = (e) => {
    e.preventDefault();
    func(data);
  };

  return (
    <BForm className={!error ? "form" : "form error"} onSubmit={handleSubmit}>
      <h2 className="form-header">{formTitle}</h2>
      {inputs.map((input) => (
        <Input
          key={input.title}
          title={input.title}
          name={input.name}
          value={data[input.name]}
          error={error?.response?.data[input.name]}
          setValue={
            input.type === "file" ? handleFileChange : handleInputChange
          }
          placeholder={input.title}
          type={input.type || "text"}
        />
      ))}
      <NonFieldErrors error={error} />
      <ServerErrors error={error} />
      <SubmitButton title={submitBtnTitle} loading={loading} />
    </BForm>
  );
};

export default Form;

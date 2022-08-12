import Form from "react-bootstrap/Form";

const Input = ({
  title,
  name,
  value,
  setValue,
  placeholder,
  type = "text",
  style = {},
  error,
}) => {
  return (
    <Form.Group className={!error ? "mb-3" : ""}>
      <Form.Label>{title}</Form.Label>
      <Form.Control
        name={name}
        onChange={setValue}
        defaultValue={value}
        className="form-input"
        placeholder={placeholder}
        type={type}
        isInvalid={error}
        style={style}
      />
      <Form.Control.Feedback type="invalid" className="text-center">
        {error}
      </Form.Control.Feedback>
    </Form.Group>
  );
};

export default Input;

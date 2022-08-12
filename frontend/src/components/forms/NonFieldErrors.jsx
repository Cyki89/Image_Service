import ErrorContainer from "./ErrorContainer";

const NonFieldErrors = ({ error }) => {
  const nonFieldErrors = error?.response?.data?.non_field_errors;
  return nonFieldErrors && <ErrorContainer errors={nonFieldErrors} />;
};

export default NonFieldErrors;

import Button from "react-bootstrap/Button";
import Spinner from "react-bootstrap/Spinner";

const SubmitButton = ({ title = "Submit", disabled = false, loading }) => {
  return (
    <>
      {!loading && (
        <Button
          className="btn-block btn-primary mt-2"
          type="submit"
          disabled={disabled}>
          {title}
        </Button>
      )}
      {loading && (
        <Button className="btn-block btn-primary mt-2" disabled>
          <Spinner animation="border" />
        </Button>
      )}
    </>
  );
};

export default SubmitButton;

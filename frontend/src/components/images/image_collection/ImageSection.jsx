import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

const ImageSection = ({ image }) => {
  return (
    <Row className="m-1">
      <Col className="sm-6">
        <span className="fg-white">Orginal Image: </span>
      </Col>
      <Col>
        <a href={`${image.link}`}>{image.name}</a>
      </Col>
    </Row>
  );
};

export default ImageSection;

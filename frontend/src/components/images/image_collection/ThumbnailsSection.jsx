import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

const ThumbnailsSection = ({ thumbnails }) => {
  return (
    <>
      {thumbnails.map((thumbnail) => (
        <Row className="m-1" key={thumbnail.id}>
          <Col>
            <span className="fg-white">Thumb {thumbnail.height}px: </span>
          </Col>
          <Col>
            <a href={`${thumbnail.link}`}>{thumbnail.name}</a>
          </Col>
        </Row>
      ))}
    </>
  );
};

export default ThumbnailsSection;

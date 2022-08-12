import Card from "react-bootstrap/Card";
import GenerateLinkSection from "./GenerateLinkSection";

import ImageSection from "./ImageSection";

import ThumbnailsSection from "./ThumbnailsSection";

const ImageCollection = ({ collection, user }) => {
  return (
    <Card bg="dark" className="my-3">
      <Card.Header className="fg-white fs-13 text-center bg-third">
        {collection.name}
      </Card.Header>
      {collection.orginal && <ImageSection image={collection.orginal} />}
      {collection.thumbnails && (
        <ThumbnailsSection thumbnails={collection.thumbnails} />
      )}
      <Card.Footer>
        {user.allow_download && (
          <GenerateLinkSection imageId={collection.orginal.id} />
        )}
      </Card.Footer>
    </Card>
  );
};

export default ImageCollection;

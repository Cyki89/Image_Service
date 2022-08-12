import { useRef } from "react";

import Button from "react-bootstrap/Button";

import GenerateLinkModal from "./GenerateLinkModal";

const GenerateLinkSection = ({ imageId }) => {
  const downloadLinkRef = useRef();

  const openModal = () => {
    downloadLinkRef.current.openModal();
  };

  return (
    <>
      <Button
        className="btn-block btn-generate-link"
        type="submit"
        onClick={openModal}>
        Generate Expire Link
      </Button>
      <GenerateLinkModal ref={downloadLinkRef} imageId={imageId} />
    </>
  );
};

export default GenerateLinkSection;

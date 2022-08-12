import { forwardRef, useImperativeHandle, useState } from "react";

import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";
import Stack from "react-bootstrap/Stack";

import useAxiosPrivate from "../../../hooks/axios/useAxiosPrivate";
import useAxiosFunction from "../../../hooks/axios/useAxiosFunction";

import { ReactComponent as CopyBtn } from "../../../copy.svg";

import Input from "../../forms/Input";
import ServerErrors from "../../forms/ServerErrors";
import SubmitButton from "../../forms/SubmitButton";

import { showSuccessNotification } from "../../../utils/notifications";

const GenerateLinkModal = ({ imageId }, ref) => {
  const [show, setShow] = useState(false);
  const [expireTime, setExpireTime] = useState();

  const axiosPrivate = useAxiosPrivate();
  const [response, error, loading, axiosFetch] = useAxiosFunction();

  useImperativeHandle(ref, () => ({
    openModal: () => setShow(true),
  }));

  const handleClose = () => setShow(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    axiosFetch({
      axiosInstance: axiosPrivate,
      method: "post",
      url: "/images/download",
      requestConfig: {
        image_id: imageId,
        expire_time: expireTime,
      },
    });
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(response.download_link);
    showSuccessNotification("Link Was Copied To Clipboard");
  };

  return (
    <Modal
      show={show}
      onHide={handleClose}
      centered
      contentClassName="bg-light-black">
      <Modal.Header closeButton closeVariant="white">
        <Modal.Title className="fg-white">Generate Download Link</Modal.Title>
      </Modal.Header>
      <Form onSubmit={handleSubmit}>
        <Modal.Body className="download-link-modal fs-11">
          <Input
            title=""
            value={expireTime}
            error={error && error.response?.data.expire_time}
            style={{ backgroundColor: "var(--bg-third)" }}
            setValue={(e) => setExpireTime(e.target.value)}
            placeholder="Expire Time"
            type="numeric"
          />
          <ServerErrors error={error} />
          {response && (
            <Stack direction="horizontal">
              <div className="mb-1 mr-1">
                <a className="download-link" href={`${response.download_link}`}>
                  {response.download_link}
                </a>
              </div>
              <CopyBtn className="copy-btn" onClick={copyToClipboard} />
            </Stack>
          )}
        </Modal.Body>
        <Modal.Footer>
          <SubmitButton
            title="Generate Url"
            loading={loading}
            disabled={response}
          />
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default forwardRef(GenerateLinkModal);

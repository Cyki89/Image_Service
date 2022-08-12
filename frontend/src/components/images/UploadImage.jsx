import Form from "../forms/Form";
import useUploadImage from "../../hooks/images/useUploadImage";

const INPUTS = [
  {
    title: "Collection Name",
    name: "name",
  },
  {
    title: "Image",
    name: "image",
    type: "file",
  },
];

const UploadImage = () => {
  return (
    <Form
      useFunc={useUploadImage}
      formData={{ name: "", image: null }}
      formTitle={"Upload Image Form"}
      submitBtnTitle={"Upload"}
      inputs={INPUTS}
    />
  );
};

export default UploadImage;

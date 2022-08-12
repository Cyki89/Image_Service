import useAxiosPrivate from "../../hooks/axios/useAxiosPrivate";
import useAxios from "../../hooks/axios/useAxios";
import useAuth from "../../hooks/useAuth";

import ImageCollection from "./image_collection/ImageCollection";
import LoadingScreen from "../special_screens/LoadingScreen";
import ErrorScreen from "../special_screens/ErrorScreen";

const ImageCollectionList = () => {
  const { user } = useAuth();
  const axiosPrivate = useAxiosPrivate();

  const [response, error, loading] = useAxios({
    axiosInstance: axiosPrivate,
    method: "get",
    url: "/images/",
  });

  return (
    <div>
      {loading && <LoadingScreen />}
      {error && (
        <ErrorScreen>
          Unexpeceted Error: {error.response?.statusText || error.message}
        </ErrorScreen>
      )}
      {response && (
        <>
          <h1 className="fg-white text-center">Image Collection List</h1>
          <div className="collection-container row fs-12">
            {response.map((collection) => (
              <div key={collection.id} className="col w-100">
                <ImageCollection collection={collection} user={user} />
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default ImageCollectionList;

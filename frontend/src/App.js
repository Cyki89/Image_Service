import { BrowserRouter } from "react-router-dom";

import { ApiProvider } from "./context/ApiContext";
import { AuthProvider } from "./context/AuthContext";
import Router from "./components/routes/Router";

import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <BrowserRouter>
      <ToastContainer />
      <ApiProvider>
        <AuthProvider>
          <Router />
        </AuthProvider>
      </ApiProvider>
    </BrowserRouter>
  );
}

export default App;

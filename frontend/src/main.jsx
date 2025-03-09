import React, { Suspense, lazy } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Provider as JotaiRoot } from "jotai";
import { GoogleOAuthProvider } from "@react-oauth/google";

const queryClient = new QueryClient();
const root = ReactDOM.createRoot(document.getElementById("root"));

export const App = lazy(() => import("./App.jsx"));

const Loader = lazy(() => import("./components/Loader.jsx"));

const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID

root.render(
  <React.StrictMode>
    <Suspense fallback={<Loader />}>
      <QueryClientProvider client={queryClient}>
        <JotaiRoot>
          <BrowserRouter>
            <GoogleOAuthProvider clientId={googleClientId}>
              <App />
            </GoogleOAuthProvider>
          </BrowserRouter>
        </JotaiRoot>
      </QueryClientProvider>
    </Suspense>
  </React.StrictMode>
);

import React, { lazy } from 'react';
import { Toaster } from 'react-hot-toast';

const Header = lazy(() => import('./components/Header'));
const RouterList = lazy(() => import('./components/RouterList'));

const App = () => {
  return (
    <>
      <Header />
      <main className="container">
        <div style={{ minHeight: '50px' }}>
          <Toaster
            toastOptions={{
              duration: 5000,
            }}
          />
          <RouterList />
        </div>
      </main>
    </>
  );
};

export default App;
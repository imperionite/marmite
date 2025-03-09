import React from "react";

const Home = () => {
  return (
    <div>
      <header>
        <h1>Welcome to Marmite</h1>
      </header>
      <div className="flex flex-col items-center">
        <section className="bg-gray-100 rounded p-4 mb-4">
          <h2 className="text-lg font-bold mb-2">Introduction</h2>
          <p className="text-gray-600">
            This is a proof-of-concept webpage design to augment and test the
            connectly-api backend REST API project at{" "}
            <a href="https://github.com/imperionite/marmite">
              {" "}
              https://github.com/imperionite/marmite
            </a>
            .
          </p>
        </section>
      </div>
    </div>
  );
};

export default Home;

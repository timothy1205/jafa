if (!process.env.REACT_APP_BACKEND_URL) {
  throw EvalError("Expected a url");
}

const config = {
  backendUrl: process.env.REACT_APP_BACKEND_URL,
};

export default config;

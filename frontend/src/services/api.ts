import axios from "axios";
import config from "./config";

const apiUrl = `${config.backendUrl}/api`;

const api = {
  postList: (subforum?: string) =>
    axios.get(`${apiUrl}/post/list`, { params: { subforum: subforum } }),
};

export default api;

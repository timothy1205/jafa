import axios from "axios";
import config from "./config";

const apiUrl = `${config.backendUrl}/api`;

const api = {
  postList: (subforum?: string) =>
    axios.get(`${apiUrl}/post/list`, { params: { subforum: subforum } }),
  vote: (post_id: string, is_like: boolean) => {
    const formData = new FormData();
    formData.append("post_id", post_id);
    formData.append("is_like", is_like.toString());
    return axios.post(`${apiUrl}/post/vote`, formData);
  }
};

export default api;

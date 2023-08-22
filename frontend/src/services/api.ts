import axios from "axios";
import config from "./config";
import { generateToast } from "./utils";

interface APIError {
  type: string;
  error: string;
}

const apiUrl = `${config.backendUrl}/api`;

const api = {
  postList: (subforum?: string) =>
    axios.get(`${apiUrl}/post/list`, { params: { subforum: subforum } }),
  vote: (post_id: string, is_like: boolean) => {
    const formData = new FormData();
    formData.append("post_id", post_id);
    formData.append("is_like", is_like.toString());
    return axios.post(`${apiUrl}/post/vote`, formData);
  },

  handleError: (err: unknown) => {
    if (!axios.isAxiosError(err)) {
      console.error(err);
      return;
    }

    const responseData = err.response?.data;
    if (responseData) {
      const apiError = responseData as APIError;
      const errMessage = `[${apiError.type}]: ${apiError.error}`;
      console.error(errMessage);
      generateToast(errMessage, "error");
    }
  },
};

export default api;

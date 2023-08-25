import axios from "axios";
import config from "./config";
import { generateToast } from "./utils";

interface APIError {
  type: string;
  error: string;
}

export interface APIResponse {
  msg: string;
}

const apiUrl = `${config.backendUrl}/api`;

export function postList(subforum?: string) {
  return axios.get(`${apiUrl}/post/list`, { params: { subforum: subforum } });
}

export function vote(post_id: string, is_like: boolean) {
  const formData = new FormData();
  formData.append("post_id", post_id);
  formData.append("is_like", is_like.toString());
  return axios.post(`${apiUrl}/post/vote`, formData);
}

export function login(username: string, password: string) {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);
  return axios.post(`${apiUrl}/user/login`, formData, {
    withCredentials: true,
  });
}

export function register(username: string, password: string) {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);
  return axios.post(`${apiUrl}/user/register`, formData, {
    withCredentials: true,
  });
}

export function getCurrentUser() {
  return axios.get(`${apiUrl}/user/get`, { withCredentials: true });
}

export function handleError(err: unknown) {
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
}

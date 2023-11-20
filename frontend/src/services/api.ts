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
const routeUrl = `${config.backendUrl}/route`;

export function getRoot(page: number = 0) {
  return axios.get(`${routeUrl}/root/${page}`);
}

export function getSubform(subforum: string, page: number = 0) {
  return axios.get(`${routeUrl}/subforum/${subforum}/${page}`);
}

export function vote(post_id: string, is_like: boolean) {
  const formData = new FormData();
  formData.append("post_id", post_id);
  formData.append("is_like", is_like.toString());
  return axios.post(`${apiUrl}/post/vote`, formData, { withCredentials: true });
}

export function login(username: string, password: string) {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);
  return axios.post(`${apiUrl}/user/login`, formData, {
    withCredentials: true,
  });
}

export function logout() {
  return axios.get(`${apiUrl}/user/logout`, { withCredentials: true });
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

export function createSubforum(title: string, description: string) {
  const formData = new FormData();
  formData.append("title", title);
  formData.append("description", description);
  return axios.post(`${apiUrl}/subforum/create`, formData, {
    withCredentials: true,
  });
}

export function createPost(subforum: string, title: string, body: string) {
  const formData = new FormData();
  formData.append("subforum", subforum);
  formData.append("title", title);
  formData.append("body", body);
  return axios.post(`${apiUrl}/post/create`, formData, {
    withCredentials: true,
  });
}

export function handleError(err: unknown) {
  if (!axios.isAxiosError(err)) {
    if (err instanceof Error) generateToast(err.message, "error");
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

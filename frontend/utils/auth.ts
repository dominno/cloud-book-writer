
import axios from 'axios';
import { NextRouter } from 'next/router';

const API_URL = 'http://127.0.0.1:8000/api';

export const loginUser = async (userData: { username: string, password: string }) => {
  try {
    const response = await axios.post(`${API_URL}/login/`, userData);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
    }
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const logoutUser = (router: NextRouter) => {
  localStorage.removeItem('token');
  router.push('/login');
};

export const isAuthenticated = () => {
  const token = localStorage.getItem('token');
  return token != null;
};


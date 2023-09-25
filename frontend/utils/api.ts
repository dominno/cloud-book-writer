import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/register/`, userData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const loginUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/login/`, userData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createSection = async (sectionData) => {
  try {
    const response = await axios.post(`${API_URL}/sections/`, sectionData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getSection = async (sectionId) => {
  try {
    const response = await axios.get(`${API_URL}/sections/${sectionId}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateSection = async (sectionId, sectionData) => {
  try {
    const response = await axios.put(`${API_URL}/sections/${sectionId}/`, sectionData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteSection = async (sectionId) => {
  try {
    const response = await axios.delete(`${API_URL}/sections/${sectionId}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getRootSections = async (page) => {
  try {
    const response = await axios.get(`${API_URL}/sections/root_list/?page=${page}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};


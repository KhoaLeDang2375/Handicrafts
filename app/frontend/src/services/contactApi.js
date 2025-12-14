import { apiCall } from './api';

export const sendContact = async (data) => {
  // data bao gồm: name, email, content
  return await apiCall('/contact/', {
    method: 'POST',
    body: JSON.stringify(data)
  });
};
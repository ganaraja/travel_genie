import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const travelAgentService = {
  /**
   * Get travel recommendation from the agent
   * @param {string} query - User's travel query
   * @param {string} userId - User ID for profile retrieval
   * @returns {Promise<Object>} Recommendation object
   */
  async getRecommendation(query, userId = 'user_123') {
    try {
      // In production, this would call the ADK agent API
      // For now, we'll simulate the response structure
      const response = await axios.post(`${API_BASE_URL}/api/recommendation`, {
        query,
        user_id: userId,
      });

      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(error.response.data.error || 'Failed to get recommendation');
      } else if (error.request) {
        throw new Error('Unable to connect to the server. Please make sure the backend is running.');
      } else {
        throw new Error(error.message || 'An unexpected error occurred');
      }
    }
  },
};

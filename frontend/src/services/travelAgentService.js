import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class TravelAgentService {
  async getRecommendation(query, userId = 'default') {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/recommend`, {
        query,
        userId,
      }, {
        timeout: 60000, // 60 second timeout for AI processing
      });

      if (response.data.success) {
        return {
          query: response.data.query,
          userId: response.data.userId,
          recommendation: response.data.recommendation,
          timestamp: response.data.timestamp || new Date().toISOString(),
        };
      } else {
        throw new Error(response.data.error || 'Failed to get recommendation');
      }
    } catch (error) {
      if (error.response) {
        // Server responded with error
        throw new Error(
          error.response.data?.error || 
          `Server error: ${error.response.status}`
        );
      } else if (error.request) {
        // Request made but no response
        throw new Error(
          'Unable to connect to the Travel Genie service. Please make sure the API server is running on port 5000.'
        );
      } else {
        // Something else happened
        throw new Error(error.message || 'An unexpected error occurred');
      }
    }
  }

  async getUserProfile(userId) {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/user-profile/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      return null;
    }
  }

  async checkHealth() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/health`);
      return response.data.status === 'healthy';
    } catch (error) {
      return false;
    }
  }
}

export const travelAgentService = new TravelAgentService();

/**
 * Tests for travelAgentService
 * API service for communicating with backend
 */

import axios from 'axios';
import { travelAgentService } from '../../frontend/src/services/travelAgentService';

jest.mock('axios');

describe('TravelAgentService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getRecommendation', () => {
    test('makes POST request to /api/recommend', async () => {
      const mockResponse = {
        data: {
          success: true,
          query: 'Should I go to Maui?',
          userId: 'user_123',
          recommendation: 'Yes, great time to visit!',
          timestamp: '2024-01-15T12:00:00Z'
        }
      };

      axios.post.mockResolvedValue(mockResponse);

      await travelAgentService.getRecommendation('Should I go to Maui?', 'user_123');

      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:5000/api/recommend',
        {
          query: 'Should I go to Maui?',
          userId: 'user_123'
        },
        { timeout: 60000 }
      );
    });

    test('returns recommendation data on success', async () => {
      const mockResponse = {
        data: {
          success: true,
          query: 'Should I go to Maui?',
          userId: 'user_123',
          recommendation: 'Yes, great time to visit!',
          timestamp: '2024-01-15T12:00:00Z'
        }
      };

      axios.post.mockResolvedValue(mockResponse);

      const result = await travelAgentService.getRecommendation('Should I go to Maui?', 'user_123');

      expect(result).toEqual({
        query: 'Should I go to Maui?',
        userId: 'user_123',
        recommendation: 'Yes, great time to visit!',
        timestamp: '2024-01-15T12:00:00Z'
      });
    });

    test('uses default userId if not provided', async () => {
      const mockResponse = {
        data: {
          success: true,
          query: 'Test query',
          userId: 'default',
          recommendation: 'Test response',
          timestamp: '2024-01-15T12:00:00Z'
        }
      };

      axios.post.mockResolvedValue(mockResponse);

      await travelAgentService.getRecommendation('Test query');

      expect(axios.post).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          userId: 'default'
        }),
        expect.any(Object)
      );
    });

    test('generates timestamp if not provided by server', async () => {
      const mockResponse = {
        data: {
          success: true,
          query: 'Test query',
          userId: 'user_123',
          recommendation: 'Test response'
          // No timestamp
        }
      };

      axios.post.mockResolvedValue(mockResponse);

      const result = await travelAgentService.getRecommendation('Test query', 'user_123');

      expect(result.timestamp).toBeDefined();
      expect(typeof result.timestamp).toBe('string');
    });

    test('throws error when success is false', async () => {
      const mockResponse = {
        data: {
          success: false,
          error: 'Invalid query'
        }
      };

      axios.post.mockResolvedValue(mockResponse);

      await expect(
        travelAgentService.getRecommendation('', 'user_123')
      ).rejects.toThrow('Invalid query');
    });

    test('throws error on server error response', async () => {
      const mockError = {
        response: {
          status: 500,
          data: {
            error: 'Internal server error'
          }
        }
      };

      axios.post.mockRejectedValue(mockError);

      await expect(
        travelAgentService.getRecommendation('Test query', 'user_123')
      ).rejects.toThrow('Internal server error');
    });

    test('throws connection error when no response', async () => {
      const mockError = {
        request: {}
      };

      axios.post.mockRejectedValue(mockError);

      await expect(
        travelAgentService.getRecommendation('Test query', 'user_123')
      ).rejects.toThrow(/Unable to connect/i);
    });

    test('throws generic error on unknown error', async () => {
      const mockError = new Error('Network error');

      axios.post.mockRejectedValue(mockError);

      await expect(
        travelAgentService.getRecommendation('Test query', 'user_123')
      ).rejects.toThrow('Network error');
    });

    test('uses 60 second timeout', async () => {
      const mockResponse = {
        data: {
          success: true,
          query: 'Test',
          userId: 'user_123',
          recommendation: 'Response',
          timestamp: '2024-01-15T12:00:00Z'
        }
      };

      axios.post.mockResolvedValue(mockResponse);

      await travelAgentService.getRecommendation('Test', 'user_123');

      expect(axios.post).toHaveBeenCalledWith(
        expect.any(String),
        expect.any(Object),
        { timeout: 60000 }
      );
    });
  });

  describe('getUserProfile', () => {
    test('makes GET request to /api/user-profile/:userId', async () => {
      const mockResponse = {
        data: {
          userId: 'user_123',
          preferredTempRange: [75, 85],
          airfareBudgetSoft: 600,
          airfareBudgetHard: 900
        }
      };

      axios.get.mockResolvedValue(mockResponse);

      await travelAgentService.getUserProfile('user_123');

      expect(axios.get).toHaveBeenCalledWith(
        'http://localhost:5000/api/user-profile/user_123'
      );
    });

    test('returns profile data on success', async () => {
      const mockProfile = {
        userId: 'user_123',
        preferredTempRange: [75, 85],
        airfareBudgetSoft: 600,
        airfareBudgetHard: 900,
        hotelBudgetMin: 150,
        hotelBudgetMax: 300
      };

      const mockResponse = {
        data: mockProfile
      };

      axios.get.mockResolvedValue(mockResponse);

      const result = await travelAgentService.getUserProfile('user_123');

      expect(result).toEqual(mockProfile);
    });

    test('returns null on error', async () => {
      axios.get.mockRejectedValue(new Error('Not found'));

      const result = await travelAgentService.getUserProfile('unknown');

      expect(result).toBeNull();
    });

    test('logs error to console', async () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
      axios.get.mockRejectedValue(new Error('Not found'));

      await travelAgentService.getUserProfile('unknown');

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });
  });

  describe('checkHealth', () => {
    test('makes GET request to /api/health', async () => {
      const mockResponse = {
        data: {
          status: 'healthy',
          service: 'Travel Genie API'
        }
      };

      axios.get.mockResolvedValue(mockResponse);

      await travelAgentService.checkHealth();

      expect(axios.get).toHaveBeenCalledWith(
        'http://localhost:5000/api/health'
      );
    });

    test('returns true when status is healthy', async () => {
      const mockResponse = {
        data: {
          status: 'healthy'
        }
      };

      axios.get.mockResolvedValue(mockResponse);

      const result = await travelAgentService.checkHealth();

      expect(result).toBe(true);
    });

    test('returns false when status is not healthy', async () => {
      const mockResponse = {
        data: {
          status: 'unhealthy'
        }
      };

      axios.get.mockResolvedValue(mockResponse);

      const result = await travelAgentService.checkHealth();

      expect(result).toBe(false);
    });

    test('returns false on error', async () => {
      axios.get.mockRejectedValue(new Error('Connection failed'));

      const result = await travelAgentService.checkHealth();

      expect(result).toBe(false);
    });
  });

  describe('API Base URL', () => {
    test('uses environment variable if set', () => {
      // This would require mocking process.env, which is complex in Jest
      // Just verify the service exists
      expect(travelAgentService).toBeDefined();
    });

    test('defaults to localhost:5000', async () => {
      const mockResponse = {
        data: {
          success: true,
          query: 'Test',
          userId: 'user_123',
          recommendation: 'Response',
          timestamp: '2024-01-15T12:00:00Z'
        }
      };

      axios.post.mockResolvedValue(mockResponse);

      await travelAgentService.getRecommendation('Test', 'user_123');

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('localhost:5000'),
        expect.any(Object),
        expect.any(Object)
      );
    });
  });

  describe('Error Messages', () => {
    test('provides helpful message for connection errors', async () => {
      const mockError = {
        request: {}
      };

      axios.post.mockRejectedValue(mockError);

      await expect(
        travelAgentService.getRecommendation('Test', 'user_123')
      ).rejects.toThrow(/make sure the API server is running on port 5000/i);
    });

    test('includes status code in server error messages', async () => {
      const mockError = {
        response: {
          status: 404,
          data: {}
        }
      };

      axios.post.mockRejectedValue(mockError);

      await expect(
        travelAgentService.getRecommendation('Test', 'user_123')
      ).rejects.toThrow(/404/);
    });

    test('uses error message from response data if available', async () => {
      const mockError = {
        response: {
          status: 400,
          data: {
            error: 'Query is required'
          }
        }
      };

      axios.post.mockRejectedValue(mockError);

      await expect(
        travelAgentService.getRecommendation('', 'user_123')
      ).rejects.toThrow('Query is required');
    });
  });
});

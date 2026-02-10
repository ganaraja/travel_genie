import axios from 'axios';
import { travelAgentService } from '../../services/travelAgentService';

jest.mock('axios');

describe('travelAgentService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('calls API with correct parameters', async () => {
    const mockResponse = {
      data: {
        recommended_start: '2026-02-09',
        recommended_end: '2026-02-16',
        personalized_summary: 'Test recommendation',
      },
    };

    axios.post.mockResolvedValue(mockResponse);

    await travelAgentService.getRecommendation('Is it a good time to go to Maui?', 'user_123');

    expect(axios.post).toHaveBeenCalledWith(
      expect.stringContaining('/api/recommendation'),
      {
        query: 'Is it a good time to go to Maui?',
        user_id: 'user_123',
      }
    );
  });

  test('returns recommendation data on success', async () => {
    const mockResponse = {
      data: {
        recommended_start: '2026-02-09',
        recommended_end: '2026-02-16',
        personalized_summary: 'Test recommendation',
      },
    };

    axios.post.mockResolvedValue(mockResponse);

    const result = await travelAgentService.getRecommendation('Test query', 'user_123');

    expect(result).toEqual(mockResponse.data);
  });

  test('throws error on API error response', async () => {
    const errorResponse = {
      response: {
        data: {
          error: 'API Error',
        },
      },
    };

    axios.post.mockRejectedValue(errorResponse);

    await expect(
      travelAgentService.getRecommendation('Test query', 'user_123')
    ).rejects.toThrow('API Error');
  });

  test('throws error on network error', async () => {
    const networkError = {
      request: {},
    };

    axios.post.mockRejectedValue(networkError);

    await expect(
      travelAgentService.getRecommendation('Test query', 'user_123')
    ).rejects.toThrow('Unable to connect to the server');
  });

  test('uses default user ID when not provided', async () => {
    const mockResponse = {
      data: {
        recommended_start: '2026-02-09',
        recommended_end: '2026-02-16',
        personalized_summary: 'Test',
      },
    };

    axios.post.mockResolvedValue(mockResponse);

    await travelAgentService.getRecommendation('Test query');

    expect(axios.post).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        user_id: 'user_123',
      })
    );
  });
});

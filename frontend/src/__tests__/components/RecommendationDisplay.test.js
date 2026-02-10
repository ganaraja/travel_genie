import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import RecommendationDisplay from '../../components/RecommendationDisplay';

describe('RecommendationDisplay', () => {
  const mockRecommendation = {
    recommended_start: '2026-02-09',
    recommended_end: '2026-02-16',
    primary_reasoning: [
      {
        factor: 'weather',
        assessment: 'Perfect temperature match',
        positive: true,
      },
      {
        factor: 'price',
        assessment: 'Within budget',
        positive: true,
      },
    ],
    personalized_summary: 'Based on your preferences, I recommend traveling from February 9 to February 16.',
    alternative_options: [
      ['2026-02-10', '2026-02-17', 'Alternative dates with similar conditions'],
    ],
    rejected_periods: [
      ['2026-02-16', '2026-02-22', 'Storm risk - moderate severity'],
    ],
  };

  test('renders recommendation header with dates', () => {
    render(<RecommendationDisplay recommendation={mockRecommendation} />);

    expect(screen.getByText(/your personalized recommendation/i)).toBeInTheDocument();
    expect(screen.getByText(/recommended travel dates/i)).toBeInTheDocument();
  });

  test('renders primary reasoning', () => {
    render(<RecommendationDisplay recommendation={mockRecommendation} />);

    expect(screen.getByText(/why this recommendation fits you/i)).toBeInTheDocument();
    expect(screen.getByText(/weather:/i)).toBeInTheDocument();
    expect(screen.getByText(/perfect temperature match/i)).toBeInTheDocument();
    expect(screen.getByText(/price:/i)).toBeInTheDocument();
    expect(screen.getByText(/within budget/i)).toBeInTheDocument();
  });

  test('renders personalized summary', () => {
    render(<RecommendationDisplay recommendation={mockRecommendation} />);

    expect(screen.getByText(/summary/i)).toBeInTheDocument();
    expect(screen.getByText(/based on your preferences/i)).toBeInTheDocument();
  });

  test('renders alternative options when provided', () => {
    render(<RecommendationDisplay recommendation={mockRecommendation} />);

    expect(screen.getByText(/alternative options/i)).toBeInTheDocument();
    expect(screen.getByText(/alternative dates with similar conditions/i)).toBeInTheDocument();
  });

  test('renders rejected periods when provided', () => {
    render(<RecommendationDisplay recommendation={mockRecommendation} />);

    expect(screen.getByText(/why other periods were rejected/i)).toBeInTheDocument();
    expect(screen.getByText(/storm risk/i)).toBeInTheDocument();
  });

  test('handles recommendation without alternative options', () => {
    const recommendationWithoutAlternatives = {
      ...mockRecommendation,
      alternative_options: [],
    };

    render(<RecommendationDisplay recommendation={recommendationWithoutAlternatives} />);

    expect(screen.queryByText(/alternative options/i)).not.toBeInTheDocument();
  });

  test('handles recommendation without rejected periods', () => {
    const recommendationWithoutRejected = {
      ...mockRecommendation,
      rejected_periods: [],
    };

    render(<RecommendationDisplay recommendation={recommendationWithoutRejected} />);

    expect(screen.queryByText(/why other periods were rejected/i)).not.toBeInTheDocument();
  });

  test('handles null recommendation gracefully', () => {
    const { container } = render(<RecommendationDisplay recommendation={null} />);
    expect(container.firstChild).toBeNull();
  });

  test('formats dates correctly', () => {
    render(<RecommendationDisplay recommendation={mockRecommendation} />);

    // Check that dates are formatted (not raw ISO strings)
    const dateElements = screen.getAllByText(/february/i);
    expect(dateElements.length).toBeGreaterThan(0);
  });
});

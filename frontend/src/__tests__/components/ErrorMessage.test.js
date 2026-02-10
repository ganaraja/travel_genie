import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ErrorMessage from '../../components/ErrorMessage';

describe('ErrorMessage', () => {
  test('renders error message', () => {
    const errorMessage = 'An error occurred';
    render(<ErrorMessage message={errorMessage} />);

    expect(screen.getByTestId('error-message')).toBeInTheDocument();
    expect(screen.getByText(/error/i)).toBeInTheDocument();
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });

  test('displays custom error message', () => {
    const customMessage = 'Failed to connect to server';
    render(<ErrorMessage message={customMessage} />);

    expect(screen.getByText(customMessage)).toBeInTheDocument();
  });

  test('has error icon', () => {
    const { container } = render(<ErrorMessage message="Test error" />);
    const icon = container.querySelector('.error-icon');
    expect(icon).toBeInTheDocument();
  });
});

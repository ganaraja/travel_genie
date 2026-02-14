import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import TravelQueryForm from '../../components/TravelQueryForm';

describe('TravelQueryForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  test('renders form elements', () => {
    render(<TravelQueryForm onSubmit={mockOnSubmit} disabled={false} />);

    expect(screen.getByLabelText(/traveler profile/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/your travel question/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /get travel recommendation/i })).toBeInTheDocument();
  });

  test('allows user to select user ID', () => {
    render(<TravelQueryForm onSubmit={mockOnSubmit} disabled={false} />);

    const select = screen.getByLabelText(/traveler profile/i);
    expect(select).toHaveValue('user_123');

    fireEvent.change(select, { target: { value: 'default' } });
    expect(select).toHaveValue('default');
  });

  test('allows user to enter query', () => {
    render(<TravelQueryForm onSubmit={mockOnSubmit} disabled={false} />);

    const textarea = screen.getByLabelText(/your travel question/i);
    fireEvent.change(textarea, { target: { value: 'Is it a good time to go to Maui?' } });

    expect(textarea).toHaveValue('Is it a good time to go to Maui?');
  });

  test('calls onSubmit with query and userId when form is submitted', () => {
    render(<TravelQueryForm onSubmit={mockOnSubmit} disabled={false} />);

    const textarea = screen.getByLabelText(/your travel question/i);
    const submitButton = screen.getByRole('button', { name: /get travel recommendation/i });

    fireEvent.change(textarea, { target: { value: 'Is it a good time to go to Maui?' } });
    fireEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
    expect(mockOnSubmit).toHaveBeenCalledWith('Is it a good time to go to Maui?', 'user_123');
  });

  test('prevents submission when query is empty', () => {
    render(<TravelQueryForm onSubmit={mockOnSubmit} disabled={false} />);

    const submitButton = screen.getByRole('button', { name: /get travel recommendation/i });
    expect(submitButton).toBeDisabled();
  });

  test('disables form elements when disabled prop is true', () => {
    render(<TravelQueryForm onSubmit={mockOnSubmit} disabled={true} />);

    const select = screen.getByLabelText(/traveler profile/i);
    const textarea = screen.getByLabelText(/your travel question/i);
    const submitButton = screen.getByRole('button', { name: /getting your recommendation/i });

    expect(select).toBeDisabled();
    expect(textarea).toBeDisabled();
    expect(submitButton).toBeDisabled();
  });

  test('trims whitespace from query before submission', () => {
    render(<TravelQueryForm onSubmit={mockOnSubmit} disabled={false} />);

    const textarea = screen.getByLabelText(/your travel question/i);
    const submitButton = screen.getByRole('button', { name: /get travel recommendation/i });

    fireEvent.change(textarea, { target: { value: '  Is it a good time to go to Maui?  ' } });
    fireEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledWith('Is it a good time to go to Maui?', 'user_123');
  });
});

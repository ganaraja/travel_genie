"""Tests for visa requirement checking functionality."""

import pytest
from api_server import check_visa_requirements


class TestVisaRequirements:
    """Tests for visa requirement checking based on citizenship."""

    def test_usa_to_usa_domestic(self):
        """Test USA citizen traveling within USA (domestic)."""
        result = check_visa_requirements("USA", "USA")
        
        assert result["required"] is False
        assert result["type"] == "domestic"
        assert result["citizenship"] == "USA"
        assert result["country"] == "USA"

    def test_usa_to_france_visa_waiver(self):
        """Test USA citizen traveling to France (visa waiver)."""
        result = check_visa_requirements("France", "USA")
        
        assert result["required"] is False
        assert result["type"] == "visa_waiver"
        assert result["max_stay"] == "90 days"
        assert result["citizenship"] == "USA"
        assert result["country"] == "France"

    def test_usa_to_japan_visa_waiver(self):
        """Test USA citizen traveling to Japan (visa waiver)."""
        result = check_visa_requirements("Japan", "USA")
        
        assert result["required"] is False
        assert result["type"] == "visa_waiver"
        assert result["max_stay"] == "90 days"

    def test_usa_to_indonesia_visa_on_arrival(self):
        """Test USA citizen traveling to Indonesia (visa on arrival)."""
        result = check_visa_requirements("Indonesia", "USA")
        
        assert result["required"] is True
        assert result["type"] == "visa_on_arrival"
        assert result["processing_time"] == "On arrival"
        assert result["cost"] == "$35"
        assert result["max_stay"] == "30 days"

    def test_usa_to_china_full_visa(self):
        """Test USA citizen traveling to China (full visa required)."""
        result = check_visa_requirements("China", "USA")
        
        assert result["required"] is True
        assert result["type"] == "visa"
        assert result["processing_time"] == "4-10 business days"
        assert result["cost"] == "$140"

    def test_usa_to_india_evisa(self):
        """Test USA citizen traveling to India (e-visa)."""
        result = check_visa_requirements("India", "USA")
        
        assert result["required"] is True
        assert result["type"] == "e-visa"
        assert result["processing_time"] == "2-4 business days"
        assert result["cost"] == "$25-100"

    def test_india_to_usa_full_visa(self):
        """Test India citizen traveling to USA (full visa required)."""
        result = check_visa_requirements("USA", "India")
        
        assert result["required"] is True
        assert result["type"] == "visa"
        assert result["processing_time"] == "3-5 weeks"
        assert result["cost"] == "$160"

    def test_india_to_france_schengen_visa(self):
        """Test India citizen traveling to France (Schengen visa)."""
        result = check_visa_requirements("France", "India")
        
        assert result["required"] is True
        assert result["type"] == "schengen_visa"
        assert result["processing_time"] == "15 days"
        assert result["cost"] == "€80"

    def test_india_to_japan_full_visa(self):
        """Test India citizen traveling to Japan (full visa required)."""
        result = check_visa_requirements("Japan", "India")
        
        assert result["required"] is True
        assert result["type"] == "visa"
        assert result["processing_time"] == "5-7 business days"
        assert result["cost"] == "$30"

    def test_india_to_indonesia_visa_free(self):
        """Test India citizen traveling to Indonesia (visa free)."""
        result = check_visa_requirements("Indonesia", "India")
        
        assert result["required"] is False
        assert result["type"] == "visa_free"
        assert result["max_stay"] == "30 days"

    def test_uk_to_usa_esta(self):
        """Test UK citizen traveling to USA (ESTA required)."""
        result = check_visa_requirements("USA", "UK")
        
        assert result["required"] is False
        assert result["type"] == "esta"
        assert result["processing_time"] == "72 hours"
        assert result["cost"] == "$21"
        assert result["max_stay"] == "90 days"

    def test_uk_to_france_visa_free(self):
        """Test UK citizen traveling to France (visa free)."""
        result = check_visa_requirements("France", "UK")
        
        assert result["required"] is False
        assert result["type"] == "visa_free"
        assert result["max_stay"] == "90 days"

    def test_uk_to_japan_visa_waiver(self):
        """Test UK citizen traveling to Japan (visa waiver)."""
        result = check_visa_requirements("Japan", "UK")
        
        assert result["required"] is False
        assert result["type"] == "visa_waiver"
        assert result["max_stay"] == "90 days"

    def test_uk_to_indonesia_visa_free(self):
        """Test UK citizen traveling to Indonesia (visa free)."""
        result = check_visa_requirements("Indonesia", "UK")
        
        assert result["required"] is False
        assert result["type"] == "visa_free"
        assert result["max_stay"] == "30 days"

    def test_unknown_combination_defaults_to_visa_required(self):
        """Test unknown citizenship/destination combination defaults to visa required."""
        result = check_visa_requirements("Brazil", "Canada")
        
        assert result["required"] is True
        assert result["type"] == "visa"
        assert result["processing_time"] == "Unknown - please check embassy"
        assert result["cost"] == "Varies"
        assert "note" in result

    def test_visa_result_structure(self):
        """Test that visa result has all required fields."""
        result = check_visa_requirements("France", "USA")
        
        assert "required" in result
        assert "type" in result
        assert "processing_time" in result
        assert "cost" in result
        assert "country" in result
        assert "citizenship" in result
        assert isinstance(result["required"], bool)
        assert isinstance(result["type"], str)

import pytest
import json
from datetime import datetime
from backend.chains.output_parser import parse_research_output
from backend.models.schemas import ResearchBrief


def test_parse_valid_research_brief():
    """Test that a valid ResearchBrief JSON is parsed correctly."""
    # Load sample JSON
    with open("sample_outputs/quantum_computing.json", "r") as f:
        sample_data = json.load(f)
    
    # Convert to JSON string
    json_string = json.dumps(sample_data)
    
    # Parse
    result = parse_research_output(json_string)
    
    # Assertions
    assert isinstance(result, ResearchBrief)
    assert result.topic == "Quantum Computing Breakthroughs in 2024"
    assert len(result.key_findings) >= 3
    assert len(result.sources) >= 3
    assert len(result.controversies) >= 2
    assert len(result.expert_opinions) >= 2
    assert result.conclusion is not None and len(result.conclusion) > 0


def test_parse_with_slightly_malformed_json():
    """Test that OutputFixingParser handles malformed JSON and returns valid ResearchBrief."""
    # Create slightly malformed JSON (missing comma, extra bracket, etc.)
    malformed_json = """{
    "topic": "Test Topic",
    "overview": "A test overview",
    "key_findings": [
        {"finding": "Finding 1", "source_url": "https://example.com"}
        {"finding": "Finding 2", "source_url": "https://example.com"}
    ],
    "controversies": ["Controversy 1", "Controversy 2"],
    "expert_opinions": ["Opinion 1", "Opinion 2"],
    "conclusion": "Test conclusion",
    "sources": [
        {"title": "Source 1", "url": "https://example.com", "date": "2024-01-01"}
    ],
    "generated_at": "2024-12-15T10:30:45.123456"
    }"""
    
    # Parse (should auto-correct)
    result = parse_research_output(malformed_json)
    
    # Assertions
    assert isinstance(result, ResearchBrief)
    assert result.topic == "Test Topic"
    assert result.overview == "A test overview"


def test_parse_multiple_sample_outputs():
    """Test parsing all sample output files."""
    sample_files = [
        "sample_outputs/quantum_computing.json",
        "sample_outputs/ai_healthcare.json",
        "sample_outputs/climate_change.json",
    ]
    
    for filepath in sample_files:
        with open(filepath, "r") as f:
            sample_data = json.load(f)
        
        json_string = json.dumps(sample_data)
        result = parse_research_output(json_string)
        
        # Validate structure
        assert isinstance(result, ResearchBrief)
        assert result.topic
        assert result.overview
        assert isinstance(result.key_findings, list)
        assert isinstance(result.sources, list)
        assert isinstance(result.controversies, list)
        assert isinstance(result.expert_opinions, list)
        assert result.conclusion


def test_research_brief_schema_validation():
    """Test that ResearchBrief schema validation works correctly."""
    # Valid data
    valid_data = {
        "topic": "Test",
        "overview": "Overview",
        "key_findings": [
            {"finding": "Finding text", "source_url": "https://example.com"}
        ],
        "controversies": ["Controversy 1"],
        "expert_opinions": ["Opinion 1"],
        "conclusion": "Conclusion text",
        "sources": [
            {"title": "Source", "url": "https://example.com", "date": "2024-01-01"}
        ],
        "generated_at": "2024-12-15T10:30:45.123456",
    }
    
    # Should create without error
    brief = ResearchBrief(**valid_data)
    assert brief.topic == "Test"
    assert len(brief.key_findings) == 1


def test_research_brief_default_values():
    """Test that ResearchBrief handles defaults correctly."""
    # Minimal data
    minimal_data = {
        "topic": "Test",
        "overview": "Overview",
        "conclusion": "Conclusion",
    }
    
    brief = ResearchBrief(**minimal_data)
    
    assert brief.topic == "Test"
    assert brief.key_findings == []
    assert brief.controversies == []
    assert brief.expert_opinions == []
    assert brief.sources == []
    assert brief.generated_at  # Should have default timestamp


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

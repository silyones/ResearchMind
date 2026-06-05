from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Source(BaseModel):
    """Represents a source/reference for research data."""
    
    title: str = Field(..., description="Title of the source")
    url: str = Field(..., description="URL of the source")
    date: str = Field(..., description="Publication or access date")


class Finding(BaseModel):
    """Represents a key finding from research."""
    
    finding: str = Field(..., description="Description of the finding")
    source_url: str = Field(..., description="URL of the source for this finding")


class ResearchBrief(BaseModel):
    """Complete research output with findings, controversies, and expert opinions."""
    
    topic: str = Field(..., description="The research topic")
    overview: str = Field(..., description="High-level overview of the topic")
    key_findings: List[Finding] = Field(default_factory=list, description="List of key findings")
    controversies: List[str] = Field(default_factory=list, description="List of controversies or debates")
    expert_opinions: List[str] = Field(default_factory=list, description="List of expert opinions")
    conclusion: str = Field(..., description="Conclusion based on research")
    sources: List[Source] = Field(default_factory=list, description="List of sources used")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when research was generated")


class ResearchRequest(BaseModel):
    """Request model for research endpoint."""
    
    topic: str = Field(..., description="Topic to research", min_length=1, max_length=500)


class ResearchResponse(BaseModel):
    """Response model for research endpoint."""
    
    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[ResearchBrief] = Field(None, description="Research brief if successful")
    error: Optional[str] = Field(None, description="Error message if request failed")

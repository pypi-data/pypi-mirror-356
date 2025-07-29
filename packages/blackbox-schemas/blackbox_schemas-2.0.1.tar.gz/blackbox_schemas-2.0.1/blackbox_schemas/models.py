"""
Auto-generated Pydantic models for BlackBox Schemas
Compatible with Pydantic v2.x
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from enum import Enum
import re


# Models from package/schema.py
from datetime import datetime
class CategoryEvaluation(BaseModel):
    category: str  = Field(description="The category name being evaluated")
    pros_cons: dict[str, list[str]]  = Field(
        description="Dictionary containing 'Pros' and 'Cons' keys, each with a list of points. Example: {'Pros':['pro1', 'pro 2', .... ], 'Cons':['Con 1', 'Con 2', ....]},",
        example={
            "Pros": ["pro1", "pro2", "pro3", "pro4"],
            "Cons": ["con1", "con2", "con3", "con4"],
        },
    )
    feasibility: str  = Field(description="Yes/No/moderate assessment of feasibility")
    observations: List[str]  = Field(
        description="List of observations for this category"
    )
    recommendations: List[str]  = Field(
        description="List of recommendations for this category"
    )



class Recommendation(BaseModel):
    decision: str  = Field(description="Go/No-Go decision/Moderate")
    summary: str  = Field(description="Summary of key factors influencing the decision")
    next_steps: List[str]  = Field(description="List of suggested next steps")



class SubmissionDetails(BaseModel):
    due_date: str  = Field(
        description="Exact submission deadline from RFP in YYYY-MM-DD format. Look for phrases like 'proposals due', 'submission deadline', 'closing date', or 'must be received by'."
    )
    submission_type: str  = Field(
        description="Type of submission method: 'online' (email, web portal, digital upload) or 'offline' (physical delivery, mail, in-person)"
    )
    submission_details: str  = Field(
        description="Specific submission location and method: email address, web portal URL, physical mailing address, or office location where proposals must be submitted"
    )
    submission_instructions: str  = Field(
        description="Detailed instructions for proposal preparation and submission: required format (PDF, hard copy), number of copies, file size limits, naming conventions, required sections, and any special submission requirements"
    )



class RFPEvaluation(BaseModel):
    evaluation: List[CategoryEvaluation]  = Field(
        description="List of category evaluations"
    )
    recommendation: Recommendation  = Field(description="Final recommendation")
    timeline_and_submission_details: SubmissionDetails  = Field(
        description="Timeline and submission details",
        alias="timeline_and_submission_details",
    )

    model_config = ConfigDict()


class LegalAdministrativeRequirements(BaseModel):
    insurance_requirements: Optional[str]
    company_info_requirements: Optional[str]
    certification_requirements: Optional[str]
    subcontracting_requirements: Optional[str]
    required_forms_and_attachments: Optional[str]
    other_admin_requirements: Optional[str]



class TechnicalOperationalRequirements(BaseModel):
    client_background: Optional[str]
    project_purpose_objectives: Optional[str]
    qualification_requirements: Optional[str]
    scope_of_work: Optional[str]
    deliverables: Optional[str]
    timeline_and_milestones: Optional[str]
    proposal_format: Optional[str]
    evaluation_criteria: Optional[str]
    budget_guidelines: Optional[str]
    location_requirements: Optional[str]
    technical_specifications: Optional[str]



class GuidanceAndClarifications(BaseModel):
    ambiguous_requirements: Optional[List[str]]  = Field(default_factory=list)
    implicit_requirements: Optional[List[str]]  = Field(default_factory=list)
    clarification_needed: Optional[List[str]]  = Field(default_factory=list)



class PageReferences(BaseModel):
    section_to_page: Optional[Dict[str, str]]  = Field(
        default_factory=dict, description="e.g., {'Scope of Work': 'Pg 6–8'}"
    )



class RFPAnalysisOutput(BaseModel):
    legal_admin_requirements: LegalAdministrativeRequirements
    technical_requirements: TechnicalOperationalRequirements
    guidance_notes: GuidanceAndClarifications
    page_references: Optional[PageReferences] = None
    rfp_metadata: Optional[Dict[str, str]]  = Field(
        default_factory=dict,
        description="Optional metadata like client name, issue date",
    )



class UserPreferencesSection(BaseModel):
    question: str  = Field(
        ..., description="The question to be answered by the content generator"
    )
    suggested_answer: str  = Field(
        ..., description="The suggested answer to the question"
    )



class UserPreferences(BaseModel):
    user_preferences: List[UserPreferencesSection]  = Field(...)



class TOCSubSection(BaseModel):
    subSectionNumber: str  = Field(..., description="The subsection number (e.g. '2.1')")
    subSectionTitle: str  = Field(..., description="The subsection title")



class TOCSection(BaseModel):
    sectionNumber: str  = Field(..., description="Section number (e.g. '2')")
    sectionTitle: str  = Field(..., description="Section title")
    subSections: List[TOCSubSection]  = Field(default_factory=list)
    agentSpecialisation: str  = Field(
        ..., description="Which agent handles this section"
    )
    specificInstruction: str  = Field(
        default="", description="Any special instructions for this section"
    )
    relevant_sections: List[str]  = Field(
        default_factory=list,
        description="List of RFP headings relevant to this section",
    )
    prompt: str  = Field(..., description="The meta-prompt for the content generator")



class TableOfContents(BaseModel):
    outline_json: List[TOCSection]  = Field(...)



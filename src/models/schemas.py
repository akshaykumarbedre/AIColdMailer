from dataclasses import dataclass
from langchain_core.pydantic_v1 import BaseModel, Field

class EmailStructure(BaseModel):
    subject: str = Field(description="The subject line of the email, should be concise, attention-grabbing, and relevant to the recipient.")
    body: str = Field(
        description="The main content of the email, including an engaging introduction, personalized messaging, a clear call to action (CTA), and formatting that enhances readability. "
                    "Consider including dynamic content (such as the recipient's name, relevant offers, or interests), bullet points for clarity, and emotional language to evoke a response. "
                    "The tone should be friendly but professional, maintaining a balance between informative and persuasive elements to increase engagement rates."
                    "No placeholder should be there, it must be complete",
    )

@dataclass
class EmailContent:
    website: str
    email: str
    subject: str
    body: str
    status: str = "Pending"

@dataclass
class Target:
    website: str
    email: str
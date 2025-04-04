from pydantic import BaseModel, Field, field_validator
import re

class CreateUserRequest(BaseModel):
    username: str = Field(
        min_length=6, 
        max_length=20, 
        description="Username must be 6-20 characters long and contain only letters, numbers, and underscores."
    )
    full_name: str = Field(
        min_length=6, 
        max_length=50, 
        description="Full name must be 6-50 characters long and contain only letters and spaces."
    )
    password: str = Field(
        min_length=8, 
        max_length=100, 
        description="Password must be at least 8 characters long."
    )

    @field_validator('username')
    def username_no_special_characters(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username should only contain letters, numbers, and underscores')
        return v

    @field_validator('full_name')
    def full_name_valid(cls, v):
        if not re.match(r'^[a-zA-Z\s]+$', v):  # Removed hyphens
            raise ValueError('Full name should only contain letters and spaces')
        return v

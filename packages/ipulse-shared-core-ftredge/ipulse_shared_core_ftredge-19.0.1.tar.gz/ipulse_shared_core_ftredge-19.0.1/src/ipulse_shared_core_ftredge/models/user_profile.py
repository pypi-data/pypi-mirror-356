""" User Profile model for storing personal information and settings. """
from datetime import date, datetime, timezone
from typing import Set, Optional, ClassVar, Dict, Any, List
from pydantic import EmailStr, Field, ConfigDict, field_validator, model_validator, computed_field
from ipulse_shared_base_ftredge import Layer, Module, list_as_lower_strings, Subject
from .base_data_model import BaseDataModel
import re  # Add re import

# ORIGINAL AUTHOR ="Russlan Ramdowar;russlan@ftredge.com"
# CLASS_ORGIN_DATE=datetime(2024, 2, 12, 20, 5)

############################ !!!!! ALWAYS UPDATE SCHEMA VERSION , IF SCHEMA IS BEING MODIFIED !!! #################################
class UserProfile(BaseDataModel):
    """
    User Profile model for storing personal information and settings.
    """
    model_config = ConfigDict(frozen=False, extra="forbid")  # Allow field modification

    # Class constants
    VERSION: ClassVar[float] = 5.0  # Incremented version for primary_usertype addition
    DOMAIN: ClassVar[str] = "_".join(list_as_lower_strings(Layer.PULSE_APP, Module.CORE.name, Subject.USER.name))
    OBJ_REF: ClassVar[str] = "userprofile"

    schema_version: float = Field(
        default=VERSION,
        frozen=True,
        description="Version of this Class == version of DB Schema"
    )

    id: str = Field(
        default="",  # Will be auto-generated from user_uid if not provided
        description=f"User Profile ID, format: {OBJ_REF}_user_uid"
    )

    user_uid: str = Field(
        ...,
        description="User UID from Firebase Auth"
    )

    # Added primary_usertype field for main role categorization
    primary_usertype: str = Field(
        ...,
        description="Primary user type (e.g., customer, internal, admin, superadmin)"
    )

    # Renamed usertypes to secondary_usertypes
    secondary_usertypes: List[str] = Field(
        default_factory=list,
        description="List of secondary user types"
    )

    # Rest of the fields remain the same
    email: EmailStr = Field(
        ...,
        description="Email address",
        frozen=True
    )
    organizations_uids: Set[str] = Field(
        default_factory=set,
        description="Organization UIDs the user belongs to"
    )

    # System identification (read-only)
    provider_id: str = Field(
        ...,
        description="User provider ID",
        frozen=True
    )
    aliases: Optional[Dict[str, str]] = Field(
        default=None,
        description="User aliases. With alias as key and description as value."
    )

    # User-editable fields
    username: str = Field(
        default="",  # Made optional with empty default - will be auto-generated
        max_length=12,  # Updated to 12 characters
        pattern="^[a-zA-Z0-9_]+$",  # Allow underscore
        description="Username (public display name), max 12 chars, alphanumeric and underscore. Auto-generated from email if not provided."
    )
    dob: Optional[date] = Field(
        default=None,
        description="Date of birth"
    )
    first_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="First name"
    )
    last_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Last name"
    )
    mobile: Optional[str] = Field(
        default=None,
        pattern=r"^\+?[1-9]\d{1,14}$",  # Added 'r' prefix for raw string
        description="Mobile phone number"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for the user"
    )

    # Remove audit fields as they're inherited from BaseDataModel

    @model_validator(mode='before')
    @classmethod
    def ensure_id_exists(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures the id field exists by generating it from user_uid if needed.
        This runs BEFORE validation, guaranteeing id will be present for validators.
        """
        if not isinstance(data, dict):
            return data

        # If id is already in the data, leave it alone
        if 'id' in data and data['id']:
            return data

        # If user_uid exists but id doesn't, generate id from user_uid
        if 'user_uid' in data and data['user_uid']:
            data['id'] = f"{cls.OBJ_REF}_{data['user_uid']}"

        return data

    @model_validator(mode='before')
    @classmethod
    def populate_username(cls, data: Any) -> Any:
        """
        Generates or sanitizes the username.
        If username is provided and non-empty, it's sanitized and truncated to 10 chars.
        If not provided or empty, it's generated from the email (part before '@'),
        sanitized, and truncated to 10 chars.
        If no email is available, generates a default username.
        """
        if not isinstance(data, dict):
            # Not a dict, perhaps an instance already, skip
            return data

        email = data.get('email')
        username = data.get('username')

        # Check if username is provided and non-empty
        if username and isinstance(username, str) and username.strip():
            # Sanitize and truncate provided username
            sanitized_username = re.sub(r'[^a-zA-Z0-9_]', '', username)
            data['username'] = sanitized_username[:12] if sanitized_username else "user"
        elif email and isinstance(email, str):
            # Generate from email
            email_prefix = email.split('@')[0]
            sanitized_prefix = re.sub(r'[^a-zA-Z0-9_]', '', email_prefix)
            data['username'] = sanitized_prefix[:12] if sanitized_prefix else "user"
        else:
            # Fallback if no email or username provided
            data['username'] = "user"

        return data
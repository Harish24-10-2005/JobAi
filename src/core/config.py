
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field

class Settings(BaseSettings):
    """
    Application Settings managed by Pydantic.
    Reads from environment variables and .env file.
    """
    
    # AI Models
    openrouter_api_key: Optional[SecretStr] = Field(None, alias="OPENROUTER_API_KEY1")
    # Fallback to standard key if 1 is missing, handled in logic or prioritized aliases
    openrouter_api_key_fallback: Optional[SecretStr] = Field(None, alias="OPENROUTER_API_KEY")
    
    groq_api_key: SecretStr = Field(..., alias="GROQ_API_KEY")
    
    # Search
    serpapi_api_key: SecretStr = Field(..., alias="SERPAPI_API_KEY")
    
    # Browser
    chrome_path: str = Field(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    user_data_dir: str = Field(r"C:\Users\LENOVO\AppData\Local\Google\Chrome\User Data")
    profile_directory: str = Field("Profile 1")
    headless: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    def get_openrouter_key(self) -> str:
        if self.openrouter_api_key:
            return self.openrouter_api_key.get_secret_value()
        if self.openrouter_api_key_fallback:
            return self.openrouter_api_key_fallback.get_secret_value()
        raise ValueError("OpenRouter API Key not found.")

settings = Settings()

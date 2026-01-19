
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field

class Settings(BaseSettings):
    """
    Application Settings managed by Pydantic.
    Reads from environment variables and .env file.
    """
    
    # AI Models - Groq
    groq_api_key: SecretStr = Field(..., alias="GROQ_API_KEY")
    groq_api_key_fallback: Optional[SecretStr] = Field(None, alias="GROQ_API_KEY1")
    groq_model: str = Field("llama-3.1-8b-instant", alias="GROQ_MODEL")
    
    # AI Models - OpenRouter
    openrouter_api_key: Optional[SecretStr] = Field(None, alias="OPENROUTER_API_KEY")
    openrouter_api_key_fallback: Optional[SecretStr] = Field(None, alias="OPENROUTER_API_KEY1")
    openrouter_model: str = Field("qwen/qwen-2.5-coder-32b-instruct:free", alias="OPENROUTER_MODEL")
    
    # AI Models - Gemini
    gemini_api_key: Optional[SecretStr] = Field(None, alias="GEMINI_API_KEY")
    gemini_model: str = Field("gemini-2.0-flash-exp", alias="GEMINI_MODEL1")
    
    # Search
    serpapi_api_key: SecretStr = Field(..., alias="SERPAPI_API_KEY")
    
    # Browser
    chrome_path: str = Field(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    user_data_dir: str = Field(r"C:\Users\LENOVO\AppData\Local\Google\Chrome\User Data")
    profile_directory: str = Field("Profile 1")
    headless: bool = False
    
    # Supabase
    supabase_url: str = Field("https://lzghvveqglhbvrfywqnv.supabase.co", alias="SUPABASE_URL")
    supabase_anon_key: str = Field(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx6Z2h2dmVxZ2xoYnZyZnl3cW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgyOTUzMzIsImV4cCI6MjA4Mzg3MTMzMn0.s5sSBIUB-rWso_D_9ay2j06G2DDXKLYPkJa8H6PtPB8",
        alias="SUPABASE_ANON_KEY"
    )
    supabase_service_key: Optional[SecretStr] = Field(None, alias="SUPABASE_SERVICE_KEY")
    
    # Encryption (for credentials)
    encryption_key: Optional[SecretStr] = Field(None, alias="ENCRYPTION_KEY")
    
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
    
    def get_encryption_key(self) -> bytes:
        """Get or generate encryption key for credential storage."""
        if self.encryption_key:
            key = self.encryption_key.get_secret_value()
            # Ensure key is 32 bytes for AES-256
            return key.encode()[:32].ljust(32, b'\0')
        # Generate a default key from other secrets (not recommended for production)
        import hashlib
        combined = f"{self.groq_api_key.get_secret_value()}"
        return hashlib.sha256(combined.encode()).digest()

settings = Settings()

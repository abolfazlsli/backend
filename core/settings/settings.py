from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # base settings 
    debug: bool
    # database settings
    db_url: str
    db_user: str
    db_pass: str
    db_name: str
    db_port: int
    # swagger configs 
    docs_url : str
    redocx_url : str
    upload_dir : str
    openapi_url : str
    title : str
    description : str
    version : str
    jwt_access_token_expire_minutes : str
    jwt_secret_key : str
    jwt_algorithm : str
    # sms_gateway : str
    # sms_api_kay : str
    class Config:
        env_file = ".env.dev"

    @property
    def sqlalchemy_database_url(self):
        return f"postgresql+psycopg2://{self.db_user}:{self.db_pass}@{self.db_url}:{self.db_port}/{self.db_name}"


setting = Settings()

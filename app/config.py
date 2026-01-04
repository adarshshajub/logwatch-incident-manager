import os

class Config:
    SECRET_KEY = "secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🔔 Email (SMTP)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "email@gmail.com"
    MAIL_PASSWORD = "app_password"
    MAIL_DEFAULT_SENDER = "Log Monitor <email@gmail.com>"

    
    SERVICENOW_INSTANCE = "https://instance.service-now.com"
    SERVICENOW_USER = "api_user"
    SERVICENOW_PASSWORD = "api_password"

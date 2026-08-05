from backend.config import settings

print("=" * 40)
print("Configuration Loaded Successfully")
print("=" * 40)

print(f"App Name       : {settings.app_name}")
print(f"Version        : {settings.app_version}")
print(f"Database       : {settings.database_url}")
print(f"Model          : {settings.nvidia_model}")
print(f"SMTP Server    : {settings.smtp_server}")
print(f"SMTP Port      : {settings.smtp_port}")
print(f"Log Level      : {settings.log_level}")
import os
from azpaddypy.mgmt.logging import create_app_logger

application_insights_connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
instrumentation_options={
                            "azure_sdk": {"enabled": True},
                            "django": {"enabled": False},
                            "fastapi": {"enabled": False},
                            "flask": {"enabled": True},
                            "psycopg2": {"enabled": True},
                            "requests": {"enabled": True},
                            "urllib": {"enabled": True},
                            "urllib3": {"enabled": True},
                        }
# Create a single instance of the logger
logger = create_app_logger(
        connection_string=application_insights_connection_string,
        service_name=__name__,
        service_version="1.0.0",
        enable_console_logging=True,
        instrumentation_options=instrumentation_options
    )

# Export the logger instance
__all__ = ['logger'] 
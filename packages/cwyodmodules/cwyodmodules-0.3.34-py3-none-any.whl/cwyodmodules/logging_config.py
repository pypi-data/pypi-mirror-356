import os
from azpaddypy.mgmt.logging import create_app_logger

application_insights_connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

# Create a single instance of the logger
logger = create_app_logger(
        connection_string=application_insights_connection_string,
        service_name=__name__,
        service_version="1.0.0",
        enable_console_logging=True,
    )

# Export the logger instance
__all__ = ['logger'] 
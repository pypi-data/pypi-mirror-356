import time
import logging
import os
from typing import Any, Callable, Dict, Optional

from distributed_logger.models.log import LogInfo
from distributed_logger.loggers.factory import LoggerFactory, EnvType
from distributed_logger.models.config import ConfigFactory
from distributed_logger.loggers.logger import Logger

logger = logging.getLogger(__name__)

class AuditLogMiddleware:
    """
    Middleware for auditing requests using distributed logging.
    Supports both WSGI and ASGI frameworks.
    """
    
    def __init__(self, get_response: Callable) -> None:
        """
        Initialize the middleware.
        
        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response
        self.logger: Optional[Logger] = None
        self._initialize_logger()

    def _initialize_logger(self) -> None:
        """Initialize the logger based on environment configuration"""
        try:
            broker_type = os.environ.get("BROKER_TYPE", "SIMPLE").upper()
            env_type = EnvType.KAFKA if broker_type == "KAFKA" else EnvType.SIMPLE

            config = ConfigFactory.create_config(
                config_type=broker_type,
                bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
                topic=os.getenv("KAFKA_TOPIC", "audit_logs"),
                client_id=os.getenv("KAFKA_CLIENT_ID", "distributed_logger"),
            )
            
            self.logger = LoggerFactory(env_type, config).get_logger()
            logger.info("Successfully initialized %s logger", broker_type)
            
        except Exception as e:
            logger.error("Failed to initialize logger: %s", str(e))
            # Fall back to simple logger if Kafka initialization fails
            if broker_type == "KAFKA":
                logger.info("Falling back to simple logger")
                self.logger = LoggerFactory(EnvType.SIMPLE, 
                                         ConfigFactory.create_config("SIMPLE")).get_logger()

    def _extract_request_data(self, request: Any) -> Dict[str, Any]:
        """
        Extract relevant data from the request object.
        
        Args:
            request: The request object (framework agnostic)
            
        Returns:
            Dict containing request data
        """
        data = {}
        
        # Handle different HTTP methods
        if hasattr(request, 'method'):
            if request.method == 'POST':
                data = request.POST.dict() if hasattr(request.POST, 'dict') else dict(request.POST)
            elif request.method == 'GET':
                data = request.GET.dict() if hasattr(request.GET, 'dict') else dict(request.GET)
            
            # Remove sensitive information
            if 'password' in data:
                data['password'] = '[REDACTED]'
            if 'token' in data:
                data['token'] = '[REDACTED]'
                
        return data

    def __call__(self, request: Any) -> Any:
        """
        Process the request and log audit information.
        
        Args:
            request: The request object
            
        Returns:
            The response from the next middleware or view
        """
        start_time = time.time()
        
        # Process the request first
        response = self.get_response(request)
        
        try:
            if not self.logger:
                logger.warning("Logger not initialized, skipping audit logging")
                return response
                
            # Create log entry
            log_info = LogInfo(
                ip_address=request.META.get('REMOTE_ADDR', ''),
                user_id=str(request.user.id) if hasattr(request, 'user') and request.user.is_authenticated else None,
                request_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)),
                action=request.path,
                request_data=self._extract_request_data(request)
            )
            
            # Add response status if available
            if hasattr(response, 'status_code'):
                log_info.request_data['status_code'] = response.status_code
                
            # Calculate and add request duration
            duration = time.time() - start_time
            log_info.request_data['duration_ms'] = int(duration * 1000)
            
            # Publish log
            self.logger.publish(log_info)
            
        except Exception as e:
            logger.error("Error logging request: %s", str(e))
            # Don't re-raise the exception - logging should not break the application
            
        return response

    def __del__(self) -> None:
        """Ensure proper cleanup of logger resources"""
        try:
            if self.logger:
                self.logger.close()
        except Exception as e:
            logger.error("Error closing logger: %s", str(e))
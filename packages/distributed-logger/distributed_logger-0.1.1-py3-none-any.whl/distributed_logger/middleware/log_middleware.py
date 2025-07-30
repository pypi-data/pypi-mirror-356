import time
from distributed_logger.models.log import LogInfo
import os
from distributed_logger.loggers.factory import LoggerFactory, EnvType
from distributed_logger.models.config import ConfigFactory


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def _get_logger(self):
        broker_type = os.environ.get("BROKER_TYPE", "SIMPLE").upper()
        if broker_type == "KAFKA":
            env_type = EnvType.KAFKA
        else:
            env_type = EnvType.SIMPLE

        config = ConfigFactory.create_config(
            config_type=broker_type,

            # Kafka settings
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            topic=os.getenv("KAFKA_TOPIC"),
            client_id=os.getenv("KAFKA_CLIENT_ID"),
            host=os.getenv("RABBITMQ_HOST"),

        )
        return LoggerFactory(env_type, config).get_logger()

    def __call__(self, request):
        start_time = time.time()

        # Process the request
        response = self.get_response(request)

        try:

            # Get the logger instance
            self.logger = self._get_logger()
            
            log_info = LogInfo(
                ip_address=request.META.get('REMOTE_ADDR',''),
                user_id=request.user.id if request.user.is_authenticated else None,
                request_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)),
                action=request.path,
                request_data=request.POST.dict() if request.method == 'POST' else request.GET.dict()
            )
            self.logger.publish(log_info)

        except Exception as e:
            print(f"Error logging request: {e}")
        return response
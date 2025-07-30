import unittest
from unittest.mock import MagicMock, patch
from distributed_logger.middleware.log_middleware import AuditLogMiddleware
from distributed_logger.models.log import LogInfo


class TestAuditLogMiddleware(unittest.TestCase):

    @patch("distributed_logger.middleware.log_middleware.LoggerFactory")
    @patch("distributed_logger.middleware.log_middleware.ConfigFactory.create_config")
    @patch.dict("os.environ", {
        "BROKER_TYPE": "SIMPLE",
        "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092",
        "KAFKA_TOPIC": "audit_logs",
        "KAFKA_CLIENT_ID": "audit_logger",
        "RABBITMQ_HOST": "localhost"
    })
    def test_middleware_logs_get_request(self, mock_create_config, mock_logger_factory):
        # Arrange
        mock_logger = MagicMock()
        mock_logger_factory.return_value.get_logger.return_value = mock_logger

        request = MagicMock()
        request.method = "GET"
        request.path = "/test/get"
        request.GET.dict.return_value = {"param": "1"}
        request.POST.dict.return_value = {}
        request.META = {"REMOTE_ADDR": "192.168.1.1"}
        request.user.is_authenticated = True
        request.user.id = 99

        get_response = MagicMock(return_value="mock_response")

        # Act
        middleware = AuditLogMiddleware(get_response)
        response = middleware(request)

        # Assert
        self.assertEqual(response, "mock_response")
        mock_logger.publish.assert_called_once()
        log_info_arg = mock_logger.publish.call_args[0][0]
        self.assertIsInstance(log_info_arg, LogInfo)
        self.assertEqual(log_info_arg.ip_address, "192.168.1.1")
        self.assertEqual(log_info_arg.user_id, 99)
        self.assertEqual(log_info_arg.action, "/test/get")
        self.assertEqual(log_info_arg.request_data, {"param": "1"})

    @patch("distributed_logger.middleware.log_middleware.LoggerFactory")
    @patch("distributed_logger.middleware.log_middleware.ConfigFactory.create_config")
    @patch.dict("os.environ", {
        "BROKER_TYPE": "SIMPLE"
    })
    def test_middleware_handles_publish_exception(self, mock_create_config, mock_logger_factory):
        # Arrange
        mock_logger = MagicMock()
        mock_logger.publish.side_effect = Exception("Simulated error")
        mock_logger_factory.return_value.get_logger.return_value = mock_logger

        request = MagicMock()
        request.method = "GET"
        request.path = "/test/error"
        request.GET.dict.return_value = {}
        request.POST.dict.return_value = {}
        request.META = {"REMOTE_ADDR": "0.0.0.0"}
        request.user.is_authenticated = False
        request.user.id = None

        get_response = MagicMock(return_value="mock_response")

        # Act
        middleware = AuditLogMiddleware(get_response)
        response = middleware(request)

        # Assert
        self.assertEqual(response, "mock_response")
        mock_logger.publish.assert_called_once()


if __name__ == "__main__":
    unittest.main()

from ed_domain.documentation.api.abc_endpoint_descriptions import \
    ABCEndpointDescriptions
from ed_domain.documentation.api.definitions import (EndpointDescription,
                                                     HttpMethod)

from ed_core.application.features.admin.dtos import (
    CreateAdminDto, SettleDriverPaymentRequestDto, UpdateAdminDto)
from ed_core.application.features.business.dtos import (BusinessReportDto,
                                                        CreateApiKeyDto,
                                                        CreateBusinessDto,
                                                        CreateOrderDto,
                                                        CreateWebhookDto,
                                                        UpdateBusinessDto)
from ed_core.application.features.common.dtos import (AdminDto, ApiKeyDto,
                                                      BusinessDto, ConsumerDto,
                                                      CreateConsumerDto,
                                                      DeliveryJobDto,
                                                      DriverDto,
                                                      NotificationDto,
                                                      OrderDto, TrackOrderDto,
                                                      UpdateLocationDto,
                                                      WebhookDto)
from ed_core.application.features.consumer.dtos import (RateDeliveryDto,
                                                        UpdateConsumerDto)
from ed_core.application.features.delivery_job.dtos import CreateDeliveryJobDto
from ed_core.application.features.driver.dtos import (
    CreateDriverDto, DriverPaymentSummaryDto, FinishOrderDeliveryRequestDto,
    FinishOrderPickUpRequestDto, UpdateDriverDto)


class CoreEndpointDescriptions(ABCEndpointDescriptions):
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._descriptions: list[EndpointDescription] = [
            # Business endpoints
            {
                "name": "get_all_businesses",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/businesses",
                "response_model": list[BusinessDto],
            },
            {
                "name": "create_a_business",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/businesses",
                "request_model": CreateBusinessDto,
                "response_model": BusinessDto,
            },
            {
                "name": "create_business",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/businesses",
                "request_model": CreateBusinessDto,
                "response_model": BusinessDto,
            },
            {
                "name": "get_business",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/businesses/{{business_id}}",
                "path_params": {"business_id": str},
                "response_model": BusinessDto,
            },
            {
                "name": "update_business",
                "method": HttpMethod.PUT,
                "path": f"{self._base_url}/businesses/{{business_id}}",
                "path_params": {"business_id": str},
                "request_model": UpdateBusinessDto,
                "response_model": BusinessDto,
            },
            {
                "name": "get_business_by_user_id",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/businesses/users/{{user_id}}",
                "path_params": {"user_id": str},
                "response_model": BusinessDto,
            },
            {
                "name": "get_business_orders",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/businesses/{{business_id}}/orders",
                "path_params": {"business_id": str},
                "response_model": list[OrderDto],
            },
            {
                "name": "create_business_order",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/businesses/{{business_id}}/orders",
                "path_params": {"business_id": str},
                "request_model": CreateOrderDto,
                "response_model": OrderDto,
            },
            {
                "name": "get_business_webhook",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/businesses/{{business_id}}/webhook",
                "path_params": {"business_id": str},
                "response_model": WebhookDto,
            },
            {
                "name": "create_business_webhook",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/businesses/{{business_id}}/webhook",
                "path_params": {"business_id": str},
                "request_model": CreateWebhookDto,
                "response_model": WebhookDto,
            },
            {
                "name": "get_business_api_keys",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/businesses/{{business_id}}/api-keys",
                "path_params": {"business_id": str},
                "response_model": list[ApiKeyDto],
            },
            {
                "name": "create_business_api_key",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/businesses/{{business_id}}/api-keys",
                "path_params": {"business_id": str},
                "request_model": CreateApiKeyDto,
                "response_model": ApiKeyDto,
            },
            {
                "name": "delete_business_api_key",
                "method": HttpMethod.DELETE,
                "path": f"{self._base_url}/businesses/{{business_id}}/api-keys/{{api_key_prefix}}",
                "path_params": {"business_id": str, "api_key_prefix": str},
            },
            {
                "name": "get_business_report",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/businesses/{{business_id}}/report",
                "path_params": {"business_id": str},
                "response_model": BusinessReportDto,
            },
            # Driver endpoints
            {
                "name": "get_drivers",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers",
                "response_model": list[DriverDto],
            },
            {
                "name": "create_driver",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers",
                "request_model": CreateDriverDto,
                "response_model": DriverDto,
            },
            {
                "name": "get_driver_delivery_jobs",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs",
                "path_params": {"driver_id": str},
                "response_model": list[DeliveryJobDto],
            },
            {
                "name": "get_driver_orders",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers/{{driver_id}}/orders",
                "path_params": {"driver_id": str},
                "response_model": list[OrderDto],
            },
            {
                "name": "get_driver",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers/{{driver_id}}",
                "path_params": {"driver_id": str},
                "response_model": DriverDto,
            },
            {
                "name": "update_driver",
                "method": HttpMethod.PUT,
                "path": f"{self._base_url}/drivers/{{driver_id}}",
                "path_params": {"driver_id": str},
                "request_model": UpdateDriverDto,
                "response_model": DriverDto,
            },
            {
                "name": "update_driver_current_location",
                "method": HttpMethod.PUT,
                "path": f"{self._base_url}/drivers/{{driver_id}}/current-location",
                "path_params": {"driver_id": str},
                "request_model": UpdateLocationDto,
                "response_model": DriverDto,
            },
            {
                "name": "get_driver_by_user_id",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers/users/{{user_id}}",
                "path_params": {"user_id": str},
                "response_model": DriverDto,
            },
            {
                "name": "claim_delivery_job",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/claim",
                "path_params": {"driver_id": str, "delivery_job_id": str},
                "response_model": DeliveryJobDto,
            },
            {
                "name": "cancel_delivery_job",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/cancel",
                "path_params": {"driver_id": str, "delivery_job_id": str},
                "response_model": DeliveryJobDto,
            },
            {
                "name": "start_order_pick_up",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/orders/{{order_id}}/pick-up",
                "path_params": {
                    "driver_id": str,
                    "delivery_job_id": str,
                    "order_id": str,
                },
            },
            {
                "name": "finish_order_pick_up",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/orders/{{order_id}}/pick-up/verify",
                "path_params": {
                    "driver_id": str,
                    "delivery_job_id": str,
                    "order_id": str,
                },
                "request_model": FinishOrderPickUpRequestDto,
            },
            {
                "name": "start_order_delivery",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/orders/{{order_id}}/deliver",
                "path_params": {
                    "driver_id": str,
                    "delivery_job_id": str,
                    "order_id": str,
                },
            },
            {
                "name": "finish_order_delivery",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs/{{delivery_job_id}}/orders/{{order_id}}/deliver/verify",
                "path_params": {
                    "driver_id": str,
                    "delivery_job_id": str,
                    "order_id": str,
                },
                "request_model": FinishOrderDeliveryRequestDto,
            },
            {
                "name": "get_driver_payment_summary",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/drivers/{{driver_id}}/payment/summary",
                "path_params": {"driver_id": str},
                "response_model": DriverPaymentSummaryDto,
            },
            # Delivery job endpoints
            {
                "name": "get_delivery_jobs",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/delivery-jobs",
                "response_model": list[DeliveryJobDto],
            },
            {
                "name": "get_delivery_job",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/delivery-jobs/{{delivery_job_id}}",
                "path_params": {"delivery_job_id": str},
                "response_model": DeliveryJobDto,
            },
            {
                "name": "create_delivery_job",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/delivery-jobs",
                "request_model": CreateDeliveryJobDto,
                "response_model": DeliveryJobDto,
            },
            # Order endpoints
            {
                "name": "get_orders",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/orders",
                "response_model": list[OrderDto],
            },
            {
                "name": "get_order",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/orders/{{order_id}}",
                "path_params": {"order_id": str},
                "response_model": OrderDto,
            },
            {
                "name": "track_order",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/orders/{{order_id}}/track",
                "path_params": {"order_id": str},
                "response_model": TrackOrderDto,
            },
            {
                "name": "cancel_order",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/orders/{{order_id}}/cancel",
                "path_params": {"order_id": str},
                "response_model": OrderDto,
            },
            # Consumer endpoints
            {
                "name": "get_consumers",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/consumers",
                "response_model": list[ConsumerDto],
            },
            {
                "name": "create_consumer",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/consumers",
                "request_model": CreateConsumerDto,
                "response_model": ConsumerDto,
            },
            {
                "name": "update_consumer",
                "method": HttpMethod.PUT,
                "path": f"{self._base_url}/consumers/{{consumer_id}}",
                "path_params": {"consumer_id": str},
                "request_model": UpdateConsumerDto,
                "response_model": ConsumerDto,
            },
            {
                "name": "get_consumer_orders",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/consumers/{{consumer_id}}/orders",
                "path_params": {"consumer_id": str},
                "response_model": list[OrderDto],
            },
            {
                "name": "rate_delivery",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/consumers/{{consumer_id}}/orders/{{order_id}}",
                "path_params": {"consumer_id": str, "order_id": str},
                "request_model": RateDeliveryDto,
                "response_model": OrderDto,
            },
            {
                "name": "get_consumer",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/consumers/{{consumer_id}}",
                "path_params": {"consumer_id": str},
                "response_model": ConsumerDto,
            },
            {
                "name": "get_consumer_by_user_id",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/consumers/users/{{user_id}}",
                "path_params": {"user_id": str},
                "response_model": ConsumerDto,
            },
            # Notification features
            {
                "name": "get_user_notifications",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/notifications/users/{{user_id}}",
                "path_params": {"user_id": str},
                "response_model": list[NotificationDto],
            },
            # API key features
            {
                "name": "get_api_key_by_prefix",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/api-keys/{{api_key_prefix}}",
                "path_params": {"api_key_prefix": str},
                "response_model": ApiKeyDto,
            },
            {
                "name": "verify_api_key",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/api-keys/{{api_key}}/verify",
                "path_params": {"api_key": str},
                "response_model": BusinessDto,
            },
            # Admin endpoints
            {
                "name": "get_admins",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/admins",
                "response_model": list[AdminDto],
            },
            {
                "name": "create_admin",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/admins",
                "request_model": CreateAdminDto,
                "response_model": AdminDto,
            },
            {
                "name": "update_admin",
                "method": HttpMethod.PUT,
                "path": f"{self._base_url}/admins/{{admin_id}}",
                "path_params": {"admin_id": str},
                "request_model": UpdateAdminDto,
                "response_model": AdminDto,
            },
            {
                "name": "get_admin",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/admins/{{admin_id}}",
                "path_params": {"admin_id": str},
                "response_model": AdminDto,
            },
            {
                "name": "get_admin_by_user_id",
                "method": HttpMethod.GET,
                "path": f"{self._base_url}/admins/users/{{user_id}}",
                "path_params": {"user_id": str},
                "response_model": AdminDto,
            },
            {
                "name": "settle_driver_payment",
                "method": HttpMethod.POST,
                "path": f"{self._base_url}/admins/{{admin_id}}/settle-driver-payment/{{driver_id}}",
                "path_params": {"admin_id": str, "driver_id": str},
                "request_model": SettleDriverPaymentRequestDto,
                "response_model": DriverPaymentSummaryDto,
            },
        ]

    @property
    def descriptions(self) -> list[EndpointDescription]:
        return self._descriptions

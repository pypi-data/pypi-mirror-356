import uvicorn
from ed_domain.common.exceptions import ApplicationException
from ed_domain.common.logging import get_logger
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from ed_core.common.singleton_helpers import SingletonMeta
from ed_core.webapi.common.helpers import GenericResponse
from ed_core.webapi.controllers import (admin_controller, api_key_controller,
                                        business_controller,
                                        consumer_controller,
                                        delivery_job_controller,
                                        delivery_job_rabbitmq_controller,
                                        driver_controller,
                                        notification_controller,
                                        order_controller)

LOG = get_logger()


class API(FastAPI, metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._routers = [
            admin_controller.router,
            business_controller.router,
            consumer_controller.router,
            delivery_job_controller.router,
            driver_controller.router,
            notification_controller.router,
            order_controller.router,
            api_key_controller.router,
        ]

    @property
    def app(self):
        return self

    def start(self) -> None:
        LOG.info("Starting api...")

        self._include_routers()
        self._contain_exceptions()

        uvicorn.run(self, host="0.0.0.0", port=8000)

    def stop(self) -> None:
        LOG.info("API does not need to be stopped...")

    def _include_routers(self) -> None:
        LOG.info("Including routers...")
        for router in self._routers:
            LOG.info(f"Including router: {router.prefix}")
            self.include_router(router)

    def _contain_exceptions(self) -> None:
        @self.exception_handler(ApplicationException)
        async def application_exception_handler(
            request: Request, exception: ApplicationException
        ) -> JSONResponse:
            LOG.error(
                f"ApplicationException occurred: {exception.message} while handling {request.url}",
                f"with error code {exception.error_code}",
                f"with the following errors {exception.errors}",
            )
            return JSONResponse(
                status_code=exception.error_code,
                content=GenericResponse(
                    is_success=False,
                    message=exception.message,
                    errors=exception.errors,
                    data=None,
                ).to_dict(),
            )

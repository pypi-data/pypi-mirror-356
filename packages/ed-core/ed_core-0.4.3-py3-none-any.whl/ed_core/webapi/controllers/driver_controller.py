from typing import Annotated
from uuid import UUID

from ed_domain.common.logging import get_logger
from fastapi import APIRouter, Depends
from rmediator.mediator import Mediator

from ed_core.application.features.common.dtos import (DeliveryJobDto,
                                                      DriverDto, OrderDto,
                                                      UpdateLocationDto)
from ed_core.application.features.delivery_job.requests.commands import (
    CancelDeliveryJobCommand, ClaimDeliveryJobCommand)
from ed_core.application.features.driver.dtos import (
    CreateDriverDto, DriverPaymentSummaryDto, FinishOrderDeliveryRequestDto,
    FinishOrderPickUpRequestDto, UpdateDriverDto)
from ed_core.application.features.driver.requests.commands import (
    CreateDriverCommand, FinishOrderDeliveryCommand, FinishOrderPickUpCommand,
    StartOrderDeliveryCommand, StartOrderPickUpCommand, UpdateDriverCommand,
    UpdateDriverCurrentLocationCommand)
from ed_core.application.features.driver.requests.queries import (
    GetAllDriversQuery, GetDriverByUserIdQuery, GetDriverDeliveryJobsQuery,
    GetDriverOrdersQuery, GetDriverPaymentSummaryQuery, GetDriverQuery)
from ed_core.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_core.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/drivers", tags=["Driver Feature"])


@router.get("", response_model=GenericResponse[list[DriverDto]])
@rest_endpoint
async def get_all_drivers(
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetAllDriversQuery())


@router.post("", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def create_driver(
    request_dto: CreateDriverDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(CreateDriverCommand(dto=request_dto))


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/orders/{order_id}/pick-up",
    response_model=GenericResponse[None],
)
@rest_endpoint
async def initiate_order_pick_up(
    driver_id: UUID,
    delivery_job_id: UUID,
    order_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(
        StartOrderPickUpCommand(driver_id, delivery_job_id, order_id)
    )


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/orders/{order_id}/pick-up/verify",
    response_model=GenericResponse[None],
)
@rest_endpoint
async def verify_order_pick_up(
    driver_id: UUID,
    delivery_job_id: UUID,
    order_id: UUID,
    dto: FinishOrderPickUpRequestDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(
        FinishOrderPickUpCommand(driver_id, delivery_job_id, order_id, dto)
    )


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/orders/{order_id}/deliver",
    response_model=GenericResponse[None],
)
@rest_endpoint
async def initiate_order_drop_off(
    driver_id: UUID,
    delivery_job_id: UUID,
    order_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(
        StartOrderDeliveryCommand(driver_id, delivery_job_id, order_id)
    )


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/orders/{order_id}/deliver/verify",
    response_model=GenericResponse[None],
)
@rest_endpoint
async def verify_order_drop_off(
    driver_id: UUID,
    delivery_job_id: UUID,
    order_id: UUID,
    dto: FinishOrderDeliveryRequestDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(
        FinishOrderDeliveryCommand(driver_id, delivery_job_id, order_id, dto)
    )


@router.get(
    "/{driver_id}/delivery-jobs", response_model=GenericResponse[list[DeliveryJobDto]]
)
@rest_endpoint
async def driver_delivery_jobs(
    driver_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverDeliveryJobsQuery(driver_id))


@router.get(
    "/{driver_id}/payment/summary",
    response_model=GenericResponse[DriverPaymentSummaryDto],
)
@rest_endpoint
async def driver_payment_summary(
    driver_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverPaymentSummaryQuery(driver_id))


@router.get("/{driver_id}/orders", response_model=GenericResponse[list[OrderDto]])
@rest_endpoint
async def driver_orders(
    driver_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverOrdersQuery(driver_id))


@router.get("/{driver_id}", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def get_driver(
    driver_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverQuery(driver_id))


@router.put("/{driver_id}", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def update_driver(
    driver_id: UUID,
    dto: UpdateDriverDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(UpdateDriverCommand(driver_id, dto))


@router.put("/{driver_id}/current-location", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def update_driver_current_location(
    driver_id: UUID,
    dto: UpdateLocationDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(UpdateDriverCurrentLocationCommand(driver_id, dto))


@router.get("/users/{user_id}", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def get_driver_by_user_id(
    user_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetDriverByUserIdQuery(user_id))


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/claim",
    response_model=GenericResponse[DeliveryJobDto],
)
@rest_endpoint
async def claim_delivery_job(
    driver_id: UUID,
    delivery_job_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(ClaimDeliveryJobCommand(driver_id, delivery_job_id))


@router.post(
    "/{driver_id}/delivery-jobs/{delivery_job_id}/cancel",
    response_model=GenericResponse[DeliveryJobDto],
)
@rest_endpoint
async def cancel_delivery_job(
    driver_id: UUID,
    delivery_job_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(CancelDeliveryJobCommand(driver_id, delivery_job_id))

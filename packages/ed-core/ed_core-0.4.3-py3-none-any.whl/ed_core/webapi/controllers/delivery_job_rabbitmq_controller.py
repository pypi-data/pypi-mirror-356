from typing import Annotated

from ed_domain.common.logging import get_logger
from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit.schemas import RabbitQueue
from rmediator.mediator import Mediator

from ed_core.application.features.delivery_job.dtos.create_delivery_job_dto import \
    CreateDeliveryJobDto
from ed_core.application.features.delivery_job.requests.commands.create_delivery_job_command import \
    CreateDeliveryJobCommand
from ed_core.common.generic_helpers import get_config
from ed_core.documentation.message_queue.rabbitmq.abc_core_rabbitmq_subscriber import \
    CoreQueues
from ed_core.webapi.dependency_setup import mediator

config = get_config()
router = RabbitRouter(config["rabbitmq"]["url"])

LOG = get_logger()


queue = RabbitQueue(name=CoreQueues.CREATE_DELIVERY_JOB, durable=True)


@router.subscriber(queue)
async def create_delivery_job(
    model: CreateDeliveryJobDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(CreateDeliveryJobCommand(dto=model))

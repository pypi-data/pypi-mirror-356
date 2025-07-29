from abc import ABC
from pydantic import BaseModel
import logging as log
from lgt_jobs.basejobs import BaseBackgroundJobData, BaseBackgroundJob
from lgt_jobs.env import smtp_login, smtp_password
from lgt_jobs.lgt_data.enums import ImageName
from redmail import EmailSender


gmail = EmailSender(
    host="smtp.gmail.com",
    port=587,
    username=smtp_login,
    password=smtp_password
)
"""
Send email
"""


class SendMailJobData(BaseBackgroundJobData, BaseModel):
    html: str
    subject: str
    recipient: str
    sender: str = "noreply@leadguru.io"
    images: list[ImageName] = []


class SendMailJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return SendMailJobData

    def exec(self, data: SendMailJobData):
        body_image = {}
        for image in data.images:
            body_image[f'IMAGE_{ImageName(image.value).name}'] = f'lgt_jobs/assets/images/{image.value}'
        with gmail:
            if not gmail.is_alive:
                gmail.connect()
            gmail.send(
                sender=f"Leadguru <{data.sender}>",
                receivers=[data.recipient],
                subject=data.subject,
                html=data.html,
                body_images=body_image
            )
        log.info('email message has been sent')

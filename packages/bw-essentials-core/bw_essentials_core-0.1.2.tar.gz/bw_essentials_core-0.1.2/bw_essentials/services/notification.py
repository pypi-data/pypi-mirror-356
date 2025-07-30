"""
Module to make API calls to Notification Service
"""
import logging

from bw_essentials.constants.services import Services
from bw_essentials.services.api_client import ApiClient

logger = logging.getLogger(__name__)


class NotificationService(ApiClient):
    """
    Handles notifications through various channels.
    """
    PLATFORM = "PLATFORM"
    NOTIFICATION_API_KEY = 'NOTIFICATION_API_KEY'
    NOTIFICATION_SENDER_NUMBER = "NOTIFICATION_SENDER_NUMBER"

    def __init__(self):
        """
        Initializes the Notification object.

        Args:
        - user: The user associated with the notification.
        """
        super().__init__("notification")
        self.name = Services.NOTIFICATION.value
        self.base_url = self.get_base_url(self.name)
        self.urls = {
            "whatsapp": "whatsapp"
        }

    def _whatsapp(self, title, template, platform, params, to, user_id):
        """
        Sends a WhatsApp notification.

        Args:
        - user_id (str): The ID of the user receiving the notification.
        - number (str): The phone number for the recipient.
        - title (str): Title of the notification.
        - template (str): Template for the WhatsApp message.
        - platform (str): The platform used for sending
            (WhatsApp, in this case).
        - params: Parameters for the notification message.

        Returns:
        None
        """
        logger.info(f"In - whatsapp {user_id =}, {to =}, "
                    f"{title =}, {template =}, {platform =}, {params =}")
        payload = {
            "from": self._get_env_var(NotificationService.NOTIFICATION_SENDER_NUMBER),
            "to": to,
            "userId": user_id,
            "platform": platform,
            "title": title,
            "template": template,
            "params": params
        }
        logger.info(f"whatsapp {payload =}")
        headers = {
            'api-key': self._get_env_var(NotificationService.NOTIFICATION_API_KEY)
        }
        self.set_headers(headers)
        resp_data = self._post(url=self.base_url, endpoint=self.urls.get('whatsapp'), data=payload)
        logger.info(f"Whatsapp response {resp_data =}")

    def send_whatsapp(self, template, title, params, to, user_id):
        logger.info(f"In - send_whatsapp_notification {user_id =} {title = } {params = } {to = }")

        self._whatsapp(title=title,
                       template=template,
                       platform=self._get_env_var(NotificationService.PLATFORM),
                       params=params,
                       to=to,
                       user_id=user_id)

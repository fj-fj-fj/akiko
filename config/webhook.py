from logging import Logger
from time import sleep
from typing import Any, Dict

logger: logger = Logger(__file__)


def configurate_webhook(self: object) -> None:
    """
    This function first gets the getWebhookinfo object.
    Then it gets the webhook URL from it, which can be empty.
    Then it checks the machine for localization. If it's a working host,
    checks for a webhook URL and hangs a hook to continue development.
    Or installs a webhook on a remote server if it was removed for some reason,
    but the development is not underway.

    """
    r: dict = _get_webhook_info(self)
    logger.debug(f'Webhook response: {r}')

    is_hook: str = r.get('result', {}).get('url')

    if self.IS_LOCALHOST:
        _set_webhook_on_localhost(is_hook, self.URL)

    if is_hook == self.APP_NAME:
        return logger.debug('Session with APP_NAME')

    _delete_webhook(self)
    sleep(0.2)
    _set_webhook(self, self.APP_NAME)


def _get_webhook_info(self: object) -> Dict[str, Any]:
    return self.session.get(f'{self.URL}getwebhookinfo').json()


def _delete_webhook(self: object) -> None:
    self.session.get(self.URL + 'deleteWebhook')


def _set_webhook(self: object, host: str) -> Dict[str, Any]:
    r: dict = self.session.get(
        f'{self.URL}setWebhook', params={'url': host}).json()
    logger.debug(f'Set webhook with {host}: {r}')
    return r


def _set_webhook_on_localhost(self: object, is_hook: str) -> None:
    from config.tunnel import TUNNEL_URL

    if is_hook == TUNNEL_URL:
        return logger.debug('Session with TUNNEL_URL')

    _delete_webhook(self)
    sleep(0.2)
    _set_webhook(self, TUNNEL_URL)

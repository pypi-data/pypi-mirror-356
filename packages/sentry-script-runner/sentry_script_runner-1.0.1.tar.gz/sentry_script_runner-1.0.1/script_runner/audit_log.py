import logging
from abc import ABC, abstractmethod

from infra_event_notifier import datadog_notifier, slack_notifier

# TODO: move this to the CLI once it exists and allow user to configure the level
logging.basicConfig(level=logging.INFO)


class AuditLogger(ABC):
    @abstractmethod
    def log(self, user: str, group: str, function: str, region: str) -> None:
        raise NotImplementedError


class StandardOutputLogger(AuditLogger):
    def __init__(self) -> None:
        self.__logger = logging.getLogger(__name__)

    def log(self, user: str, group: str, function: str, region: str) -> None:
        self.__logger.info(f"User: {user}, Group: {group}, Function: {function}")


class DatadogEventLogger(AuditLogger):
    def __init__(self, api_key: str) -> None:
        self.__notifier = datadog_notifier.DatadogNotifier(api_key)

    def log(self, user: str, group: str, function: str, region: str) -> None:
        self.__notifier.send(
            title="Script Runner Action",
            body=f"{group}:{function}",
            tags={
                "group": group,
                "function": function,
                "region": region,
                "source": "script-runner",
                "sentry_user": user,
                "source_category": "infra-tools",
            },
        )


class SlackEventLogger(AuditLogger):
    def __init__(self, eng_pipes_key: str, eng_pipes_url: str) -> None:
        self.__notifier = slack_notifier.SlackNotifier(eng_pipes_key, eng_pipes_url)

    def log(self, user: str, group: str, function: str, region: str) -> None:
        self.__notifier.send(
            title="Script Runner Action",
            body=f"User: {user}, Group: {group}, Function: {function}, Region: {region}",
        )

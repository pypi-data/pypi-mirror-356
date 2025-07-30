import logging
from time import time
from typing import Any, Dict, List, Optional, Tuple

from conftool.cli import ConftoolClient
from conftool.kvobject import Entity
from .api import RequestctlApi
from .constants import ACTION_ENTITIES
from .error import RequestctlError

logger = logging.getLogger("reqctl cleanup")
DAY_IN_SECONDS = 86400
STATE_KEEP = "keep"
STATE_LOG_MATCHING = "log_matching"
STATE_DISABLE = "disable"
STATE_DELETE = "delete"


class RequestctlCleanupReport:
    """
    Data class that holds the report of which objects should be kept, modified, or deleted.
    """

    def __init__(self):
        self.reports = {
            STATE_KEEP: [],
            STATE_LOG_MATCHING: [],
            STATE_DISABLE: [],
            STATE_DELETE: [],
        }

    def classify(self, slug: str, category: str):
        """
        Classify the object based on its properties.

        Args:
            obj: The object to classify.
        """
        if category not in self.reports.keys():
            raise ValueError(f"Unknown category: {category}")
        self.reports[category].append(slug)

    def report(self) -> Dict[str, List[str]]:
        """
        Report the classified objects.

        Returns:
            A dictionary with the classified objects.
        """
        return self.reports

    @property
    def keep(self) -> List[str]:
        """
        Get the list of objects to keep.

        Returns:
            A list of objects to keep.
        """
        return self.reports[STATE_KEEP]

    @property
    def to_log_matching(self) -> List[str]:
        """
        Get the list of objects to set to log_matching.

        Returns:
            A list of objects to set to log_matching.
        """
        return self.reports[STATE_LOG_MATCHING]

    @property
    def to_disable(self) -> List[str]:
        """
        Get the list of objects to disable.

        Returns:
            A list of objects to disable.
        """
        return self.reports[STATE_DISABLE]

    @property
    def to_delete(self) -> List[str]:
        """
        Get the list of objects to delete.

        Returns:
            A list of objects to delete.
        """
        return self.reports[STATE_DELETE]


class RequestctlMaintenance:
    """
    Class that allows to handle maintenance of the action entities.

    Specifically, it allows to perform the following actions:
    - Leave alone any filter marked with the "keep" tag.
    - For any enabled action, if it's been last modified more than 30 days ago,
      set the rule to log_matching only.
    - For any rule that is disabled but has log_matching set to true,
      disable log_matching if the rule has not been modified in the last 60 days.
    - For any rule that is disabled and has log_matching set to false,
      remove the rule if it has not been modified in the last 180 days.
    """

    def __init__(
        self,
        cl: ConftoolClient,
        dry_run: bool = False,
        enabled_days: int = 30,
        log_matching_days: int = 60,
        disabled_days: int = 180,
    ):
        """
        Initialize the RequestctlMaintenance class.

        Args:
            cl (ConftoolClient): ConftoolClient instance to use for the maintenance.
            dry_run (bool): If True, do not write to the backend, just validate all objects with
                the new schema.
            enabled_days (int): The number of days to wait before disabling an enabled rule.
            log_matching_days (int): The number of days to wait before disabling a rule that is in
                logging mode.
            disabled_days (int): The number of days to wait before deleting a disabled rule.
        """
        self.api = RequestctlApi(cl)
        self.dry_run = dry_run
        self.enabled_delay = enabled_days
        self.log_matching_delay = log_matching_days
        self.disabled_delay = disabled_days
        self.now = int(time())

    def run(self):
        logger.info("Generating report")
        report = self.report()
        for entity_name, report_obj in report.items():
            logger.info(f"Running cleanup for {entity_name}")
            self.process_report(report_obj, entity_name)

    def report(self) -> Dict[str, "RequestctlCleanupReport"]:
        """
        Report the classified objects.

        Returns:
            A dictionary with the classified objects.
        """
        report = {}
        for entity_name in ACTION_ENTITIES:
            report[entity_name] = RequestctlCleanupReport()
            for obj in self.api.all(entity_name):
                try:
                    self._report(obj, report[entity_name])
                except RequestctlError as e:
                    logger.error(f"Error processing {obj.key}: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error processing {obj.key}: {e}")
        return report

    def _report(self, entity: Entity, report: "RequestctlCleanupReport"):
        """
        Report the classified objects.

        Args:
            entity: The entity to report.
            report: The report object to update.
        """
        if entity.keep:
            report.classify(entity.pprint(), STATE_KEEP)
        elif entity.enabled:
            if self.is_older_than(entity, self.enabled_delay):
                report.classify(entity.pprint(), STATE_LOG_MATCHING)
        elif entity.log_matching:
            if self.is_older_than(entity, self.log_matching_delay):
                report.classify(entity.pprint(), STATE_DISABLE)
        elif self.is_older_than(entity, self.disabled_delay):
            report.classify(entity.pprint(), STATE_DELETE)

    def _write(self, slug: str, entity_name: str, payload: Optional[Dict[str, Any]]) -> bool:
        """
        Write the payload to the entity.

        Args:
            slug: The slug of the entity.
            entity_name: The name of the entity.
            payload: The payload to write.

        Returns:
            True if the write was successful, False otherwise.
        """
        if self.dry_run:
            if payload is None:
                logger.info(f"Would delete {entity_name}/{slug}")
            else:
                logger.info(f"Would write {payload} to {entity_name}/{slug}")
            return True
        try:
            obj = self.api.get(entity_name, slug)
            if not obj:
                logger.error(f"Object {entity_name}/{slug} not found.")
                return False
            if payload is None:
                self.api.delete(obj)
            else:
                self.api.write(obj, payload)
            return True
        except RequestctlError as e:
            logger.error(f"Error writing {payload} to {entity_name}/{slug}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error writing {payload} to {entity_name}/{slug}: {e}")
            return False

    def process_report(
        self, report: "RequestctlCleanupReport", entity_name: str
    ) -> List[Tuple[str, str]]:
        """
        Process a report.

        Args:
            report: The report to process.
        """
        errors = []
        for obj in report.keep:
            logger.debug(f"Keeping {entity_name}/{obj} because it has the 'keep' property set.")

        for obj in report.to_log_matching:
            logger.info(
                f"Setting {obj} to log_matching because it has not been modified in "
                f"the last {self.enabled_delay} days."
            )
            if not self._write(obj, entity_name, {"enabled": False, "log_matching": True}):
                errors.append((obj, STATE_LOG_MATCHING))

        for obj in report.to_disable:
            logger.info(
                f"Disabling log_matching for {obj} because it has not been modified in "
                f"the last {self.log_matching_delay} days."
            )
            if not self._write(obj, entity_name, {"log_matching": False}):
                errors.append((obj, STATE_DISABLE))

        for obj in report.to_delete:
            logger.info(
                f"Deleting {obj} because it has not been modified in the last "
                f"{self.disabled_delay} days."
            )
            if not self._write(obj, entity_name, None):
                errors.append((obj, STATE_DELETE))

        return errors

    def is_older_than(self, obj: Entity, days: int) -> bool:
        """
        Check if the object is older than the given number of days.

        Args:
            obj: The object to check.
            days: The number of days to check against.

        Returns:
            True if the object is older than the given number of days, False otherwise.
        """
        if not obj.last_modified:
            logger.debug(f"Object {obj.key} has no last_modified date.")
            return False
        if days <= 0:
            logger.debug(f"Days is less than or equal to 0: {days}.")
            return False
        return (self.now - obj.last_modified) > (days * DAY_IN_SECONDS)

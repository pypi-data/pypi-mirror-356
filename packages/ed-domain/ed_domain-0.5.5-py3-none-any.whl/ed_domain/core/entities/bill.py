from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from ed_domain.core.entities.base_entity import BaseEntity


class BillStatus(StrEnum):
    PENDING = "pending"
    WITH_DRIVER = "with_driver"
    DONE = "done"
    CANCELLED = "cancelled"


@dataclass
class Bill(BaseEntity):
    amount_in_birr: float
    bill_status: BillStatus
    due_date: datetime

    def set_complete(self):
        self.bill_status = BillStatus.DONE
        self.update()

    def set_with_driver(self):
        self.bill_status = BillStatus.WITH_DRIVER
        self.update()

    def update_status(self, new_status: BillStatus):
        if new_status not in BillStatus:
            raise ValueError(f"Invalid bill status: {new_status}")

        self.bill_status = new_status
        self.update()

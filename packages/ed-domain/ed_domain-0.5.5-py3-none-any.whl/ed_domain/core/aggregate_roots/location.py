from dataclasses import dataclass
from datetime import datetime

from ed_domain.core.entities.base_entity import BaseEntity


@dataclass
class Location(BaseEntity):
    address: str
    latitude: float
    longitude: float
    postal_code: str
    city: str
    country: str
    last_used: datetime

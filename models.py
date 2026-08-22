from dataclasses import dataclass
from typing import Optional

@dataclass
class Job:
    title:str
    company : str
    location : str
    url : str
    source :str #"reed" or "adzuna"
    salary : Optional[str] = None
    description : Optional[str] = None
    @property
    def dedup_key(self) -> str:
        """Normalized title+company, used to spot the same job listed on both sites."""
        return f"{self.title.strip().lower()}|{self.company.strip().lower()}"
    
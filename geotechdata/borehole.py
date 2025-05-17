from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd  # For generating the summary table
import matplotlib.pyplot as plt  # For plotting

@dataclass
class SPTData:
    depth: float  # Depth at which the SPT was conducted (in meters)
    blow_data: Optional[List[int]] = field(default=None)  # Optional list of blow counts for each 15 cm increment
    blow_counts: int = field(init=False)  # Total number of blows recorded, calculated from blow_data

    def __post_init__(self):
        """Calculate blow_counts as the sum of the last two numbers in blow_data."""
        if self.blow_data and len(self.blow_data) >= 2:
            self.blow_counts = sum(self.blow_data[-2:])
        else:
            self.blow_counts = 0  # Default to 0 if blow_data is None or has fewer than 2 elements

@dataclass
class BoreholeData:
    borehole_id: str  # Unique identifier for the borehole
    total_depth: Optional[float] = None  # Total depth of the borehole (in meters), optional
    spt_data: List[SPTData] = field(default_factory=list)  # List of SPT data entries

    def add_spt_data(self, depth: float, blows: Optional[List[int]] = None):
        """Add SPT data for a specific depth."""
        self.spt_data.append(SPTData(depth=depth, blow_data=blows))

    def generate_spt_summary(self) -> pd.DataFrame:
        """
        Generate a summary table of SPT results.

        Returns:
            pd.DataFrame: A DataFrame containing depth, blow data, and blow counts.
        """
        data = {
            "Depth (m)": [spt.depth for spt in self.spt_data],
            "Blow Data": [spt.blow_data for spt in self.spt_data],
            "Blow Counts": [spt.blow_counts for spt in self.spt_data],
        }
        return pd.DataFrame(data)

    def plot_blow_counts(self):
        """
        Plot blow counts versus depth as an XY line plot.
        """
        depths = [spt.depth for spt in self.spt_data]
        blow_counts = [spt.blow_counts for spt in self.spt_data]

        plt.figure(figsize=(8, 6))
        plt.plot(blow_counts, depths, marker="o", linestyle="-", color="b", label="Blow Counts")
        plt.gca().invert_yaxis()  # Invert the Y-axis to show depth increasing downward
        plt.xlabel("Blow Counts")
        plt.ylabel("Depth (m)")
        plt.title(f"SPT Blow Counts vs Depth for Borehole {self.borehole_id}")
        plt.legend()
        plt.grid(True)
        plt.show()
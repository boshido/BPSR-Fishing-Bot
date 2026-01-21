from typing import Dict, Any


class StatsTracker:
    def __init__(self):
        self.stats = {"cycles": 0, "timeouts": 0}

    def add_stat(self, stat_name: str, default_value: Any = 0) -> None:
        """Add a new stat to track"""
        if stat_name not in self.stats:
            self.stats[stat_name] = default_value

    def increment(self, stat_name: str, value: int = 1) -> None:
        """Increment a stat by a value"""
        if stat_name in self.stats:
            self.stats[stat_name] += value
        else:
            self.stats[stat_name] = value

    def set(self, stat_name: str, value: Any) -> None:
        """Set a stat to a specific value"""
        self.stats[stat_name] = value

    def get(self, stat_name: str, default: Any = None) -> Any:
        """Get a stat value"""
        return self.stats.get(stat_name, default)

    def get_all(self) -> Dict[str, Any]:
        """Get all stats as a dictionary"""
        return self.stats.copy()

    def show(self) -> None:
        """Display all stats"""
        print("\n" + "=" * 50)
        print("📊 STATISTICS")
        print("=" * 50)
        for stat, value in self.stats.items():
            title = stat.replace("_", " ").title()
            if stat == "cycles":
                title = "Cycles completed"
            elif stat == "fish_caught":
                title = "Fish caught"
            elif stat == "fish_escaped":
                title = "Fish escaped"
            elif stat == "rod_breaks":
                title = "Rod breaks"
            elif stat == "timeouts":
                title = "Timeouts"
            print(f"  {title}: {value}")
        print("=" * 50)

    def reset(self) -> None:
        """Reset all stats to zero"""
        for key in self.stats:
            self.stats[key] = 0

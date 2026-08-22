"""Template Manager for Hourly Setpoints in Emmeti Mirai."""
from __future__ import annotations
import logging
from typing import Any
from datetime import datetime

_LOGGER = logging.getLogger(__name__)


class TemplateProfile:
    """Represents a temperature profile with hourly setpoints."""

    def __init__(self, profile_id: str, name: str, description: str = "") -> None:
        self.profile_id = profile_id
        self.name = name
        self.description = description
        self.hourly_setpoints: dict[int, float] = {}
        self.active = False
        self.last_updated = datetime.now()

    def set_hourly_setpoint(self, hour: int, temperature: float) -> bool:
        """Set temperature for a specific hour (0-23)."""
        if not 0 <= hour < 24:
            _LOGGER.error("Invalid hour: %s. Must be 0-23", hour)
            return False
        if not isinstance(temperature, (int, float)):
            _LOGGER.error("Invalid temperature: %s. Must be a number", temperature)
            return False
        self.hourly_setpoints[hour] = float(temperature)
        self.last_updated = datetime.now()
        return True

    def get_hourly_setpoint(self, hour: int) -> float | None:
        """Get temperature for a specific hour."""
        if not 0 <= hour < 24:
            return None
        return self.hourly_setpoints.get(hour)

    def get_current_setpoint(self) -> float | None:
        """Get setpoint for current hour."""
        current_hour = datetime.now().hour
        return self.get_hourly_setpoint(current_hour)

    def fill_day(self, base_temperature: float) -> None:
        """Fill all 24 hours with the same base temperature."""
        for hour in range(24):
            self.hourly_setpoints[hour] = base_temperature
        self.last_updated = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        """Convert profile to dictionary."""
        return {
            "profile_id": self.profile_id,
            "name": self.name,
            "description": self.description,
            "hourly_setpoints": self.hourly_setpoints,
            "active": self.active,
            "last_updated": self.last_updated.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TemplateProfile:
        """Create profile from dictionary."""
        profile = cls(
            data["profile_id"],
            data["name"],
            data.get("description", "")
        )
        profile.hourly_setpoints = data.get("hourly_setpoints", {})
        profile.active = data.get("active", False)
        if "last_updated" in data:
            profile.last_updated = datetime.fromisoformat(data["last_updated"])
        return profile


class TemplateManager:
    """Manages temperature profiles and hourly setpoints."""

    def __init__(self) -> None:
        self._profiles: dict[str, TemplateProfile] = {}
        self._active_profile: str | None = None

    def create_profile(self, profile_id: str, name: str, description: str = "") -> TemplateProfile:
        """Create a new template profile."""
        if profile_id in self._profiles:
            _LOGGER.warning("Profile %s already exists", profile_id)
            return self._profiles[profile_id]
        profile = TemplateProfile(profile_id, name, description)
        self._profiles[profile_id] = profile
        _LOGGER.info("Created profile: %s", profile_id)
        return profile

    def get_profile(self, profile_id: str) -> TemplateProfile | None:
        """Get a profile by ID."""
        return self._profiles.get(profile_id)

    def list_profiles(self) -> list[TemplateProfile]:
        """List all profiles."""
        return list(self._profiles.values())

    def delete_profile(self, profile_id: str) -> bool:
        """Delete a profile."""
        if profile_id not in self._profiles:
            _LOGGER.warning("Profile %s not found", profile_id)
            return False
        if self._active_profile == profile_id:
            self._active_profile = None
        del self._profiles[profile_id]
        _LOGGER.info("Deleted profile: %s", profile_id)
        return True

    def activate_profile(self, profile_id: str) -> bool:
        """Activate a profile."""
        if profile_id not in self._profiles:
            _LOGGER.warning("Profile %s not found", profile_id)
            return False
        if self._active_profile:
            self._profiles[self._active_profile].active = False
        self._active_profile = profile_id
        self._profiles[profile_id].active = True
        _LOGGER.info("Activated profile: %s", profile_id)
        return True

    def get_active_profile(self) -> TemplateProfile | None:
        """Get the currently active profile."""
        if not self._active_profile:
            return None
        return self._profiles.get(self._active_profile)

    def get_current_setpoint(self) -> float | None:
        """Get setpoint for current hour from active profile."""
        profile = self.get_active_profile()
        if not profile:
            return None
        return profile.get_current_setpoint()

    def to_dict(self) -> dict[str, Any]:
        """Convert manager state to dictionary."""
        return {
            "profiles": {pid: p.to_dict() for pid, p in self._profiles.items()},
            "active_profile": self._active_profile,
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        """Load manager state from dictionary."""
        self._profiles = {}
        for profile_data in data.get("profiles", {}).values():
            profile = TemplateProfile.from_dict(profile_data)
            self._profiles[profile.profile_id] = profile
        self._active_profile = data.get("active_profile")
        _LOGGER.info("Loaded %d profiles", len(self._profiles))

"""
    * SPDX-FileCopyrightText: Copyright 2024 LG Electronics Inc.
    * SPDX-License-Identifier: Apache-2.0
"""
from typing import Any

from ..thinq_api import ThinQApi
from .connect_device import ConnectSubDeviceProfile
from .const import Location, Property, Resource
from .washer import WasherSubDevice


class WashcomboProfile(ConnectSubDeviceProfile):
    def __init__(self, profile: dict[str, Any], location_name: Location = None, use_sub_notification: bool = False):
        super().__init__(
            profile,
            location_name=location_name,
            resource_map={
                "runState": Resource.RUN_STATE,
                "operation": Resource.OPERATION,
                "mode": Resource.MODE,
                "remoteControlEnable": Resource.REMOTE_CONTROL_ENABLE,
                "timer": Resource.TIMER,
                "detergent": Resource.DETERGENT,
                "cycle": Resource.CYCLE,
            },
            profile_map={
                "runState": {"currentState": Property.CURRENT_STATE},
                "operation": {
                    "washerOperationMode": Property.WASHER_OPERATION_MODE,
                },
                "mode": {
                    "washerMode": Property.WASHER_MODE,
                },
                "remoteControlEnable": {"remoteControlEnabled": Property.REMOTE_CONTROL_ENABLED},
                "timer": {
                    "remainHour": Property.REMAIN_HOUR,
                    "remainMinute": Property.REMAIN_MINUTE,
                    "totalHour": Property.TOTAL_HOUR,
                    "totalMinute": Property.TOTAL_MINUTE,
                    "relativeHourToStop": Property.RELATIVE_HOUR_TO_STOP,
                    "relativeMinuteToStop": Property.RELATIVE_MINUTE_TO_STOP,
                    "relativeHourToStart": Property.RELATIVE_HOUR_TO_START,
                    "relativeMinuteToStart": Property.RELATIVE_MINUTE_TO_START,
                },
                "detergent": {"detergentSetting": Property.DETERGENT_SETTING},
                "cycle": {"cycleCount": Property.CYCLE_COUNT},
            },
            use_sub_notification=use_sub_notification,
        )

    def generate_properties(self, property: list[dict[str, Any]] | dict[str, Any]) -> None:
        """Get properties."""
        if isinstance(property, list):
            for location_property in property:
                if location_property.get("location", {}).get("locationName") != self._location_name:
                    continue
                super().generate_properties(location_property)
        else:
            super().generate_properties(property)


class WashcomboDevice(WasherSubDevice):
    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str):
        self._location = value

    @property
    def group_id(self) -> str:
        return self._group_id

    @group_id.setter
    def group_id(self, value: str):
        self._group_id = value

    async def set_washer_operation_mode(self, operation: str) -> dict | None:
        payload = self.profiles.get_enum_attribute_payload(Property.WASHER_OPERATION_MODE, operation)
        return await self._do_attribute_command({"location": {"locationName": self.location}, **payload})

    async def set_washer_mode(self, mode: str) -> dict | None:
        operation_payload = self.profiles.get_enum_attribute_payload(Property.WASHER_OPERATION_MODE, "START")
        payload = self.profiles.get_enum_attribute_payload(Property.WASHER_MODE, mode)
        return await self._do_attribute_command(
            {"location": {"locationName": self.location}, **operation_payload, **payload}
        )

    async def set_relative_hour_to_start(self, hour: int) -> dict | None:
        payload = self.profiles.get_range_attribute_payload(Property.RELATIVE_HOUR_TO_START, hour)
        return await self._do_attribute_command({"location": {"locationName": self.location}, **payload})

    async def set_relative_hour_to_stop(self, hour: int) -> dict | None:
        payload = self.profiles.get_range_attribute_payload(Property.RELATIVE_HOUR_TO_STOP, hour)
        return await self._do_attribute_command({"location": {"locationName": self.location}, **payload})

    def __init__(
        self,
        thinq_api: ThinQApi,
        device_id: str,
        device_type: str,
        model_name: str,
        alias: str,
        group_id: str,
        reportable: bool,
        profile: dict[str, Any],
        location: str,
    ):
        super().__init__(
            profiles=WashcomboProfile(profile=profile, location_name=location, use_sub_notification=True),
            location_name=location,
            single_unit=True,
            thinq_api=thinq_api,
            device_id=device_id,
            device_type=device_type,
            model_name=model_name,
            alias=alias,
            reportable=reportable,
        )
        self.group_id = group_id
        self.location = location

"""Merrytek MSA 201Z Tuya 24GHz microwave presence sensor"""

from zigpy.quirks.v2 import EntityPlatform, EntityType
from zigpy.quirks.v2.homeassistant import UnitOfLength, UnitOfTime
from zigpy.quirks.v2.homeassistant.sensor import SensorDeviceClass, SensorStateClass
import zigpy.types as t
from zigpy.zcl.clusters.measurement import OccupancySensing

from zhaquirks.tuya import TuyaLocalCluster
from zhaquirks.tuya.builder import TuyaQuirkBuilder


class TuyaOccupancySensing(OccupancySensing, TuyaLocalCluster):
    """Tuya local OccupancySensing cluster."""


class TuyaEnvironmentAdaptingMode(t.enum8):
    """Tuya presence state enum."""

    Default = 0x00
    Minor = 0x01
    Medium = 0x02
    Deep = 0x03
    Adapting = 0x04


class TuyaBreathingDetectionMode(t.enum8):
    """Tuya breathing detection mode enum."""

    Off = 0x00
    On = 0x01


class TuyaStatusIndication(t.enum8):
    """Tuya status indication enum."""

    Approaching = 0x00
    Departing = 0x01
    Clear = 0x02


class TuyaLedIndicatorMode(t.enum8):
    """Tuya LED indicator enum."""

    Off = 0x00
    On = 0x01


class TuyaEnableSensorMode(t.enum8):
    """Tuya status indication enum."""

    Off = 0x00
    On = 0x01


class TuyaMotionPresenceSensitivityMode(t.enum8): 
    """Tuya motion presence sensitivity enum."""

    Low = 0x00
    Medium = 0x01
    High = 0x02


# Merrytek MSA 201Z
(
    TuyaQuirkBuilder("_TZE200_hyhl5y36", "TS0601")
    .tuya_dp(
        dp_id=1,
        ep_attribute=TuyaOccupancySensing.ep_attribute,
        attribute_name=OccupancySensing.AttributeDefs.occupancy.name,
        converter=lambda x: True if x in (1, 2) else False,
    )
    .adds(TuyaOccupancySensing)
    .tuya_number(
        dp_id=2,
        attribute_name="trigger_distance",
        type=t.uint16_t,
        device_class=SensorDeviceClass.DISTANCE,
        unit=UnitOfLength.METERS,
        min_value=0,
        max_value=4,
        step=0.1,
        translation_key="trigger_distance",
        fallback_name="Trigger distance",
    )
    .tuya_illuminance(dp_id=101)
    .tuya_number(
        dp_id=102,
        attribute_name="lux_change_trigger",
        type=t.uint16_t,
        device_class=SensorDeviceClass.ILLUMINANCE,
        min_value=10,
        max_value=100,
        step=10,
        translation_key="lux_change_trigger",
        fallback_name="Lux Change Trigger",
    )
    .tuya_enum(
        dp_id=103,
        attribute_name="environment_adapting",
        enum_class=TuyaEnvironmentAdaptingMode,
        translation_key="environment_adapting",
        fallback_name="Environment adapting",
    )
    .tuya_sensor(
        dp_id=104,
        attribute_name="presence_duration",
        type=t.uint16_t,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DURATION,
        unit=UnitOfTime.MINUTES,
        translation_key="presence_duration",
        fallback_name="Presence duration",
    )
    .tuya_sensor(
        dp_id=105,
        attribute_name="absence_duration",
        type=t.uint16_t,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DURATION,
        unit=UnitOfTime.MINUTES,
        translation_key="absence_duration",
        fallback_name="Absence duration",
    )
    .tuya_number(
        dp_id=106,
        attribute_name="hold_time",
        type=t.uint16_t,
        device_class=SensorDeviceClass.DURATION,
        unit=UnitOfTime.SECONDS,
        min_value=3,
        max_value=7200,
        step=1,
        translation_key="hold_time",
        fallback_name="Hold Time",
    )
    .tuya_enum(
        dp_id=107,
        attribute_name="indicator",
        enum_class=TuyaLedIndicatorMode,
        translation_key="indicator",
        fallback_name="Indicator",
    )
    .tuya_enum(
        dp_id=108,
        attribute_name="current_status",
        enum_class=TuyaStatusIndication,
        entity_platform=EntityPlatform.SENSOR,
        entity_type=EntityType.STANDARD,
        translation_key="current_status",
        fallback_name="Current status",
    )
    .tuya_enum(
        dp_id=109,
        attribute_name="enable_sensor",
        enum_class=TuyaEnableSensorMode,
        translation_key="enable_sensor",
        fallback_name="Enable sensor",
    )
    .tuya_enum(
        dp_id=110,
        attribute_name="sensitivity_setting",
        enum_class=TuyaMotionPresenceSensitivityMode,
        translation_key="sensitivity_setting",
        fallback_name="Sensitivity setting",
    )
    .tuya_enum(
        dp_id=111,
        attribute_name="breathing_detection",
        enum_class=TuyaBreathingDetectionMode,
        translation_key="breathing_detection",
        fallback_name="Breathing detection",
    )
    # Not sure what this is for, but it's visible in the Tuya Developer Platform. Assuming it's an enum, but not implementing.
    # .tuya_enum(
    #     dp_id=112,
    #     attribute_name="status_flip",
    #     enum_class=TuyaStatusFlipIndicationMode,
    #     entity_platform=EntityPlatform.SENSOR,
    #     entity_type=EntityType.STANDARD,
    #     translation_key="status_flip",
    #     fallback_name="Status flip",
    # )
    .skip_configuration()
    .add_to_registry()
)
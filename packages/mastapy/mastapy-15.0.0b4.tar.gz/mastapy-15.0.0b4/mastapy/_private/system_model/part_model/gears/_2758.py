"""ConicalGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.gears import _2765

_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1274
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2669, _2692, _2696
    from mastapy._private.system_model.part_model.gears import (
        _2748,
        _2750,
        _2752,
        _2753,
        _2754,
        _2766,
        _2769,
        _2771,
        _2773,
        _2775,
        _2779,
        _2781,
        _2783,
        _2785,
        _2786,
        _2789,
    )

    Self = TypeVar("Self", bound="ConicalGear")
    CastSelf = TypeVar("CastSelf", bound="ConicalGear._Cast_ConicalGear")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGear:
    """Special nested class for casting ConicalGear to subclasses."""

    __parent__: "ConicalGear"

    @property
    def gear(self: "CastSelf") -> "_2765.Gear":
        return self.__parent__._cast(_2765.Gear)

    @property
    def mountable_component(self: "CastSelf") -> "_2692.MountableComponent":
        from mastapy._private.system_model.part_model import _2692

        return self.__parent__._cast(_2692.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2669.Component":
        from mastapy._private.system_model.part_model import _2669

        return self.__parent__._cast(_2669.Component)

    @property
    def part(self: "CastSelf") -> "_2696.Part":
        from mastapy._private.system_model.part_model import _2696

        return self.__parent__._cast(_2696.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2748.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2748

        return self.__parent__._cast(_2748.AGMAGleasonConicalGear)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2750.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2750

        return self.__parent__._cast(_2750.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2752.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2752

        return self.__parent__._cast(_2752.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2753.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2753

        return self.__parent__._cast(_2753.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2754.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2754

        return self.__parent__._cast(_2754.BevelGear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2769.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2769

        return self.__parent__._cast(_2769.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2771.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2771

        return self.__parent__._cast(_2771.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2773.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2773

        return self.__parent__._cast(_2773.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2775.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2775

        return self.__parent__._cast(_2775.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2779.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2779

        return self.__parent__._cast(_2779.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2781.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2781

        return self.__parent__._cast(_2781.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2783.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2783

        return self.__parent__._cast(_2783.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2785.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2785

        return self.__parent__._cast(_2785.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2786.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2786

        return self.__parent__._cast(_2786.StraightBevelSunGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2789.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2789

        return self.__parent__._cast(_2789.ZerolBevelGear)

    @property
    def conical_gear(self: "CastSelf") -> "ConicalGear":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class ConicalGear(_2765.Gear):
    """ConicalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def orientation(self: "Self") -> "_2766.GearOrientations":
        """mastapy.system_model.part_model.gears.GearOrientations"""
        temp = pythonnet_property_get(self.wrapped, "Orientation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PartModel.Gears.GearOrientations"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model.gears._2766", "GearOrientations"
        )(value)

    @orientation.setter
    @exception_bridge
    @enforce_parameter_types
    def orientation(self: "Self", value: "_2766.GearOrientations") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PartModel.Gears.GearOrientations"
        )
        pythonnet_property_set(self.wrapped, "Orientation", value)

    @property
    @exception_bridge
    def active_gear_design(self: "Self") -> "_1274.ConicalGearDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def conical_gear_design(self: "Self") -> "_1274.ConicalGearDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGear":
        """Cast to another type.

        Returns:
            _Cast_ConicalGear
        """
        return _Cast_ConicalGear(self)

"""MountableComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2669

_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import (
        _2490,
        _2493,
        _2497,
    )
    from mastapy._private.system_model.part_model import (
        _2660,
        _2664,
        _2670,
        _2672,
        _2688,
        _2689,
        _2694,
        _2696,
        _2698,
        _2700,
        _2701,
        _2707,
        _2709,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2816,
        _2819,
        _2822,
        _2825,
        _2827,
        _2829,
        _2836,
        _2838,
        _2845,
        _2848,
        _2849,
        _2850,
        _2852,
        _2854,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2806
    from mastapy._private.system_model.part_model.gears import (
        _2748,
        _2750,
        _2752,
        _2753,
        _2754,
        _2756,
        _2758,
        _2760,
        _2762,
        _2763,
        _2765,
        _2769,
        _2771,
        _2773,
        _2775,
        _2779,
        _2781,
        _2783,
        _2785,
        _2786,
        _2787,
        _2789,
    )

    Self = TypeVar("Self", bound="MountableComponent")
    CastSelf = TypeVar("CastSelf", bound="MountableComponent._Cast_MountableComponent")


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponent:
    """Special nested class for casting MountableComponent to subclasses."""

    __parent__: "MountableComponent"

    @property
    def component(self: "CastSelf") -> "_2669.Component":
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
    def bearing(self: "CastSelf") -> "_2664.Bearing":
        from mastapy._private.system_model.part_model import _2664

        return self.__parent__._cast(_2664.Bearing)

    @property
    def connector(self: "CastSelf") -> "_2672.Connector":
        from mastapy._private.system_model.part_model import _2672

        return self.__parent__._cast(_2672.Connector)

    @property
    def mass_disc(self: "CastSelf") -> "_2688.MassDisc":
        from mastapy._private.system_model.part_model import _2688

        return self.__parent__._cast(_2688.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2689.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2689

        return self.__parent__._cast(_2689.MeasurementComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2694.OilSeal":
        from mastapy._private.system_model.part_model import _2694

        return self.__parent__._cast(_2694.OilSeal)

    @property
    def planet_carrier(self: "CastSelf") -> "_2698.PlanetCarrier":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.PlanetCarrier)

    @property
    def point_load(self: "CastSelf") -> "_2700.PointLoad":
        from mastapy._private.system_model.part_model import _2700

        return self.__parent__._cast(_2700.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2701.PowerLoad":
        from mastapy._private.system_model.part_model import _2701

        return self.__parent__._cast(_2701.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2707.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2707

        return self.__parent__._cast(_2707.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2709.VirtualComponent":
        from mastapy._private.system_model.part_model import _2709

        return self.__parent__._cast(_2709.VirtualComponent)

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
    def concept_gear(self: "CastSelf") -> "_2756.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2756

        return self.__parent__._cast(_2756.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2758.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2758

        return self.__parent__._cast(_2758.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2760.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2760

        return self.__parent__._cast(_2760.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2762.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2762

        return self.__parent__._cast(_2762.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2763.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2763

        return self.__parent__._cast(_2763.FaceGear)

    @property
    def gear(self: "CastSelf") -> "_2765.Gear":
        from mastapy._private.system_model.part_model.gears import _2765

        return self.__parent__._cast(_2765.Gear)

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
    def worm_gear(self: "CastSelf") -> "_2787.WormGear":
        from mastapy._private.system_model.part_model.gears import _2787

        return self.__parent__._cast(_2787.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2789.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2789

        return self.__parent__._cast(_2789.ZerolBevelGear)

    @property
    def ring_pins(self: "CastSelf") -> "_2806.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2806

        return self.__parent__._cast(_2806.RingPins)

    @property
    def clutch_half(self: "CastSelf") -> "_2816.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2816

        return self.__parent__._cast(_2816.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2819.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2819

        return self.__parent__._cast(_2819.ConceptCouplingHalf)

    @property
    def coupling_half(self: "CastSelf") -> "_2822.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2822

        return self.__parent__._cast(_2822.CouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2825.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2825

        return self.__parent__._cast(_2825.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2827.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2827

        return self.__parent__._cast(_2827.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2829.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2829

        return self.__parent__._cast(_2829.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2836.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2836

        return self.__parent__._cast(_2836.RollingRing)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2838.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2838

        return self.__parent__._cast(_2838.ShaftHubConnection)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2845.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2845

        return self.__parent__._cast(_2845.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2848.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2848

        return self.__parent__._cast(_2848.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2849.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2849

        return self.__parent__._cast(_2849.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2850.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2850

        return self.__parent__._cast(_2850.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2852.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2852

        return self.__parent__._cast(_2852.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2854.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2854

        return self.__parent__._cast(_2854.TorqueConverterTurbine)

    @property
    def mountable_component(self: "CastSelf") -> "MountableComponent":
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
class MountableComponent(_2669.Component):
    """MountableComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def rotation_about_axis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAboutAxis")

        if temp is None:
            return 0.0

        return temp

    @rotation_about_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def rotation_about_axis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotationAboutAxis",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def inner_component(self: "Self") -> "_2660.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_connection(self: "Self") -> "_2493.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_socket(self: "Self") -> "_2497.CylindricalSocket":
        """mastapy.system_model.connections_and_sockets.CylindricalSocket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSocket")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def is_mounted(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsMounted")

        if temp is None:
            return False

        return temp

    @exception_bridge
    @enforce_parameter_types
    def mount_on(
        self: "Self", shaft: "_2660.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2490.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def try_mount_on(
        self: "Self", shaft: "_2660.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2670.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryMountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponent":
        """Cast to another type.

        Returns:
            _Cast_MountableComponent
        """
        return _Cast_MountableComponent(self)

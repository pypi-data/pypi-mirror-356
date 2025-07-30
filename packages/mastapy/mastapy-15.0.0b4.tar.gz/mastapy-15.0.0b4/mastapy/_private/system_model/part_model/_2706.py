"""SpecialisedAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2659

_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2668, _2680, _2691, _2696
    from mastapy._private.system_model.part_model.couplings import (
        _2813,
        _2815,
        _2818,
        _2821,
        _2824,
        _2826,
        _2837,
        _2844,
        _2846,
        _2851,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2804
    from mastapy._private.system_model.part_model.gears import (
        _2749,
        _2751,
        _2755,
        _2757,
        _2759,
        _2761,
        _2764,
        _2767,
        _2770,
        _2772,
        _2774,
        _2776,
        _2777,
        _2780,
        _2782,
        _2784,
        _2788,
        _2790,
    )

    Self = TypeVar("Self", bound="SpecialisedAssembly")
    CastSelf = TypeVar(
        "CastSelf", bound="SpecialisedAssembly._Cast_SpecialisedAssembly"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssembly:
    """Special nested class for casting SpecialisedAssembly to subclasses."""

    __parent__: "SpecialisedAssembly"

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        return self.__parent__._cast(_2659.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2696.Part":
        from mastapy._private.system_model.part_model import _2696

        return self.__parent__._cast(_2696.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def bolted_joint(self: "CastSelf") -> "_2668.BoltedJoint":
        from mastapy._private.system_model.part_model import _2668

        return self.__parent__._cast(_2668.BoltedJoint)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2680.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2680

        return self.__parent__._cast(_2680.FlexiblePinAssembly)

    @property
    def microphone_array(self: "CastSelf") -> "_2691.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2691

        return self.__parent__._cast(_2691.MicrophoneArray)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2749.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2749

        return self.__parent__._cast(_2749.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2751.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2751

        return self.__parent__._cast(_2751.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2755.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2755

        return self.__parent__._cast(_2755.BevelGearSet)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2757.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2757

        return self.__parent__._cast(_2757.ConceptGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2759.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2759

        return self.__parent__._cast(_2759.ConicalGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2761.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2761

        return self.__parent__._cast(_2761.CylindricalGearSet)

    @property
    def face_gear_set(self: "CastSelf") -> "_2764.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2764

        return self.__parent__._cast(_2764.FaceGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2767.GearSet":
        from mastapy._private.system_model.part_model.gears import _2767

        return self.__parent__._cast(_2767.GearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2770.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2770

        return self.__parent__._cast(_2770.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2772.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2772

        return self.__parent__._cast(_2772.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2774.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2774

        return self.__parent__._cast(_2774.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2776.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2776

        return self.__parent__._cast(_2776.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2777.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2777

        return self.__parent__._cast(_2777.PlanetaryGearSet)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2780.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2780

        return self.__parent__._cast(_2780.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2782.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2782

        return self.__parent__._cast(_2782.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2784.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2784

        return self.__parent__._cast(_2784.StraightBevelGearSet)

    @property
    def worm_gear_set(self: "CastSelf") -> "_2788.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2788

        return self.__parent__._cast(_2788.WormGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2790.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2790

        return self.__parent__._cast(_2790.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2804.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2804

        return self.__parent__._cast(_2804.CycloidalAssembly)

    @property
    def belt_drive(self: "CastSelf") -> "_2813.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2813

        return self.__parent__._cast(_2813.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2815.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2815

        return self.__parent__._cast(_2815.Clutch)

    @property
    def concept_coupling(self: "CastSelf") -> "_2818.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2818

        return self.__parent__._cast(_2818.ConceptCoupling)

    @property
    def coupling(self: "CastSelf") -> "_2821.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2821

        return self.__parent__._cast(_2821.Coupling)

    @property
    def cvt(self: "CastSelf") -> "_2824.CVT":
        from mastapy._private.system_model.part_model.couplings import _2824

        return self.__parent__._cast(_2824.CVT)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2826.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2826

        return self.__parent__._cast(_2826.PartToPartShearCoupling)

    @property
    def rolling_ring_assembly(self: "CastSelf") -> "_2837.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2837

        return self.__parent__._cast(_2837.RollingRingAssembly)

    @property
    def spring_damper(self: "CastSelf") -> "_2844.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2844

        return self.__parent__._cast(_2844.SpringDamper)

    @property
    def synchroniser(self: "CastSelf") -> "_2846.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2846

        return self.__parent__._cast(_2846.Synchroniser)

    @property
    def torque_converter(self: "CastSelf") -> "_2851.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2851

        return self.__parent__._cast(_2851.TorqueConverter)

    @property
    def specialised_assembly(self: "CastSelf") -> "SpecialisedAssembly":
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
class SpecialisedAssembly(_2659.AbstractAssembly):
    """SpecialisedAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssembly":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssembly
        """
        return _Cast_SpecialisedAssembly(self)

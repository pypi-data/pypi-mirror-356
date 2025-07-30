"""AGMAGleasonConicalGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2759

_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2659, _2696, _2706
    from mastapy._private.system_model.part_model.gears import (
        _2751,
        _2755,
        _2767,
        _2770,
        _2780,
        _2782,
        _2784,
        _2790,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearSet")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearSet:
    """Special nested class for casting AGMAGleasonConicalGearSet to subclasses."""

    __parent__: "AGMAGleasonConicalGearSet"

    @property
    def conical_gear_set(self: "CastSelf") -> "_2759.ConicalGearSet":
        return self.__parent__._cast(_2759.ConicalGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2767.GearSet":
        from mastapy._private.system_model.part_model.gears import _2767

        return self.__parent__._cast(_2767.GearSet)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2706.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2706

        return self.__parent__._cast(_2706.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2659

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
    def hypoid_gear_set(self: "CastSelf") -> "_2770.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2770

        return self.__parent__._cast(_2770.HypoidGearSet)

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
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2790.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2790

        return self.__parent__._cast(_2790.ZerolBevelGearSet)

    @property
    def agma_gleason_conical_gear_set(self: "CastSelf") -> "AGMAGleasonConicalGearSet":
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
class AGMAGleasonConicalGearSet(_2759.ConicalGearSet):
    """AGMAGleasonConicalGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearSet":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearSet
        """
        return _Cast_AGMAGleasonConicalGearSet(self)

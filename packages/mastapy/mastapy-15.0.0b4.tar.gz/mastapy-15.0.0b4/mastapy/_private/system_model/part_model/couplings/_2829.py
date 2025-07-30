"""Pulley"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.couplings import _2822

_PULLEY = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Pulley")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2669, _2692, _2696
    from mastapy._private.system_model.part_model.couplings import _2825

    Self = TypeVar("Self", bound="Pulley")
    CastSelf = TypeVar("CastSelf", bound="Pulley._Cast_Pulley")


__docformat__ = "restructuredtext en"
__all__ = ("Pulley",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Pulley:
    """Special nested class for casting Pulley to subclasses."""

    __parent__: "Pulley"

    @property
    def coupling_half(self: "CastSelf") -> "_2822.CouplingHalf":
        return self.__parent__._cast(_2822.CouplingHalf)

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
    def cvt_pulley(self: "CastSelf") -> "_2825.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2825

        return self.__parent__._cast(_2825.CVTPulley)

    @property
    def pulley(self: "CastSelf") -> "Pulley":
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
class Pulley(_2822.CouplingHalf):
    """Pulley

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PULLEY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_Pulley":
        """Cast to another type.

        Returns:
            _Cast_Pulley
        """
        return _Cast_Pulley(self)

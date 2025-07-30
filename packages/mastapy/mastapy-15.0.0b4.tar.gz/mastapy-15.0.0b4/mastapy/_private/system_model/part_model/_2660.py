"""AbstractShaft"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2661

_ABSTRACT_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaft"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2669, _2696
    from mastapy._private.system_model.part_model.cycloidal import _2805
    from mastapy._private.system_model.part_model.shaft_model import _2712

    Self = TypeVar("Self", bound="AbstractShaft")
    CastSelf = TypeVar("CastSelf", bound="AbstractShaft._Cast_AbstractShaft")


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaft:
    """Special nested class for casting AbstractShaft to subclasses."""

    __parent__: "AbstractShaft"

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2661.AbstractShaftOrHousing":
        return self.__parent__._cast(_2661.AbstractShaftOrHousing)

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
    def shaft(self: "CastSelf") -> "_2712.Shaft":
        from mastapy._private.system_model.part_model.shaft_model import _2712

        return self.__parent__._cast(_2712.Shaft)

    @property
    def cycloidal_disc(self: "CastSelf") -> "_2805.CycloidalDisc":
        from mastapy._private.system_model.part_model.cycloidal import _2805

        return self.__parent__._cast(_2805.CycloidalDisc)

    @property
    def abstract_shaft(self: "CastSelf") -> "AbstractShaft":
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
class AbstractShaft(_2661.AbstractShaftOrHousing):
    """AbstractShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaft":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaft
        """
        return _Cast_AbstractShaft(self)

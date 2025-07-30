"""AbstractShaftFromCAD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.import_from_cad import _2728

_ABSTRACT_SHAFT_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "AbstractShaftFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import (
        _2729,
        _2739,
        _2743,
    )

    Self = TypeVar("Self", bound="AbstractShaftFromCAD")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractShaftFromCAD._Cast_AbstractShaftFromCAD"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftFromCAD:
    """Special nested class for casting AbstractShaftFromCAD to subclasses."""

    __parent__: "AbstractShaftFromCAD"

    @property
    def component_from_cad(self: "CastSelf") -> "_2728.ComponentFromCAD":
        return self.__parent__._cast(_2728.ComponentFromCAD)

    @property
    def component_from_cad_base(self: "CastSelf") -> "_2729.ComponentFromCADBase":
        from mastapy._private.system_model.part_model.import_from_cad import _2729

        return self.__parent__._cast(_2729.ComponentFromCADBase)

    @property
    def planet_shaft_from_cad(self: "CastSelf") -> "_2739.PlanetShaftFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2739

        return self.__parent__._cast(_2739.PlanetShaftFromCAD)

    @property
    def shaft_from_cad(self: "CastSelf") -> "_2743.ShaftFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2743

        return self.__parent__._cast(_2743.ShaftFromCAD)

    @property
    def abstract_shaft_from_cad(self: "CastSelf") -> "AbstractShaftFromCAD":
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
class AbstractShaftFromCAD(_2728.ComponentFromCAD):
    """AbstractShaftFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def offset(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftFromCAD":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftFromCAD
        """
        return _Cast_AbstractShaftFromCAD(self)

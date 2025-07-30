"""SynchroniserSleeve"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.couplings import _2849

_SYNCHRONISER_SLEEVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserSleeve"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2669, _2692, _2696
    from mastapy._private.system_model.part_model.couplings import _2822

    Self = TypeVar("Self", bound="SynchroniserSleeve")
    CastSelf = TypeVar("CastSelf", bound="SynchroniserSleeve._Cast_SynchroniserSleeve")


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserSleeve",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserSleeve:
    """Special nested class for casting SynchroniserSleeve to subclasses."""

    __parent__: "SynchroniserSleeve"

    @property
    def synchroniser_part(self: "CastSelf") -> "_2849.SynchroniserPart":
        return self.__parent__._cast(_2849.SynchroniserPart)

    @property
    def coupling_half(self: "CastSelf") -> "_2822.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2822

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
    def synchroniser_sleeve(self: "CastSelf") -> "SynchroniserSleeve":
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
class SynchroniserSleeve(_2849.SynchroniserPart):
    """SynchroniserSleeve

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER_SLEEVE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def hub_bore(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "HubBore")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @hub_bore.setter
    @exception_bridge
    @enforce_parameter_types
    def hub_bore(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "HubBore", value)

    @property
    @exception_bridge
    def hub_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HubHeight")

        if temp is None:
            return 0.0

        return temp

    @hub_height.setter
    @exception_bridge
    @enforce_parameter_types
    def hub_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HubHeight", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def hub_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HubWidth")

        if temp is None:
            return 0.0

        return temp

    @hub_width.setter
    @exception_bridge
    @enforce_parameter_types
    def hub_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HubWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def sleeve_outer_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SleeveOuterDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @sleeve_outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def sleeve_outer_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SleeveOuterDiameter", value)

    @property
    @exception_bridge
    def sleeve_selection_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SleeveSelectionHeight")

        if temp is None:
            return 0.0

        return temp

    @sleeve_selection_height.setter
    @exception_bridge
    @enforce_parameter_types
    def sleeve_selection_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SleeveSelectionHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def sleeve_selection_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SleeveSelectionWidth")

        if temp is None:
            return 0.0

        return temp

    @sleeve_selection_width.setter
    @exception_bridge
    @enforce_parameter_types
    def sleeve_selection_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SleeveSelectionWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def sleeve_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SleeveWidth")

        if temp is None:
            return 0.0

        return temp

    @sleeve_width.setter
    @exception_bridge
    @enforce_parameter_types
    def sleeve_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SleeveWidth", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SynchroniserSleeve":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserSleeve
        """
        return _Cast_SynchroniserSleeve(self)

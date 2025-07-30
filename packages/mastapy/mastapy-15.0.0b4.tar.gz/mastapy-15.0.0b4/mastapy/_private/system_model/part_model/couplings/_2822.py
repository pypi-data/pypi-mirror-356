"""CouplingHalf"""

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
from mastapy._private.system_model.part_model import _2692

_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2669, _2696
    from mastapy._private.system_model.part_model.couplings import (
        _2816,
        _2819,
        _2825,
        _2827,
        _2829,
        _2836,
        _2845,
        _2848,
        _2849,
        _2850,
        _2852,
        _2854,
    )

    Self = TypeVar("Self", bound="CouplingHalf")
    CastSelf = TypeVar("CastSelf", bound="CouplingHalf._Cast_CouplingHalf")


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalf",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalf:
    """Special nested class for casting CouplingHalf to subclasses."""

    __parent__: "CouplingHalf"

    @property
    def mountable_component(self: "CastSelf") -> "_2692.MountableComponent":
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
    def clutch_half(self: "CastSelf") -> "_2816.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2816

        return self.__parent__._cast(_2816.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2819.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2819

        return self.__parent__._cast(_2819.ConceptCouplingHalf)

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
    def coupling_half(self: "CastSelf") -> "CouplingHalf":
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
class CouplingHalf(_2692.MountableComponent):
    """CouplingHalf

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bore(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bore.setter
    @exception_bridge
    @enforce_parameter_types
    def bore(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Bore", value)

    @property
    @exception_bridge
    def diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Diameter", value)

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalf":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalf
        """
        return _Cast_CouplingHalf(self)

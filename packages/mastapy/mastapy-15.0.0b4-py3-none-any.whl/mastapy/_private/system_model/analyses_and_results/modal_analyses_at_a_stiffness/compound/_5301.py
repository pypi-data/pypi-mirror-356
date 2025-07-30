"""CouplingHalfCompoundModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5341,
)

_COUPLING_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "CouplingHalfCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5167,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5285,
        _5287,
        _5290,
        _5304,
        _5343,
        _5346,
        _5352,
        _5356,
        _5368,
        _5378,
        _5379,
        _5380,
        _5383,
        _5384,
    )

    Self = TypeVar("Self", bound="CouplingHalfCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfCompoundModalAnalysisAtAStiffness._Cast_CouplingHalfCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting CouplingHalfCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "CouplingHalfCompoundModalAnalysisAtAStiffness"

    @property
    def mountable_component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5341.MountableComponentCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(
            _5341.MountableComponentCompoundModalAnalysisAtAStiffness
        )

    @property
    def component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5287.ComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5287,
        )

        return self.__parent__._cast(_5287.ComponentCompoundModalAnalysisAtAStiffness)

    @property
    def part_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5343.PartCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5343,
        )

        return self.__parent__._cast(_5343.PartCompoundModalAnalysisAtAStiffness)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7883.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7883,
        )

        return self.__parent__._cast(_7883.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7880.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2890.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.DesignEntityAnalysis)

    @property
    def clutch_half_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5285.ClutchHalfCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5285,
        )

        return self.__parent__._cast(_5285.ClutchHalfCompoundModalAnalysisAtAStiffness)

    @property
    def concept_coupling_half_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5290.ConceptCouplingHalfCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5290,
        )

        return self.__parent__._cast(
            _5290.ConceptCouplingHalfCompoundModalAnalysisAtAStiffness
        )

    @property
    def cvt_pulley_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5304.CVTPulleyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5304,
        )

        return self.__parent__._cast(_5304.CVTPulleyCompoundModalAnalysisAtAStiffness)

    @property
    def part_to_part_shear_coupling_half_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5346.PartToPartShearCouplingHalfCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5346,
        )

        return self.__parent__._cast(
            _5346.PartToPartShearCouplingHalfCompoundModalAnalysisAtAStiffness
        )

    @property
    def pulley_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5352.PulleyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5352,
        )

        return self.__parent__._cast(_5352.PulleyCompoundModalAnalysisAtAStiffness)

    @property
    def rolling_ring_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5356.RollingRingCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5356,
        )

        return self.__parent__._cast(_5356.RollingRingCompoundModalAnalysisAtAStiffness)

    @property
    def spring_damper_half_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5368.SpringDamperHalfCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5368,
        )

        return self.__parent__._cast(
            _5368.SpringDamperHalfCompoundModalAnalysisAtAStiffness
        )

    @property
    def synchroniser_half_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5378.SynchroniserHalfCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5378,
        )

        return self.__parent__._cast(
            _5378.SynchroniserHalfCompoundModalAnalysisAtAStiffness
        )

    @property
    def synchroniser_part_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5379.SynchroniserPartCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5379,
        )

        return self.__parent__._cast(
            _5379.SynchroniserPartCompoundModalAnalysisAtAStiffness
        )

    @property
    def synchroniser_sleeve_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5380.SynchroniserSleeveCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5380,
        )

        return self.__parent__._cast(
            _5380.SynchroniserSleeveCompoundModalAnalysisAtAStiffness
        )

    @property
    def torque_converter_pump_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5383.TorqueConverterPumpCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5383,
        )

        return self.__parent__._cast(
            _5383.TorqueConverterPumpCompoundModalAnalysisAtAStiffness
        )

    @property
    def torque_converter_turbine_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5384.TorqueConverterTurbineCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5384,
        )

        return self.__parent__._cast(
            _5384.TorqueConverterTurbineCompoundModalAnalysisAtAStiffness
        )

    @property
    def coupling_half_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "CouplingHalfCompoundModalAnalysisAtAStiffness":
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
class CouplingHalfCompoundModalAnalysisAtAStiffness(
    _5341.MountableComponentCompoundModalAnalysisAtAStiffness
):
    """CouplingHalfCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5167.CouplingHalfModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.CouplingHalfModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5167.CouplingHalfModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.CouplingHalfModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalfCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfCompoundModalAnalysisAtAStiffness
        """
        return _Cast_CouplingHalfCompoundModalAnalysisAtAStiffness(self)

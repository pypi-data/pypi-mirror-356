"""InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation"""

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
    _6479,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound",
    "InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7876,
        _7880,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6377,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
        _6449,
        _6453,
        _6456,
        _6461,
        _6466,
        _6471,
        _6474,
        _6477,
        _6482,
        _6484,
        _6492,
        _6498,
        _6503,
        _6507,
        _6511,
        _6514,
        _6517,
        _6527,
        _6536,
        _6539,
        _6546,
        _6549,
        _6552,
        _6555,
        _6564,
        _6570,
        _6573,
    )

    Self = TypeVar(
        "Self",
        bound="InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation._Cast_InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = (
    "InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation",
)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: (
        "InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation"
    )

    @property
    def connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6479.ConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        return self.__parent__._cast(
            _6479.ConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7876.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7876,
        )

        return self.__parent__._cast(_7876.ConnectionCompoundAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6449.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6449,
        )

        return self.__parent__._cast(
            _6449.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def belt_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6453.BeltConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6453,
        )

        return self.__parent__._cast(
            _6453.BeltConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6456.BevelDifferentialGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6456,
        )

        return self.__parent__._cast(
            _6456.BevelDifferentialGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6461.BevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6461,
        )

        return self.__parent__._cast(
            _6461.BevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def clutch_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6466.ClutchConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6466,
        )

        return self.__parent__._cast(
            _6466.ClutchConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_coupling_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6471.ConceptCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6471,
        )

        return self.__parent__._cast(
            _6471.ConceptCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6474.ConceptGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6474,
        )

        return self.__parent__._cast(
            _6474.ConceptGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6477.ConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6477,
        )

        return self.__parent__._cast(
            _6477.ConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coupling_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6482.CouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6482,
        )

        return self.__parent__._cast(
            _6482.CouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cvt_belt_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6484.CVTBeltConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6484,
        )

        return self.__parent__._cast(
            _6484.CVTBeltConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6492.CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6492,
        )

        return self.__parent__._cast(
            _6492.CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def face_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6498.FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6498,
        )

        return self.__parent__._cast(
            _6498.FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6503.GearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6503,
        )

        return self.__parent__._cast(
            _6503.GearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def hypoid_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6507.HypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6507,
        )

        return self.__parent__._cast(
            _6507.HypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6511.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6511,
        )

        return self.__parent__._cast(
            _6511.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6514.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6514,
        )

        return self.__parent__._cast(
            _6514.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6517.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6517,
        )

        return self.__parent__._cast(
            _6517.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_to_part_shear_coupling_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6527.PartToPartShearCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6527,
        )

        return self.__parent__._cast(
            _6527.PartToPartShearCouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def ring_pins_to_disc_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6536.RingPinsToDiscConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6536,
        )

        return self.__parent__._cast(
            _6536.RingPinsToDiscConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def rolling_ring_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6539.RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6539,
        )

        return self.__parent__._cast(
            _6539.RollingRingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6546.SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6546,
        )

        return self.__parent__._cast(
            _6546.SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6549.SpringDamperConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6549,
        )

        return self.__parent__._cast(
            _6549.SpringDamperConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6552.StraightBevelDiffGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6552,
        )

        return self.__parent__._cast(
            _6552.StraightBevelDiffGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6555.StraightBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6555,
        )

        return self.__parent__._cast(
            _6555.StraightBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6564.TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6564,
        )

        return self.__parent__._cast(
            _6564.TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def worm_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6570.WormGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6570,
        )

        return self.__parent__._cast(
            _6570.WormGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6573.ZerolBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6573,
        )

        return self.__parent__._cast(
            _6573.ZerolBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def inter_mountable_component_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation":
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
class InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation(
    _6479.ConnectionCompoundHarmonicAnalysisOfSingleExcitation
):
    """InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6377.InterMountableComponentConnectionHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.InterMountableComponentConnectionHarmonicAnalysisOfSingleExcitation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6377.InterMountableComponentConnectionHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.InterMountableComponentConnectionHarmonicAnalysisOfSingleExcitation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation(
            self
        )

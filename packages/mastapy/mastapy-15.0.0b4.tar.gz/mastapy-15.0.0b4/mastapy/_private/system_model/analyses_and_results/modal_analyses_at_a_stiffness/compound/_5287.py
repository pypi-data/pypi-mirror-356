"""ComponentCompoundModalAnalysisAtAStiffness"""

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
    _5343,
)

_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "ComponentCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5154,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5263,
        _5264,
        _5266,
        _5270,
        _5273,
        _5276,
        _5277,
        _5278,
        _5281,
        _5285,
        _5290,
        _5291,
        _5294,
        _5298,
        _5301,
        _5304,
        _5307,
        _5309,
        _5312,
        _5313,
        _5314,
        _5315,
        _5318,
        _5320,
        _5323,
        _5324,
        _5328,
        _5331,
        _5334,
        _5337,
        _5338,
        _5340,
        _5341,
        _5342,
        _5346,
        _5349,
        _5350,
        _5351,
        _5352,
        _5353,
        _5356,
        _5359,
        _5360,
        _5363,
        _5368,
        _5369,
        _5372,
        _5375,
        _5376,
        _5378,
        _5379,
        _5380,
        _5383,
        _5384,
        _5385,
        _5386,
        _5387,
        _5390,
    )

    Self = TypeVar("Self", bound="ComponentCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentCompoundModalAnalysisAtAStiffness._Cast_ComponentCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting ComponentCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "ComponentCompoundModalAnalysisAtAStiffness"

    @property
    def part_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5343.PartCompoundModalAnalysisAtAStiffness":
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
    def abstract_shaft_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5263.AbstractShaftCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5263,
        )

        return self.__parent__._cast(
            _5263.AbstractShaftCompoundModalAnalysisAtAStiffness
        )

    @property
    def abstract_shaft_or_housing_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5264.AbstractShaftOrHousingCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5264,
        )

        return self.__parent__._cast(
            _5264.AbstractShaftOrHousingCompoundModalAnalysisAtAStiffness
        )

    @property
    def agma_gleason_conical_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5266.AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5266,
        )

        return self.__parent__._cast(
            _5266.AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def bearing_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5270.BearingCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5270,
        )

        return self.__parent__._cast(_5270.BearingCompoundModalAnalysisAtAStiffness)

    @property
    def bevel_differential_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5273.BevelDifferentialGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5273,
        )

        return self.__parent__._cast(
            _5273.BevelDifferentialGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_planet_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5276.BevelDifferentialPlanetGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5276,
        )

        return self.__parent__._cast(
            _5276.BevelDifferentialPlanetGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_sun_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5277.BevelDifferentialSunGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5277,
        )

        return self.__parent__._cast(
            _5277.BevelDifferentialSunGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5278.BevelGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5278,
        )

        return self.__parent__._cast(_5278.BevelGearCompoundModalAnalysisAtAStiffness)

    @property
    def bolt_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5281.BoltCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5281,
        )

        return self.__parent__._cast(_5281.BoltCompoundModalAnalysisAtAStiffness)

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
    def concept_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5291.ConceptGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5291,
        )

        return self.__parent__._cast(_5291.ConceptGearCompoundModalAnalysisAtAStiffness)

    @property
    def conical_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5294.ConicalGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5294,
        )

        return self.__parent__._cast(_5294.ConicalGearCompoundModalAnalysisAtAStiffness)

    @property
    def connector_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5298.ConnectorCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5298,
        )

        return self.__parent__._cast(_5298.ConnectorCompoundModalAnalysisAtAStiffness)

    @property
    def coupling_half_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5301.CouplingHalfCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5301,
        )

        return self.__parent__._cast(
            _5301.CouplingHalfCompoundModalAnalysisAtAStiffness
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
    def cycloidal_disc_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5307.CycloidalDiscCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5307,
        )

        return self.__parent__._cast(
            _5307.CycloidalDiscCompoundModalAnalysisAtAStiffness
        )

    @property
    def cylindrical_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5309.CylindricalGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5309,
        )

        return self.__parent__._cast(
            _5309.CylindricalGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def cylindrical_planet_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5312.CylindricalPlanetGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5312,
        )

        return self.__parent__._cast(
            _5312.CylindricalPlanetGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def datum_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5313.DatumCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5313,
        )

        return self.__parent__._cast(_5313.DatumCompoundModalAnalysisAtAStiffness)

    @property
    def external_cad_model_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5314.ExternalCADModelCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5314,
        )

        return self.__parent__._cast(
            _5314.ExternalCADModelCompoundModalAnalysisAtAStiffness
        )

    @property
    def face_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5315.FaceGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5315,
        )

        return self.__parent__._cast(_5315.FaceGearCompoundModalAnalysisAtAStiffness)

    @property
    def fe_part_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5318.FEPartCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5318,
        )

        return self.__parent__._cast(_5318.FEPartCompoundModalAnalysisAtAStiffness)

    @property
    def gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5320.GearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5320,
        )

        return self.__parent__._cast(_5320.GearCompoundModalAnalysisAtAStiffness)

    @property
    def guide_dxf_model_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5323.GuideDxfModelCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5323,
        )

        return self.__parent__._cast(
            _5323.GuideDxfModelCompoundModalAnalysisAtAStiffness
        )

    @property
    def hypoid_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5324.HypoidGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5324,
        )

        return self.__parent__._cast(_5324.HypoidGearCompoundModalAnalysisAtAStiffness)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5328.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5328,
        )

        return self.__parent__._cast(
            _5328.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5331.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5331,
        )

        return self.__parent__._cast(
            _5331.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> (
        "_5334.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtAStiffness"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5334,
        )

        return self.__parent__._cast(
            _5334.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def mass_disc_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5337.MassDiscCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5337,
        )

        return self.__parent__._cast(_5337.MassDiscCompoundModalAnalysisAtAStiffness)

    @property
    def measurement_component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5338.MeasurementComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5338,
        )

        return self.__parent__._cast(
            _5338.MeasurementComponentCompoundModalAnalysisAtAStiffness
        )

    @property
    def microphone_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5340.MicrophoneCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5340,
        )

        return self.__parent__._cast(_5340.MicrophoneCompoundModalAnalysisAtAStiffness)

    @property
    def mountable_component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5341.MountableComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5341,
        )

        return self.__parent__._cast(
            _5341.MountableComponentCompoundModalAnalysisAtAStiffness
        )

    @property
    def oil_seal_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5342.OilSealCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5342,
        )

        return self.__parent__._cast(_5342.OilSealCompoundModalAnalysisAtAStiffness)

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
    def planet_carrier_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5349.PlanetCarrierCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5349,
        )

        return self.__parent__._cast(
            _5349.PlanetCarrierCompoundModalAnalysisAtAStiffness
        )

    @property
    def point_load_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5350.PointLoadCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5350,
        )

        return self.__parent__._cast(_5350.PointLoadCompoundModalAnalysisAtAStiffness)

    @property
    def power_load_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5351.PowerLoadCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5351,
        )

        return self.__parent__._cast(_5351.PowerLoadCompoundModalAnalysisAtAStiffness)

    @property
    def pulley_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5352.PulleyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5352,
        )

        return self.__parent__._cast(_5352.PulleyCompoundModalAnalysisAtAStiffness)

    @property
    def ring_pins_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5353.RingPinsCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5353,
        )

        return self.__parent__._cast(_5353.RingPinsCompoundModalAnalysisAtAStiffness)

    @property
    def rolling_ring_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5356.RollingRingCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5356,
        )

        return self.__parent__._cast(_5356.RollingRingCompoundModalAnalysisAtAStiffness)

    @property
    def shaft_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5359.ShaftCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5359,
        )

        return self.__parent__._cast(_5359.ShaftCompoundModalAnalysisAtAStiffness)

    @property
    def shaft_hub_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5360.ShaftHubConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5360,
        )

        return self.__parent__._cast(
            _5360.ShaftHubConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def spiral_bevel_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5363.SpiralBevelGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5363,
        )

        return self.__parent__._cast(
            _5363.SpiralBevelGearCompoundModalAnalysisAtAStiffness
        )

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
    def straight_bevel_diff_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5369.StraightBevelDiffGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5369,
        )

        return self.__parent__._cast(
            _5369.StraightBevelDiffGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5372.StraightBevelGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5372,
        )

        return self.__parent__._cast(
            _5372.StraightBevelGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_planet_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5375.StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5375,
        )

        return self.__parent__._cast(
            _5375.StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_sun_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5376.StraightBevelSunGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5376,
        )

        return self.__parent__._cast(
            _5376.StraightBevelSunGearCompoundModalAnalysisAtAStiffness
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
    def unbalanced_mass_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5385.UnbalancedMassCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5385,
        )

        return self.__parent__._cast(
            _5385.UnbalancedMassCompoundModalAnalysisAtAStiffness
        )

    @property
    def virtual_component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5386.VirtualComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5386,
        )

        return self.__parent__._cast(
            _5386.VirtualComponentCompoundModalAnalysisAtAStiffness
        )

    @property
    def worm_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5387.WormGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5387,
        )

        return self.__parent__._cast(_5387.WormGearCompoundModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5390.ZerolBevelGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5390,
        )

        return self.__parent__._cast(
            _5390.ZerolBevelGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "ComponentCompoundModalAnalysisAtAStiffness":
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
class ComponentCompoundModalAnalysisAtAStiffness(
    _5343.PartCompoundModalAnalysisAtAStiffness
):
    """ComponentCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

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
    ) -> "List[_5154.ComponentModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ComponentModalAnalysisAtAStiffness]

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
    ) -> "List[_5154.ComponentModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ComponentModalAnalysisAtAStiffness]

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
    def cast_to(self: "Self") -> "_Cast_ComponentCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_ComponentCompoundModalAnalysisAtAStiffness
        """
        return _Cast_ComponentCompoundModalAnalysisAtAStiffness(self)

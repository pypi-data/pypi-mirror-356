"""ConnectionSteadyStateSynchronousResponseOnAShaft"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7878

_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "ConnectionSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2888, _2890, _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7875
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3495,
        _3496,
        _3501,
        _3503,
        _3508,
        _3513,
        _3516,
        _3518,
        _3521,
        _3524,
        _3529,
        _3532,
        _3536,
        _3537,
        _3539,
        _3545,
        _3550,
        _3554,
        _3557,
        _3558,
        _3561,
        _3564,
        _3574,
        _3577,
        _3584,
        _3586,
        _3591,
        _3593,
        _3596,
        _3599,
        _3600,
        _3603,
        _3612,
        _3618,
        _3621,
    )
    from mastapy._private.system_model.connections_and_sockets import _2493

    Self = TypeVar("Self", bound="ConnectionSteadyStateSynchronousResponseOnAShaft")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionSteadyStateSynchronousResponseOnAShaft._Cast_ConnectionSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting ConnectionSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "ConnectionSteadyStateSynchronousResponseOnAShaft"

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7878.ConnectionStaticLoadAnalysisCase":
        return self.__parent__._cast(_7878.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7875.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7875,
        )

        return self.__parent__._cast(_7875.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2888.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2888

        return self.__parent__._cast(_2888.ConnectionAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2892.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2890.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.DesignEntityAnalysis)

    @property
    def abstract_shaft_to_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3495.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3495,
        )

        return self.__parent__._cast(
            _3495.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3496.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3496,
        )

        return self.__parent__._cast(
            _3496.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def belt_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3501.BeltConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3501,
        )

        return self.__parent__._cast(
            _3501.BeltConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3503.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3503,
        )

        return self.__parent__._cast(
            _3503.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3508.BevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3508,
        )

        return self.__parent__._cast(
            _3508.BevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def clutch_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3513.ClutchConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3513,
        )

        return self.__parent__._cast(
            _3513.ClutchConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coaxial_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3516.CoaxialConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3516,
        )

        return self.__parent__._cast(
            _3516.CoaxialConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3518.ConceptCouplingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3518,
        )

        return self.__parent__._cast(
            _3518.ConceptCouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3521.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3521,
        )

        return self.__parent__._cast(
            _3521.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3524.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3524,
        )

        return self.__parent__._cast(
            _3524.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3529.CouplingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3529,
        )

        return self.__parent__._cast(
            _3529.CouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cvt_belt_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3532.CVTBeltConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3532,
        )

        return self.__parent__._cast(
            _3532.CVTBeltConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_central_bearing_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3536.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3536,
        )

        return self.__parent__._cast(
            _3536.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3537.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3537,
        )

        return self.__parent__._cast(
            _3537.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3539.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3539,
        )

        return self.__parent__._cast(
            _3539.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def face_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3545.FaceGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3545,
        )

        return self.__parent__._cast(
            _3545.FaceGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3550.GearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3550,
        )

        return self.__parent__._cast(
            _3550.GearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def hypoid_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3554.HypoidGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3554,
        )

        return self.__parent__._cast(
            _3554.HypoidGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3557.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3557,
        )

        return self.__parent__._cast(
            _3557.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3558.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3558,
        )

        return self.__parent__._cast(
            _3558.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3561.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3561,
        )

        return self.__parent__._cast(
            _3561.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3564.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3564,
        )

        return self.__parent__._cast(
            _3564.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_to_part_shear_coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3574.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3574,
        )

        return self.__parent__._cast(
            _3574.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def planetary_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3577.PlanetaryConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3577,
        )

        return self.__parent__._cast(
            _3577.PlanetaryConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def ring_pins_to_disc_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3584.RingPinsToDiscConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3584,
        )

        return self.__parent__._cast(
            _3584.RingPinsToDiscConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def rolling_ring_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3586.RollingRingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3586,
        )

        return self.__parent__._cast(
            _3586.RollingRingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def shaft_to_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3591.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3591,
        )

        return self.__parent__._cast(
            _3591.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3593.SpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3593,
        )

        return self.__parent__._cast(
            _3593.SpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spring_damper_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3596.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3596,
        )

        return self.__parent__._cast(
            _3596.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3600.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3600,
        )

        return self.__parent__._cast(
            _3600.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3603.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3603,
        )

        return self.__parent__._cast(
            _3603.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3612.TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3612,
        )

        return self.__parent__._cast(
            _3612.TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def worm_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3618.WormGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3618,
        )

        return self.__parent__._cast(
            _3618.WormGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3621.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3621,
        )

        return self.__parent__._cast(
            _3621.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "ConnectionSteadyStateSynchronousResponseOnAShaft":
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
class ConnectionSteadyStateSynchronousResponseOnAShaft(
    _7878.ConnectionStaticLoadAnalysisCase
):
    """ConnectionSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2493.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2493.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "_3599.SteadyStateSynchronousResponseOnAShaft":
        """mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.SteadyStateSynchronousResponseOnAShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SteadyStateSynchronousResponseOnAShaft"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ConnectionSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_ConnectionSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_ConnectionSteadyStateSynchronousResponseOnAShaft(self)

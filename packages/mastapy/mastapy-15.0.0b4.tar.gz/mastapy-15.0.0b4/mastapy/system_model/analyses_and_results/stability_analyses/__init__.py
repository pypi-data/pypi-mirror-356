"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4018 import (
        AbstractAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4019 import (
        AbstractShaftOrHousingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4020 import (
        AbstractShaftStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4021 import (
        AbstractShaftToMountableComponentConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4022 import (
        AGMAGleasonConicalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4023 import (
        AGMAGleasonConicalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4024 import (
        AGMAGleasonConicalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4025 import (
        AssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4026 import (
        BearingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4027 import (
        BeltConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4028 import (
        BeltDriveStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4029 import (
        BevelDifferentialGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4030 import (
        BevelDifferentialGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4031 import (
        BevelDifferentialGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4032 import (
        BevelDifferentialPlanetGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4033 import (
        BevelDifferentialSunGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4034 import (
        BevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4035 import (
        BevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4036 import (
        BevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4037 import (
        BoltedJointStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4038 import (
        BoltStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4039 import (
        ClutchConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4040 import (
        ClutchHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4041 import (
        ClutchStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4042 import (
        CoaxialConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4043 import (
        ComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4044 import (
        ConceptCouplingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4045 import (
        ConceptCouplingHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4046 import (
        ConceptCouplingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4047 import (
        ConceptGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4048 import (
        ConceptGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4049 import (
        ConceptGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4050 import (
        ConicalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4051 import (
        ConicalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4052 import (
        ConicalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4053 import (
        ConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4054 import (
        ConnectorStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4055 import (
        CouplingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4056 import (
        CouplingHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4057 import (
        CouplingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4058 import (
        CriticalSpeed,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4059 import (
        CVTBeltConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4060 import (
        CVTPulleyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4061 import (
        CVTStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4062 import (
        CycloidalAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4063 import (
        CycloidalDiscCentralBearingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4064 import (
        CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4065 import (
        CycloidalDiscStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4066 import (
        CylindricalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4067 import (
        CylindricalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4068 import (
        CylindricalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4069 import (
        CylindricalPlanetGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4070 import (
        DatumStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4071 import (
        DynamicModelForStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4072 import (
        ExternalCADModelStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4073 import (
        FaceGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4074 import (
        FaceGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4075 import (
        FaceGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4076 import (
        FEPartStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4077 import (
        FlexiblePinAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4078 import (
        GearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4079 import (
        GearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4080 import (
        GearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4081 import (
        GuideDxfModelStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4082 import (
        HypoidGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4083 import (
        HypoidGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4084 import (
        HypoidGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4085 import (
        InterMountableComponentConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4086 import (
        KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4087 import (
        KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4088 import (
        KlingelnbergCycloPalloidConicalGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4089 import (
        KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4090 import (
        KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4091 import (
        KlingelnbergCycloPalloidHypoidGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4092 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4093 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4094 import (
        KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4095 import (
        MassDiscStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4096 import (
        MeasurementComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4097 import (
        MicrophoneArrayStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4098 import (
        MicrophoneStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4099 import (
        MountableComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4100 import (
        OilSealStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4101 import (
        PartStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4102 import (
        PartToPartShearCouplingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4103 import (
        PartToPartShearCouplingHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4104 import (
        PartToPartShearCouplingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4105 import (
        PlanetaryConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4106 import (
        PlanetaryGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4107 import (
        PlanetCarrierStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4108 import (
        PointLoadStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4109 import (
        PowerLoadStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4110 import (
        PulleyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4111 import (
        RingPinsStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4112 import (
        RingPinsToDiscConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4113 import (
        RollingRingAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4114 import (
        RollingRingConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4115 import (
        RollingRingStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4116 import (
        RootAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4117 import (
        ShaftHubConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4118 import (
        ShaftStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4119 import (
        ShaftToMountableComponentConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4120 import (
        SpecialisedAssemblyStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4121 import (
        SpiralBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4122 import (
        SpiralBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4123 import (
        SpiralBevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4124 import (
        SpringDamperConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4125 import (
        SpringDamperHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4126 import (
        SpringDamperStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4127 import (
        StabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4128 import (
        StabilityAnalysisDrawStyle,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4129 import (
        StabilityAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4130 import (
        StraightBevelDiffGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4131 import (
        StraightBevelDiffGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4132 import (
        StraightBevelDiffGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4133 import (
        StraightBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4134 import (
        StraightBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4135 import (
        StraightBevelGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4136 import (
        StraightBevelPlanetGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4137 import (
        StraightBevelSunGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4138 import (
        SynchroniserHalfStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4139 import (
        SynchroniserPartStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4140 import (
        SynchroniserSleeveStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4141 import (
        SynchroniserStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4142 import (
        TorqueConverterConnectionStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4143 import (
        TorqueConverterPumpStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4144 import (
        TorqueConverterStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4145 import (
        TorqueConverterTurbineStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4146 import (
        UnbalancedMassStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4147 import (
        VirtualComponentStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4148 import (
        WormGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4149 import (
        WormGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4150 import (
        WormGearStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4151 import (
        ZerolBevelGearMeshStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4152 import (
        ZerolBevelGearSetStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses._4153 import (
        ZerolBevelGearStabilityAnalysis,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.stability_analyses._4018": [
            "AbstractAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4019": [
            "AbstractShaftOrHousingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4020": [
            "AbstractShaftStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4021": [
            "AbstractShaftToMountableComponentConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4022": [
            "AGMAGleasonConicalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4023": [
            "AGMAGleasonConicalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4024": [
            "AGMAGleasonConicalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4025": [
            "AssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4026": [
            "BearingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4027": [
            "BeltConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4028": [
            "BeltDriveStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4029": [
            "BevelDifferentialGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4030": [
            "BevelDifferentialGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4031": [
            "BevelDifferentialGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4032": [
            "BevelDifferentialPlanetGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4033": [
            "BevelDifferentialSunGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4034": [
            "BevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4035": [
            "BevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4036": [
            "BevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4037": [
            "BoltedJointStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4038": [
            "BoltStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4039": [
            "ClutchConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4040": [
            "ClutchHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4041": [
            "ClutchStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4042": [
            "CoaxialConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4043": [
            "ComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4044": [
            "ConceptCouplingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4045": [
            "ConceptCouplingHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4046": [
            "ConceptCouplingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4047": [
            "ConceptGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4048": [
            "ConceptGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4049": [
            "ConceptGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4050": [
            "ConicalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4051": [
            "ConicalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4052": [
            "ConicalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4053": [
            "ConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4054": [
            "ConnectorStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4055": [
            "CouplingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4056": [
            "CouplingHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4057": [
            "CouplingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4058": [
            "CriticalSpeed"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4059": [
            "CVTBeltConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4060": [
            "CVTPulleyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4061": [
            "CVTStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4062": [
            "CycloidalAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4063": [
            "CycloidalDiscCentralBearingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4064": [
            "CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4065": [
            "CycloidalDiscStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4066": [
            "CylindricalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4067": [
            "CylindricalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4068": [
            "CylindricalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4069": [
            "CylindricalPlanetGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4070": [
            "DatumStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4071": [
            "DynamicModelForStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4072": [
            "ExternalCADModelStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4073": [
            "FaceGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4074": [
            "FaceGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4075": [
            "FaceGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4076": [
            "FEPartStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4077": [
            "FlexiblePinAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4078": [
            "GearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4079": [
            "GearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4080": [
            "GearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4081": [
            "GuideDxfModelStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4082": [
            "HypoidGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4083": [
            "HypoidGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4084": [
            "HypoidGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4085": [
            "InterMountableComponentConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4086": [
            "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4087": [
            "KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4088": [
            "KlingelnbergCycloPalloidConicalGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4089": [
            "KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4090": [
            "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4091": [
            "KlingelnbergCycloPalloidHypoidGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4092": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4093": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4094": [
            "KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4095": [
            "MassDiscStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4096": [
            "MeasurementComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4097": [
            "MicrophoneArrayStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4098": [
            "MicrophoneStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4099": [
            "MountableComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4100": [
            "OilSealStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4101": [
            "PartStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4102": [
            "PartToPartShearCouplingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4103": [
            "PartToPartShearCouplingHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4104": [
            "PartToPartShearCouplingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4105": [
            "PlanetaryConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4106": [
            "PlanetaryGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4107": [
            "PlanetCarrierStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4108": [
            "PointLoadStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4109": [
            "PowerLoadStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4110": [
            "PulleyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4111": [
            "RingPinsStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4112": [
            "RingPinsToDiscConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4113": [
            "RollingRingAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4114": [
            "RollingRingConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4115": [
            "RollingRingStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4116": [
            "RootAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4117": [
            "ShaftHubConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4118": [
            "ShaftStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4119": [
            "ShaftToMountableComponentConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4120": [
            "SpecialisedAssemblyStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4121": [
            "SpiralBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4122": [
            "SpiralBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4123": [
            "SpiralBevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4124": [
            "SpringDamperConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4125": [
            "SpringDamperHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4126": [
            "SpringDamperStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4127": [
            "StabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4128": [
            "StabilityAnalysisDrawStyle"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4129": [
            "StabilityAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4130": [
            "StraightBevelDiffGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4131": [
            "StraightBevelDiffGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4132": [
            "StraightBevelDiffGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4133": [
            "StraightBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4134": [
            "StraightBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4135": [
            "StraightBevelGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4136": [
            "StraightBevelPlanetGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4137": [
            "StraightBevelSunGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4138": [
            "SynchroniserHalfStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4139": [
            "SynchroniserPartStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4140": [
            "SynchroniserSleeveStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4141": [
            "SynchroniserStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4142": [
            "TorqueConverterConnectionStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4143": [
            "TorqueConverterPumpStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4144": [
            "TorqueConverterStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4145": [
            "TorqueConverterTurbineStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4146": [
            "UnbalancedMassStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4147": [
            "VirtualComponentStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4148": [
            "WormGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4149": [
            "WormGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4150": [
            "WormGearStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4151": [
            "ZerolBevelGearMeshStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4152": [
            "ZerolBevelGearSetStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results.stability_analyses._4153": [
            "ZerolBevelGearStabilityAnalysis"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractAssemblyStabilityAnalysis",
    "AbstractShaftOrHousingStabilityAnalysis",
    "AbstractShaftStabilityAnalysis",
    "AbstractShaftToMountableComponentConnectionStabilityAnalysis",
    "AGMAGleasonConicalGearMeshStabilityAnalysis",
    "AGMAGleasonConicalGearSetStabilityAnalysis",
    "AGMAGleasonConicalGearStabilityAnalysis",
    "AssemblyStabilityAnalysis",
    "BearingStabilityAnalysis",
    "BeltConnectionStabilityAnalysis",
    "BeltDriveStabilityAnalysis",
    "BevelDifferentialGearMeshStabilityAnalysis",
    "BevelDifferentialGearSetStabilityAnalysis",
    "BevelDifferentialGearStabilityAnalysis",
    "BevelDifferentialPlanetGearStabilityAnalysis",
    "BevelDifferentialSunGearStabilityAnalysis",
    "BevelGearMeshStabilityAnalysis",
    "BevelGearSetStabilityAnalysis",
    "BevelGearStabilityAnalysis",
    "BoltedJointStabilityAnalysis",
    "BoltStabilityAnalysis",
    "ClutchConnectionStabilityAnalysis",
    "ClutchHalfStabilityAnalysis",
    "ClutchStabilityAnalysis",
    "CoaxialConnectionStabilityAnalysis",
    "ComponentStabilityAnalysis",
    "ConceptCouplingConnectionStabilityAnalysis",
    "ConceptCouplingHalfStabilityAnalysis",
    "ConceptCouplingStabilityAnalysis",
    "ConceptGearMeshStabilityAnalysis",
    "ConceptGearSetStabilityAnalysis",
    "ConceptGearStabilityAnalysis",
    "ConicalGearMeshStabilityAnalysis",
    "ConicalGearSetStabilityAnalysis",
    "ConicalGearStabilityAnalysis",
    "ConnectionStabilityAnalysis",
    "ConnectorStabilityAnalysis",
    "CouplingConnectionStabilityAnalysis",
    "CouplingHalfStabilityAnalysis",
    "CouplingStabilityAnalysis",
    "CriticalSpeed",
    "CVTBeltConnectionStabilityAnalysis",
    "CVTPulleyStabilityAnalysis",
    "CVTStabilityAnalysis",
    "CycloidalAssemblyStabilityAnalysis",
    "CycloidalDiscCentralBearingConnectionStabilityAnalysis",
    "CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis",
    "CycloidalDiscStabilityAnalysis",
    "CylindricalGearMeshStabilityAnalysis",
    "CylindricalGearSetStabilityAnalysis",
    "CylindricalGearStabilityAnalysis",
    "CylindricalPlanetGearStabilityAnalysis",
    "DatumStabilityAnalysis",
    "DynamicModelForStabilityAnalysis",
    "ExternalCADModelStabilityAnalysis",
    "FaceGearMeshStabilityAnalysis",
    "FaceGearSetStabilityAnalysis",
    "FaceGearStabilityAnalysis",
    "FEPartStabilityAnalysis",
    "FlexiblePinAssemblyStabilityAnalysis",
    "GearMeshStabilityAnalysis",
    "GearSetStabilityAnalysis",
    "GearStabilityAnalysis",
    "GuideDxfModelStabilityAnalysis",
    "HypoidGearMeshStabilityAnalysis",
    "HypoidGearSetStabilityAnalysis",
    "HypoidGearStabilityAnalysis",
    "InterMountableComponentConnectionStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis",
    "MassDiscStabilityAnalysis",
    "MeasurementComponentStabilityAnalysis",
    "MicrophoneArrayStabilityAnalysis",
    "MicrophoneStabilityAnalysis",
    "MountableComponentStabilityAnalysis",
    "OilSealStabilityAnalysis",
    "PartStabilityAnalysis",
    "PartToPartShearCouplingConnectionStabilityAnalysis",
    "PartToPartShearCouplingHalfStabilityAnalysis",
    "PartToPartShearCouplingStabilityAnalysis",
    "PlanetaryConnectionStabilityAnalysis",
    "PlanetaryGearSetStabilityAnalysis",
    "PlanetCarrierStabilityAnalysis",
    "PointLoadStabilityAnalysis",
    "PowerLoadStabilityAnalysis",
    "PulleyStabilityAnalysis",
    "RingPinsStabilityAnalysis",
    "RingPinsToDiscConnectionStabilityAnalysis",
    "RollingRingAssemblyStabilityAnalysis",
    "RollingRingConnectionStabilityAnalysis",
    "RollingRingStabilityAnalysis",
    "RootAssemblyStabilityAnalysis",
    "ShaftHubConnectionStabilityAnalysis",
    "ShaftStabilityAnalysis",
    "ShaftToMountableComponentConnectionStabilityAnalysis",
    "SpecialisedAssemblyStabilityAnalysis",
    "SpiralBevelGearMeshStabilityAnalysis",
    "SpiralBevelGearSetStabilityAnalysis",
    "SpiralBevelGearStabilityAnalysis",
    "SpringDamperConnectionStabilityAnalysis",
    "SpringDamperHalfStabilityAnalysis",
    "SpringDamperStabilityAnalysis",
    "StabilityAnalysis",
    "StabilityAnalysisDrawStyle",
    "StabilityAnalysisOptions",
    "StraightBevelDiffGearMeshStabilityAnalysis",
    "StraightBevelDiffGearSetStabilityAnalysis",
    "StraightBevelDiffGearStabilityAnalysis",
    "StraightBevelGearMeshStabilityAnalysis",
    "StraightBevelGearSetStabilityAnalysis",
    "StraightBevelGearStabilityAnalysis",
    "StraightBevelPlanetGearStabilityAnalysis",
    "StraightBevelSunGearStabilityAnalysis",
    "SynchroniserHalfStabilityAnalysis",
    "SynchroniserPartStabilityAnalysis",
    "SynchroniserSleeveStabilityAnalysis",
    "SynchroniserStabilityAnalysis",
    "TorqueConverterConnectionStabilityAnalysis",
    "TorqueConverterPumpStabilityAnalysis",
    "TorqueConverterStabilityAnalysis",
    "TorqueConverterTurbineStabilityAnalysis",
    "UnbalancedMassStabilityAnalysis",
    "VirtualComponentStabilityAnalysis",
    "WormGearMeshStabilityAnalysis",
    "WormGearSetStabilityAnalysis",
    "WormGearStabilityAnalysis",
    "ZerolBevelGearMeshStabilityAnalysis",
    "ZerolBevelGearSetStabilityAnalysis",
    "ZerolBevelGearStabilityAnalysis",
)

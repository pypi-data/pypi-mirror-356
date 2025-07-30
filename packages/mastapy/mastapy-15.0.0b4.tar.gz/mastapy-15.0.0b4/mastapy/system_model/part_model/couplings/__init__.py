"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.couplings._2813 import BeltDrive
    from mastapy._private.system_model.part_model.couplings._2814 import BeltDriveType
    from mastapy._private.system_model.part_model.couplings._2815 import Clutch
    from mastapy._private.system_model.part_model.couplings._2816 import ClutchHalf
    from mastapy._private.system_model.part_model.couplings._2817 import ClutchType
    from mastapy._private.system_model.part_model.couplings._2818 import ConceptCoupling
    from mastapy._private.system_model.part_model.couplings._2819 import (
        ConceptCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2820 import (
        ConceptCouplingHalfPositioning,
    )
    from mastapy._private.system_model.part_model.couplings._2821 import Coupling
    from mastapy._private.system_model.part_model.couplings._2822 import CouplingHalf
    from mastapy._private.system_model.part_model.couplings._2823 import (
        CrowningSpecification,
    )
    from mastapy._private.system_model.part_model.couplings._2824 import CVT
    from mastapy._private.system_model.part_model.couplings._2825 import CVTPulley
    from mastapy._private.system_model.part_model.couplings._2826 import (
        PartToPartShearCoupling,
    )
    from mastapy._private.system_model.part_model.couplings._2827 import (
        PartToPartShearCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2828 import (
        PitchErrorFlankOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2829 import Pulley
    from mastapy._private.system_model.part_model.couplings._2830 import (
        RigidConnectorSettings,
    )
    from mastapy._private.system_model.part_model.couplings._2831 import (
        RigidConnectorStiffnessType,
    )
    from mastapy._private.system_model.part_model.couplings._2832 import (
        RigidConnectorTiltStiffnessTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2833 import (
        RigidConnectorToothLocation,
    )
    from mastapy._private.system_model.part_model.couplings._2834 import (
        RigidConnectorToothSpacingType,
    )
    from mastapy._private.system_model.part_model.couplings._2835 import (
        RigidConnectorTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2836 import RollingRing
    from mastapy._private.system_model.part_model.couplings._2837 import (
        RollingRingAssembly,
    )
    from mastapy._private.system_model.part_model.couplings._2838 import (
        ShaftHubConnection,
    )
    from mastapy._private.system_model.part_model.couplings._2839 import (
        SplineFitOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2840 import (
        SplineHalfManufacturingError,
    )
    from mastapy._private.system_model.part_model.couplings._2841 import (
        SplineLeadRelief,
    )
    from mastapy._private.system_model.part_model.couplings._2842 import (
        SplinePitchErrorInputType,
    )
    from mastapy._private.system_model.part_model.couplings._2843 import (
        SplinePitchErrorOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2844 import SpringDamper
    from mastapy._private.system_model.part_model.couplings._2845 import (
        SpringDamperHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2846 import Synchroniser
    from mastapy._private.system_model.part_model.couplings._2847 import (
        SynchroniserCone,
    )
    from mastapy._private.system_model.part_model.couplings._2848 import (
        SynchroniserHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2849 import (
        SynchroniserPart,
    )
    from mastapy._private.system_model.part_model.couplings._2850 import (
        SynchroniserSleeve,
    )
    from mastapy._private.system_model.part_model.couplings._2851 import TorqueConverter
    from mastapy._private.system_model.part_model.couplings._2852 import (
        TorqueConverterPump,
    )
    from mastapy._private.system_model.part_model.couplings._2853 import (
        TorqueConverterSpeedRatio,
    )
    from mastapy._private.system_model.part_model.couplings._2854 import (
        TorqueConverterTurbine,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.couplings._2813": ["BeltDrive"],
        "_private.system_model.part_model.couplings._2814": ["BeltDriveType"],
        "_private.system_model.part_model.couplings._2815": ["Clutch"],
        "_private.system_model.part_model.couplings._2816": ["ClutchHalf"],
        "_private.system_model.part_model.couplings._2817": ["ClutchType"],
        "_private.system_model.part_model.couplings._2818": ["ConceptCoupling"],
        "_private.system_model.part_model.couplings._2819": ["ConceptCouplingHalf"],
        "_private.system_model.part_model.couplings._2820": [
            "ConceptCouplingHalfPositioning"
        ],
        "_private.system_model.part_model.couplings._2821": ["Coupling"],
        "_private.system_model.part_model.couplings._2822": ["CouplingHalf"],
        "_private.system_model.part_model.couplings._2823": ["CrowningSpecification"],
        "_private.system_model.part_model.couplings._2824": ["CVT"],
        "_private.system_model.part_model.couplings._2825": ["CVTPulley"],
        "_private.system_model.part_model.couplings._2826": ["PartToPartShearCoupling"],
        "_private.system_model.part_model.couplings._2827": [
            "PartToPartShearCouplingHalf"
        ],
        "_private.system_model.part_model.couplings._2828": ["PitchErrorFlankOptions"],
        "_private.system_model.part_model.couplings._2829": ["Pulley"],
        "_private.system_model.part_model.couplings._2830": ["RigidConnectorSettings"],
        "_private.system_model.part_model.couplings._2831": [
            "RigidConnectorStiffnessType"
        ],
        "_private.system_model.part_model.couplings._2832": [
            "RigidConnectorTiltStiffnessTypes"
        ],
        "_private.system_model.part_model.couplings._2833": [
            "RigidConnectorToothLocation"
        ],
        "_private.system_model.part_model.couplings._2834": [
            "RigidConnectorToothSpacingType"
        ],
        "_private.system_model.part_model.couplings._2835": ["RigidConnectorTypes"],
        "_private.system_model.part_model.couplings._2836": ["RollingRing"],
        "_private.system_model.part_model.couplings._2837": ["RollingRingAssembly"],
        "_private.system_model.part_model.couplings._2838": ["ShaftHubConnection"],
        "_private.system_model.part_model.couplings._2839": ["SplineFitOptions"],
        "_private.system_model.part_model.couplings._2840": [
            "SplineHalfManufacturingError"
        ],
        "_private.system_model.part_model.couplings._2841": ["SplineLeadRelief"],
        "_private.system_model.part_model.couplings._2842": [
            "SplinePitchErrorInputType"
        ],
        "_private.system_model.part_model.couplings._2843": ["SplinePitchErrorOptions"],
        "_private.system_model.part_model.couplings._2844": ["SpringDamper"],
        "_private.system_model.part_model.couplings._2845": ["SpringDamperHalf"],
        "_private.system_model.part_model.couplings._2846": ["Synchroniser"],
        "_private.system_model.part_model.couplings._2847": ["SynchroniserCone"],
        "_private.system_model.part_model.couplings._2848": ["SynchroniserHalf"],
        "_private.system_model.part_model.couplings._2849": ["SynchroniserPart"],
        "_private.system_model.part_model.couplings._2850": ["SynchroniserSleeve"],
        "_private.system_model.part_model.couplings._2851": ["TorqueConverter"],
        "_private.system_model.part_model.couplings._2852": ["TorqueConverterPump"],
        "_private.system_model.part_model.couplings._2853": [
            "TorqueConverterSpeedRatio"
        ],
        "_private.system_model.part_model.couplings._2854": ["TorqueConverterTurbine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeltDrive",
    "BeltDriveType",
    "Clutch",
    "ClutchHalf",
    "ClutchType",
    "ConceptCoupling",
    "ConceptCouplingHalf",
    "ConceptCouplingHalfPositioning",
    "Coupling",
    "CouplingHalf",
    "CrowningSpecification",
    "CVT",
    "CVTPulley",
    "PartToPartShearCoupling",
    "PartToPartShearCouplingHalf",
    "PitchErrorFlankOptions",
    "Pulley",
    "RigidConnectorSettings",
    "RigidConnectorStiffnessType",
    "RigidConnectorTiltStiffnessTypes",
    "RigidConnectorToothLocation",
    "RigidConnectorToothSpacingType",
    "RigidConnectorTypes",
    "RollingRing",
    "RollingRingAssembly",
    "ShaftHubConnection",
    "SplineFitOptions",
    "SplineHalfManufacturingError",
    "SplineLeadRelief",
    "SplinePitchErrorInputType",
    "SplinePitchErrorOptions",
    "SpringDamper",
    "SpringDamperHalf",
    "Synchroniser",
    "SynchroniserCone",
    "SynchroniserHalf",
    "SynchroniserPart",
    "SynchroniserSleeve",
    "TorqueConverter",
    "TorqueConverterPump",
    "TorqueConverterSpeedRatio",
    "TorqueConverterTurbine",
)

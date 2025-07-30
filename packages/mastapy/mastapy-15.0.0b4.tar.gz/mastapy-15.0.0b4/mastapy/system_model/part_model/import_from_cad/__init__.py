"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.import_from_cad._2726 import (
        AbstractShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2727 import (
        ClutchFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2728 import (
        ComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2729 import (
        ComponentFromCADBase,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2730 import (
        ConceptBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2731 import (
        ConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2732 import (
        CylindricalGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2733 import (
        CylindricalGearInPlanetarySetFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2734 import (
        CylindricalPlanetGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2735 import (
        CylindricalRingGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2736 import (
        CylindricalSunGearFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2737 import (
        HousedOrMounted,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2738 import (
        MountableComponentFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2739 import (
        PlanetShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2740 import (
        PulleyFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2741 import (
        RigidConnectorFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2742 import (
        RollingBearingFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2743 import (
        ShaftFromCAD,
    )
    from mastapy._private.system_model.part_model.import_from_cad._2744 import (
        ShaftFromCADAuto,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.import_from_cad._2726": [
            "AbstractShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2727": ["ClutchFromCAD"],
        "_private.system_model.part_model.import_from_cad._2728": ["ComponentFromCAD"],
        "_private.system_model.part_model.import_from_cad._2729": [
            "ComponentFromCADBase"
        ],
        "_private.system_model.part_model.import_from_cad._2730": [
            "ConceptBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2731": ["ConnectorFromCAD"],
        "_private.system_model.part_model.import_from_cad._2732": [
            "CylindricalGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2733": [
            "CylindricalGearInPlanetarySetFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2734": [
            "CylindricalPlanetGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2735": [
            "CylindricalRingGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2736": [
            "CylindricalSunGearFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2737": ["HousedOrMounted"],
        "_private.system_model.part_model.import_from_cad._2738": [
            "MountableComponentFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2739": [
            "PlanetShaftFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2740": ["PulleyFromCAD"],
        "_private.system_model.part_model.import_from_cad._2741": [
            "RigidConnectorFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2742": [
            "RollingBearingFromCAD"
        ],
        "_private.system_model.part_model.import_from_cad._2743": ["ShaftFromCAD"],
        "_private.system_model.part_model.import_from_cad._2744": ["ShaftFromCADAuto"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftFromCAD",
    "ClutchFromCAD",
    "ComponentFromCAD",
    "ComponentFromCADBase",
    "ConceptBearingFromCAD",
    "ConnectorFromCAD",
    "CylindricalGearFromCAD",
    "CylindricalGearInPlanetarySetFromCAD",
    "CylindricalPlanetGearFromCAD",
    "CylindricalRingGearFromCAD",
    "CylindricalSunGearFromCAD",
    "HousedOrMounted",
    "MountableComponentFromCAD",
    "PlanetShaftFromCAD",
    "PulleyFromCAD",
    "RigidConnectorFromCAD",
    "RollingBearingFromCAD",
    "ShaftFromCAD",
    "ShaftFromCADAuto",
)

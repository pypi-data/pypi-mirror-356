"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.acoustics._2864 import (
        AcousticAnalysisOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2865 import (
        AcousticAnalysisSetup,
    )
    from mastapy._private.system_model.part_model.acoustics._2866 import (
        AcousticAnalysisSetupCacheReporting,
    )
    from mastapy._private.system_model.part_model.acoustics._2867 import (
        AcousticAnalysisSetupCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2868 import (
        AcousticEnvelopeType,
    )
    from mastapy._private.system_model.part_model.acoustics._2869 import (
        AcousticInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2870 import (
        CacheMemoryEstimates,
    )
    from mastapy._private.system_model.part_model.acoustics._2871 import (
        FEPartInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2872 import (
        FESurfaceSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2873 import HoleInFaceGroup
    from mastapy._private.system_model.part_model.acoustics._2874 import (
        MeshedResultPlane,
    )
    from mastapy._private.system_model.part_model.acoustics._2875 import (
        MeshedResultSphere,
    )
    from mastapy._private.system_model.part_model.acoustics._2876 import (
        MeshedResultSurface,
    )
    from mastapy._private.system_model.part_model.acoustics._2877 import (
        MeshedResultSurfaceBase,
    )
    from mastapy._private.system_model.part_model.acoustics._2878 import (
        MicrophoneArrayDesign,
    )
    from mastapy._private.system_model.part_model.acoustics._2879 import (
        PartSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2880 import (
        ResultPlaneOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2881 import (
        ResultSphereOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2882 import (
        ResultSurfaceCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2883 import (
        ResultSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2884 import (
        SphericalEnvelopeCentreDefinition,
    )
    from mastapy._private.system_model.part_model.acoustics._2885 import (
        SphericalEnvelopeType,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.acoustics._2864": ["AcousticAnalysisOptions"],
        "_private.system_model.part_model.acoustics._2865": ["AcousticAnalysisSetup"],
        "_private.system_model.part_model.acoustics._2866": [
            "AcousticAnalysisSetupCacheReporting"
        ],
        "_private.system_model.part_model.acoustics._2867": [
            "AcousticAnalysisSetupCollection"
        ],
        "_private.system_model.part_model.acoustics._2868": ["AcousticEnvelopeType"],
        "_private.system_model.part_model.acoustics._2869": [
            "AcousticInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2870": ["CacheMemoryEstimates"],
        "_private.system_model.part_model.acoustics._2871": [
            "FEPartInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2872": [
            "FESurfaceSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2873": ["HoleInFaceGroup"],
        "_private.system_model.part_model.acoustics._2874": ["MeshedResultPlane"],
        "_private.system_model.part_model.acoustics._2875": ["MeshedResultSphere"],
        "_private.system_model.part_model.acoustics._2876": ["MeshedResultSurface"],
        "_private.system_model.part_model.acoustics._2877": ["MeshedResultSurfaceBase"],
        "_private.system_model.part_model.acoustics._2878": ["MicrophoneArrayDesign"],
        "_private.system_model.part_model.acoustics._2879": [
            "PartSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2880": ["ResultPlaneOptions"],
        "_private.system_model.part_model.acoustics._2881": ["ResultSphereOptions"],
        "_private.system_model.part_model.acoustics._2882": ["ResultSurfaceCollection"],
        "_private.system_model.part_model.acoustics._2883": ["ResultSurfaceOptions"],
        "_private.system_model.part_model.acoustics._2884": [
            "SphericalEnvelopeCentreDefinition"
        ],
        "_private.system_model.part_model.acoustics._2885": ["SphericalEnvelopeType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticAnalysisOptions",
    "AcousticAnalysisSetup",
    "AcousticAnalysisSetupCacheReporting",
    "AcousticAnalysisSetupCollection",
    "AcousticEnvelopeType",
    "AcousticInputSurfaceOptions",
    "CacheMemoryEstimates",
    "FEPartInputSurfaceOptions",
    "FESurfaceSelectionForAcousticEnvelope",
    "HoleInFaceGroup",
    "MeshedResultPlane",
    "MeshedResultSphere",
    "MeshedResultSurface",
    "MeshedResultSurfaceBase",
    "MicrophoneArrayDesign",
    "PartSelectionForAcousticEnvelope",
    "ResultPlaneOptions",
    "ResultSphereOptions",
    "ResultSurfaceCollection",
    "ResultSurfaceOptions",
    "SphericalEnvelopeCentreDefinition",
    "SphericalEnvelopeType",
)

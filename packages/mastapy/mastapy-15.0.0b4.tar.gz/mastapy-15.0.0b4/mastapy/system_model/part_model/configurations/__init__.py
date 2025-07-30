"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.configurations._2855 import (
        ActiveFESubstructureSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2856 import (
        ActiveFESubstructureSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2857 import (
        ActiveShaftDesignSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2858 import (
        ActiveShaftDesignSelectionGroup,
    )
    from mastapy._private.system_model.part_model.configurations._2859 import (
        BearingDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2860 import (
        BearingDetailSelection,
    )
    from mastapy._private.system_model.part_model.configurations._2861 import (
        DesignConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2862 import (
        PartDetailConfiguration,
    )
    from mastapy._private.system_model.part_model.configurations._2863 import (
        PartDetailSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.configurations._2855": [
            "ActiveFESubstructureSelection"
        ],
        "_private.system_model.part_model.configurations._2856": [
            "ActiveFESubstructureSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2857": [
            "ActiveShaftDesignSelection"
        ],
        "_private.system_model.part_model.configurations._2858": [
            "ActiveShaftDesignSelectionGroup"
        ],
        "_private.system_model.part_model.configurations._2859": [
            "BearingDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2860": [
            "BearingDetailSelection"
        ],
        "_private.system_model.part_model.configurations._2861": [
            "DesignConfiguration"
        ],
        "_private.system_model.part_model.configurations._2862": [
            "PartDetailConfiguration"
        ],
        "_private.system_model.part_model.configurations._2863": [
            "PartDetailSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ActiveFESubstructureSelection",
    "ActiveFESubstructureSelectionGroup",
    "ActiveShaftDesignSelection",
    "ActiveShaftDesignSelectionGroup",
    "BearingDetailConfiguration",
    "BearingDetailSelection",
    "DesignConfiguration",
    "PartDetailConfiguration",
    "PartDetailSelection",
)

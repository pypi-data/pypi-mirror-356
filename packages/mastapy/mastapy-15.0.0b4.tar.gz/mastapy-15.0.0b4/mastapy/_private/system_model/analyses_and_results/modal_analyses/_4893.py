"""DynamicModelForModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6636

_DYNAMIC_MODEL_FOR_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "DynamicModelForModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2889
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7872,
        _7881,
        _7887,
    )

    Self = TypeVar("Self", bound="DynamicModelForModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DynamicModelForModalAnalysis._Cast_DynamicModelForModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicModelForModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicModelForModalAnalysis:
    """Special nested class for casting DynamicModelForModalAnalysis to subclasses."""

    __parent__: "DynamicModelForModalAnalysis"

    @property
    def dynamic_analysis(self: "CastSelf") -> "_6636.DynamicAnalysis":
        return self.__parent__._cast(_6636.DynamicAnalysis)

    @property
    def fe_analysis(self: "CastSelf") -> "_7881.FEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7881,
        )

        return self.__parent__._cast(_7881.FEAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7887.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7887,
        )

        return self.__parent__._cast(_7887.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7872.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7872,
        )

        return self.__parent__._cast(_7872.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2889.Context":
        from mastapy._private.system_model.analyses_and_results import _2889

        return self.__parent__._cast(_2889.Context)

    @property
    def dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "DynamicModelForModalAnalysis":
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
class DynamicModelForModalAnalysis(_6636.DynamicAnalysis):
    """DynamicModelForModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_MODEL_FOR_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicModelForModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_DynamicModelForModalAnalysis
        """
        return _Cast_DynamicModelForModalAnalysis(self)

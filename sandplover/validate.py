"""Validation and repair functionality for sandsuet data specification.

This module provides tools to validate datasets against the sandsuet v1.0.0
specification and repair common issues.
"""

import abc
from dataclasses import dataclass, field
from typing import Dict, List, Union

import xarray as xr


# =============================================================================
# Exception Classes
# =============================================================================


class ValidationError(Exception):
    """Base exception for sandsuet specification violations."""

    pass


class HierarchyError(ValidationError):
    """Raised when dataset hierarchy is invalid (Spec 1)."""

    pass


class DimensionError(ValidationError):
    """Raised when dimensions don't meet specification (Spec 4)."""

    pass


class CoordinateError(ValidationError):
    """Raised when coordinates are invalid (Spec 5)."""

    pass


class VariableError(ValidationError):
    """Raised when variables don't meet specification (Spec 6)."""

    pass


# =============================================================================
# Validation Result Classes
# =============================================================================


@dataclass
class ValidationIssue:
    """Represents a single validation issue.

    Parameters
    ----------
    severity : str
        Issue severity level: 'error', 'warning', or 'info'.
    code : str
        Short identifier for the issue type (e.g., 'SPEC_5a').
    message : str
        Human-readable description of the issue.
    specification : str
        Reference to the relevant section of the sandsuet specification.
    repairable : bool
        Whether this issue can be automatically repaired.
    """

    severity: str
    code: str
    message: str
    specification: str
    repairable: bool

    def __post_init__(self):
        """Validate severity level."""
        valid_severities = {"error", "warning", "info"}
        if self.severity not in valid_severities:
            raise ValueError(
                f"Invalid severity '{self.severity}'. "
                f"Must be one of {valid_severities}"
            )


@dataclass
class ValidationReport:
    """Complete validation report for a dataset.

    Parameters
    ----------
    valid : bool
        Whether the dataset passes validation.
    issues : list of ValidationIssue
        All issues found during validation.
    """

    valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)

    def errors(self) -> List[ValidationIssue]:
        """Return only errors."""
        return [i for i in self.issues if i.severity == "error"]

    def warnings(self) -> List[ValidationIssue]:
        """Return only warnings."""
        return [i for i in self.issues if i.severity == "warning"]

    def repairable_issues(self) -> List[ValidationIssue]:
        """Return issues that can be auto-repaired."""
        return [i for i in self.issues if i.repairable]

    def summary(self) -> str:
        """Generate human-readable summary."""
        lines = ["Validation Report", "=" * 17]
        status = "VALID" if self.valid else "INVALID"
        lines.append(f"Status: {status}")
        lines.append(f"Errors: {len(self.errors())}")
        lines.append(f"Warnings: {len(self.warnings())}")
        return "\n".join(lines)


# =============================================================================
# Base Validator Class
# =============================================================================


class BaseValidator(abc.ABC):
    """Base class for all validators."""

    @abc.abstractmethod
    def validate(self, dataset: xr.DataTree) -> List[ValidationIssue]:
        """Validate a specific aspect of the dataset.

        Parameters
        ----------
        dataset : xr.DataTree
            The dataset to validate.

        Returns
        -------
        list of ValidationIssue
            Any issues found during validation.
        """
        pass


# =============================================================================
# Specific Validator Classes (Placeholders)
# =============================================================================


class HierarchyValidator(BaseValidator):
    """Validates Specification 1: Hierarchical organization."""

    def validate(self, dataset: xr.DataTree) -> List[ValidationIssue]:
        """Check hierarchy requirements."""
        issues = []
        # TODO: Implement hierarchy validation
        return issues


class GridValidator(BaseValidator):
    """Validates Specification 2: Rectilinear grid requirement."""

    def validate(self, dataset: xr.DataTree) -> List[ValidationIssue]:
        """Check grid requirements."""
        issues = []
        # TODO: Implement grid validation
        return issues


class MetadataValidator(BaseValidator):
    """Validates Specification 3: Required metadata."""

    def validate(self, dataset: xr.DataTree) -> List[ValidationIssue]:
        """Check metadata requirements."""
        issues = []
        # TODO: Implement metadata validation
        return issues


class DimensionValidator(BaseValidator):
    """Validates Specification 4: Dimension ordering and constraints."""

    def validate(self, dataset: xr.DataTree) -> List[ValidationIssue]:
        """Check dimension requirements."""
        issues = []
        # TODO: Implement dimension validation
        return issues


class CoordinateValidator(BaseValidator):
    """Validates Specification 5: Coordinate specifications."""

    def validate(self, dataset: xr.DataTree) -> List[ValidationIssue]:
        """Check coordinate requirements."""
        issues = []
        # TODO: Implement coordinate validation
        return issues


class VariableValidator(BaseValidator):
    """Validates Specification 6: Variable requirements."""

    def validate(self, dataset: xr.DataTree) -> List[ValidationIssue]:
        """Check variable requirements."""
        issues = []
        # TODO: Implement variable validation
        return issues


# =============================================================================
# Main Validator Class (Orchestrator)
# =============================================================================


class SandsuetValidator:
    """Main validator orchestrating all validation checks."""

    def __init__(self):
        """Initialize the validator."""
        self.validators = [
            HierarchyValidator(),
            GridValidator(),
            MetadataValidator(),
            DimensionValidator(),
            CoordinateValidator(),
            VariableValidator(),
        ]

    def validate(
        self, data: Union[str, xr.DataTree, xr.Dataset, Dict]
    ) -> ValidationReport:
        """Validate a dataset against sandsuet specification.

        Parameters
        ----------
        data : str, xr.DataTree, xr.Dataset, or dict
            Data to validate.

        Returns
        -------
        ValidationReport
            Complete validation report with all issues found.
        """
        issues = []

        # Load data if needed
        dataset = self._load_data(data)

        # Run all validators
        for validator in self.validators:
            validator_issues = validator.validate(dataset)
            issues.extend(validator_issues)

        # Determine if valid (only errors make it invalid)
        errors = [i for i in issues if i.severity == "error"]
        valid = len(errors) == 0

        return ValidationReport(valid=valid, issues=issues)

    def _load_data(
        self, data: Union[str, xr.DataTree, xr.Dataset, Dict]
    ) -> xr.DataTree:
        """Load data into xarray DataTree format."""
        if isinstance(data, xr.DataTree):
            return data
        elif isinstance(data, xr.Dataset):
            return xr.DataTree(data)
        elif isinstance(data, str):
            return xr.open_datatree(data)
        elif isinstance(data, dict):
            dataset = xr.Dataset(data)
            return xr.DataTree(dataset)
        else:
            raise TypeError(
                f"Unsupported data type: {type(data)}. "
                "Expected str, xr.DataTree, xr.Dataset, or dict."
            )

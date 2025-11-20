"""Tests for the validation module."""

import numpy as np
import pytest
import xarray as xr

from sandplover.validate import (
    SandsuetValidator,
    ValidationIssue,
    ValidationReport,
)


# =============================================================================
# Test ValidationIssue
# =============================================================================


class TestValidationIssue:
    """Test ValidationIssue dataclass."""

    def test_create_issue(self):
        """Test creating a validation issue."""
        issue = ValidationIssue(
            severity="error",
            code="TEST_001",
            message="Test message",
            specification="Test spec",
            repairable=False,
        )
        assert issue.severity == "error"
        assert issue.code == "TEST_001"
        assert issue.message == "Test message"
        assert issue.specification == "Test spec"
        assert issue.repairable is False

    def test_invalid_severity(self):
        """Test that invalid severity raises error."""
        with pytest.raises(ValueError, match="Invalid severity"):
            ValidationIssue(
                severity="critical",
                code="TEST_002",
                message="Test",
                specification="Test",
                repairable=False,
            )


# =============================================================================
# Test ValidationReport
# =============================================================================


class TestValidationReport:
    """Test ValidationReport dataclass."""

    def test_empty_report(self):
        """Test creating empty validation report."""
        report = ValidationReport(valid=True, issues=[])
        assert report.valid is True
        assert len(report.issues) == 0
        assert len(report.errors()) == 0
        assert len(report.warnings()) == 0

    def test_report_with_errors(self):
        """Test report containing errors."""
        issues = [
            ValidationIssue(
                severity="error",
                code="E1",
                message="Error 1",
                specification="Spec 1",
                repairable=False,
            ),
        ]
        report = ValidationReport(valid=False, issues=issues)
        assert report.valid is False
        assert len(report.errors()) == 1

    def test_summary_generation(self):
        """Test summary generation."""
        report = ValidationReport(valid=True, issues=[])
        summary = report.summary()
        assert "VALID" in summary
        assert "Errors: 0" in summary


# =============================================================================
# Test SandsuetValidator
# =============================================================================


class TestSandsuetValidator:
    """Test main SandsuetValidator orchestrator."""

    def test_validator_creation(self):
        """Test validator can be created."""
        validator = SandsuetValidator()
        assert validator is not None

    def test_validator_has_all_validators(self):
        """Test validator includes all sub-validators."""
        validator = SandsuetValidator()
        assert len(validator.validators) == 6

    def test_validate_with_dataset(self):
        """Test validation with xarray Dataset."""
        validator = SandsuetValidator()
        ds = xr.Dataset(
            {"temp": (["time", "x", "y"], np.zeros((2, 3, 4)))},
            coords={"time": np.arange(2), "x": np.arange(3), "y": np.arange(4)},
        )
        report = validator.validate(ds)
        assert isinstance(report, ValidationReport)
        assert report.valid is True

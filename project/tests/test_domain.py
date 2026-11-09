"""Stage 7 domain tests for Patient, Practitioner and Appointment contracts, and validation of required fields.

Constraints, construction verification, validating contracts, and ensuring that the domain objects are immutable once created. And transitions between states are valid and enforced.
"""

from datetime import datetime, timezone

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
    required_text,
    validate_required_text,
    validate_date_time,
)

WHEN = datetime(2026, 11, 2, 8, tzinfo=timezone.aedt)  # 8am AEDT, 2 Nov 2026

# Patient domain tests

def test_domain_patient_valid_construction() -> None:
    """A valid patient can be constructed with required fields."""
    patient = Patient('P1', 'Alex Fox')
    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Fox'

def test_domain_patient_invalid_construction() -> None:
    """A patient cannot be constructed with invalid required fields."""
    with pytest.raises(ValueError):
        Patient('', 'Alex Fox')
    with pytest.raises(ValueError):
        Patient('P1', '')

@pytest.mark.parametrize('invalid_id', ['', ' ', '  ', None, 7, 0, -1, 3.14, True, False, [], {}, set(), object()])
def test_domain_patient_invalid_id(invalid_id) -> None:
    """A patient cannot be constructed with an invalid ID/non-string."""
    with pytest.raises(ValueError):
        Patient(invalid_id, 'Alex Fox') # type: ignore[arg-type]

@pytest.mark.parametrize('invalid_name', ['', ' ', '  ', None, 7, 0, -1, 3.14, True, False, [], {}, set(), object()])
def test_domain_patient_invalid_name(invalid_name) -> None:
    """A patient cannot be constructed with an invalid name/non-string/blank."""
    with pytest.raises(ValueError):
        Patient('P1', invalid_name) # type: ignore[arg-type]

# Practitioner domain tests
def test_domain_practitioner_valid_construction() -> None:
    """A valid practitioner can be constructed with required fields."""
    practitioner = Practitioner('D1', 'Ben Taylor', 'General')
    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Ben Taylor'
    assert practitioner.specialty == 'General'

@pytest.mark.parametrize('invalid_id', ['', ' ', '  ', None, 7, 0, -1, 3.14, True, False, [], {}, set(), object()])
def test_domain_practitioner_invalid_id(invalid_id) -> None:
    """A practitioner cannot be constructed with an invalid ID/non-string/blank."""
    with pytest.raises(ValueError):
        Practitioner(invalid_id, 'Ben Taylor', 'General') # type: ignore[arg-type]
    with pytest.raises(ValueError):
        Practitioner('D1', invalid_id, 'General') # type: ignore[arg-type]

@pytest.mark.parametrize('invalid_specialty', ['', ' ', '  ', None, 7, 0, -1, 3.14, True, False, [], {}, set(), object()])
def test_domain_practitioner_invalid_specialty(invalid_specialty) -> None:
    """A practitioner cannot be constructed with an invalid specialty/non-string/blank."""
    with pytest.raises(ValueError):
        Practitioner('D1', 'Ben Taylor', invalid_specialty) # type: ignore[arg-type]


# Appointment domain tests and status transitions

def test_domain_appointment_initial_status_is_scheduled() -> None:
    """A newly created appointment should have status SCHEDULED."""
    appointment = Appointment('A1', 'P1', 'D1', WHEN)
    assert appointment.status == AppointmentStatus.SCHEDULED

def test_domain_appointment_valid_construction_and_fields() -> None:
    """A valid appointment can be constructed with required fields."""
    appointment = Appointment('A1', 'P1', 'D1', WHEN)
    assert appointment.appointment_id == 'A1'
    assert appointment.patient_id == 'P1'
    assert appointment.practitioner_id == 'D1'
    assert appointment.when == WHEN
    assert appointment.status == AppointmentStatus.SCHEDULED

def test_domain_appointment_cancelled_status_transition() -> None:
    """An appointment can transition from SCHEDULED to CANCELLED."""
    appointment = Appointment('A1', 'P1', 'D1', WHEN)
    cancelled_appointment = appointment.cancel()
    assert cancelled_appointment.status == AppointmentStatus.CANCELLED

def test_domain_appointment_invalid_fields() -> None:
    """An appointment cannot be constructed with invalid required fields."""
    with pytest.raises(ValueError):
        Appointment('', 'P1', 'D1', WHEN)
    with pytest.raises(ValueError):
        Appointment('A1', '', 'D1', WHEN)
    with pytest.raises(ValueError):
        Appointment('A1', 'P1', '', WHEN)
    with pytest.raises(ValueError):
        Appointment('A1', 'P1', 'D1', None)


### DateTime validation tests

def test_domain_appointment_datetime_boundaries_rejected() -> None:
    """Appointments cannot be created with invalid datetime values."""
    with pytest.raises(ValueError):
        Appointment('A1', 'P1', 'D1', datetime(2026, 11, 2, 8, tzinfo=timezone.aedt))  #AEDT, timezone-aware
    with pytest.raises(ValueError):
        Appointment('A1', 'P1', 'D1', datetime(2026, 11, 2, 8))  # naive datetime without timezone

## Cancellation Domain Transition Tests

def test_domain_appointment_cancel_changes_status() -> None:
    """Cancelling an appointment should change its status to CANCELLED."""
    practitioner = Practitioner('D1', 'Ben Taylor', 'General')
    patient = Patient('P1', 'Alex Fox')
    appointment = Appointment('A1', 'P1', 'D1', WHEN)
    cancelled_appointment = appointment.cancel()
    assert cancelled_appointment.status == AppointmentStatus.CANCELLED

def test_domain_appointment_repeated_cancellation_raises_error() -> None:
    """Attempting to cancel an already cancelled appointment should raise an error."""
    appointment = Appointment('A1', 'P1', 'D1', WHEN)
    cancelled_appointment = appointment.cancel()
    with pytest.raises(ValueError):
        cancelled_appointment.cancel()
    assert cancelled_appointment.status == AppointmentStatus.CANCELLED

def test_domain_appointment_cancel_completed_transition() -> None:
    """Cancelling an appointment should not allow further transitions."""
    appointment = Appointment('A1', 'P1', 'D1', WHEN)
    cancelled_appointment = appointment.cancel()
    with pytest.raises(ValueError):
        cancelled_appointment.cancel()
    assert cancelled_appointment.status == AppointmentStatus.CANCELLED
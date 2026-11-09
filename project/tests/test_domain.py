"""Stage 7 domain tests for validation, appointment state, and transitions."""

from datetime import datetime, timezone

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
    required_text,
    validate_date_time,
)

WHEN = datetime(2026, 11, 2, 8)
INVALID_TEXT = ['', ' ', '  ', None, 7, 0, -1, 3.14, True, False, [], {}, set(), object()]

# Patient domain tests
def test_required_text_trims_and_rejects_invalid_values() -> None:
    assert required_text('  Alex Fox  ', 'Name') == 'Alex Fox'
    for value in INVALID_TEXT:
        with pytest.raises(ValueError):
            required_text(value, 'Name')


def test_patient_valid_construction() -> None:
    patient = Patient(' P1 ', ' Alex Fox ')
    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Fox'


@pytest.mark.parametrize('invalid_id', INVALID_TEXT)
def test_patient_rejects_invalid_id(invalid_id) -> None:
    with pytest.raises(ValueError):
        Patient(invalid_id, 'Alex Fox')


@pytest.mark.parametrize('invalid_name', INVALID_TEXT)
def test_patient_rejects_invalid_name(invalid_name) -> None:
    with pytest.raises(ValueError):
        Patient('P1', invalid_name)


def test_practitioner_valid_construction() -> None:
    practitioner = Practitioner(' D1 ', ' Ben Taylor ', ' General ')
    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Ben Taylor'
    assert practitioner.specialty == 'General'


@pytest.mark.parametrize('invalid_id', INVALID_TEXT)
def test_practitioner_rejects_invalid_id(invalid_id) -> None:
    with pytest.raises(ValueError):
        Practitioner(invalid_id, 'Ben Taylor', 'General')


@pytest.mark.parametrize('invalid_name', INVALID_TEXT)
def test_practitioner_rejects_invalid_name(invalid_name) -> None:
    with pytest.raises(ValueError):
        Practitioner('D1', invalid_name, 'General')


@pytest.mark.parametrize('invalid_specialty', INVALID_TEXT)
def test_practitioner_rejects_invalid_specialty(invalid_specialty) -> None:
    with pytest.raises(ValueError):
        Practitioner('D1', 'Ben Taylor', invalid_specialty)

# Appointment domain tests
def make_appointment(
    status: AppointmentStatus = AppointmentStatus.SCHEDULED,
) -> Appointment:
    return Appointment(
        'A1',
        Patient('P1', 'Alex Fox'),
        Practitioner('D1', 'Ben Taylor', 'General'),
        WHEN,
        status,
    )

def test_appointment_valid_construction_and_default_status() -> None:
    appointment = make_appointment()
    assert appointment.appointment_id == 'A1'
    assert appointment.patient.patient_id == 'P1'
    assert appointment.practitioner.practitioner_id == 'D1'
    assert appointment.date_time == WHEN
    assert appointment.status is AppointmentStatus.SCHEDULED


def test_appointment_rejects_invalid_fields() -> None:
    patient = Patient('P1', 'Alex Fox')
    practitioner = Practitioner('D1', 'Ben Taylor', 'General')
    with pytest.raises(ValueError):
        Appointment('', patient, practitioner, WHEN)
    with pytest.raises(ValueError):
        Appointment('A1', 'P1', practitioner, WHEN)
    with pytest.raises(ValueError):
        Appointment('A1', patient, 'D1', WHEN)
    with pytest.raises(ValueError):
        Appointment('A1', patient, practitioner, None)
    with pytest.raises(ValueError):
        Appointment('A1', patient, practitioner, WHEN, 'scheduled')

# Datetime validation tests
def test_validate_date_time_requires_naive_minute_precision_datetime() -> None:
    assert validate_date_time(WHEN) == WHEN
    invalid_values = [
        None,
        '2026-11-02 08:00',
        datetime(2026, 11, 2, 8, tzinfo=timezone.utc),
        datetime(2026, 11, 2, 8, 0, 1),
        datetime(2026, 11, 2, 8, 0, 0, 1),
    ]
    for value in invalid_values:
        with pytest.raises(ValueError):
            validate_date_time(value)

# Cancellation Domain transition tests
def test_cancelling_scheduled_appointment_changes_status() -> None:
    appointment = make_appointment()
    assert appointment.cancel() is None
    assert appointment.status is AppointmentStatus.CANCELLED


def test_repeated_cancellation_raises_and_preserves_cancelled_status() -> None:
    appointment = make_appointment()
    appointment.cancel()
    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED


def test_completed_appointment_cannot_be_cancelled() -> None:
    appointment = make_appointment(AppointmentStatus.COMPLETED)
    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is AppointmentStatus.COMPLETED

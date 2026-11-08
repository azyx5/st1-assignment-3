"""Valid Stage 6 service tests for lookup and cancellation contracts."""

from __future__ import annotations

from datetime import datetime
from typing import NamedTuple

import pytest 

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus, Patient, Practitioner
from smartcare.services import AppointmentService, PatientService, PractitionerService

WHEN = datetime(2026, 11, 2, 8)
INVALID_IDS = ['', ' ', '  ', None, 7, 0, -1, 3.14, True, False, [], {}, set(), object()]


class Session(NamedTuple):
    """A test session with a data store and registered participants."""

    store: SmartCareDataStore
    patient_service: PatientService
    practitioner_service: PractitionerService
    appointment_service: AppointmentService
    patient: Patient
    practitioner: Practitioner
    appointment: Appointment


def setup_session() -> Session:
    """Create a basic registered patient, practitioner and appointment."""
    store = SmartCareDataStore()
    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient = patient_service.register_patient('P1', 'Alex Fox')
    practitioner = practitioner_service.register_practitioner(
        'D1',
        'Ben Taylor',
        'General',
    )
    appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        WHEN,
    )

    return Session(
        store=store,
        patient_service=patient_service,
        practitioner_service=practitioner_service,
        appointment_service=appointment_service,
        patient=patient,
        practitioner=practitioner,
        appointment=appointment,
    )

#FR01-02 Patient Lookup/search & registration
def test_find_patient_returns_registered_object() -> None:
    """A registered patient ID must return the original object."""
    session = setup_session()
    found = session.patient_service.find_patient('P1')
    assert found is session.patient
    assert found.name == 'Alex Fox'


def test_find_patient_trims_and_is_case_sensitive() -> None:
    """Whitespace should be trimmed and IDs should remain case-sensitive."""
    session = setup_session()
    assert session.patient_service.find_patient(' P1 ') is session.patient
    with pytest.raises(LookupError):
        session.patient_service.find_patient('p1')


@pytest.mark.parametrize('invalid_id', INVALID_IDS)
def test_find_patient_invalid_id_raises_value_error(invalid_id) -> None:
    """Blank or malformed patient IDs must raise ValueError."""
    session = setup_session()
    with pytest.raises(ValueError):
        session.patient_service.find_patient(invalid_id)


def test_find_unknown_patient_raises_lookup_error() -> None:
    """Unknown patient IDs must raise LookupError without creating a record."""
    session = setup_session()
    with pytest.raises(LookupError):
        session.patient_service.find_patient('P2')
    assert session.store.find_patient('P2') is None


#FR03 Practitioner Lookup & registration
def test_find_practitioner_returns_registered_object() -> None:
    """A registered practitioner ID must return the original object."""
    session = setup_session()
    found = session.practitioner_service.find_practitioner('D1')
    assert found is session.practitioner
    assert found.specialty == 'General'


def test_find_practitioner_trims_and_is_case_sensitive() -> None:
    """Whitespace should be trimmed and IDs should remain case-sensitive."""
    session = setup_session()
    assert session.practitioner_service.find_practitioner(' D1 ') is session.practitioner
    with pytest.raises(LookupError):
        session.practitioner_service.find_practitioner('d1')


@pytest.mark.parametrize('invalid_id', INVALID_IDS)
def test_find_practitioner_invalid_id_raises_value_error(invalid_id) -> None:
    """Blank or malformed practitioner IDs must raise ValueError."""
    session = setup_session()
    with pytest.raises(ValueError):
        session.practitioner_service.find_practitioner(invalid_id)


def test_find_unknown_practitioner_raises_lookup_error() -> None:
    """Unknown practitioner IDs must raise LookupError without creating a record."""
    session = setup_session()
    with pytest.raises(LookupError):
        session.practitioner_service.find_practitioner('D2')
    assert session.store.find_practitioner('D2') is None

# FR06-FR07 Appointment Lookup/retained history & Cancellation
def test_cancel_appointment_returns_cancelled_object() -> None:
    """Cancel should return the original appointment object in the cancelled state."""
    session = setup_session()
    cancelled = session.appointment_service.cancel_appointment('A1')
    assert cancelled is session.appointment
    assert cancelled.status is AppointmentStatus.CANCELLED


def test_cancelled_appointment_remains_in_store_and_can_be_retrieved() -> None:
    """Cancelled appointments must remain stored and retrievable."""
    session = setup_session()
    cancelled = session.appointment_service.cancel_appointment('A1')
    assert session.store.find_appointment('A1') is cancelled
    assert session.appointment_service.find_appointment('A1') is cancelled
    assert cancelled.date_time == WHEN
    assert session.store.list_appointments() == [cancelled]


def test_cancel_unknown_appointment_raises_lookup_error() -> None:
    """Unknown appointment IDs must raise LookupError."""
    session = setup_session()
    with pytest.raises(LookupError):
        session.appointment_service.cancel_appointment('A2')
    assert session.store.find_appointment('A2') is None


def test_cancel_appointment_repeatedly_raises_value_error() -> None:
    """Cancelling the same appointment twice should fail on the second call."""
    session = setup_session()
    session.appointment_service.cancel_appointment('A1')
    with pytest.raises(ValueError):
        session.appointment_service.cancel_appointment('A1')


def test_cancel_appointment_trimmed_id_and_case_sensitivity() -> None:
    """Cancellation should trim whitespace and be case-sensitive."""
    session = setup_session()
    assert session.appointment_service.cancel_appointment(' A1 ') is session.appointment
    with pytest.raises(LookupError):
        session.appointment_service.cancel_appointment('a1')


@pytest.mark.parametrize('invalid_id', INVALID_IDS)
def test_find_appointment_invalid_id_raises_value_error(invalid_id) -> None:
    """Blank or malformed appointment IDs must raise ValueError."""
    session = setup_session()
    with pytest.raises(ValueError):
        session.appointment_service.find_appointment(invalid_id)

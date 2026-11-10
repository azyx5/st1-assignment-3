"""Stage 8 regression checks

Covers progression tests for the domain and service layers, including validation, appointment state, and transitions. Practitioner conflict prevention, retrieval, and cancellation are also tested.
"""

from datetime import datetime

import pytest

from project.tests.test_services import WHEN
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus, Patient, Practitioner
from smartcare.services import (AppointmentService,
    PatientService,
    PractitionerService,
)

WHEN = datetime(2026, 11, 2, 8)

def setup_regression_session() -> tuple[SmartCareDataStore, PatientService, PractitionerService, AppointmentService, Patient, Practitioner]:
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
    appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        WHEN,
    )

    return store, patient_service, practitioner_service, appointment_service, patient, practitioner

#Pracritioner conflict prevention, retrieval, and cancellation tests

def test_same_practitioner_time_conflict_rejects_without_affecting_existing_appointment() -> None:
    store, patient_service, practitioner_service, appointment_service, patient, practitioner = setup_regression_session()
    with pytest.raises(ValueError):
        appointment_service.book_appointment(
            'A2',
            'P1',
            'D1',
            WHEN,
        )
    # Ensures the original appointment still remains valid and unchanged
    appointment = appointment_service.get_appointment('A1')
    assert appointment.status == AppointmentStatus.SCHEDULED

    # Book initial appointment with D1 at WHEN
    a1 = appointment_service.book_appointment('A1', 'P1', 'D1', WHEN)
    assert a1.status == AppointmentStatus.SCHEDULED
    assert store.get_appointment('A1') == a1

    #Attempt conflicted booking with same practitioner at same time
    with pytest.raises(ValueError):
        appointment_service.book_appointment('A2', 'P1', 'D1', WHEN)
    assert 'Practitioner D1 already has an appointment at this time' in str(ValueError)

    # State preservation check: original appointment remains unchanged
    a1_after_conflict = appointment_service.get_appointment('A1')
    assert a1_after_conflict.status == AppointmentStatus.SCHEDULED
    assert store.find_appointment('A1') == a1_after_conflict
    assert store.find_appointment('A2') is None  # Conflicted appointment should not exist

    # However, booking with a different practitioner at the same time should succeed
    a2 = appointment_service.book_appointment('A2', 'P1', 'D2', WHEN)
    assert a2.practitioner.practitioner_id == 'D2'
    assert a2.status is AppointmentStatus.SCHEDULED
    assert store.list_appointments() == [a1_after_conflict, a2]


# Retained history and retrievability of cancelled appointments

def test_cancelled_appointment_remains_retrievable_and_secure() -> None:
    """regression test: cancelled appointments remain stored and retrievable"""
    store, patient_service, practitioner_service, appointment_service, patient, practitioner = setup_regression_session()
    appointment = appointment_service.book_appointment('A1', 'P1', 'D1', WHEN)
    assert appointment.status == AppointmentStatus.SCHEDULED

    # Ensure the appointment is initially scheduled in the store
    a1 = store.find_appointment('A1')
    assert a1.status == AppointmentStatus.SCHEDULED

    # Cancel the appointment
    appointment_service.cancel_appointment('A1')
    cancelled_appointment = appointment_service.find_appointment('A1')
    assert cancelled_appointment.status == AppointmentStatus.CANCELLED

    # Ensure the cancelled appointment is still retrievable from the store
    assert store.find_appointment('A1') == cancelled_appointment
    stored_lookup = store.find_appointment('A1')
    assert stored_lookup is a1, 'store.find_appointment should return the same object as initially stored, returned None for cancelled appointment'

    # Ensure the cancelled appointment is still the same object as initially stored
    service_lookup = appointment_service.find_appointment('A1')
    assert service_lookup is a1, 'Ensuring the service still returns the same object as initially stored and not return LookupError'
    assert service_lookup.status == AppointmentStatus.CANCELLED

    #History preservation check: ensure thathe appointment history reflects  cancellation
    assert store.list_appointments() == [a1], 'The store should still have the cancelled appointment in its history for future records or basic recordkeeping'

    # Ensure that attempting to book a new appointment at the same time with the same practitioner now succeeds
    new_appointment = appointment_service.book_appointment('A2', 'P1', 'D1', WHEN)
    assert new_appointment.status == AppointmentStatus.SCHEDULED
    assert store.list_appointments() == [a1, new_appointment]

    # Make sure that repeated cancellations do not remove the appointment from the store
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')
    assert a1.status == AppointmentStatus.CANCELLED
    assert store.list_appointments() == [a1, new_appointment], 'The store should still have the cancelled appointment in history after repeated cancellation attempts'


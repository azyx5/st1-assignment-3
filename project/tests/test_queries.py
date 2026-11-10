## Tests for smartcare.queries functions
"""Sorting and selection tests for smartcare.queries. QRY-01-QRY-03, FP-01-FP-03"""

from datetime import datetime
import pytest

from smartcare.queries import appointment_sort_key, select_appointments
from smartcare.domain import Appointment, AppointmentStatus, Practitioner, Patient
WHEN = datetime(2024, 6, 1, 10, 0)

T1, T2, T3, T4 = WHEN, datetime(2024, 6, 1, 11, 0), datetime(2024, 6, 1, 12, 0), datetime(2024, 6, 1, 13, 0)


def buiild_test_fixture():
    """Build a test fixture with a patient, practitioner, and a list of appointments."""
    appointments: list[Appointment] = []
    patient = Patient('P1', 'Alex Fox')
    practitioner = Practitioner('D1', 'Ben Taylor', 'General')
    appointments = [
        Appointment('A1', patient, practitioner, T1, AppointmentStatus.SCHEDULED),
        Appointment('A2', patient, practitioner, T2, AppointmentStatus.SCHEDULED),
        Appointment('A3', patient, practitioner, T3, AppointmentStatus.CANCELLED),
        Appointment('A4', patient, practitioner, T4, AppointmentStatus.SCHEDULED),
    ]
    return appointments, practitioner, patient

def test_select_appointments_filters_and_sorts_correctly() -> None:
    """Test that select_appointments filters by practitioner and status, and sorts correctly. QRY-01"""
    appointments, practitioner, patient = buiild_test_fixture()
    filtered = select_appointments(appointments, practitioner.practitioner_id, AppointmentStatus.SCHEDULED)
    assert all(a.practitioner_id == practitioner.practitioner_id for a in filtered)
    assert all(a.status == AppointmentStatus.SCHEDULED for a in filtered)
    assert filtered == sorted(filtered, key=appointment_sort_key)

def test_select_appointments_unmatched_practitioner_returns_empty() -> None:
    """Test that select_appointments returns an empty list for a practitioner with no appointments. QRY-01"""
    appointments, practitioner, patient = buiild_test_fixture()
    filtered = select_appointments(appointments, 'D2', AppointmentStatus.SCHEDULED)
    assert filtered == []

def test_select_appointments_unmatched_status_returns_empty() -> None:
    """Test that select_appointments returns an empty list for a status with no appointments. QRY-02"""
    appointments, practitioner, patient = buiild_test_fixture()
    filtered = select_appointments(appointments, practitioner.practitioner_id, AppointmentStatus.COMPLETED, AppointmentStatus.SCHEDULED, AppointmentStatus.CANCELLED)
    assert filtered == []

def test_select_appointments_sorts_correctly() -> None:
    """Test that select_appointments returns appointments sorted by the sort key. QRY-03"""
    appointments, practitioner, patient = buiild_test_fixture()
    filtered = select_appointments(appointments, practitioner.practitioner_id, AppointmentStatus.SCHEDULED)
    assert filtered == sorted(filtered, key=appointment_sort_key)

def test_select_appointments_returns_all_matching_statuses() -> None:
    """Test that select_appointments returns all appointments matching any of the given statuses. FP-01"""
    for st, expected_id in [
        (AppointmentStatus.SCHEDULED, ['A1', 'A2', 'A4']),
        (AppointmentStatus.CANCELLED, ['A3']),
    ]:
        appointments, practitioner, patient = buiild_test_fixture()
        filtered = select_appointments(appointments, practitioner.practitioner_id, st)
        assert [a.appointment_id for a in filtered] == expected_id
    appointments, practitioner, patient = buiild_test_fixture()
    filtered = select_appointments(appointments, practitioner.practitioner_id, AppointmentStatus.SCHEDULED, AppointmentStatus.CANCELLED)
    assert all(a.status in (AppointmentStatus.SCHEDULED, AppointmentStatus.CANCELLED) for a in filtered)
    assert filtered == sorted(filtered, key=appointment_sort_key)


def test_select_appointment_orders_by_datetime_and_id_tiebreak() -> None:
    p1 = Patient(patient_id='P1', name='Patient 1')
    d1 = Practitioner(practitioner_id='D1', name='Doctor 1')
    # Unsorted appointments with same datetime but different IDs to test tiebreak
    source = [
        Appointment ('C_ID', p1, d1, T2, AppointmentStatus.SCHEDULED),
        Appointment ('B_ID', p1, d1, T1, AppointmentStatus.CANCELLED),
        Appointment ('A_ID', p1, d1, T1, AppointmentStatus.COMPLETED),
    ]
    sorted_appointments = sorted(source, key=appointment_sort_key)
    assert sorted_appointments == [
        Appointment ('A_ID', p1, d1, T1, AppointmentStatus.COMPLETED),
        Appointment ('B_ID', p1, d1, T1, AppointmentStatus.CANCELLED),
        Appointment ('C_ID', p1, d1, T2, AppointmentStatus.SCHEDULED),
    ]





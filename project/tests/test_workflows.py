"""Tests for the workflows in the SmartCare application."""

from datetime import datetime
import pytest

from smartcare.console import run_menu
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

T1, T2 = datetime(2026, 10, 1, 9, 0), datetime(2026, 10, 1, 10, 0)
T3, T4 = datetime(2026, 10, 1, 11, 0), datetime(2026, 10, 1, 12, 0)

@pytest.fixture
def populated_services():
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    patients.register_patient('P1', 'Alex Fox')
    practitioners.register_practitioner('DR1', 'Ben Taylor', 'General practice')
    appointments.book_appointment('A1', 'P1', 'DR1', T1)

    return patients, practitioners, appointments, store

def test_list_practitioner_appointments_empty_for_known_practitioner(populated_services) -> None:
    populated_services[1].register_practitioner('DR2', 'Casey Jones', 'General')
    assert populated_services[2].list_practitioner_appointments('DR2') == []

def test_list_practitioner_appointments_unknown_practitioner_raises_lookup_error(populated_services) -> None:
    with pytest.raises(LookupError):
        populated_services[2].list_practitioner_appointments('DR_UNKNOWN')

def test_list_practitioner_appointments_blank_practitioner_raises_value_error(populated_services) -> None:
    with pytest.raises(ValueError):
        populated_services[2].list_practitioner_appointments('')

def test_list_practitioner_appointments_none_practitioner_raises_value_error(populated_services) -> None:
    with pytest.raises(ValueError):
        populated_services[2].list_practitioner_appointments(None)

def test_list_practitioner_appointments_valid_practitioner_returns_appointments(populated_services) -> None:
    result = populated_services[2].list_practitioner_appointments('DR1')
    assert len(result) == 1
    assert result[0].practitioner.practitioner_id == 'DR1'
    assert result[0].patient.patient_id == 'P1'
    assert result[0].status == AppointmentStatus.SCHEDULED
    assert result[0].date_time == T1

def test_list_practitioner_appointments_filtered_by_status(populated_services) -> None:
    appointments = populated_services[2]
    appointments.book_appointment('A2', 'P1', 'DR1', T2)
    appointments.cancel_appointment('A2')
    result = populated_services[2].list_practitioner_appointments(
        'DR1',
        status=AppointmentStatus.SCHEDULED,
    )
    assert len(result) == 1
    assert result[0].practitioner.practitioner_id == 'DR1'
    assert result[0].status == AppointmentStatus.SCHEDULED
    # Ensure the cancelled appointment is not included
    result_cancelled = populated_services[2].list_practitioner_appointments(
        'DR1',
        status=AppointmentStatus.CANCELLED,
    )
    assert len(result_cancelled) == 1
    assert result_cancelled[0].practitioner.practitioner_id == 'DR1'
    assert result_cancelled[0].status == AppointmentStatus.CANCELLED

def test_list_practitioner_appointments_returns_new_appointments(populated_services) -> None:
    appointments = populated_services[2]
    # Book a new appointment
    appointments.book_appointment('A3', 'P1', 'DR1', T3)
    result = populated_services[2].list_practitioner_appointments('DR1')
    assert any(appt.appointment_id == 'A3' for appt in result)
    # Ensure the new appointment has the correct details
    new_appt = next(appt for appt in result if appt.appointment_id == 'A3')
    assert new_appt.practitioner.practitioner_id == 'DR1'
    assert new_appt.patient.patient_id == 'P1'
    assert new_appt.status == AppointmentStatus.SCHEDULED
    assert new_appt.date_time == T3
    # Ensure the new appointment is included when filtering by status
    result_filtered = populated_services[2].list_practitioner_appointments(
        'DR1',
        status=AppointmentStatus.SCHEDULED,
    )
    assert any(appt.appointment_id == 'A3' for appt in result_filtered)

def test_ui01_end_to_end_booking_cancellation_and_history(populated_services) -> None:
    patients, practitioners, appointments, store = populated_services
    appointments.book_appointment('A4', 'P1', 'DR1', T4)
    appointments.cancel_appointment('A4')
    history = appointments.list_practitioner_appointments('DR1')
    assert any(appt.appointment_id == 'A4' for appt in history)
    cancelled_appt = next(appt for appt in history if appt.appointment_id == 'A4')
    assert cancelled_appt.status == AppointmentStatus.CANCELLED
    assert store.find_appointment('A4') is cancelled_appt
    with pytest.raises(ValueError):
        appointments.cancel_appointment('A4')
    assert store.find_appointment('A4') is cancelled_appt

def test_ui02_console_interactive_full_demonstration(monkeypatch, capsys) -> None:
    inputs = iter([
        '1', 'P1', 'Alex Fox',
        '3', 'DR1', 'Ben Taylor', 'General practice',
        '5', 'A5', 'P1', 'DR1', '2026-10-01 12:00',
        '6', 'A5',
        '7', 'A5',
        '8', 'DR1', 'cancelled',
        '8', 'DR1', 'scheduled',
        '8', 'DR1', '',
        '0',
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert 'Registered patient P1.' in captured.out
    assert 'Appointment: A5' in captured.out
    assert 'Status: cancelled' in captured.out
    assert 'No appointments found.' in captured.out
    assert 'Goodbye.' in captured.out


def test_ui02_console_handles_invalid_input(monkeypatch, capsys) -> None:
    inputs = iter([
        'invalid',
        '0',
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert 'Invalid option.' in captured.out
    assert 'Goodbye.' in captured.out

def test_ui02_console_handles_empty_input(monkeypatch, capsys) -> None:
    inputs = iter([
        '',
        '0',
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert 'Invalid option.' in captured.out
    assert 'Goodbye.' in captured.out

def test_ui02_console_recovers_from_invalid_status(monkeypatch, capsys) -> None:
    inputs = iter(['8', 'DR1', 'unknown', '0'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    run_menu()
    captured = capsys.readouterr()
    assert 'Error: Invalid appointment status' in captured.out
    assert 'Goodbye.' in captured.out

def test_ui02_console_exits_cleanly_on_eof(monkeypatch, capsys) -> None:
    def eof_input(_: str) -> str:
        raise EOFError

    monkeypatch.setattr('builtins.input', eof_input)
    run_menu()
    assert 'Goodbye.' in capsys.readouterr().out
    

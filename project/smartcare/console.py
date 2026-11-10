"""Console helpers and a small runnable starting demonstration."""

import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

MENU_TEXT = """MAIN MENU
1. Register Patient
2. Find Patient
3. Register Practitioner
4. Find Practitioner
5. Book Appointment
6. Find Appointment
7. Cancel Appointment
8. List Appointments
9. Exit
"""

STATUS_MAP = {
    '': (None, 'All Statuses'),
    'scheduled': (AppointmentStatus.SCHEDULED, 'Scheduled'),
    'cancelled': (AppointmentStatus.CANCELLED, 'Cancelled'),
    'completed': (AppointmentStatus.COMPLETED, 'Completed'),
}

def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'Appointment: {appointment.appointment_id}\n'
        f'Patient: {appointment.patient.patient_id} - {appointment.patient.name}\n'
        f'Practitioner: {appointment.practitioner.practitioner_id} - '
        f'{appointment.practitioner.name} ({appointment.practitioner.specialty})\n'
        f'Date/time: {appointment.date_time:%Y-%m-%d %H:%M}\n'
        f'Status: {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Fox')
    practitioners.register_practitioner(
        'DR1',
        'Ben Taylor',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


def run_menu() -> None:
    """Run the interactive SmartCare menu until the user exits or sends EOF."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    while True:
        print(MENU_TEXT)
        try:
            choice = input('Choose an option: ').strip()
            if choice == '0':
                print('Goodbye.')
                return
            if choice == '1':
                patient = patients.register_patient(
                    input('Patient ID: '),
                    input('Patient name: '),
                )
                print(f'Registered patient {patient.patient_id}.')
            elif choice == '2':
                patient = patients.find_patient(input('Patient ID: '))
                print(f'{patient.patient_id}: {patient.name}')
            elif choice == '3':
                practitioner = practitioners.register_practitioner(
                    input('Practitioner ID: '),
                    input('Practitioner name: '),
                    input('Specialty: '),
                )
                print(f'Registered practitioner {practitioner.practitioner_id}.')
            elif choice == '4':
                practitioner = practitioners.find_practitioner(
                    input('Practitioner ID: '),
                )
                print(
                    f'{practitioner.practitioner_id}: {practitioner.name} '
                    f'({practitioner.specialty})',
                )
            elif choice == '5':
                appointment = appointments.book_appointment(
                    input('Appointment ID: '),
                    input('Patient ID: '),
                    input('Practitioner ID: '),
                    parse_date_time(input('Date/time (YYYY-MM-DD HH:MM): ')),
                )
                print(format_appointment(appointment))
            elif choice == '6':
                appointment = appointments.find_appointment(
                    input('Appointment ID: '),
                )
                print(format_appointment(appointment))
            elif choice == '7':
                appointment = appointments.cancel_appointment(
                    input('Appointment ID: '),
                )
                print(format_appointment(appointment))
            elif choice == '8':
                practitioner_id = input('Practitioner ID: ')
                status_text = input(
                    'Status (scheduled, cancelled, completed, or blank for all): ',
                ).strip().lower()
                if status_text not in STATUS_MAP:
                    raise ValueError('Invalid appointment status')
                status, _ = STATUS_MAP[status_text]
                matching = appointments.list_practitioner_appointments(
                    practitioner_id,
                    status,
                )
                if not matching:
                    print('No appointments found.')
                for appointment in matching:
                    print(format_appointment(appointment))
            else:
                print('Invalid option.')
        except EOFError:
            print('Goodbye.')
            return
        except (ValueError, LookupError) as error:
            print(f'Error: {error}')

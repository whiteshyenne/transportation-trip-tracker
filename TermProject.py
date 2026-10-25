"""Transportation Trip Tracker. Run with Python 3.10 or newer."""
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / 'trips.json'
STATUSES = ('Scheduled', 'Completed', 'Cancelled')


@dataclass
class Trip:
    trip_id: int
    trip_date: str
    passenger: str
    destination: str
    miles: str
    fare: str
    status: str = 'Scheduled'

    def __post_init__(self):
        if type(self.trip_id) is not int or self.trip_id < 1:
            raise ValueError('Trip ID must be a positive integer.')
        datetime.strptime(self.trip_date, '%Y-%m-%d')
        if not isinstance(self.passenger, str) or not self.passenger.strip():
            raise ValueError('Passenger cannot be blank.')
        if not isinstance(self.destination, str) or not self.destination.strip():
            raise ValueError('Destination cannot be blank.')
        for value in (self.miles, self.fare):
            number = Decimal(value)
            if not number.is_finite() or number < 0:
                raise ValueError('Miles and fare must be finite and nonnegative.')
        if self.status not in STATUSES:
            raise ValueError('Invalid trip status.')

    def complete(self):
        self.status = 'Completed'


def load_trips(path=DATA_FILE):
    """Validate the entire file before permitting changes to its contents."""
    if not path.exists():
        return []
    with path.open(encoding='utf-8') as source:
        records = json.load(source)
    if not isinstance(records, list):
        raise ValueError('The data file must contain a list.')
    trips = [Trip(**record) for record in records]
    if len({trip.trip_id for trip in trips}) != len(trips):
        raise ValueError('Duplicate trip IDs found.')
    return trips


def save_trips(trips, path=DATA_FILE):
    """Replace the original only after a complete temporary write."""
    temporary = path.with_suffix('.tmp')
    try:
        with temporary.open('w', encoding='utf-8') as target:
            json.dump([asdict(trip) for trip in trips], target, indent=2)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print('Please enter a value.')


def get_number(prompt):
    while True:
        try:
            number = Decimal(input(prompt).strip())
            if not number.is_finite() or number < 0:
                raise ValueError
            return str(number.quantize(Decimal('0.01')))
        except (InvalidOperation, ValueError):
            print('Enter a nonnegative number, such as 12.50.')


def add_trip(trips):
    while True:
        date = input('Trip date (YYYY-MM-DD): ').strip()
        try:
            datetime.strptime(date, '%Y-%m-%d')
            break
        except ValueError:
            print('Enter a valid calendar date in YYYY-MM-DD format.')
    trip = Trip(max((t.trip_id for t in trips), default=0) + 1,
                date, get_text('Passenger name or alias: '),
                get_text('Destination: '), get_number('Miles: '),
                get_number('Fare ($): '))
    trips.append(trip)
    print(f'Trip {trip.trip_id} added.')


def display_trips(trips):
    if not trips:
        print('No matching trips found.')
        return
    for trip in sorted(trips, key=lambda t: (t.trip_date, t.trip_id)):
        print(f'#{trip.trip_id} | {trip.trip_date} | {trip.passenger} | '
              f'{trip.destination} | {trip.miles} miles | '
              f'${Decimal(trip.fare):.2f} | {trip.status}')


def search_trips(trips):
    query = get_text('Search passenger or destination: ').casefold()
    display_trips([t for t in trips if query in t.passenger.casefold()
                   or query in t.destination.casefold()])


def update_status(trips):
    display_trips(trips)
    if not trips:
        return
    try:
        trip_id = int(input('Trip ID to update: '))
    except ValueError:
        print('The trip ID must be a whole number.')
        return
    trip = next((t for t in trips if t.trip_id == trip_id), None)
    if trip is None:
        print('That trip ID was not found.')
        return
    choice = input('1 Scheduled, 2 Completed, 3 Cancelled: ').strip()
    if choice not in ('1', '2', '3'):
        print('Invalid status choice.')
        return
    if choice == '2':
        trip.complete()
    else:
        trip.status = STATUSES[int(choice) - 1]
    print('Status updated.')


def show_summary(trips):
    completed = [t for t in trips if t.status == 'Completed']
    revenue = sum((Decimal(t.fare) for t in completed), Decimal('0'))
    miles = sum((Decimal(t.miles) for t in completed), Decimal('0'))
    print(f'Total trips: {len(trips)}')
    for status in STATUSES:
        print(f'{status}: {sum(t.status == status for t in trips)}')
    print(f'Completed miles: {miles:.2f}\nCompleted revenue: ${revenue:.2f}')
    if miles:
        print(f'Revenue per completed mile: ${revenue / miles:.2f}')
    else:
        print('Revenue per mile: N/A (no completed miles).')


def export_csv(trips, path=None):
    path = path or DATA_FILE.with_name('trip_report.csv')
    with path.open('w', newline='', encoding='utf-8') as target:
        writer = csv.DictWriter(target, fieldnames=list(Trip.__dataclass_fields__))
        writer.writeheader()
        for trip in trips:
            record = asdict(trip)
            # Keep user-entered text from becoming spreadsheet formulas.
            for field in ('passenger', 'destination'):
                if record[field].lstrip().startswith(('=', '+', '-', '@')):
                    record[field] = "'" + record[field]
            writer.writerow(record)
    print(f'CSV report saved to {path.name}.')


def main():
    print('Transportation Trip Tracker')
    print('Use fictional passengers for classroom demonstrations.')
    try:
        trips = load_trips()
    except (OSError, ValueError, TypeError, InvalidOperation) as error:
        print(f'Cannot load trips: {error}')
        print('Existing data was not changed. Repair the file or restore a backup.')
        return
    while True:
        print('\n1 Add trip\n2 View trips\n3 Search trips\n4 Update status'
              '\n5 Summary\n6 Export CSV\n7 Save and exit')
        try:
            choice = input('Choose 1-7: ').strip()
            if choice == '1':
                add_trip(trips)
            elif choice == '2':
                display_trips(trips)
            elif choice == '3':
                search_trips(trips)
            elif choice == '4':
                update_status(trips)
            elif choice == '5':
                show_summary(trips)
            elif choice == '6':
                export_csv(trips)
            elif choice == '7':
                save_trips(trips)
                print('Trips saved. Goodbye!')
                return
            else:
                print('Choose a number from 1 through 7.')
                continue
            if choice in ('1', '4'):
                save_trips(trips)
                print('Trips saved.')
        except OSError as error:
            print(f'File operation failed: {error}')
            print('Changes remain in memory. Try Save and exit again.')
        except (EOFError, KeyboardInterrupt):
            print('\nInput stopped. Attempting to save trips.')
            try:
                save_trips(trips)
            except OSError as error:
                print(f'Could not save: {error}')
            return


if __name__ == '__main__':
    main()

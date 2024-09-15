import random
import json
from datetime import datetime, timedelta

def random_date(start_date, end_date):
    """Generate a random date between start_date and end_date"""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def random_time():
    """Generate a random time"""
    return f"{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}"

def generate_entries(fpga_id, num_entries, start_index):
    """Generate a dictionary of entries for a given FPGA ID, starting from start_index"""
    entries = {}
    start_date = datetime(2020, 5, 1)
    end_date = datetime.now()
    
    for i in range(num_entries):
        entry_date = random_date(start_date, end_date).strftime("%d-%m-%Y")
        entry_time = random_time()
        elevation = random.randint(-300, 300)
        direction = random.randint(0, 360)
        
        entry = {
            "fpga_id": fpga_id,
            "elevation": elevation,
            "direction": direction,
            "date": entry_date,
            "time": entry_time
        }
        # Create a unique key for each entry
        entry_key = str(start_index + i)
        entries[entry_key] = entry
    
    return entries

def main():
    all_entries = {}
    start_index = 1
    
    num_fpga = int(input("Enter the number of FPGA IDs: "))
    starting_id = 100001  # Starting FPGA ID
    
    for _ in range(num_fpga):
        fpga_id = str(starting_id)
        num_entries = int(input(f"Enter number of entries for FPGA ID {fpga_id}: "))
        entries = generate_entries(fpga_id, num_entries, start_index)
        all_entries.update(entries)
        start_index += num_entries
        starting_id = int(starting_id) + 1  # Increment FPGA ID for next iteration
    
    # Write the data to a JSON file
    with open('test_gunshots.json', 'w') as json_file:
        json.dump(all_entries, json_file, indent=4)
    
    print("\nData has been written to test_gunshots.json")

if __name__ == "__main__":
    main()

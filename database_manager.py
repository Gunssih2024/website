import os
import json
from collections import defaultdict
from typing import Dict, List
from datetime import datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta

#             start_date = today - timedelta(days=6)  # 6 days before today to include today
#             start_date = today - timedelta(days=29)  # 29 days before today to include today
# start_date = today.replace(day=1) - timedelta(days=1)  # End of the previous month

            # for _ in range(4):  # Move back 5 months
            #     start_date = start_date.replace(day=1) - timedelta(days=1)

#             start_of_year = datetime(today.year, 1, 1)
#             start_date = datetime(today.year - 5, 1, 1)




def convert_gunshot_data(gunshot_list: Dict, fpgas_list: Dict) -> Dict:
    # Convert string dates to datetime objects
    def parse_date(date_str):
        return datetime.strptime(date_str, "%d-%m-%Y")

    # Helper to compute elevation data over a time range for each FPGA
    def get_elevation_data(filtered_data: List[Dict], time_range: str) -> Dict:
        grouped_data = defaultdict(lambda: {
            "labels": [],
            "elevations": []
        })
        total_elevation = defaultdict(int)
        if not filtered_data:
            return grouped_data, total_elevation
        
        # Group data by the specified time range

        if time_range == "today":

            today = datetime.now().strftime("%d-%m-%Y")  # Format today's date as "DD-MM-YYYY"

            elevation_by_time_out = {}

            for entry in filtered_data:
                # Check if the entry date is today's date
                if entry["date"] == today:
                    # Process the time part of the entry
                    entry_time = datetime.strptime(entry["time"], "%H:%M:%S")
                    hour_label = entry_time.strftime("%I%p").lower()  # Convert to lowercase to match labels
                    
                    if entry["fpga_id"] not in elevation_by_time_out:
                        elevation_by_time_out[entry["fpga_id"]] = {hour_label: (entry["elevation"], 1)} 
                    else:
                        temp_elevation = elevation_by_time_out[entry["fpga_id"]]
                        if hour_label in temp_elevation:
                            temp_temp_elevation, temp_itr = temp_elevation[hour_label]
                            temp_itr += 1
                            temp_temp_elevation += entry["elevation"]
                            elevation_by_time_out[entry["fpga_id"]][hour_label] = (temp_temp_elevation, temp_itr)
                        else:
                            elevation_by_time_out[entry["fpga_id"]][hour_label] = (entry["elevation"], 1)
            # print(elevation_by_time_out)
            # second operation for today
            # labels_time = ["12am", "01am", "02am", "03am", "04am", "05am", "06am", "07am", "08am", "09am", "10am", "11am", "12pm", "01pm", "02pm", "03pm", "04pm", "05pm", "06pm", "07pm", "08pm", "09pm", "10pm", "11pm"]
            result = {
                "labels":["12am", "01am", "02am", "03am", "04am", "05am", "06am", "07am", "08am", "09am", "10am", "11am", "12pm", "01pm", "02pm", "03pm", "04pm", "05pm", "06pm", "07pm", "08pm", "09pm", "10pm", "11pm"]
            }
            for i,y in fpgas_list.items():
                value_list = [0] * len(result["labels"])
                if i in elevation_by_time_out:
                    for j,k in elevation_by_time_out[i].items():
                        value_list[result["labels"].index(j)] = int(k[0]/k[1])
                        # print(j,k)
                else:
                    pass
                result[i] = value_list
                # print(i, value_list)
            # print(return_with_label)


        elif time_range == "7days":
            today = datetime.now()

            start_date = today - timedelta(days=6)  # 6 days before today to include today
            end_date = today

            # Create a dictionary to hold elevations by day for each fpga_id
            elevation_by_fpga_id = {}

            # Define the labels for the days of the week
            day_labels = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

            for entry in filtered_data:
                fpga_id = entry["fpga_id"]
                
                # Initialize the fpga_id entry if it does not exist
                if fpga_id not in elevation_by_fpga_id:
                    elevation_by_fpga_id[fpga_id] = {label: (0, 0) for label in day_labels}
                
                # Parse the date from the entry
                entry_date = datetime.strptime(entry["date"], "%d-%m-%Y")  # Use "%d-%m-%Y" format

                # Check if the date is within the last 7 days
                if start_date <= entry_date <= end_date:
                    # Get the day of the week for the date
                    day_label = entry_date.strftime("%a").lower()[:3]  # First three letters of the day

                    # Map the day abbreviation to the full label
                    day_mapping = {
                        'mon': 'mon',
                        'tue': 'tue',
                        'wed': 'wed',
                        'thu': 'thu',
                        'fri': 'fri',
                        'sat': 'sat',
                        'sun': 'sun'
                    }
                    
                    if day_label in day_mapping:
                        day_label = day_mapping[day_label]
                        
                        # Update the elevation data for the specific fpga_id and day
                        temp_elevation, temp_count = elevation_by_fpga_id[fpga_id][day_label]
                        temp_count += 1
                        temp_elevation += entry["elevation"]
                        elevation_by_fpga_id[fpga_id][day_label] = (temp_elevation, temp_count)

            # print(elevation_by_fpga_id)
            


            
                        
                        
            # second operation for today
            days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

            result = {
                'labels': days_of_week,
            }

            # Find the first day in the first key's data
            first_key = next(iter(elevation_by_fpga_id))
            first_day_index = days_of_week.index(next(day for day in days_of_week if day in elevation_by_fpga_id[first_key]))


            for key,y in fpgas_list.items():
                value_list = [0] * len(days_of_week)
                
                if key in elevation_by_fpga_id.keys():
                    for day, (value, _) in elevation_by_fpga_id[key].items():
                        day_index = days_of_week.index(day)
                        value_list[day_index] = int(value / _) if _ != 0 else value
                else:
                    pass

                # Shift the list to align with the first day's index
                value_list = value_list[first_day_index:] + value_list[:first_day_index]
                result[key] = value_list



            # for key, day_data in elevation_by_fpga_id.items():
            #     # Initialize value list with 0s
            #     value_list = [0] * len(days_of_week)
                
            #     for day, (value, _) in elevation_by_time_out[key].items():
            #         day_index = days_of_week.index(day)
            #         value_list[day_index] = int(value)

            #     # Shift the list to align with the first day's index
            #     value_list = value_list[first_day_index:] + value_list[:first_day_index]
            #     result[key] = value_list

            # print(result)

            # return_with_label = {
            #     "labels":["Mon", "01am", "02am", "03am", "04am", "05am", "06am", "07am", "08am", "09am", "10am", "11am", "12pm", "01pm", "02pm", "03pm", "04pm", "05pm", "06pm", "07pm", "08pm", "09pm", "10pm", "11pm"]
            # }
            
            # for i,y in fpgas_list.items():
            #     value_list = [0] * len(return_with_label["labels"])
            #     if i in elevation_by_time_out:
            #         for j,k in elevation_by_time_out[i].items():
            #             value_list[return_with_label["labels"].index(j)] = int(k[0]/k[1])
            #             # print(j,k)
            #     else:
            #         pass
            #     return_with_label[i] = value_list
        
        elif time_range == "30days":
            today = datetime.now()

            # Calculate the date range for the last 30 days
            start_date = today - timedelta(days=29)  # 29 days before today to include today

            end_date = today

            # Create a dictionary to hold elevations by date for each fpga_id
            elevation_by_fpga_id = {}

            # Initialize the dictionary with the date labels in 'DD-MM-YYYY' format
            date_labels = {
                (start_date + timedelta(days=i)).strftime("%d-%m-%Y"): (0, 0)
                for i in range(30)
            }

            # Process the filtered_data to update the elevations
            for entry in filtered_data:
                fpga_id = entry["fpga_id"]
                
                # Initialize the fpga_id entry if it does not exist
                if fpga_id not in elevation_by_fpga_id:
                    elevation_by_fpga_id[fpga_id] = date_labels.copy()  # Copy the template for each fpga_id

                # Parse the date from the entry
                entry_date = datetime.strptime(entry["date"], "%d-%m-%Y")  # Use "%d-%m-%Y" format

                # Check if the date is within the last 30 days
                if start_date <= entry_date <= end_date:
                    # Format the date to match the dictionary keys
                    formatted_date = entry_date.strftime("%d-%m-%Y")
                    
                    # Update the elevation data for the specific fpga_id and date
                    if formatted_date in elevation_by_fpga_id[fpga_id]:
                        temp_elevation, temp_count = elevation_by_fpga_id[fpga_id][formatted_date]
                        temp_count += 1
                        temp_elevation += entry["elevation"]
                        elevation_by_fpga_id[fpga_id][formatted_date] = (temp_elevation, temp_count)

            # Prepare the result dictionary for output
            result = {
                'labels': [date.strftime("%d-%m-%Y") for date in (start_date + timedelta(days=i) for i in range(30))],
            }


            for key,y in fpgas_list.items():
                value_list = [0] * len(result['labels'])
                
                if key in elevation_by_fpga_id.keys():
                    for date_str, (elevation, _) in elevation_by_fpga_id[key].items():
                        day_index = result['labels'].index(date_str)
                        value_list[day_index] = int(elevation / _) if _ != 0 else elevation
                else:
                    pass

                # Shift the list to align with the first day's index
                result[key] = value_list

            # Convert the elevation data into a format where each key has a list of values for each date
            # for key in elevation_by_fpga_id:
            #     value_list = [0] * len(result['labels'])
                
            #     for date_str, (elevation, _) in elevation_by_fpga_id[key].items():
            #         day_index = result['labels'].index(date_str)
            #         value_list[day_index] = int(elevation)
                
            #     result[key] = value_list

            # print(result)            # print(elevation_by_fpga_id)        
        
        elif time_range == "6months":
            today = datetime.now()

            # Calculate the start of the month 5 months ago
            start_date = today.replace(day=1) - timedelta(days=1)  # End of the previous month

            for _ in range(4):  # Move back 5 months
                start_date = start_date.replace(day=1) - timedelta(days=1)
            start_date = start_date.replace(day=1)  # First day of the month 5 months ago

            # Calculate the end date as the first day of the next month after today
            
            end_date = today   # First day of next month
            # print(start_date)
            # Create a dictionary to hold elevations by month for each fpga_id
            elevation_by_fpga_id = {}

            # Generate month labels from start_date to end_date
            current_date = start_date
            month_labels = {}

            while current_date < end_date:
                month_key = current_date.strftime("%b-%Y").lower()  # Include the year to differentiate months across years
                if month_key not in month_labels:
                    month_labels[month_key] = (0, 0)
                next_month = current_date.month % 12 + 1
                next_year = current_date.year + (current_date.month // 12)
                current_date = current_date.replace(month=next_month, year=next_year, day=1)  # Move to the next month
            # print(month_labels)
            # Process the filtered_data to update the elevations
            for entry in filtered_data:
                fpga_id = entry["fpga_id"]
                
                # Initialize the fpga_id entry if it does not exist
                if fpga_id not in elevation_by_fpga_id:
                    elevation_by_fpga_id[fpga_id] = month_labels.copy()  # Copy the template for each fpga_id

                # Parse the date from the entry
                entry_date = datetime.strptime(entry["date"], "%d-%m-%Y")  # Use "%d-%m-%Y" format

                # Check if the date is within the last 6 months
                if start_date <= entry_date < end_date:
                    # Format the month to match the dictionary keys
                    month_key = entry_date.strftime("%b-%Y").lower()  # Include the year to differentiate months across years

                    # Update the elevation data for the specific fpga_id and month
                    if month_key in elevation_by_fpga_id[fpga_id]:
                        temp_elevation, temp_count = elevation_by_fpga_id[fpga_id][month_key]
                        temp_count += 1
                        temp_elevation += entry["elevation"]
                        elevation_by_fpga_id[fpga_id][month_key] = (temp_elevation, temp_count)

            # Prepare the result dictionary for output
            # print(month_labels.keys())
            result = {
                'labels': list(month_labels.keys()),  # Ensure the labels are sorted by month
            }

            for key,y in fpgas_list.items():
                value_list = [0] * len(result['labels'])
                
                if key in elevation_by_fpga_id.keys():
                    for month_key, (elevation, _) in elevation_by_fpga_id[key].items():
                        if month_key in result['labels']:
                            month_index = result['labels'].index(month_key)
                            value_list[month_index] = int(elevation / _) if _ != 0 else elevation
                else:
                    pass

                # Shift the list to align with the first day's index
                result[key] = value_list

            # Convert the elevation data into a format where each key has a list of values for each month
            # for key in elevation_by_fpga_id:
            #     value_list = [0] * len(result['labels'])
                
            #     for month_key, (elevation, _) in elevation_by_fpga_id[key].items():
            #         if month_key in result['labels']:
            #             month_index = result['labels'].index(month_key)
            #             value_list[month_index] = int(elevation)
                
            #     result[key] = value_list

            # print(result)        



        elif time_range == "year":
            today = datetime.now()

            # Determine the start of the current year
            start_of_year = datetime(today.year, 1, 1)

            # Use the current date as the end date
            end_date = today

            # Create a dictionary to hold elevations by month for each fpga_id
            elevation_by_fpga_id = {}

            # Generate month labels from the start of the year to the current date
            month_labels = {}
            current_date = start_of_year

            while current_date <= end_date:
                month_key = current_date.strftime("%b").lower()
                if month_key not in month_labels:
                    month_labels[month_key] = (0, 0)
                current_date = (current_date + timedelta(days=31)).replace(day=1)  # Move to the next month

            # Process the filtered_data to update the elevations
            for entry in filtered_data:
                fpga_id = entry["fpga_id"]
                
                # Initialize the fpga_id entry if it does not exist
                if fpga_id not in elevation_by_fpga_id:
                    elevation_by_fpga_id[fpga_id] = month_labels.copy()  # Copy the template for each fpga_id

                # Parse the date from the entry
                entry_date = datetime.strptime(entry["date"], "%d-%m-%Y")  # Use "%d-%m-%Y" format

                # Check if the date is within the current year
                if start_of_year <= entry_date <= end_date:
                    # Format the month to match the dictionary keys
                    month_label = entry_date.strftime("%b").lower()  # First three letters of the month

                    # Update the elevation data for the specific fpga_id and month
                    if month_label in elevation_by_fpga_id[fpga_id]:
                        temp_elevation, temp_count = elevation_by_fpga_id[fpga_id][month_label]
                        temp_count += 1
                        temp_elevation += entry["elevation"]
                        elevation_by_fpga_id[fpga_id][month_label] = (temp_elevation, temp_count)

            result = {
                'labels': list(month_labels.keys()),  # Ensure the labels are sorted by month
            }

            for key,y in fpgas_list.items():
                value_list = [0] * len(result['labels'])
                
                if key in elevation_by_fpga_id.keys():
                    for month_key, (elevation, _) in elevation_by_fpga_id[key].items():
                        if month_key in result['labels']:
                            month_index = result['labels'].index(month_key)
                            value_list[month_index] = int(elevation / _) if _ != 0 else elevation
                else:
                    pass

                # Shift the list to align with the first day's index
                result[key] = value_list

            # print(result)


        elif time_range == "5year":
            today = datetime.now()

            # Calculate the start of the period 5 years ago
            start_date = datetime(today.year - 5, 1, 1)
            end_date = today

            # Function to get the quarter label
            def get_quarter_label(date):
                year = date.year
                month = date.month
                quarter = (month - 1) // 3 + 1
                return f"{year} Q{quarter}"

            # Initialize the dictionary to hold elevations by quarter for each fpga_id
            elevation_by_fpga_id = {}

            # Generate quarter labels from the start date to the end date
            quarter_labels = {}
            current_date = start_date
            
            while current_date <= end_date:
                quarter_label = get_quarter_label(current_date)
                if quarter_label not in quarter_labels:
                    quarter_labels[quarter_label] = (0, 0)
                # Move to the next quarter
                current_date = (current_date + timedelta(days=91)).replace(day=1)  # Move approximately 3 months ahead
            # print(quarter_labels)
            # Process the filtered_data to update the elevations
            for entry in filtered_data:
                fpga_id = entry["fpga_id"]
                
                # Initialize the fpga_id entry if it does not exist
                if fpga_id not in elevation_by_fpga_id:
                    elevation_by_fpga_id[fpga_id] = quarter_labels.copy()  # Copy the template for each fpga_id

                # Parse the date from the entry
                entry_date = datetime.strptime(entry["date"], "%d-%m-%Y")  # Use "%d-%m-%Y" format

                # Check if the date is within the last 5 years
                if start_date <= entry_date <= end_date:
                    # Format the quarter to match the dictionary keys
                    quarter_label = get_quarter_label(entry_date)

                    # Update the elevation data for the specific fpga_id and quarter
                    if quarter_label in elevation_by_fpga_id[fpga_id]:
                        temp_elevation, temp_count = elevation_by_fpga_id[fpga_id][quarter_label]
                        temp_count += 1
                        temp_elevation += entry["elevation"]
                        elevation_by_fpga_id[fpga_id][quarter_label] = (temp_elevation, temp_count)


            result = {
                'labels': list(quarter_labels.keys()),  # Ensure the labels are sorted by month
            }

            for key,y in fpgas_list.items():
                value_list = [0] * len(result['labels'])
                
                if key in elevation_by_fpga_id.keys():
                    for quarter_key, (elevation, i) in elevation_by_fpga_id[key].items():
                        if quarter_key in result['labels']:
                            quarter_index = result['labels'].index(quarter_key)
                            value_list[quarter_index] = int(elevation / i) if i != 0 else elevation
                else:
                    pass
                        
                # Shift the list to align with the first day's index
                result[key] = value_list
            # print(elevation_by_fpga_id,"hehe\n",result)

        return result
    
    # Convert gunshot data to list
    filtered_gunshot_data = [
        {
            "fpga_id": item["fpga_id"],
            "elevation": item["elevation"],
            "date": item["date"],
            "time": item["time"]
        }
        for item in gunshot_list.values()
    ]

    # Calculate data for each period
    today_data = get_elevation_data(filtered_gunshot_data, "today")
    seven_days_data = get_elevation_data(filtered_gunshot_data, "7days")
    thirty_days_data = get_elevation_data(filtered_gunshot_data, "30days")
    six_months_data = get_elevation_data(filtered_gunshot_data, "6months")
    year_data = get_elevation_data(filtered_gunshot_data, "year")
    five_year_data = get_elevation_data(filtered_gunshot_data, "5year")
    
    # print(today_data, seven_days_data,thirty_days_data,six_months_data,year_data,five_year_data)
    
    # updated_data = {}
    # updated_data = {f"elevations_{fpga_id}": data["elevations"] for fpga_id, data in today_data.items()}
    # updated_data["labels"] = ["12am", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm"]
    return {
        "dates": {
            "today": {
                "data":today_data
                # "data": {f"elevations_{fpga_id}": data["elevations"] for fpga_id, data in today_data.items()}
            },
            "7days": {
                "data": seven_days_data
            },
            "30days": {
                "data": thirty_days_data
            },
            "6months": {
                "data": six_months_data
            },
            "year": {
                "data": year_data
            },
            "5year": {
                "data": five_year_data
            }
        }
    }


def calculate_gunshot_data(gunshot_list: Dict, fpgas_list: Dict):
    # Initialize counters
    today_counter = {fpga_id: 0 for fpga_id in fpgas_list.keys()}
    seven_days_counter = {fpga_id: 0 for fpga_id in fpgas_list.keys()}
    thirty_days_counter = {fpga_id: 0 for fpga_id in fpgas_list.keys()}
    six_months_counter = {fpga_id: 0 for fpga_id in fpgas_list.keys()}
    this_year_counter = {fpga_id: 0 for fpga_id in fpgas_list.keys()}
    five_years_counter = {fpga_id: 0 for fpga_id in fpgas_list.keys()}
    
    # Get today's date
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=6)
    thirty_days_ago = today - timedelta(days=29)
    six_months_ago = today.replace(day=1) - timedelta(days=1)  # End of the previous month
    for _ in range(4):  # Move back 5 months
        six_months_ago = six_months_ago.replace(day=1) - timedelta(days=1)
    this_year = datetime(today.year, 1, 1).date()
    five_years_ago = datetime(today.year - 5, 1, 1).date()
    
    def parse_date(date_str):
        # Convert date string to datetime object
        return datetime.strptime(date_str, "%d-%m-%Y").date()
    
    for entry in gunshot_list.values():
        fpga_id = entry["fpga_id"]
        entry_date = parse_date(entry["date"])
        
        if entry_date == today:
            today_counter[fpga_id] += 1
        
        if seven_days_ago <= entry_date <= today:
            seven_days_counter[fpga_id] += 1
        
        if thirty_days_ago <= entry_date <= today:
            thirty_days_counter[fpga_id] += 1
        
        if six_months_ago <= entry_date <= today:
            six_months_counter[fpga_id] += 1
        
        if this_year <= entry_date <= today:
            this_year_counter[fpga_id] += 1
        
        if five_years_ago <= entry_date <= today:
            five_years_counter[fpga_id] += 1
    
    today_transformed  = {"labels": list(today_counter.keys()), "values": list(today_counter.values())}
    seven_days_transformed = {"labels": list(seven_days_counter.keys()), "values": list(seven_days_counter.values())}
    thirty_days_transformed = {"labels": list(thirty_days_counter.keys()), "values": list(thirty_days_counter.values())}
    six_months_transformed = {"labels": list(six_months_counter.keys()), "values": list(six_months_counter.values())}
    this_year_transformed = {"labels": list(this_year_counter.keys()), "values": list(this_year_counter.values())}
    five_years_transformed = {"labels": list(five_years_counter.keys()), "values": list(five_years_counter.values())}

    return {
    "dates": {
        "today": {
            "data": today_transformed
        },
        "7days": {
            "data": seven_days_transformed
        },
        "30days": {
            "data": thirty_days_transformed
        },
        "6months": {
            "data": six_months_transformed
        },
        "year": {
            "data": this_year_transformed
        },
        "5year": {
            "data": five_years_transformed
        }
    }
}


class DbManager:
    def __init__(self, fpgas_file, gunshot_file) -> None:
        self.fpgas_file = fpgas_file
        self.gunshot_file = gunshot_file

        if not os.path.exists(fpgas_file):
            file = open(fpgas_file, "w")
            file.write("{}")
            file.close()

        if not os.path.exists(gunshot_file):
            file = open(gunshot_file, "w")
            file.write("{}")
            file.close()

    def add_fpga(self, name: str) -> int:
        try:
            fpgas_list = self.get_fpgas()

            if fpgas_list:
                max_id = max(int(id) for id in fpgas_list.keys())
                new_id = max_id + 1
            else:
                new_id = 100001
            new_id_str = str(new_id)

            fpgas_list[new_id_str] = {"name": name}

            with open(self.fpgas_file, "w") as fpgas:
                json.dump(fpgas_list, fpgas)

            return new_id
        except:
            return "error"


    def add_gunshot(self, fpga_id:str, elevation:int, direction:int) -> int:
        if self.get_fpgas(fpga_id) == {}:
            return 1

        gunshots_list = self.get_gunshot()

        gunshot_id = str(len(gunshots_list) + 1)
        gunshot_info = {"fpga_id":fpga_id,
                        "elevation":elevation,
                        "direction":direction,
                        "date":datetime.today().strftime('%d-%m-%Y'),
                        "time":datetime.today().strftime('%H:%M:%S')
                    }

        gunshots_list[gunshot_id] = gunshot_info

        with open(self.gunshot_file, "w") as gunshots:
            json.dump(gunshots_list, gunshots)
        
        return 0

    def get_fpgas(self, id:str="") -> dict:
        with open(self.fpgas_file, "r") as fpgas:
            fpgas_list = json.load(fpgas)

        if not id:
            return fpgas_list
        else:
            return fpgas_list.get(id, {})

    def get_gunshot(self) -> dict:
        with open(self.gunshot_file, "r") as gunshots:
            gunshot_list = json.load(gunshots)

        return gunshot_list
    
    def get_gunshot_specific_elevation(self) -> dict:
        # this returns elevation data of today, 7 days, this month, six months , year, 5 years
        with open(self.gunshot_file, "r") as gunshots:
            gunshot_list = json.load(gunshots)
        with open(self.fpgas_file, "r") as fpgas:
            fpgas_list = json.load(fpgas)

        return convert_gunshot_data(gunshot_list, fpgas_list)
    
    def gunshot_counter(self) -> dict:
        # this returns gunshots data of today, 7 days, this month, six months , year, 5 years

        with open(self.gunshot_file, "r") as gunshots:
            gunshot_list = json.load(gunshots)
        with open(self.fpgas_file, "r") as fpgas:
            fpgas_list = json.load(fpgas)

        return calculate_gunshot_data(gunshot_list, fpgas_list)

    # operations done on data
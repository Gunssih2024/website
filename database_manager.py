import os
import json
from collections import defaultdict
from typing import Dict, List
from datetime import datetime, timedelta
import calendar

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
        # labels_time = ["12am", "01am", "02am", "03am", "04am", "05am", "06am", "07am", "08am", "09am", "10am", "11am", "12pm", "01pm", "02pm", "03pm", "04pm", "05pm", "06pm", "07pm", "08pm", "09pm", "10pm", "11pm"]
        if not filtered_data:
            return grouped_data, total_elevation
        
        # Group data by the specified time range
        if time_range == "today":
            # elevation_by_time = {label: 0 for label in labels_time}
            elevation_by_time_out = {}
            # print(elevation_by_time)
            # print("suadhfansdfoj")
            # Process the filtered_data to update the elevations
            for entry in filtered_data:
                # print(entry)
                entry_time = datetime.strptime(entry["time"], "%H:%M:%S")
                hour_label = entry_time.strftime("%I%p").lower()  # Convert to lowercase to match labels
                # Check if the hour_label is in the labels dictionary
                # print(elevation_by_time)
                # print(hour_label, "bombastic")
                # if hour_label in elevation_by_time:
                if entry["fpga_id"] not in elevation_by_time_out:
                    elevation_by_time_out[entry["fpga_id"]] = {hour_label:(entry["elevation"], 1)} 
                else:
                    temp_elevation = elevation_by_time_out[entry["fpga_id"]]
                    if hour_label in temp_elevation:
                        temp_temp_elevation, temp_itr = temp_elevation[hour_label] 
                        temp_itr +=1
                        temp_temp_elevation += entry["elevation"]
                        elevation_by_time_out[entry["fpga_id"]][hour_label] = (temp_temp_elevation, temp_itr)
                    else:
                        elevation_by_time_out[entry["fpga_id"]][hour_label] = (entry["elevation"], 1)

                        # print(temp_elevation, "temp", hour_label)
                        # temp_elevation += entry["elevation"]
                        # temp_itr+=1
                        # elevation_by_time_out[entry["fpga_id"]] = (temp_elevation, temp_itr)

                    # elevation_by_time[hour_label] += entry["elevation"]
                    # print("bombastic", entry["elevation"], hour_label)
            # print(elevation_by_time_out)



        elif time_range == "7days":
            today = datetime.now()

            # Calculate the date range for the last 7 days
            start_date = today - timedelta(days=6)  # 6 days before today to include today
            end_date = today

            # Create a dictionary to hold elevations by day for each fpga_id
            elevation_by_fpga_id = {}

            # Define the labels for the days of the week
            day_labels = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

            # Initialize the dictionary with the day labels
            # Note: This initialization will be done per fpga_id inside the loop
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




    
        # elif time_range == "7days":
        #     end_date = datetime.now().date()
        #     start_date = end_date - timedelta(days=6)
        #     for entry in filtered_data:
        #         entry_date = parse_date(entry["date"]).date()
        #         if start_date <= entry_date <= end_date:
        #             day_label = entry_date.strftime("%a")
        #             fpga_id = entry["fpga_id"]
        #             if day_label not in grouped_data[fpga_id]["labels"]:
        #                 grouped_data[fpga_id]["labels"].append(day_label)
        #             index = grouped_data[fpga_id]["labels"].index(day_label)
        #             if len(grouped_data[fpga_id]["elevations"]) <= index:
        #                 grouped_data[fpga_id]["elevations"].extend([0] * (index + 1 - len(grouped_data[fpga_id]["elevations"])))
        #             grouped_data[fpga_id]["elevations"][index] += entry["elevation"]
        #             total_elevation[fpga_id] += entry["elevation"]
        
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

            # print(elevation_by_fpga_id)

        # elif time_range == "30days":
        #     end_date = datetime.now().date()
        #     start_date = end_date - timedelta(days=29)
        #     for entry in filtered_data:
        #         entry_date = parse_date(entry["date"]).date()
        #         if start_date <= entry_date <= end_date:
        #             day_label = entry_date.strftime("%d")
        #             fpga_id = entry["fpga_id"]
        #             if day_label not in grouped_data[fpga_id]["labels"]:
        #                 grouped_data[fpga_id]["labels"].append(day_label)
        #             index = grouped_data[fpga_id]["labels"].index(day_label)
        #             if len(grouped_data[fpga_id]["elevations"]) <= index:
        #                 grouped_data[fpga_id]["elevations"].extend([0] * (index + 1 - len(grouped_data[fpga_id]["elevations"])))
        #             grouped_data[fpga_id]["elevations"][index] += entry["elevation"]
        #             total_elevation[fpga_id] += entry["elevation"]
        
        elif time_range == "6months":
            today = datetime.now()

            # Calculate the start of the month 6 months ago
            six_months_ago = today - timedelta(days=180)  # Approximate 6 months

            # Calculate the start and end dates
            start_date = six_months_ago.replace(day=1)  # First day of the month 6 months ago
            end_date = today.replace(day=1) + timedelta(days=31)  # First day of next month, to include current month fully

            # Create a dictionary to hold elevations by month for each fpga_id
            elevation_by_fpga_id = {}

            # Generate month labels from start_date to end_date
            current_date = start_date
            month_labels = {}

            while current_date < end_date:
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

                # Check if the date is within the last 6 months
                if start_date <= entry_date < end_date:
                    # Format the month to match the dictionary keys
                    month_label = entry_date.strftime("%b").lower()  # First three letters of the month

                    # Update the elevation data for the specific fpga_id and month
                    if month_label in elevation_by_fpga_id[fpga_id]:
                        temp_elevation, temp_count = elevation_by_fpga_id[fpga_id][month_label]
                        temp_count += 1
                        temp_elevation += entry["elevation"]
                        elevation_by_fpga_id[fpga_id][month_label] = (temp_elevation, temp_count)

            # print(elevation_by_fpga_id)

        # elif time_range == "6months":
        #     end_date = datetime.now().date()
        #     start_date = end_date - timedelta(days=180)
        #     for entry in filtered_data:
        #         entry_date = parse_date(entry["date"]).date()
        #         if start_date <= entry_date <= end_date:
        #             month_label = entry_date.strftime("%b")
        #             fpga_id = entry["fpga_id"]
        #             if month_label not in grouped_data[fpga_id]["labels"]:
        #                 grouped_data[fpga_id]["labels"].append(month_label)
        #             index = grouped_data[fpga_id]["labels"].index(month_label)
        #             if len(grouped_data[fpga_id]["elevations"]) <= index:
        #                 grouped_data[fpga_id]["elevations"].extend([0] * (index + 1 - len(grouped_data[fpga_id]["elevations"])))
        #             grouped_data[fpga_id]["elevations"][index] += entry["elevation"]
        #             total_elevation[fpga_id] += entry["elevation"]
        
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

            # print(elevation_by_fpga_id)

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

            # print(elevation_by_fpga_id)


        # elif time_range == "year":
        #     end_date = datetime.now().date()
        #     start_date = end_date - timedelta(days=365)
        #     for entry in filtered_data:
        #         entry_date = parse_date(entry["date"]).date()
        #         if start_date <= entry_date <= end_date:
        #             month_label = entry_date.strftime("%b")
        #             fpga_id = entry["fpga_id"]
        #             if month_label not in grouped_data[fpga_id]["labels"]:
        #                 grouped_data[fpga_id]["labels"].append(month_label)
        #             index = grouped_data[fpga_id]["labels"].index(month_label)
        #             if len(grouped_data[fpga_id]["elevations"]) <= index:
        #                 grouped_data[fpga_id]["elevations"].extend([0] * (index + 1 - len(grouped_data[fpga_id]["elevations"])))
        #             grouped_data[fpga_id]["elevations"][index] += entry["elevation"]
        #             total_elevation[fpga_id] += entry["elevation"]
        
        return grouped_data, total_elevation
    
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
    today_data, today_total = get_elevation_data(filtered_gunshot_data, "today")
    seven_days_data, seven_days_total = get_elevation_data(filtered_gunshot_data, "7days")
    thirty_days_data, thirty_days_total = get_elevation_data(filtered_gunshot_data, "30days")
    six_months_data, six_months_total = get_elevation_data(filtered_gunshot_data, "6months")
    year_data, year_total = get_elevation_data(filtered_gunshot_data, "year")
    five_year_data, five_year_total = get_elevation_data(filtered_gunshot_data, "5year")

    # Calculate 'upDown' values
    # def calculate_updown(current_total, previous_total):
    #     if previous_total == 0:
    #         return 0
    #     return round(((current_total - previous_total) / previous_total) * 100, 1)
    
    def previous_total(time_range: str):
        if time_range == "today":
            return today_total  # There is no previous total for today
        elif time_range == "7days":
            return seven_days_total  # Use this as the base for previous periods
        elif time_range == "30days":
            return thirty_days_total
        elif time_range == "6months":
            return six_months_total
        elif time_range == "year":
            return year_total
        elif time_range == "5year":
            return five_year_total
        return 0
    
    updated_data = {f"elevations_{fpga_id}": data["elevations"] for fpga_id, data in today_data.items()}
    updated_data["labels"] = ["12am", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm"]
    return {
        "dates": {
            "today": {
                # "total": sum(today_data[fpga_id]["elevations"][-1] for fpga_id in today_data),
                # "upDown": calculate_updown(
                #     sum(today_data[fpga_id]["elevations"][-1] for fpga_id in today_data),
                #     previous_total("7days")
                # ),
                "data":updated_data
                # "data": {f"elevations_{fpga_id}": data["elevations"] for fpga_id, data in today_data.items()}
            },
            "7days": {
                "total": sum(seven_days_data[fpga_id]["elevations"][-1] for fpga_id in seven_days_data),
                # "upDown": calculate_updown(
                #     sum(seven_days_data[fpga_id]["elevations"][-1] for fpga_id in seven_days_data),
                #     previous_total("30days")
                # ),
                "data": {f"elevations_{fpga_id}": data["elevations"] for fpga_id, data in seven_days_data.items()}
            },
            "30days": {
                "total": sum(thirty_days_data[fpga_id]["elevations"][-1] for fpga_id in thirty_days_data),
                # "upDown": calculate_updown(
                #     sum(thirty_days_data[fpga_id]["elevations"][-1] for fpga_id in thirty_days_data),
                #     previous_total("6months")
                # ),
                "data": {f"elevations_{fpga_id}": data["elevations"] for fpga_id, data in thirty_days_data.items()}
            },
            "6months": {
                "total": sum(six_months_data[fpga_id]["elevations"][-1] for fpga_id in six_months_data),
                # "upDown": calculate_updown(
                #     sum(six_months_data[fpga_id]["elevations"][-1] for fpga_id in six_months_data),
                #     previous_total("year")
                # ),
                "data": {f"elevations_{fpga_id}": data["elevations"] for fpga_id, data in six_months_data.items()}
            },
            "year": {
                "total": sum(year_data[fpga_id]["elevations"][-1] for fpga_id in year_data),
                # "upDown": 0,  # There is no upDown value for the year in this context
                "data": {f"elevations_{fpga_id}": data["elevations"] for fpga_id, data in year_data.items()}
            },
            "5year": {
                "total": sum(year_data[fpga_id]["elevations"][-1] for fpga_id in five_year_data),
                # "upDown": 0,  # There is no upDown value for the year in this context
                "data": {f"elevations_{fpga_id}": data["elevations"] for fpga_id, data in five_year_data.items()}
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
    
    def get_gunshot_specific(self) -> dict:
        # this returns data of today, 7 days, this month, six months , year, all time
        with open(self.gunshot_file, "r") as gunshots:
            gunshot_list = json.load(gunshots)
        with open(self.fpgas_file, "r") as fpgas:
            fpgas_list = json.load(fpgas)

        return convert_gunshot_data(gunshot_list, fpgas_list)

    # operations done on data


from datetime import timedelta, timezone
import datetime
import json
from accounts.models import Staff_Day_of_Visit


def generate_form_errors(args,formset=False):
    i = 1
    message = ""
    if not formset:
        for field in args:	
            if field.errors:
                message += "\n"
                message += field.label + " : "
                message += str(field.errors)

        for err in args.non_field_errors():
            message += str(err)
    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message += "\n"
                    message += field.label + " : "
                    message += str(field.errors)
            for err in form.non_field_errors():
                message += str(err)

    message = message.replace("<li>", "")
    message = message.replace("</li>", "")
    message = message.replace('<ul class="errorlist">', "")
    message = message.replace("</ul>", "")
    return message


def generate_serializer_errors(args):
    message = ""
    print (args)
    for key, values in args.items():
        error_message = ""
        for value in values:
            error_message += value + ","
        error_message = error_message[:-1]

        message += "%s : %s | " %(key,error_message)
    return message[:-3]

def get_custom_id(model):
    custom_id = 1
    # try:
    latest_custom_id =  model.objects.all().order_by("-created_date")[:1]
    if latest_custom_id:
        for auto in latest_custom_id:
            custom_id = int(auto.custom_id) + 1
    # except:
        # pass
    return custom_id

def get_next_visit_date(visit_schedule):
    # Check if visit_schedule is already a dictionary
    if isinstance(visit_schedule, dict):
        visit_schedule_data = visit_schedule
    else:
        # Parse visit_schedule JSON
        visit_schedule_data = json.loads(visit_schedule)
    
    # Get the current date
    current_date = datetime.date.today()
    
    # Define a dictionary to map weekdays to their index
    weekday_indices = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }

    # Define a helper function to convert 'Week1', 'Week2', etc., to a numerical week index
    def get_week_number(week_str):
        if week_str.startswith("Week"):
            try:
                return int(week_str[4:])
            except ValueError:
                return None
        return None

    # Find the nearest next visit date
    nearest_next_visit_date = None
    
    # Iterate over each day of the week
    for day, weeks in visit_schedule_data.items():
        # Check if there are any scheduled weeks for visiting
        if weeks and isinstance(weeks, list):
            # Convert valid week strings to numerical values
            valid_weeks = [get_week_number(week) for week in weeks if get_week_number(week) is not None]
            
            if valid_weeks:
                # Find the earliest scheduled week
                earliest_week = min(valid_weeks)
                
                try:
                    # Calculate the first day of the earliest week in the current month
                    first_day_of_month = current_date.replace(day=1)
                    days_to_add = (earliest_week - 1) * 7 + weekday_indices[day]
                    
                    # Calculate the next visit date
                    next_visit_date = first_day_of_month + datetime.timedelta(days=days_to_add)
                    
                    # If the next visit date is in the past, calculate for the next month
                    if next_visit_date < current_date:
                        first_day_of_next_month = (first_day_of_month + datetime.timedelta(days=32)).replace(day=1)
                        next_visit_date = first_day_of_next_month + datetime.timedelta(days=days_to_add)
                    
                    # Find the nearest next visit date from today
                    if nearest_next_visit_date is None or next_visit_date < nearest_next_visit_date:
                        nearest_next_visit_date = next_visit_date
                
                except (ValueError, IndexError):
                    pass  # Ignore if there's an error in calculating the next visit date
    
    if nearest_next_visit_date == current_date:
        nearest_next_visit_date = "Today"
        
    return nearest_next_visit_date

# # Example usage
# visit_schedule = '{"Friday": ["Week2", "Week4", "Week1", "Week5"], "Monday": ["Week1", "Week5", "Week4", "Week2", "Week3"], "Sunday": ["Week4", "Week1"], "Tuesday": ["Week5", "Week4"], "Saturday": ["Week4", "Week5", "Week2"], "Thursday": ["Week5", "Week1"], "Wednesday": ["Week2", "Week3", "Week4"]}'
# next_visit_dates = get_next_visit_date(visit_schedule)
# print(next_visit_dates)
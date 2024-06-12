import pytz
import traceback
from typing import Optional, Dict

from django.utils import timezone
from datetime import datetime, time
from django.conf import settings

TIME_ZONE = settings.TIME_ZONE


def get_date_time_dict_in_ist(
    datetime_utc_object: datetime,
    need_date: bool = True,
    need_time: bool = True,
    noon_format: bool = False,
    date_format: str = "%d/%m/%Y",
    time_format: str = "%I:%M:%S",
    default_timezone: Optional[str] = TIME_ZONE,
    *args,
    **kwargs,
) -> Dict[str, str]:
    """
    Returns the formatted date and time dictionary in IST timezone.

    Args:
        datetime_utc_object (datetime): The datetime object in UTC timezone.
        need_date (bool, optional): Whether to include date in the dictionary. Defaults to True.
        need_time (bool, optional): Whether to include time in the dictionary. Defaults to True.
        noon_format (bool, optional): Whether to include AM/PM in the time string. Defaults to False.
        date_format (str, optional): The format for the date part. Defaults to "%d/%m/%Y".
        time_format (str, optional): The format for the time part. Defaults to "%I:%M:%S".
        default_timezone (str, optional): The timezone to convert to. Defaults to "Asia/Kolkata".

    Returns:
        Dict[str, str]: The formatted date and time dictionary.
    """
    try:
        # Convert UTC datetime to IST timezone
        ist_timezone = pytz.timezone(default_timezone)
        ist_datetime_object = datetime_utc_object.astimezone(ist_timezone)

        # Initialize empty dictionary
        date_time_dict = {}

        # Format date if needed
        if need_date:
            date_string = ist_datetime_object.strftime(date_format)
            date_time_dict["date"] = date_string

        # Format time if needed
        if need_time:
            time_string = ist_datetime_object.strftime(time_format)

            # Add AM/PM if requested
            if noon_format:
                noon_string = ist_datetime_object.strftime("%p")
                time_string += " " + noon_string

            date_time_dict["time"] = time_string

        return date_time_dict
    except Exception as e:
        print(e, traceback.format_exc())


def convert_string_to_datetime_object(
    string_date: str,
    date_format: str = "%d/%m/%Y",
    *args,
    **kwargs,
) -> datetime:
    """
    Convert a string date to a datetime object.

    Args:
        string_date (str): The string representation of the date.
        date_format (str, optional): The format of the input date string. Defaults to "%d/%m/%Y".

    Returns:
        datetime: The datetime object representing the parsed date.
    """
    try:
        naive_date = datetime.strptime(string_date, date_format)
        date_object = timezone.make_aware(naive_date, timezone.get_current_timezone())
        return date_object
    except ValueError:
        return None


def convert_string_to_time_obj(
    time_in_string: str, time_format: str = "%H:%M", *args, **kwargs
) -> time:
    """
    Convert a string time to a time object.
    """
    try:
        try:
            time_str = datetime.strptime(time_in_string, time_format)
        except ValueError as e:
            print(e, traceback.format_exc())
        return time_str.time()
    except Exception as e:
        print(e, traceback.format_exc())
        return None

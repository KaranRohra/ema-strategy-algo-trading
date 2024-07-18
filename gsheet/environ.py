from gsheet import connection
from constants import SheetIndex
from utils.common import title_to_snake, time_str_to_curr_datetime
from datetime import datetime as dt


class Environ:
    def __init__(self) -> None: ...

    def set_values(
        self,
        start_time,
        end_time,
        force_stop,
        entry_time_frame,
        exit_time_frame,
        send_email,
    ):
        self.start_time = time_str_to_curr_datetime(start_time)
        self.end_time = time_str_to_curr_datetime(end_time)
        self.force_stop = force_stop == "1"
        self.entry_time_frame = int(entry_time_frame)
        self.exit_time_frame = int(exit_time_frame)
        self.send_email = send_email == "1"

    def set_environ(self):
        worksheet = connection.get_sheet().get_worksheet(SheetIndex.ENVIRON)
        values = worksheet.get_all_values()
        environ = {}

        for row in values:
            if len(row) >= 2:
                environ[title_to_snake(row[0])] = row[1]
        print(f"[{dt.now()}] [Google Sheet Environ]: {environ}")
        self.set_values(**environ)


GOOGLE_SHEET_ENVIRON = Environ()

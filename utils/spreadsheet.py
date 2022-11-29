import gspread
from oauth2client.service_account import ServiceAccountCredentials


def read_value(cell, spreadsheet_id, sheet_name, keys=None):
    """Fetch value from spreadsheet"""
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        keys["gcp_service_key"],
        gspread.auth.DEFAULT_SCOPES + ["https://spreadsheets.google.com/feeds"],
    )
    gc = gspread.authorize(creds)
    wks = gc.open_by_url(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    sh = wks.worksheet(sheet_name)
    return sh.acell(cell).value


def append_row(row_data, row_idx, spreadsheet_id, sheet_name, keys=None):
    """Append row to spreadsheet"""
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        keys["gcp_service_key"],
        gspread.auth.DEFAULT_SCOPES + ["https://spreadsheets.google.com/feeds"],
    )
    gc = gspread.authorize(creds)
    wks = gc.open_by_url(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    sh = wks.worksheet(sheet_name)
    sh.insert_row(row_data, row_idx)


def write_value(value, cell, spreadsheet_id, sheet_name, keys=None):
    """Write value to spreadsheet"""
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        keys["gcp_service_key"],
        gspread.auth.DEFAULT_SCOPES + ["https://spreadsheets.google.com/feeds"],
    )
    gc = gspread.authorize(creds)
    wks = gc.open_by_url(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    sh = wks.worksheet(sheet_name)
    sh.update(cell, value)


def write_fomula(formula, cell, spreadsheet_id, sheet_name, keys=None):
    """Write formula to spreadsheet"""
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        keys["gcp_service_key"],
        gspread.auth.DEFAULT_SCOPES + ["https://spreadsheets.google.com/feeds"],
    )
    gc = gspread.authorize(creds)
    wks = gc.open_by_url(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    sh = wks.worksheet(sheet_name)
    sh.update(cell, formula, raw=False)


def get_last_updated_date(spreadsheet_id, sheet_name, keys=None):
    """Get last updated date for daily update"""
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        keys["gcp_service_key"],
        gspread.auth.DEFAULT_SCOPES + ["https://spreadsheets.google.com/feeds"],
    )
    gc = gspread.authorize(creds)
    wks = gc.open_by_url(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    sh = wks.worksheet(sheet_name)
    return sh.col_values(1)[-1]

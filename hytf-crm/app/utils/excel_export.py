from io import BytesIO
from typing import Iterable, Sequence
from openpyxl import Workbook


def export_rows_to_xlsx(headers: Sequence[str], rows: Iterable[Sequence]) -> bytes:
    wb = Workbook(write_only=True)
    ws = wb.create_sheet("data")
    ws.append(list(headers))
    for r in rows:
        ws.append(list(r))
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()
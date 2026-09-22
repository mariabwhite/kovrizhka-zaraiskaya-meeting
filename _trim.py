import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
p = Path(r"C:\Users\Whitenois\Desktop\Новый центр управления\08_Projects\14_Krotova_Cedric\Kovrizhka_firmstyle\06_2026-09-21_incoming") / "client-meeting-2026-09-22.html"
lines = p.read_text(encoding='utf-8').splitlines(keepends=True)
new = lines[:374] + lines[567:]
p.write_text("".join(new), encoding='utf-8', newline='')
print(f'was {len(lines)} now {len(new)}')

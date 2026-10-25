import openpyxl, json, os, sys
wb = openpyxl.load_workbook("s.xlsx")
os.makedirs("img", exist_ok=True)
out = []
for si, ws in enumerate(wb.worksheets):
    cells = []
    for row in ws.iter_rows():
        for c in row:
            if c.value is None and not c.hyperlink and not c.comment:
                continue
            d = {"r": c.row, "c": c.column, "v": c.value if isinstance(c.value, (int, float, str)) else str(c.value)}
            if c.hyperlink: d["link"] = c.hyperlink.target
            if c.comment: d["note"] = c.comment.text
            if c.fill and c.fill.fgColor and c.fill.fgColor.rgb not in (None, "00000000") and isinstance(c.fill.fgColor.rgb, str): d["bg"] = c.fill.fgColor.rgb
            if c.font and c.font.bold: d["b"] = 1
            cells.append(d)
    imgs = []
    for k, im in enumerate(ws._images):
        a = im.anchor
        fr = getattr(a, "_from", None)
        ext = (im.format or "png").lower()
        name = f"img/s{si:02d}_{k:03d}.{ext}"
        open(name, "wb").write(im._data())
        imgs.append({"file": name, "r": (fr.row + 1) if fr else None, "c": (fr.col + 1) if fr else None, "w": im.width, "h": im.height})
    out.append({"sheet": ws.title, "merged": [str(m) for m in ws.merged_cells.ranges], "cells": cells, "images": imgs})
json.dump(out, open("sheet.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for s in out:
    print(f"{s['sheet'][:40]:40s} cells {len(s['cells']):5d} images {len(s['images']):3d}")

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import mm


def fmt(x):
    if pd.isna(x):
        return ""
    if isinstance(x, float):
        return f"{x:.6g}"
    return str(x)


def wrap_header(text: str) -> str:
    # simple header wrapping: split on common separators
    # you can customize more if you want
    for sep in ["[", "]", "(", ")", "_"]:
        text = text.replace(sep, " " + sep + " ")
    text = " ".join(text.split())
    # allow ReportLab to wrap by spaces
    return text


def df_to_pdf_column_slices(
    csv_path: str,
    pdf_path: str,
    title: str = "Appendix: Boiler KPIs – All Runs",
    id_cols=("run", "param_group", "param_value"),
    kpi_cols_per_page: int = 7,
    pagesize=landscape(A4),
    font_size_body: int = 7,
    font_size_header: int = 7,
    left_margin_mm: float = 10,
    right_margin_mm: float = 10,
    top_margin_mm: float = 10,
    bottom_margin_mm: float = 10,
):
    df = pd.read_csv(csv_path)

    # Ensure ID columns exist
    for c in id_cols:
        if c not in df.columns:
            raise ValueError(f"Missing expected ID column: {c}")

    # Order: ID cols first, then the rest
    other_cols = [c for c in df.columns if c not in id_cols]
    df = df[list(id_cols) + other_cols]

    # Styles for wrapped cells
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        "header",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=font_size_header,
        leading=font_size_header + 1,
    )
    body_style = ParagraphStyle(
        "body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=font_size_body,
        leading=font_size_body + 1,
    )

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=pagesize,
        leftMargin=left_margin_mm * mm,
        rightMargin=right_margin_mm * mm,
        topMargin=top_margin_mm * mm,
        bottomMargin=bottom_margin_mm * mm,
    )

    page_width, _ = pagesize
    usable_width = page_width - doc.leftMargin - doc.rightMargin

    story = []
    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 6 * mm))

    # Slice KPI columns across pages
    kpis = other_cols
    slices = [kpis[i:i + kpi_cols_per_page] for i in range(0, len(kpis), kpi_cols_per_page)]

    for si, kpi_slice in enumerate(slices, start=1):
        cols = list(id_cols) + kpi_slice
        sub = df[cols].applymap(fmt)

        # Build table data with wrapped header Paragraphs
        header_row = [Paragraph(wrap_header(c), header_style) for c in cols]
        body_rows = [
            [Paragraph(str(v), body_style) for v in row]
            for row in sub.values.tolist()
        ]
        data = [header_row] + body_rows

        # Column widths: give IDs a fixed share, spread the rest
        id_share = 0.30  # 30% width for ID columns total
        id_w = usable_width * id_share
        kpi_w = usable_width - id_w

        id_widths = [id_w * 0.50, id_w * 0.30, id_w * 0.20]  # run, group, value
        kpi_width_each = kpi_w / max(1, len(kpi_slice))
        col_widths = id_widths + [kpi_width_each] * len(kpi_slice)

        tbl = Table(data, colWidths=col_widths, repeatRows=1)

        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),

            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),

            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),

            # Align IDs left; KPI numbers right
            ("ALIGN", (0, 1), (2, -1), "LEFT"),
            ("ALIGN", (3, 1), (-1, -1), "RIGHT"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ]))

        story.append(Paragraph(f"KPI columns {si}/{len(slices)}", styles["Italic"]))
        story.append(Spacer(1, 2 * mm))
        story.append(tbl)

        if si < len(slices):
            story.append(PageBreak())

    doc.build(story)


if __name__ == "__main__":
    df_to_pdf_column_slices(
        csv_path="results/summary/boiler_kpis_all_runs.csv",
        pdf_path="boiler_kpis_all_runs_appendix.pdf",
        kpi_cols_per_page=7,   # try 6–8
        font_size_body=7,      # try 8 if you reduce cols/page
        font_size_header=7,
    )

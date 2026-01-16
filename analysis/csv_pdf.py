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
    for sep in ["[", "]", "(", ")", "_"]:
        text = text.replace(sep, " " + sep + " ")
    return " ".join(text.split())


def csv_to_pdf_column_slices(
    csv_path: str,
    pdf_path: str,
    title: str,
    id_cols: list[str],
    kpi_cols_per_page: int = 7,
    id_share: float = 0.38,      # more space for IDs since stage/kind exist
    pagesize=landscape(A4),
    font_size_body: int = 7,
    font_size_header: int = 7,
    margins_mm=(10, 10, 10, 10), # left, right, top, bottom
):
    df = pd.read_csv(csv_path)

    for c in id_cols:
        if c not in df.columns:
            raise ValueError(f"Missing expected ID column: {c}")

    other_cols = [c for c in df.columns if c not in id_cols]
    df = df[id_cols + other_cols]

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

    left_mm, right_mm, top_mm, bottom_mm = margins_mm
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=pagesize,
        leftMargin=left_mm * mm,
        rightMargin=right_mm * mm,
        topMargin=top_mm * mm,
        bottomMargin=bottom_mm * mm,
    )

    page_width, _ = pagesize
    usable_width = page_width - doc.leftMargin - doc.rightMargin

    story = []
    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 6 * mm))

    kpis = other_cols
    slices = [kpis[i:i + kpi_cols_per_page] for i in range(0, len(kpis), kpi_cols_per_page)]

    # ID width distribution (weighted): run wider, then group/value, then stage/kind
    # Adjust if you want different emphasis.
    id_weights = []
    for c in id_cols:
        if c == "run":
            id_weights.append(3.0)
        elif c in ("param_group", "stage"):
            id_weights.append(2.0)
        elif c in ("param_value", "kind"):
            id_weights.append(1.5)
        else:
            id_weights.append(1.5)

    id_total_w = usable_width * id_share
    kpi_total_w = usable_width - id_total_w
    id_widths = [id_total_w * w / sum(id_weights) for w in id_weights]

    for si, kpi_slice in enumerate(slices, start=1):
        cols = id_cols + kpi_slice
        sub = df[cols].applymap(fmt)

        header_row = [Paragraph(wrap_header(c), header_style) for c in cols]
        body_rows = [[Paragraph(str(v), body_style) for v in row] for row in sub.values.tolist()]
        data = [header_row] + body_rows

        kpi_width_each = kpi_total_w / max(1, len(kpi_slice))
        col_widths = id_widths + [kpi_width_each] * len(kpi_slice)

        tbl = Table(data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("ALIGN", (0, 1), (len(id_cols)-1, -1), "LEFT"),
            ("ALIGN", (len(id_cols), 1), (-1, -1), "RIGHT"),
        ]))

        story.append(Paragraph(f"Columns slice {si}/{len(slices)}", styles["Italic"]))
        story.append(Spacer(1, 2 * mm))
        story.append(tbl)

        if si < len(slices):
            story.append(PageBreak())

    doc.build(story)


if __name__ == "__main__":
    # ---- CONFIG FOR stages_summary_all_runs.csv ----
    csv_to_pdf_column_slices(
        csv_path="results/summary/stages_summary_all_runs.csv",
        pdf_path="stages_summary_all_runs_appendix.pdf",
        title="Appendix: Stages Summary – All Runs",
        id_cols=["run", "param_group", "param_value", "stage", "kind"],
        kpi_cols_per_page=7,   # try 6–8
        id_share=0.42,         # more ID space (stage/kind)
        font_size_body=7,
        font_size_header=7,
    )

    # ---- If you also want the boiler_kpis file via same script, add a second call:
    # csv_to_pdf_column_slices(
    #     csv_path="results/summary/boiler_kpis_all_runs.csv",
    #     pdf_path="boiler_kpis_all_runs_appendix.pdf",
    #     title="Appendix: Boiler KPIs – All Runs",
    #     id_cols=["run", "param_group", "param_value"],
    #     kpi_cols_per_page=7,
    #     id_share=0.30,
    # )

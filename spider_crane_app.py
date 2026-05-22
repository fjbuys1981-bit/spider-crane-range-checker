import io
import re
from pathlib import Path
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps


st.set_page_config(
    page_title="Preston Hire - Spider Crane Range Checker",
    page_icon="SC",
    layout="wide",
)


PH_YELLOW = "#F5D800"
PH_BLACK = "#1A1A1A"
PH_RED = "#E8400C"
PH_GREEN = "#27AE60"
PH_ORANGE = "#F39C12"
PH_WHITE = "#FFFFFF"
PH_STEEL = "#EEF1F3"
PH_MUTED = "#6B7280"
PH_LINE = "#D8DEE4"
ASSET_DIR = Path(__file__).with_name("cad_assets")


FLEET_GUIDE = {
    "SC295C": {
        "tagline": "Narrowest, multiple outrigger settings.",
        "unit_tare_kg": 2040,
        "outriggers_max_m": "3.885 x 3.935",
        "outriggers_min_m": "2.31 x 2.57",
        "unit_dimensions_m": "0.60 x 2.73 x 1.375",
        "capacity_min_radius": "2.93t @ 1.4m",
        "capacity_max_radius": "130kg @ 8.41m",
        "min_radius_m": 1.4,
        "min_radius_capacity_kg": 2930,
        "max_radius_m": 8.41,
        "max_radius_capacity_kg": 130,
        "boom_length_m": 8.65,
        "capacity_points": [
            [1.0, 2900],
            [1.4, 2900],
            [1.5, 2650],
            [1.8, 2250],
            [2.0, 2050],
            [2.5, 1650],
            [3.0, 1300],
            [3.5, 1000],
            [3.835, 900],
            [4.0, 750],
            [4.5, 600],
            [5.0, 500],
            [5.5, 420],
            [6.0, 360],
            [6.5, 320],
            [6.89, 270],
            [7.0, 200],
            [8.0, 150],
            [8.41, 130],
        ],
        "capacity_points_min": [
            [1.0, 2000],
            [1.4, 2000],
            [1.5, 2000],
            [1.8, 1450],
            [2.0, 1100],
            [2.5, 650],
            [3.0, 500],
            [3.5, 380],
            [4.0, 300],
            [4.5, 250],
            [5.0, 200],
            [5.5, 160],
            [6.0, 130],
            [6.5, 100],
            [7.0, 70],
            [8.0, 40],
            [8.41, 30],
        ],
        "hook_drop_1_part": "800kg / 59.5m",
        "features": "Diesel/Electric, radio remote, electric option, searcher hook 500mm / 300kg",
    },
    "SC305C": {
        "tagline": "Powerful yet compact, lifts nearly 3t @ 2.5m.",
        "unit_tare_kg": 3770,
        "outriggers_max_m": "4.504 x 4.880",
        "outriggers_min_m": "3.712 x 4.291",
        "unit_dimensions_m": "1.28 x 4.285 x 1.695",
        "capacity_min_radius": "2.98t @ 2.5m",
        "capacity_max_radius": "250kg @ 12.1m",
        "min_radius_m": 2.5,
        "min_radius_capacity_kg": 2980,
        "max_radius_m": 12.1,
        "max_radius_capacity_kg": 250,
        "boom_length_m": 12.5,
        "capacity_points": [
            [2.5, 2980],
            [3.0, 2390],
            [4.0, 1990],
            [5.0, 1340],
            [6.0, 990],
            [7.0, 730],
            [8.0, 570],
            [9.0, 500],
            [10.0, 435],
            [11.0, 280],
            [12.1, 250],
        ],
        "hook_drop_1_part": "750kg / 64.36m",
        "features": "Diesel, radio remote, 360 degree slew",
    },
    "SC376C": {
        "tagline": "Stretches and lifts from a tiny chassis, lifts 100kg @ 14.5m.",
        "unit_tare_kg": 4020,
        "outriggers_max_m": "4.44 x 4.565",
        "outriggers_min_m": "3.205 x 3.7",
        "unit_dimensions_m": "1.3 x 4.34 x 1.8",
        "capacity_min_radius": "3.03t @ 2.5m",
        "capacity_max_radius": "100kg @ 14.45m",
        "min_radius_m": 2.5,
        "min_radius_capacity_kg": 3030,
        "max_radius_m": 14.45,
        "max_radius_capacity_kg": 100,
        "boom_length_m": 14.9,
        "capacity_points": [
            [2.0, 2900],
            [2.5, 2900],
            [3.0, 2350],
            [3.5, 1950],
            [4.0, 1670],
            [4.5, 1450],
            [5.0, 1300],
            [5.69, 1070],
            [6.0, 840],
            [7.0, 690],
            [7.88, 590],
            [8.0, 520],
            [9.0, 470],
            [10.07, 380],
            [11.0, 240],
            [12.26, 230],
            [13.0, 110],
            [14.45, 100],
        ],
        "hook_drop_1_part": "800kg / 77.1m",
        "features": "Diesel/Electric, radio remote, optional fly jib 2.0m / 700kg",
    },
    "SC405C": {
        "tagline": "Very versatile, Pick 'n' Carry 500kg, lift 210kg @ 16.4m.",
        "unit_tare_kg": 5720,
        "outriggers_max_m": "6.1 x 5.252",
        "outriggers_min_m": "5.3 x 4.331",
        "unit_dimensions_m": "1.38 x 4.98 x 1.98",
        "capacity_min_radius": "3.83t @ 2.7m",
        "capacity_max_radius": "210kg @ 16.4m",
        "min_radius_m": 2.7,
        "min_radius_capacity_kg": 3830,
        "max_radius_m": 16.4,
        "max_radius_capacity_kg": 210,
        "boom_length_m": 16.8,
        "capacity_points": [
            [2.7, 3830],
            [3.5, 3030],
            [4.0, 2580],
            [5.0, 2030],
            [6.0, 1680],
            [7.0, 1380],
            [8.0, 1130],
            [9.0, 880],
            [10.0, 830],
            [11.0, 690],
            [12.0, 530],
            [13.0, 430],
            [14.0, 320],
            [15.0, 260],
            [16.4, 210],
        ],
        "hook_drop_1_part": "700kg / 82.0m",
        "features": "Diesel, radio remote, Pick & Carry 500kg, optional fly jib 4.5m / 170kg",
    },
    "SC547C": {
        "tagline": "Full remote control and lifts 50kg @ 17.8m.",
        "unit_tare_kg": 5220,
        "outriggers_max_m": "5.94 x 5.9",
        "outriggers_min_m": "4.08 x 4.67",
        "unit_dimensions_m": "1.38 x 4.955 x 1.98",
        "capacity_min_radius": "4.05t @ 2.5m",
        "capacity_max_radius": "50kg @ 17.83m",
        "min_radius_m": 2.5,
        "min_radius_capacity_kg": 4050,
        "max_radius_m": 17.83,
        "max_radius_capacity_kg": 50,
        "boom_length_m": 18.2,
        "capacity_points": [
            [2.5, 4000],
            [2.7, 3850],
            [3.0, 3500],
            [3.5, 3000],
            [4.0, 2550],
            [4.5, 2250],
            [5.0, 2000],
            [5.5, 1800],
            [6.0, 1630],
            [7.0, 1350],
            [7.51, 1300],
            [8.0, 1100],
            [9.0, 900],
            [10.0, 800],
            [11.0, 600],
            [12.0, 500],
            [13.0, 350],
            [14.0, 290],
            [15.0, 230],
            [16.0, 160],
            [17.0, 80],
            [17.83, 50],
        ],
        "hook_drop_1_part": "1000kg / 93.7m",
        "features": "Diesel/Electric, radio remote, searcher hook 800mm / 500kg",
    },
    "SC706C": {
        "tagline": "Powerful and versatile, lifts 6t @ 3m and 200kg @ 18.6m.",
        "unit_tare_kg": 8080,
        "outriggers_max_m": "6.46 x 6.55",
        "outriggers_min_m": "4.62 x 5.28",
        "unit_dimensions_m": "1.67 x 5.61 x 2.185",
        "capacity_min_radius": "6t @ 3.0m",
        "capacity_max_radius": "200kg @ 18.6m",
        "min_radius_m": 3.0,
        "min_radius_capacity_kg": 6000,
        "max_radius_m": 18.6,
        "max_radius_capacity_kg": 200,
        "boom_length_m": 19.5,
        "capacity_points": [
            [2.4, 6000],
            [3.0, 6000],
            [3.5, 5450],
            [4.0, 4850],
            [4.3, 3950],
            [5.0, 3750],
            [6.0, 2950],
            [7.0, 2400],
            [8.0, 1800],
            [9.0, 1400],
            [10.0, 1200],
            [11.0, 1000],
            [12.0, 850],
            [13.0, 700],
            [14.0, 600],
            [15.0, 500],
            [16.0, 400],
            [18.0, 250],
            [18.6, 200],
        ],
        "hook_drop_1_part": "1500kg / 101m",
        "features": "Diesel/Electric, radio remote, optional fly jib 2.11/3.11m / 800kg",
    },
    "SC815C": {
        "tagline": "Will Pick 'n' Carry 1000kg, reach 25.5m with fly jib.",
        "unit_tare_kg": 10230,
        "outriggers_max_m": "6.52 x 6.77",
        "outriggers_min_m": "4.95 x 5.74",
        "unit_dimensions_m": "1.74 x 5.9 x 2.49",
        "capacity_min_radius": "8.09t @ 2.4m",
        "capacity_max_radius": "340kg @ 18.8m",
        "min_radius_m": 2.4,
        "min_radius_capacity_kg": 8090,
        "max_radius_m": 18.8,
        "max_radius_capacity_kg": 340,
        "boom_length_m": 19.6,
        "capacity_points": [
            [2.4, 8090],
            [4.92, 8000],
            [6.0, 6390],
            [7.0, 5490],
            [8.0, 4190],
            [9.0, 3190],
            [10.0, 2290],
            [11.0, 1690],
            [12.0, 1290],
            [13.0, 1040],
            [14.0, 890],
            [15.0, 740],
            [16.0, 640],
            [17.0, 590],
            [18.8, 340],
        ],
        "hook_drop_1_part": "1450kg / 126.0m",
        "features": "Diesel, full remote, onboard cameras, Pick & Carry 1.0t @ 5m",
    },
}


def footprint_dims(card, setup):
    key = "outriggers_min_m" if setup == "Min footprint" else "outriggers_max_m"
    values = re.findall(r"\d+(?:\.\d+)?", card[key])
    if len(values) >= 2:
        return float(values[0]), float(values[1])
    return 0.0, 0.0


def footprint_fits(card, setup, floor_length, floor_width):
    length, width = footprint_dims(card, setup)
    fits_normal = length <= floor_length and width <= floor_width
    fits_rotated = width <= floor_length and length <= floor_width
    return fits_normal or fits_rotated


def resolve_setup(card, requested_setup, floor_length, floor_width):
    if requested_setup == "Auto fit floor":
        if footprint_fits(card, "Max footprint", floor_length, floor_width):
            return "Max footprint"
        if footprint_fits(card, "Min footprint", floor_length, floor_width):
            return "Min footprint"
        return "Max footprint"
    return requested_setup


def estimated_capacity(card, radius, setup):
    if setup == "Min footprint":
        points = card.get("capacity_points_min")
        if not points:
            points = [[radius, capacity * 0.65] for radius, capacity in card.get("capacity_points", [])]
    else:
        points = card.get("capacity_points")
    if points:
        points = sorted(points, key=lambda item: item[0])
        if radius <= points[0][0]:
            return points[0][1]
        if radius >= points[-1][0]:
            return points[-1][1]
        for (r1, c1), (r2, c2) in zip(points, points[1:]):
            if r1 <= radius <= r2:
                ratio = (radius - r1) / (r2 - r1)
                return c1 + ratio * (c2 - c1)

    min_radius = card["min_radius_m"]
    max_radius = card["max_radius_m"]
    min_capacity = card["min_radius_capacity_kg"]
    max_capacity = card["max_radius_capacity_kg"]
    if setup == "Min footprint":
        min_capacity *= 0.65
        max_capacity *= 0.65
    if radius <= min_radius:
        return min_capacity
    if radius >= max_radius:
        return max_capacity
    ratio = (radius - min_radius) / (max_radius - min_radius)
    return min_capacity + ratio * (max_capacity - min_capacity)


def get_brochure_status(card, working_radius, boom_length, total_load, setup, floor_length, floor_width):
    issues = []
    warnings = []

    if working_radius < card["min_radius_m"]:
        issues.append(f"Radius is below range minimum of {card['min_radius_m']:.2f} m.")
    if working_radius > card["max_radius_m"]:
        issues.append(f"Radius exceeds range maximum of {card['max_radius_m']:.2f} m.")
    if boom_length > card["boom_length_m"]:
        issues.append(f"Boom length exceeds range maximum of {card['boom_length_m']:.2f} m.")

    footprint_length, footprint_width = footprint_dims(card, setup)
    if not footprint_fits(card, setup, floor_length, floor_width):
        issues.append(
            f"{setup} requires approximately {footprint_length:.2f} x {footprint_width:.2f} m, which does not fit the entered floor area."
        )

    allowed = estimated_capacity(card, working_radius, setup)
    utilisation = (total_load / allowed) * 100 if allowed else 0
    if total_load > allowed:
        issues.append(f"Total load exceeds estimated chart capacity of {allowed:.0f} kg at this radius.")
    elif utilisation >= 80:
        warnings.append("Lift is above 80% of the estimated chart envelope.")

    if issues:
        return "RED ZONE", PH_RED, utilisation, allowed, issues, warnings
    if warnings:
        return "CHECK ZONE", PH_ORANGE, utilisation, allowed, issues, warnings
    if setup == "Min footprint" and not card.get("capacity_points_min"):
        warnings.append("Min footprint capacity is conservatively estimated until the exact min-footprint chart is loaded.")
    return "WITHIN RANGE", PH_GREEN, utilisation, allowed, issues, warnings


def find_suitable_cranes(working_radius, boom_length, total_load, requested_setup, floor_length, floor_width):
    matches = []
    for crane_name, card in FLEET_GUIDE.items():
        setup = resolve_setup(card, requested_setup, floor_length, floor_width)
        status, status_color, utilisation, allowed, issues, warnings = get_brochure_status(
            card, working_radius, boom_length, total_load, setup, floor_length, floor_width
        )
        if not issues:
            matches.append(
                {
                    "crane": crane_name,
                    "card": card,
                    "setup": setup,
                    "status": status,
                    "status_color": status_color,
                    "utilisation": utilisation,
                    "allowed": allowed,
                    "warnings": warnings,
                }
            )
    return sorted(matches, key=lambda item: (item["card"]["min_radius_capacity_kg"], item["card"]["unit_tare_kg"]))


def fleet_guide_df():
    return pd.DataFrame(
        [
            {
                "Crane": name,
                "Tare": f"{card['unit_tare_kg']} kg",
                "Max Outriggers": f"{card['outriggers_max_m']} m",
                "Min Radius Capacity": card["capacity_min_radius"],
                "Max Radius Capacity": card["capacity_max_radius"],
                "Boom Length": f"{card['boom_length_m']} m",
                "Hook Drop": card["hook_drop_1_part"],
            }
            for name, card in FLEET_GUIDE.items()
        ]
    )


def create_pdf_report_bytes(summary_df, result_df, title):
    lines = [
        "PRESTON HIRE",
        "Spider Crane Range Report",
        f"Generated: {datetime.now().strftime('%d %b %Y %H:%M')}",
        "",
        title,
        "",
        "Inputs",
    ]
    lines.extend(f"{row.Item}: {row.Value}" for row in summary_df.itertuples())
    lines.extend(["", "Results"])
    lines.extend(f"{row.Item}: {row.Value}" for row in result_df.itertuples())
    lines.extend(
        [
            "",
            "Planning note: spider crane range check only.",
            "Confirm the manufacturer load chart, hook height, boom configuration, ground conditions, and temporary works requirements before site use.",
        ]
    )

    def esc(value):
        return str(value).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    content = ["BT", "/F1 18 Tf", "72 770 Td", f"({esc(lines[0])}) Tj", "/F1 11 Tf", "0 -24 Td"]
    for line in lines[1:]:
        content.append(f"({esc(line)}) Tj")
        content.append("0 -16 Td")
    content.append("ET")
    stream = "\n".join(content).encode("latin-1", errors="replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode("ascii")
    )
    return bytes(pdf)


def cad_image_path(crane_name):
    return None


def chart_image_path(crane_name):
    path = ASSET_DIR / f"{crane_name}_chart.jpg"
    if path.exists():
        return path
    return None


def load_font(size, bold=False):
    candidates = [
        "arialbd.ttf" if bold else "arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def draw_wrapped(draw, text, xy, font, fill, max_width, line_gap=6):
    words = str(text).split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_width or not current:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    x, y = xy
    line_height = draw.textbbox((0, 0), "Ag", font=font)[3] + line_gap
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def create_lift_plan_pdf_bytes(crane_name, card, working_radius, boom_length, hook_height, total_load, allowed_load, status, utilisation, setup, floor_length, floor_width):
    width, height = 1240, 1754
    image = Image.new("RGB", (width, height), "#EEF1F3")
    draw = ImageDraw.Draw(image)
    title_font = load_font(44, bold=True)
    h_font = load_font(30, bold=True)
    body_font = load_font(25)
    small_font = load_font(20)
    status_color = PH_RED if status == "RED ZONE" else PH_ORANGE if status == "CHECK ZONE" else PH_GREEN

    margin = 58
    draw.rounded_rectangle((margin, 45, width - margin, 155), radius=14, fill=PH_BLACK)
    draw.rectangle((margin, 45, margin + 18, 155), fill=PH_YELLOW)
    draw.text((95, 68), "PRESTON HIRE", font=title_font, fill=PH_YELLOW)
    draw.text((95, 118), f"{crane_name} Spider Crane Range Checker", font=body_font, fill=PH_WHITE)

    draw.rounded_rectangle((margin, 185, width - margin, 285), radius=12, fill=status_color)
    draw.text((88, 214), f"STATUS: {status}", font=h_font, fill=PH_WHITE)
    draw.text((88, 252), f"{utilisation:.1f}% of selected setup capacity", font=body_font, fill=PH_WHITE)

    left_box = (margin, 315, 590, 660)
    right_box = (620, 315, width - margin, 660)
    draw.rounded_rectangle(left_box, radius=12, fill="white", outline=PH_LINE, width=2)
    draw.rounded_rectangle(right_box, radius=12, fill="white", outline=PH_LINE, width=2)

    draw.text((88, 345), "Lift Inputs", font=h_font, fill=PH_BLACK)
    y = 397
    required_rows = [
        ("Radius", f"{working_radius:.2f} m"),
        ("Load weight", f"{total_load:.0f} kg"),
        ("Boom length", f"{boom_length:.2f} m"),
        ("Hook height", f"{hook_height:.2f} m"),
    ]
    for label, value in required_rows:
        draw.text((88, y), label, font=small_font, fill=PH_MUTED)
        draw.text((318, y - 5), value, font=body_font, fill=PH_BLACK)
        y += 50

    draw.text((650, 345), "Setup", font=h_font, fill=PH_BLACK)
    y = 397
    setup_rows = [
        ("Outriggers", setup),
        ("Floor area", f"{floor_length:.2f} x {floor_width:.2f} m"),
        ("Estimated capacity", f"{allowed_load:.0f} kg"),
        ("Utilisation", f"{utilisation:.1f}%"),
    ]
    for label, value in setup_rows:
        draw.text((650, y), label, font=small_font, fill=PH_MUTED)
        draw.text((880, y - 5), value, font=body_font, fill=PH_BLACK)
        y += 50

    chart_box = (margin, 700, width - margin, 1500)
    draw.rounded_rectangle(chart_box, radius=12, fill="white", outline=PH_LINE, width=2)
    draw.text((88, 730), "Crane Chart Reference", font=h_font, fill=PH_BLACK)
    visual_path = chart_image_path(crane_name) or cad_image_path(crane_name)
    if visual_path:
        visual = Image.open(visual_path).convert("RGB")
        visual = ImageOps.contain(visual, (1060, 690), method=Image.Resampling.LANCZOS)
        paste_x = margin + (width - margin * 2 - visual.width) // 2
        paste_y = 780 + (690 - visual.height) // 2
        image.paste(visual, (paste_x, paste_y))
        draw.text((88, 1465), f"Reference image: {visual_path.name}", font=small_font, fill=PH_MUTED)
    else:
        draw.text((120, 1080), "Reference image not available for this crane yet.", font=h_font, fill=PH_MUTED)

    draw.rounded_rectangle((margin, 1530, width - margin, 1660), radius=12, fill="white", outline=PH_LINE, width=2)
    note_text = (
        f"{card['tagline']} Max radius {card['max_radius_m']:.2f} m. "
        f"Max boom length {card['boom_length_m']:.2f} m. "
        f"Min-radius capacity {card['capacity_min_radius']}. "
        f"Max-radius capacity {card['capacity_max_radius']}. "
        "Confirm the exact manufacturer load chart, configuration, ground conditions, and lift plan before site use."
    )
    draw_wrapped(draw, note_text, (88, 1560), small_font, PH_BLACK, width - 176)

    buffer = io.BytesIO()
    image.save(buffer, format="PDF", resolution=150.0)
    return buffer.getvalue()


st.markdown(
    f"""
    <style>
    .stApp {{ background: {PH_STEEL}; }}
    [data-testid="stSidebar"] {{ background: {PH_BLACK}; }}
    [data-testid="stSidebar"] * {{ color: {PH_WHITE}; }}
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] *,
    [data-testid="stSidebar"] [data-baseweb="input"] * {{ color: {PH_BLACK}; }}
    [data-testid="stSidebar"] svg {{ color: {PH_BLACK}; fill: {PH_BLACK}; }}
    .ph-hero {{
        background: {PH_BLACK};
        padding: 24px 28px;
        border-radius: 8px;
        border-left: 10px solid {PH_YELLOW};
    }}
    .ph-hero h1 {{
        color: {PH_YELLOW};
        margin: 0;
        font-size: 2rem;
        letter-spacing: 0;
    }}
    .ph-hero h3 {{
        color: white;
        margin: 6px 0 0;
        font-weight: 500;
    }}
    .metric-card {{
        background: white;
        border: 1px solid {PH_LINE};
        border-radius: 8px;
        padding: 16px;
        min-height: 116px;
    }}
    .metric-card .label {{
        color: {PH_MUTED};
        font-size: 0.84rem;
        margin-bottom: 6px;
    }}
    .metric-card .value {{
        color: {PH_BLACK};
        font-size: 1.55rem;
        font-weight: 700;
        line-height: 1.1;
    }}
    .status-banner {{
        padding: 18px 22px;
        border-radius: 8px;
        color: white;
    }}
    .status-banner h2, .status-banner h1 {{ margin: 0; }}
    .section-title {{
        color: {PH_BLACK};
        font-weight: 700;
        margin: 8px 0 2px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="ph-hero">
        <h1>PRESTON HIRE</h1>
        <h3>Spider Crane Range Checker</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("Crane Selection")
selection_mode = st.sidebar.radio("Selection Mode", ["Auto select crane", "Choose crane manually"])

st.sidebar.header("Lift Inputs")
working_radius = st.sidebar.number_input(
    "Working Radius (m)",
    min_value=0.1,
    max_value=35.0,
    value=6.0,
    step=0.1,
)
boom_length = st.sidebar.number_input(
    "Boom Length (m)",
    min_value=0.1,
    max_value=35.0,
    value=8.0,
    step=0.1,
)
hook_height = st.sidebar.number_input(
    "Hook Height (m)",
    min_value=0.0,
    max_value=40.0,
    value=6.0,
    step=0.1,
)
lifted_load = st.sidebar.number_input("Lifted Load (kg)", min_value=0, max_value=15000, value=500, step=25)
hook_weight = st.sidebar.number_input("Hook / Attachment Weight (kg)", min_value=0, max_value=1500, value=50, step=5)

total_load = lifted_load + hook_weight

st.sidebar.header("Floor / Outriggers")
floor_length = st.sidebar.number_input("Available Floor Length (m)", min_value=1.0, max_value=30.0, value=8.0, step=0.1)
floor_width = st.sidebar.number_input("Available Floor Width (m)", min_value=1.0, max_value=30.0, value=8.0, step=0.1)
requested_setup = st.sidebar.selectbox("Outrigger Setup", ["Auto fit floor", "Max footprint", "Min footprint"])

suitable_cranes = find_suitable_cranes(working_radius, boom_length, total_load, requested_setup, floor_length, floor_width)

if selection_mode == "Auto select crane":
    if suitable_cranes:
        crane_name = suitable_cranes[0]["crane"]
    else:
        crane_name = max(FLEET_GUIDE, key=lambda name: FLEET_GUIDE[name]["min_radius_capacity_kg"])
    st.sidebar.success(f"Selected: {crane_name}" if suitable_cranes else "No crane fits these inputs.")
else:
    crane_name = st.sidebar.selectbox("Crane Model", list(FLEET_GUIDE.keys()))

card = FLEET_GUIDE[crane_name]
selected_setup = resolve_setup(card, requested_setup, floor_length, floor_width)
status, status_color, utilisation, allowed_load, issues, warnings = get_brochure_status(
    card, working_radius, boom_length, total_load, selected_setup, floor_length, floor_width
)
st.write("")
st.markdown('<h3 class="section-title">Fleet Quick Reference</h3>', unsafe_allow_html=True)
f1, f2, f3, f4 = st.columns(4)
with f1:
    st.markdown(
        f"""<div class="metric-card"><div class="label">{crane_name}</div><div class="value">{card['capacity_min_radius']}</div></div>""",
        unsafe_allow_html=True,
    )
with f2:
    st.markdown(
        f"""<div class="metric-card"><div class="label">Max Radius Capacity</div><div class="value">{card['capacity_max_radius']}</div></div>""",
        unsafe_allow_html=True,
    )
with f3:
    st.markdown(
        f"""<div class="metric-card"><div class="label">Outrigger Setup</div><div class="value">{selected_setup}</div></div>""",
        unsafe_allow_html=True,
    )
with f4:
    st.markdown(
        f"""<div class="metric-card"><div class="label">Capacity At Radius</div><div class="value">{allowed_load:.0f} kg</div></div>""",
        unsafe_allow_html=True,
    )
st.caption(f"{card['tagline']} Source: Preston Hire Cranes Quick Reference Guide.")

st.markdown(
    f"""
    <div class="status-banner" style="background:{status_color};">
        <h2>STATUS: {status}</h2>
        <h1>{utilisation:.1f}% of Estimated Chart Envelope</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

if issues:
    for issue in issues:
        st.error(issue)
elif warnings:
    for warning in warnings:
        st.warning(warning)
else:
    st.success("The entered lift is within the crane range check.")

st.info(
    "This is a spider crane range check using crane-specific capacity points read from the supplied charts. Always confirm the final lift against the manufacturer's official chart."
)

if suitable_cranes:
    st.markdown('<h3 class="section-title">Suitable Cranes</h3>', unsafe_allow_html=True)
    suitable_df = pd.DataFrame(
        [
            {
                "Crane": item["crane"],
                "Estimated Capacity": f"{item['allowed']:.0f} kg",
                "Utilisation": f"{item['utilisation']:.1f}%",
                "Outriggers": item["setup"],
                "Status": item["status"],
                "Boom Limit": f"{item['card']['boom_length_m']:.2f} m",
                "Max Radius": f"{item['card']['max_radius_m']:.2f} m",
            }
            for item in suitable_cranes
        ]
    )
    st.dataframe(suitable_df, use_container_width=True, hide_index=True)
else:
    st.error("No crane in the range list fits the entered load, radius, and boom length.")

summary_df = pd.DataFrame(
    {
        "Item": [
            "Crane",
            "Selection Mode",
            "Outrigger Setup",
            "Available Floor Area",
            "Working Radius",
            "Boom Length",
            "Hook Height",
            "Lifted Load",
            "Hook / Attachment",
            "Total Load",
            "Min Radius Capacity",
            "Max Radius Capacity",
            "Estimated Capacity At Radius",
            "Status",
        ],
        "Value": [
            crane_name,
            selection_mode,
            selected_setup,
            f"{floor_length:.2f} x {floor_width:.2f} m",
            f"{working_radius:.2f} m",
            f"{boom_length:.2f} m",
            f"{hook_height:.2f} m",
            f"{lifted_load:.0f} kg",
            f"{hook_weight:.0f} kg",
            f"{total_load:.0f} kg",
            card["capacity_min_radius"],
            card["capacity_max_radius"],
            f"{allowed_load:.0f} kg",
            status,
        ],
    }
)

result_df = pd.DataFrame(
    {
        "Item": [
            "Min Radius",
            "Max Radius",
            "Max Boom Length",
            "Selected Footprint",
            "Unit Tare",
            "Max Outriggers",
            "Min Outriggers",
            "Unit Dimensions",
            "Hook Drop (1 Part)",
            "Features",
        ],
        "Value": [
            f"{card['min_radius_m']:.2f} m",
            f"{card['max_radius_m']:.2f} m",
            f"{card['boom_length_m']:.2f} m",
            f"{footprint_dims(card, selected_setup)[0]:.2f} x {footprint_dims(card, selected_setup)[1]:.2f} m",
            f"{card['unit_tare_kg']} kg",
            f"{card['outriggers_max_m']} m",
            f"{card['outriggers_min_m']} m",
            f"{card['unit_dimensions_m']} m",
            card["hook_drop_1_part"],
            card["features"],
        ],
    }
)

tab_summary, tab_range, tab_drawing, tab_fleet, tab_export, tab_notes = st.tabs(
    ["Summary", "Range Chart", "Lift Drawing", "Fleet Guide", "Export", "Notes"]
)

with tab_summary:
    left, right = st.columns(2)
    with left:
        st.markdown('<h3 class="section-title">Lift Check</h3>', unsafe_allow_html=True)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
    with right:
        st.markdown('<h3 class="section-title">Crane Details</h3>', unsafe_allow_html=True)
        st.dataframe(result_df, use_container_width=True, hide_index=True)

with tab_range:
    st.markdown('<h3 class="section-title">Range Envelope</h3>', unsafe_allow_html=True)
    chart_points = card.get("capacity_points") or [
        [card["min_radius_m"], card["min_radius_capacity_kg"]],
        [card["max_radius_m"], card["max_radius_capacity_kg"]],
    ]
    envelope_x = [point[0] for point in chart_points]
    envelope_y = [point[1] for point in chart_points]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=envelope_x,
            y=envelope_y,
            mode="lines+markers",
            line=dict(color=PH_GREEN, width=4),
            marker=dict(size=10),
            name="Estimated chart envelope",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[working_radius],
            y=[total_load],
            mode="markers+text",
            marker=dict(size=18, color=status_color),
            text=[status],
            textposition="top center",
            name="Entered lift",
        )
    )
    fig.update_layout(
        height=430,
        plot_bgcolor=PH_BLACK,
        paper_bgcolor=PH_BLACK,
        font=dict(color=PH_WHITE),
        xaxis_title="Working radius (m)",
        yaxis_title="Load (kg)",
        margin=dict(l=10, r=10, t=24, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_drawing:
    st.markdown('<h3 class="section-title">Lift Plan Preview</h3>', unsafe_allow_html=True)
    chart_path = chart_image_path(crane_name) or cad_image_path(crane_name)
    if chart_path:
        st.image(str(chart_path), use_container_width=True)
    else:
        st.info("No chart image is available for this crane yet.")
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Radius", f"{working_radius:.2f} m")
    p2.metric("Load Weight", f"{total_load:.0f} kg")
    p3.metric("Boom Length", f"{boom_length:.2f} m")
    p4.metric("Hook Height", f"{hook_height:.2f} m")
    p5, p6, p7 = st.columns(3)
    p5.metric("Outriggers", selected_setup)
    p6.metric("Floor Size", f"{floor_length:.2f} x {floor_width:.2f} m")
    p7.metric("Status", status)
    st.info(
        f"Lift plan inputs: hook height {hook_height:.2f} m, floor size {floor_length:.2f} x {floor_width:.2f} m, "
        f"outrigger setup {selected_setup}."
    )

with tab_fleet:
    st.markdown('<h3 class="section-title">Preston Hire Crane Quick Reference</h3>', unsafe_allow_html=True)
    st.dataframe(fleet_guide_df(), use_container_width=True, hide_index=True)

with tab_export:
    st.markdown('<h3 class="section-title">Save and Export</h3>', unsafe_allow_html=True)
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "inputs": dict(zip(summary_df["Item"], summary_df["Value"])),
        "crane_details": dict(zip(result_df["Item"], result_df["Value"])),
    }
    csv_buffer = io.StringIO()
    pd.concat(
        [summary_df.rename(columns={"Item": "Metric"}), result_df.rename(columns={"Item": "Metric"})],
        ignore_index=True,
    ).to_csv(csv_buffer, index=False)

    e1, e2, e3 = st.columns(3)
    with e1:
        st.download_button(
            "Download CSV",
            csv_buffer.getvalue().encode("utf-8"),
            "spider-crane-range-check.csv",
            "text/csv",
            use_container_width=True,
            key="export_csv",
        )
    with e2:
        pdf = create_lift_plan_pdf_bytes(
            crane_name,
            card,
            working_radius,
            boom_length,
            hook_height,
            total_load,
            allowed_load,
            status,
            utilisation,
            selected_setup,
            floor_length,
            floor_width,
        )
        st.download_button(
            "Download PDF Lift Plan",
            pdf,
            "spider-crane-lift-plan.pdf",
            "application/pdf",
            use_container_width=True,
            key="export_pdf_lift_plan",
        )
    with e3:
        chart_path = chart_image_path(crane_name) or cad_image_path(crane_name)
        if chart_path:
            st.download_button(
                "Download Chart Image",
                chart_path.read_bytes(),
                chart_path.name,
                "image/jpeg" if chart_path.suffix.lower() in {".jpg", ".jpeg"} else "image/png",
                use_container_width=True,
                key="export_chart_image",
            )
        else:
            st.info("No chart image is available to download.")

with tab_notes:
    st.markdown('<h3 class="section-title">MVP Notes</h3>', unsafe_allow_html=True)
    st.write(
        "This app now uses the Preston Hire quick reference guide as the working source. It does not calculate outrigger point loading."
    )
    st.write(
        "The range chart uses crane-specific capacity points from the supplied chart material. "
        "Always confirm the exact manufacturer load chart, boom configuration, hook height, falls, ground conditions, and lift plan before use."
    )

st.write("")
st.markdown(
    f"""
    <div style="background:{PH_BLACK};padding:15px;border-radius:8px;">
        <p style="color:{PH_YELLOW};margin:0;">PRESTON HIRE | Spider Crane Range Checker</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Deployment")
st.sidebar.code("streamlit run spider_crane_app.py")



import io
import math
import re
from pathlib import Path
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
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
    path = ASSET_DIR / f"{crane_name}.png"
    if path.exists() and path.stat().st_size > 12000:
        return path
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
    width, height = 1600, 1100
    image = Image.new("RGB", (width, height), "#EEF1F3")
    draw = ImageDraw.Draw(image)
    title_font = load_font(44, bold=True)
    h_font = load_font(28, bold=True)
    body_font = load_font(24)
    small_font = load_font(19)
    status_color = PH_RED if status == "RED ZONE" else PH_ORANGE if status == "CHECK ZONE" else PH_GREEN

    draw.rounded_rectangle((55, 45, width - 55, 150), radius=14, fill=PH_BLACK)
    draw.rectangle((55, 45, 72, 150), fill=PH_YELLOW)
    draw.text((95, 70), "PRESTON HIRE", font=title_font, fill=PH_YELLOW)
    draw.text((95, 118), f"{crane_name} Lift Plan", font=body_font, fill=PH_WHITE)

    draw.rounded_rectangle((55, 185, 510, 510), radius=12, fill="white", outline=PH_LINE, width=2)
    draw.ellipse((85, 218, 123, 256), fill=status_color)
    draw.text((140, 220), status, font=h_font, fill=PH_BLACK)
    y = 285
    required_rows = [
        ("Radius", f"{working_radius:.2f} m"),
        ("Load weight", f"{total_load:.0f} kg"),
        ("Boom length", f"{boom_length:.2f} m"),
        ("Hook height", f"{hook_height:.2f} m"),
        ("Outriggers", setup),
        ("Floor area", f"{floor_length:.2f} x {floor_width:.2f} m"),
        ("Estimated capacity", f"{allowed_load:.0f} kg"),
        ("Utilisation", f"{utilisation:.1f}%"),
    ]
    for label, value in required_rows:
        draw.text((90, y), label, font=small_font, fill=PH_MUTED)
        draw.text((300, y - 4), value, font=body_font, fill=PH_BLACK)
        y += 42

    draw.rounded_rectangle((545, 185, width - 55, 790), radius=12, fill="white", outline=PH_LINE, width=2)
    visual_path = chart_image_path(crane_name) or cad_image_path(crane_name)
    if visual_path:
        visual = Image.open(visual_path).convert("RGB")
        visual = ImageOps.contain(visual, (960, 545), method=Image.Resampling.LANCZOS)
        paste_x = 545 + (1000 - visual.width) // 2
        paste_y = 220 + (520 - visual.height) // 2
        image.paste(visual, (paste_x, paste_y))
        draw.rounded_rectangle((570, 205, 1045, 286), radius=10, fill=(255, 255, 255), outline=PH_LINE, width=2)
        draw.text((592, 222), f"Radius: {working_radius:.2f} m", font=body_font, fill=PH_BLACK)
        draw.text((592, 254), f"Load: {total_load:.0f} kg   Boom: {boom_length:.2f} m", font=body_font, fill=PH_BLACK)
        draw.text((570, 750), f"Reference image: {visual_path.name}", font=small_font, fill=PH_MUTED)
    else:
        draw.text((600, 460), "Reference image not available for this crane yet.", font=h_font, fill=PH_MUTED)

    draw.rounded_rectangle((55, 830, width - 55, 1010), radius=12, fill="white", outline=PH_LINE, width=2)
    draw.text((85, 860), "Range Parameters", font=h_font, fill=PH_BLACK)
    brochure_text = (
        f"{card['tagline']} Max radius {card['max_radius_m']:.2f} m. "
        f"Max boom length {card['boom_length_m']:.2f} m. "
        f"Min-radius capacity {card['capacity_min_radius']}. "
        f"Max-radius capacity {card['capacity_max_radius']}. "
        "This is a spider crane range check only; confirm the exact manufacturer load chart, configuration, ground conditions, and lift plan before site use."
    )
    draw_wrapped(draw, brochure_text, (85, 905), body_font, PH_BLACK, width - 170)

    buffer = io.BytesIO()
    image.save(buffer, format="PDF", resolution=150.0)
    return buffer.getvalue()


def create_lift_drawing_svg(crane_name, card, working_radius, boom_length, hook_height, total_load, allowed_load, status, setup, floor_length, floor_width):
    max_span = max(card["max_radius_m"], boom_length, working_radius, 1)
    scale = 555 / max_span
    base_x = 96
    ground_y = 392
    radius_x = base_x + working_radius * scale
    boom_angle = math.atan2(max(hook_height, 0.5), max(working_radius, 0.5))
    boom_end_x = base_x + min(boom_length, max_span) * math.cos(boom_angle) * scale
    boom_end_y = ground_y - min(boom_length, max_span) * math.sin(boom_angle) * scale
    boom_end_y = max(72, min(ground_y - 32, boom_end_y))
    hook_x = radius_x
    hook_y = max(boom_end_y + 45, ground_y - hook_height * scale)
    hook_y = min(ground_y - 22, hook_y)
    status_color = PH_RED if status == "RED ZONE" else PH_ORANGE if status == "CHECK ZONE" else PH_GREEN

    def text(value):
        return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="560" viewBox="0 0 900 560">
  <style>
    .title {{ font: 700 24px Arial, sans-serif; fill: #F5D800; }}
    .white {{ font: 13px Arial, sans-serif; fill: #FFFFFF; }}
    .label {{ font: 700 15px Arial, sans-serif; fill: #1A1A1A; }}
    .small {{ font: 13px Arial, sans-serif; fill: #1A1A1A; }}
    .muted {{ font: 12px Arial, sans-serif; fill: #6B7280; }}
  </style>
  <rect width="900" height="560" fill="#EEF1F3"/>
  <rect x="28" y="22" width="844" height="70" rx="8" fill="#1A1A1A"/>
  <rect x="28" y="22" width="10" height="70" fill="#F5D800"/>
  <text x="55" y="52" class="title">PRESTON HIRE</text>
  <text x="55" y="76" class="white">{text(crane_name)} range sketch | Status: {text(status)}</text>

  <rect x="614" y="118" width="238" height="228" rx="8" fill="#FFFFFF" stroke="#D8DEE4"/>
  <circle cx="636" cy="143" r="9" fill="{status_color}"/>
  <text x="654" y="148" class="label">{text(status)}</text>
  <text x="630" y="184" class="small">Total load: {total_load:.0f} kg</text>
  <text x="630" y="208" class="small">Est. envelope: {allowed_load:.0f} kg</text>
  <text x="630" y="232" class="small">Radius: {working_radius:.2f} m</text>
  <text x="630" y="256" class="small">Boom length: {boom_length:.2f} m</text>
  <text x="630" y="280" class="small">Hook height: {hook_height:.2f} m</text>
  <text x="630" y="304" class="small">Outriggers: {text(setup)}</text>
  <text x="630" y="328" class="small">Floor: {floor_length:.2f} x {floor_width:.2f} m</text>

  <line x1="55" y1="{ground_y}" x2="805" y2="{ground_y}" stroke="#1A1A1A" stroke-width="3"/>
  <rect x="{base_x - 42}" y="{ground_y - 22}" width="84" height="22" rx="4" fill="#333"/>
  <circle cx="{base_x - 26}" cy="{ground_y + 4}" r="9" fill="#555"/>
  <circle cx="{base_x + 26}" cy="{ground_y + 4}" r="9" fill="#555"/>
  <line x1="{base_x - 62}" y1="{ground_y}" x2="{base_x - 112}" y2="{ground_y + 46}" stroke="#27AE60" stroke-width="8"/>
  <line x1="{base_x + 62}" y1="{ground_y}" x2="{base_x + 122}" y2="{ground_y + 46}" stroke="#27AE60" stroke-width="8"/>
  <rect x="{base_x - 128}" y="{ground_y + 40}" width="44" height="8" fill="#1A1A1A"/>
  <rect x="{base_x + 106}" y="{ground_y + 40}" width="44" height="8" fill="#1A1A1A"/>
  <line x1="{base_x}" y1="{ground_y - 20}" x2="{boom_end_x:.1f}" y2="{boom_end_y:.1f}" stroke="#27AE60" stroke-width="15" stroke-linecap="round"/>
  <line x1="{boom_end_x:.1f}" y1="{boom_end_y:.1f}" x2="{hook_x:.1f}" y2="{hook_y:.1f}" stroke="#1A1A1A" stroke-width="3"/>
  <circle cx="{hook_x:.1f}" cy="{hook_y:.1f}" r="10" fill="#E8400C"/>
  <path d="M {hook_x - 8:.1f} {hook_y + 8:.1f} q 8 18 16 0" fill="none" stroke="#1A1A1A" stroke-width="4"/>

  <line x1="{base_x}" y1="{ground_y + 70}" x2="{radius_x:.1f}" y2="{ground_y + 70}" stroke="#E8400C" stroke-width="3"/>
  <line x1="{base_x}" y1="{ground_y + 58}" x2="{base_x}" y2="{ground_y + 82}" stroke="#E8400C" stroke-width="3"/>
  <line x1="{radius_x:.1f}" y1="{ground_y + 58}" x2="{radius_x:.1f}" y2="{ground_y + 82}" stroke="#E8400C" stroke-width="3"/>
  <text x="{(base_x + radius_x) / 2 - 42:.1f}" y="{ground_y + 100}" class="label">Radius {working_radius:.2f} m</text>
  <text x="{boom_end_x - 48:.1f}" y="{boom_end_y - 14:.1f}" class="label">Boom {boom_length:.2f} m</text>
  <text x="{hook_x + 16:.1f}" y="{hook_y + 5:.1f}" class="label">Load {total_load:.0f} kg</text>

  <text x="55" y="520" class="muted">Spider crane range sketch only. Confirm manufacturer load chart, boom configuration, ground conditions, and lift plan before use.</text>
</svg>"""


def create_lift_drawing_html(svg):
    return f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>Spider Crane Range Sketch</title></head>
<body style="margin:0;background:#eef1f3;">{svg}</body>
</html>"""


def visual_preview_html(crane_name, working_radius, boom_length, total_load, status):
    path = chart_image_path(crane_name) or cad_image_path(crane_name)
    if not path:
        return create_lift_drawing_html(
            create_lift_drawing_svg(
                crane_name,
                FLEET_GUIDE[crane_name],
                working_radius,
                boom_length,
                0,
                total_load,
                0,
                status,
                "Max footprint",
                0,
                0,
            )
        )

    import base64

    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    color = PH_RED if status == "RED ZONE" else PH_ORANGE if status == "CHECK ZONE" else PH_GREEN
    return f"""<!doctype html>
<html>
<body style="margin:0;background:#eef1f3;font-family:Arial,sans-serif;">
  <div style="width:100%;height:560px;box-sizing:border-box;padding:18px;background:#eef1f3;">
    <div style="background:#1A1A1A;color:#F5D800;padding:14px 18px;border-radius:8px;font-weight:700;font-size:22px;">
      PRESTON HIRE | {crane_name} Lift Reference
    </div>
    <div style="position:relative;background:white;border:1px solid #D8DEE4;border-radius:8px;margin-top:14px;height:455px;overflow:hidden;">
      <img src="data:{mime};base64,{encoded}" style="width:100%;height:100%;object-fit:contain;">
      <div style="position:absolute;top:16px;left:16px;background:white;border:2px solid {color};border-radius:8px;padding:12px 16px;box-shadow:0 4px 18px rgba(0,0,0,.12);font-size:18px;">
        <div style="font-weight:700;color:{color};margin-bottom:6px;">{status}</div>
        <div>Radius: <strong>{working_radius:.2f} m</strong></div>
        <div>Load: <strong>{total_load:.0f} kg</strong></div>
        <div>Boom length: <strong>{boom_length:.2f} m</strong></div>
      </div>
    </div>
  </div>
</body>
</html>"""


def clean_slug(value):
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower()


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
drawing_svg = create_lift_drawing_svg(
    crane_name, card, working_radius, boom_length, hook_height, total_load, allowed_load, status, selected_setup, floor_length, floor_width
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
    st.markdown('<h3 class="section-title">Lift Drawing</h3>', unsafe_allow_html=True)
    components.html(visual_preview_html(crane_name, working_radius, boom_length, total_load, status), height=580, scrolling=False)
    d1, d2 = st.columns(2)
    filename_base = clean_slug(f"{crane_name}-lift-sketch")
    with d1:
        st.download_button(
            "Download Drawing SVG",
            drawing_svg.encode("utf-8"),
            f"{filename_base}.svg",
            "image/svg+xml",
            use_container_width=True,
            key="drawing_tab_svg",
        )
    with d2:
        st.download_button(
            "Download Drawing HTML",
            create_lift_drawing_html(drawing_svg).encode("utf-8"),
            f"{filename_base}.html",
            "text/html",
            use_container_width=True,
            key="drawing_tab_html",
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
        st.download_button(
            "Download Drawing SVG",
            drawing_svg.encode("utf-8"),
            f"{filename_base}.svg",
            "image/svg+xml",
            use_container_width=True,
            key="export_svg",
        )

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



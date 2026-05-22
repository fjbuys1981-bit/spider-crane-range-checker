# Preston Hire Spider Crane Calculator

Streamlit MVP for range suitability checking for Preston Hire spider cranes. It uses the Preston Hire quick-reference crane names for selection.

The app auto-selects the smallest suitable crane from entered load, radius, boom length, and hook height. It highlights RED ZONE when the entered lift is outside the range parameters.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run spider_crane_app.py
```

## Deploy On Streamlit

Upload these files to GitHub:

- `spider_crane_app.py`
- `cad_assets/`
- `requirements.txt`

When creating the Streamlit app, use:

- Main file path: `spider_crane_app.py`

## Notes

This MVP does not calculate outrigger point loads. It checks the entered load, radius, boom length, and hook height against the crane range and creates a PDF lift plan with radius, load weight, boom length, hook height, status, and the available CAD reference image.

It does not replace the crane manufacturer load chart or a temporary works review. Confirm the selected lift radius, hook height, boom stage, falls, rated capacity, ground conditions, and mat design before use on site.


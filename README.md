# BMI Calculator (Python Programming — Task 2, Advanced Tier)

**OASIS INFOBYTE Summer Internship Program**

A desktop GUI application (tkinter) that calculates Body Mass Index,
classifies it into standard health categories with colour-coded feedback,
stores historical records per user in SQLite, and plots a BMI trend chart.

## Features

- GUI built with tkinter (no command line)
- BMI formula: `BMI = weight (kg) / height (m)²`
- Standard classification: Underweight / Normal / Overweight / Obese
- Colour-coded result (blue / green / orange / red)
- Multi-user support — records saved per named user
- Historical records stored in a local SQLite database (`bmi_records.db`)
- "Show My BMI Trend" button plots a line chart (matplotlib) of a user's BMI
  over time (needs at least 2 saved records for that name)
- Input validation: rejects non-numeric or non-positive weight/height
- Error handling for database read/write failures

## Setup

```bash
pip install matplotlib
```

(`tkinter` and `sqlite3` ship with standard Python installs.)

## Run

```bash
python bmi_calculator.py
```

Enter a name, weight in kilograms, and height in metres, then click
**Calculate**. Calculate a few times for the same name (with slightly
different weights) to populate enough history to view the trend graph.

## Notes

- The SQLite database file `bmi_records.db` is created automatically in the
  same folder on first run.
- BMI categories used: Underweight (<18.5), Normal (18.5–24.9), Overweight
  (25–29.9), Obese (≥30) — standard WHO classification.

## Self-sourcing references used

- YouTube: "Python tkinter GUI tutorial beginners"
- YouTube: "Python matplotlib line chart tutorial"
- Official tkinter docs (docs.python.org)
- "Python sqlite3 tutorial CRUD"

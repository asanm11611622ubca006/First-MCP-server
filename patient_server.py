"""
Patient Data MCP Server
========================
An MCP server that exposes tools for querying a patient dataset.
Connect this to Claude Desktop to query patients using natural language.

Run:  uv run patient_server.py
"""

import csv
import os
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Initialise the MCP server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "Patient Data Server",
    instructions=(
        "You are connected to a patient database with ~200 records. "
        "Each patient has: patient_id, name, age, gender, and disease. "
        "Use the available tools to look up, filter, and summarise patient data."
    ),
)

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patients.csv")


def _load_patients() -> list[dict]:
    """Load patients from the CSV file and return as a list of dicts."""
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        patients = []
        for row in reader:
            row["patient_id"] = int(row["patient_id"])
            row["age"] = int(row["age"])
            patients.append(row)
    return patients


def _format_patient(p: dict) -> str:
    """Format a single patient record as a readable string."""
    return (
        f"ID: {p['patient_id']} | Name: {p['name']} | "
        f"Age: {p['age']} | Gender: {p['gender']} | Disease: {p['disease']}"
    )


def _format_patients(patients: list[dict]) -> str:
    """Format a list of patient records, with a count header."""
    if not patients:
        return "No patients found matching the criteria."
    header = f"Found {len(patients)} patient(s):\n"
    rows = "\n".join(_format_patient(p) for p in patients)
    return header + rows


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------


@mcp.tool(structured_output=False)
def get_patient_by_id(patient_id: int) -> str:
    """
    Look up a single patient by their unique patient ID.

    Args:
        patient_id: The numeric ID of the patient (e.g. 1, 42, 200).

    Returns:
        The patient record, or a "not found" message.
    """
    patients = _load_patients()
    for p in patients:
        if p["patient_id"] == patient_id:
            return _format_patient(p)
    return f"No patient found with ID {patient_id}."


@mcp.tool(structured_output=False)
def list_patients_above_age(age: int) -> str:
    """
    List all patients whose age is strictly greater than the given value.

    Args:
        age: The age threshold. Returns patients older than this number.

    Returns:
        A formatted list of matching patients, or a message if none match.
    """
    patients = _load_patients()
    results = [p for p in patients if p["age"] > age]
    results.sort(key=lambda p: p["age"], reverse=True)
    return _format_patients(results)


@mcp.tool(structured_output=False)
def find_patients_by_disease(disease: str) -> str:
    """
    Find all patients diagnosed with a specific disease.
    The search is case-insensitive.

    Args:
        disease: The disease name to search for (e.g. "Diabetes", "asthma").

    Returns:
        A formatted list of matching patients.
    """
    patients = _load_patients()
    disease_lower = disease.lower()
    results = [p for p in patients if p["disease"].lower() == disease_lower]
    results.sort(key=lambda p: p["name"])
    return _format_patients(results)


@mcp.tool(structured_output=False)
def list_all_diseases() -> str:
    """
    List all unique diseases present in the patient dataset.
    Useful for discovering what diseases can be queried.

    Returns:
        A sorted list of disease names.
    """
    patients = _load_patients()
    diseases = sorted(set(p["disease"] for p in patients))
    return f"Diseases in the dataset ({len(diseases)}):\n" + "\n".join(
        f"  • {d}" for d in diseases
    )


@mcp.tool(structured_output=False)
def search_patients_by_name(name: str) -> str:
    """
    Search for patients whose name contains the given text.
    The search is case-insensitive and supports partial matches.

    Args:
        name: Full or partial patient name to search for (e.g. "john", "Smith").

    Returns:
        A formatted list of matching patients.
    """
    patients = _load_patients()
    name_lower = name.lower()
    results = [p for p in patients if name_lower in p["name"].lower()]
    results.sort(key=lambda p: p["name"])
    return _format_patients(results)


@mcp.tool(structured_output=False)
def get_patient_statistics() -> str:
    """
    Get summary statistics for the entire patient dataset.
    Includes total count, age statistics, gender breakdown,
    and disease distribution.

    Returns:
        A formatted statistical summary.
    """
    patients = _load_patients()

    total = len(patients)
    ages = [p["age"] for p in patients]
    avg_age = sum(ages) / total if total else 0
    min_age = min(ages) if ages else 0
    max_age = max(ages) if ages else 0

    # Gender breakdown
    gender_counts: dict[str, int] = {}
    for p in patients:
        gender_counts[p["gender"]] = gender_counts.get(p["gender"], 0) + 1

    # Disease distribution
    disease_counts: dict[str, int] = {}
    for p in patients:
        disease_counts[p["disease"]] = disease_counts.get(p["disease"], 0) + 1

    lines = [
        f"📊 Patient Dataset Statistics",
        f"{'─' * 40}",
        f"Total patients: {total}",
        f"",
        f"Age Statistics:",
        f"  Average age: {avg_age:.1f}",
        f"  Youngest:    {min_age}",
        f"  Oldest:      {max_age}",
        f"",
        f"Gender Breakdown:",
    ]
    for g, c in sorted(gender_counts.items()):
        pct = (c / total * 100) if total else 0
        lines.append(f"  {g}: {c} ({pct:.1f}%)")

    lines.append("")
    lines.append("Disease Distribution:")
    for d, c in sorted(disease_counts.items(), key=lambda x: -x[1]):
        pct = (c / total * 100) if total else 0
        lines.append(f"  {d}: {c} ({pct:.1f}%)")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")

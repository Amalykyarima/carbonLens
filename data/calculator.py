import pandas as pd
from data.materials import MATERIALS


def calculate_project(items: list[dict]) -> pd.DataFrame:
    """
    items: [{"material": str, "quantity": float, "element": str}, ...]
    Returns a DataFrame with carbon, cost, and ratio columns.
    """
    rows = []
    for item in items:
        mat = MATERIALS.get(item["material"])
        if not mat:
            continue

        qty = item["quantity"]
        element = item.get("element", item["material"])
        unit = mat["unit"]

        # Carbon calculation
        if unit in ("m³", "m²"):
            if unit == "m³":
                mass_kg = qty * mat["density_kg_m3"]
            else:
                # For m² materials use a nominal 10mm thickness for mass estimate
                mass_kg = qty * mat.get("density_kg_m3", 2000) * 0.01
        else:  # tonne
            mass_kg = qty * 1000

        carbon_kgco2e = mass_kg * mat["carbon_factor"]

        # Cost calculation
        if unit == "m³":
            cost_gbp = qty * mat.get("cost_per_m3", 0)
        elif unit == "m²":
            cost_gbp = qty * mat.get("cost_per_m2", 0)
        else:  # tonne
            cost_gbp = qty * mat.get("cost_per_tonne", 0)

        rows.append({
            "Element": element,
            "Material": item["material"],
            "Category": mat["category"],
            "Quantity": qty,
            "Unit": unit,
            "Carbon (kgCO₂e)": round(carbon_kgco2e, 1),
            "Cost (£)": round(cost_gbp, 2),
            "Carbon factor": mat["carbon_factor"],
            "Carbon/£ ratio": round(carbon_kgco2e / cost_gbp, 4) if cost_gbp > 0 else 0,
        })

    return pd.DataFrame(rows)


def get_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    total_carbon = df["Carbon (kgCO₂e)"].sum()
    total_cost = df["Cost (£)"].sum()
    highest_carbon = df.loc[df["Carbon (kgCO₂e)"].idxmax(), "Element"]
    best_ratio = df.loc[df["Carbon/£ ratio"].idxmin(), "Element"] if (df["Carbon/£ ratio"] > 0).any() else "N/A"
    return {
        "total_carbon": round(total_carbon, 1),
        "total_cost": round(total_cost, 2),
        "highest_carbon_element": highest_carbon,
        "best_value_element": best_ratio,
        "num_elements": len(df),
        "avg_carbon_per_gbp": round(total_carbon / total_cost, 4) if total_cost > 0 else 0,
    }


def build_context_for_ai(df: pd.DataFrame, summary: dict) -> str:
    if df.empty:
        return "No project data has been entered yet."
    lines = [
        "## Current project data",
        f"- Total embodied carbon: {summary['total_carbon']:,} kgCO₂e",
        f"- Total estimated cost: £{summary['total_cost']:,.2f}",
        f"- Number of elements: {summary['num_elements']}",
        f"- Highest carbon element: {summary['highest_carbon_element']}",
        "",
        "### Element breakdown:",
    ]
    for _, row in df.iterrows():
        lines.append(
            f"- {row['Element']} ({row['Material']}): "
            f"{row['Carbon (kgCO₂e)']:,} kgCO₂e, £{row['Cost (£)']:,.2f}, "
            f"{row['Quantity']} {row['Unit']}"
        )
    return "\n".join(lines)

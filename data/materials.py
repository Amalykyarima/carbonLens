
# Embodied carbon values from ICE Database v3.0 (University of Bath)
# kgCO2e per kg of material | cost_per_unit in £ | unit = measurement basis

MATERIALS = {
    # ── Concrete & Masonry ──────────────────────────────────────────────────
    "Concrete (general)": {
        "category": "Concrete & Masonry",
        "carbon_factor": 0.103,   # kgCO2e/kg
        "density_kg_m3": 2400,
        "cost_per_m3": 110,
        "unit": "m³",
        "description": "General-purpose ready-mix concrete"
    },
    "Concrete (high-strength)": {
        "category": "Concrete & Masonry",
        "carbon_factor": 0.172,
        "density_kg_m3": 2450,
        "cost_per_m3": 145,
        "unit": "m³",
        "description": "C40+ high-strength structural concrete"
    },
    "Precast concrete": {
        "category": "Concrete & Masonry",
        "carbon_factor": 0.135,
        "density_kg_m3": 2400,
        "cost_per_m3": 180,
        "unit": "m³",
        "description": "Factory-produced precast concrete elements"
    },
    "Brick (clay)": {
        "category": "Concrete & Masonry",
        "carbon_factor": 0.213,
        "density_kg_m3": 1800,
        "cost_per_m3": 260,
        "unit": "m³",
        "description": "Fired clay brickwork"
    },
    "Concrete block": {
        "category": "Concrete & Masonry",
        "carbon_factor": 0.093,
        "density_kg_m3": 2000,
        "cost_per_m3": 130,
        "unit": "m³",
        "description": "Dense aggregate concrete blockwork"
    },

    # ── Steel ───────────────────────────────────────────────────────────────
    "Structural steel (virgin)": {
        "category": "Steel & Metals",
        "carbon_factor": 2.46,
        "density_kg_m3": 7850,
        "cost_per_tonne": 1100,
        "unit": "tonne",
        "description": "Primary structural steel sections"
    },
    "Structural steel (recycled)": {
        "category": "Steel & Metals",
        "carbon_factor": 0.44,
        "density_kg_m3": 7850,
        "cost_per_tonne": 950,
        "unit": "tonne",
        "description": "EAF recycled structural steel"
    },
    "Reinforcement bar (rebar)": {
        "category": "Steel & Metals",
        "carbon_factor": 1.99,
        "density_kg_m3": 7850,
        "cost_per_tonne": 850,
        "unit": "tonne",
        "description": "Steel reinforcement for concrete"
    },
    "Aluminium (virgin)": {
        "category": "Steel & Metals",
        "carbon_factor": 11.46,
        "density_kg_m3": 2700,
        "cost_per_tonne": 2400,
        "unit": "tonne",
        "description": "Primary aluminium — high embodied carbon"
    },
    "Aluminium (recycled)": {
        "category": "Steel & Metals",
        "carbon_factor": 1.69,
        "density_kg_m3": 2700,
        "cost_per_tonne": 2000,
        "unit": "tonne",
        "description": "Secondary recycled aluminium"
    },

    # ── Timber ──────────────────────────────────────────────────────────────
    "Glulam timber": {
        "category": "Timber",
        "carbon_factor": 0.51,
        "density_kg_m3": 500,
        "cost_per_m3": 1200,
        "unit": "m³",
        "description": "Glued laminated structural timber"
    },
    "CLT (Cross-Laminated Timber)": {
        "category": "Timber",
        "carbon_factor": 0.44,
        "density_kg_m3": 480,
        "cost_per_m3": 1500,
        "unit": "m³",
        "description": "Mass timber — carbon sequestration benefit"
    },
    "Softwood (sawn)": {
        "category": "Timber",
        "carbon_factor": 0.26,
        "density_kg_m3": 450,
        "cost_per_m3": 400,
        "unit": "m³",
        "description": "General sawn softwood framing"
    },
    "Engineered timber (LVL)": {
        "category": "Timber",
        "carbon_factor": 0.48,
        "density_kg_m3": 510,
        "cost_per_m3": 900,
        "unit": "m³",
        "description": "Laminated veneer lumber"
    },

    # ── Insulation ──────────────────────────────────────────────────────────
    "Mineral wool": {
        "category": "Insulation",
        "carbon_factor": 1.28,
        "density_kg_m3": 25,
        "cost_per_m3": 18,
        "unit": "m³",
        "description": "Rockwool/glasswool insulation"
    },
    "EPS (expanded polystyrene)": {
        "category": "Insulation",
        "carbon_factor": 3.29,
        "density_kg_m3": 20,
        "cost_per_m3": 12,
        "unit": "m³",
        "description": "Rigid board insulation"
    },
    "PIR insulation board": {
        "category": "Insulation",
        "carbon_factor": 3.43,
        "density_kg_m3": 32,
        "cost_per_m3": 22,
        "unit": "m³",
        "description": "Polyisocyanurate rigid insulation"
    },
    "Hemp insulation": {
        "category": "Insulation",
        "carbon_factor": 0.38,
        "density_kg_m3": 30,
        "cost_per_m3": 35,
        "unit": "m³",
        "description": "Natural fibre — low embodied carbon"
    },

    # ── Glass & Cladding ────────────────────────────────────────────────────
    "Float glass": {
        "category": "Glass & Cladding",
        "carbon_factor": 0.91,
        "density_kg_m3": 2500,
        "cost_per_m2": 55,
        "unit": "m²",
        "description": "Standard flat glass"
    },
    "Triple-glazed unit": {
        "category": "Glass & Cladding",
        "carbon_factor": 1.38,
        "density_kg_m3": 2500,
        "cost_per_m2": 180,
        "unit": "m²",
        "description": "High-performance triple glazing"
    },
    "Terracotta cladding": {
        "category": "Glass & Cladding",
        "carbon_factor": 0.68,
        "density_kg_m3": 1900,
        "cost_per_m2": 120,
        "unit": "m²",
        "description": "Fired clay rainscreen panels"
    },
}

CATEGORIES = sorted(set(m["category"] for m in MATERIALS.values()))

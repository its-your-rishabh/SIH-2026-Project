# ThermoShelter AI (SIH26051)

An interactive thermodynamic solver and real-time 3D shelter visualization dashboard developed for Smart India Hackathon 2026.

## 📌 Project Overview
ThermoShelter AI dynamically calculates heat transfer dynamics and models insulation requirements for extreme-weather defense shelters.

* **Team Name:** Team Agnit (Team45)
* **Team Leader:** Mantosh Kumar Chaudhary
* **Team Members:** Mohd Tokeer Raza, Meenakshi Pandey, Neha, Krishna Gupta, Rishabh Upadhyay

---

## 🧮 Thermodynamic Formulation

$$U = \frac{k}{d}$$

$$Q = U \cdot A \cdot \Delta T$$

Where:
* $U$ = Thermal Transmittance ($\text{W/m}^2\text{K}$)
* $k$ = Thermal Conductivity ($0.04 \text{ W/mK}$)
* $d$ = Insulation Layer Thickness ($\text{m}$)
* $A$ = Surface Area ($48 \text{ m}^2$)
* $\Delta T$ = Temperature Difference ($T_{\text{indoor}} - T_{\text{outdoor}}$)

---

## 🚀 How to Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

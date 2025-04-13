import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import platform

# This must come before any other Streamlit command
# This must come before any other Streamlit command
st.set_page_config(page_title="CEM Heat Exchanger Analysis", layout="wide", page_icon="🔥")
# ==== Secure Key Access ====
API_KEY = "M_A_K_1995"  # Change this in production
user_key = st.sidebar.text_input("Enter API Key:", type="password")

if user_key != API_KEY:
    st.sidebar.error("Unauthorized access. Please enter a valid API Key.")
    st.stop()
# === Sound Support ===
if platform.system() == "Windows":
    import winsound
    def play_warning_sound():
        winsound.Beep(1000, 500)
else:
    def play_warning_sound():
        st.write("🔔 Warning sound (non-Windows system)")

# === Shared Input Sidebar ===
st.sidebar.header("📥 Global Input Parameters")
D = st.sidebar.number_input("Tube Outside Diameter (m)", value=0.025, step=0.001)
t = st.sidebar.number_input("Tube Thickness (m)", value=0.002, step=0.0001)
L = st.sidebar.number_input("Tube Length (m)", value=1.0, step=0.1)
rho_material = st.sidebar.number_input("Tube Material Density (kg/m³)", value=7850.0)
E = st.sidebar.number_input("Modulus of Elasticity (Pa)", value=2.1e11, format="%.2e")
fluid_velocity = st.sidebar.number_input("Fluid Velocity (m/s)", value=2.0)
fluid_density = st.sidebar.number_input("Fluid Density (kg/m³)", value=1000.0)
fluid_viscosity = st.sidebar.number_input("Fluid Viscosity (Pa.s)", value=0.001)

# === Tabs ===
tabs = st.tabs([
    "Natural Frequency",
    "Reynolds Number",
    "Vortex Shedding",
    "Turbulent Buffeting",
    "Acoustic Resonance",
    "Fluid Elastic Instability",
    "FIV Damage Effects",
    "Download Results"
])

results = {}

# === TAB 1: Natural Frequency ===
with tabs[0]:
    st.header(" Natural Frequency")
    I = (np.pi / 64) * (D**4 - (D - 2*t)**4)
    m = rho_material * (np.pi * (D**2 - (D - 2*t)**2)) / 4
    f_n = (1 / (2 * np.pi)) * np.sqrt(E * I / (m * L**2))
    results["Natural Frequency"] = f"{f_n:.2f} Hz"
    st.success(f"Natural Frequency: {f_n:.2f} Hz")

# === TAB 2: Reynolds Number ===
with tabs[1]:
    st.header(" Reynolds Number")
    Re = (fluid_velocity * D * fluid_density) / fluid_viscosity
    results["Reynolds Number"] = f"{Re:.2f}"
    st.success(f"Reynolds Number: {Re:.2f}")

# === TAB 3: Vortex Shedding ===
with tabs[2]:
    st.header("Vortex Shedding")
    St = 0.2
    shedding_freq = (St * fluid_velocity) / D
    results["Vortex Shedding Frequency"] = f"{shedding_freq:.2f} Hz"
    st.success(f"Vortex Shedding Frequency: {shedding_freq:.2f} Hz")

# === TAB 4: Turbulent Buffeting ===
with tabs[3]:
    st.header("Turbulent Buffeting")
    turbulence_intensity = 0.1
    buffeting_effect = fluid_velocity * D * turbulence_intensity
    results["Turbulent Buffeting Effect"] = f"{buffeting_effect:.2f} N"
    st.success(f"Turbulent Buffeting Effect: {buffeting_effect:.2f} N")

# === TAB 5: Acoustic Resonance ===
with tabs[4]:
    st.header(" Acoustic Resonance in Shell and Tube Heat Exchanger")

    st.subheader("1. Fluid Properties")
    gamma = st.number_input("Heat Capacity Ratio (γ)", value=1.4, min_value=1.0)
    R = st.number_input("Specific Gas Constant R (J/kg·K)", value=287.0)
    T = st.number_input("Temperature (K)", value=300.0)
    speed_of_sound = np.sqrt(gamma * R * T)
    st.success(f"✅ Calculated Speed of Sound: **{speed_of_sound:.2f} m/s**")

    st.subheader("2. Heat Exchanger Info")
    heat_exchanger_type = st.selectbox("Heat Exchanger Type", ["Shell and Tube", "Double Pipe", "Plate Type"])
    make = st.text_input("Heat Exchanger Make")

    st.subheader("3. Geometry & Pitch")
    length_shell = st.number_input("Shell Length (m)", min_value=0.1, value=1.0)
    pitch_type = st.selectbox("Tube Pitch Type", ["Square", "Triangular"])
    tube_pitch = st.number_input("Tube Pitch (m)", min_value=0.001, value=0.025)
    K = 1.0 if pitch_type == "Square" else 1.15

    f_axial = speed_of_sound / (2 * length_shell)
    f_angular = (speed_of_sound * K) / (2 * np.pi * tube_pitch)

    st.write(f" **Axial Resonance Frequency:** {f_axial:.2f} Hz")
    st.write(f"**Angular Resonance Frequency:** {f_angular:.2f} Hz")

    st.caption("Note: Axial resonance is based on shell length. Angular resonance depends on pitch type and layout.")
    results["Axial Resonance"] = f"{f_axial:.2f} Hz"
    results["Angular Resonance"] = f"{f_angular:.2f} Hz"

# === TAB 6: Fluid Elastic Instability ===
with tabs[5]:
    st.header(" Fluid Elastic Instability")
    instability_factor = fluid_velocity * D
    results["Fluid Elastic Instability Factor"] = f"{instability_factor:.2f}"
    st.success(f"Fluid Elastic Instability Factor: {instability_factor:.2f}")

# === TAB 7: FIV Damage Effects ===
with tabs[6]:
    st.header("⚠️ FIV Damage Effects")
    d_inner = D - 2 * t
    A_cs = np.pi * (D**2 - d_inner**2) / 4
    V = A_cs * L
    mass = V * rho_material
    I = (np.pi / 64) * (D**4 - d_inner**4)
    stiffness = (3 * E * I) / (L ** 3)
    F_amp = 0.5 * fluid_density * fluid_velocity**2 * D
    damping_ratio = 0.02
    fn = np.sqrt(stiffness / mass)
    omega = fn
    time = np.linspace(0, 5, 1000)
    fluid_force = F_amp * np.sin(omega * time)
    displacement = (F_amp / stiffness) * np.exp(-damping_ratio * omega * time) * np.sin(omega * time)

    max_disp = np.max(displacement)
    wear_events = np.sum(np.abs(displacement) > 0.008)
    collision_threshold = 0.01
    noise_level_db = 90 if max_disp > 0.012 else 60
    pressure_drop = 15 if wear_events > 100 else 5
    scc_risk = "High" if wear_events > 150 else "Low"

    results.update({
        "Tube Mass": f"{mass:.3f} kg",
        "Tube Stiffness": f"{stiffness:.1f} N/m",
        "Fluid Force Amplitude": f"{F_amp:.2f} N",
        "Natural Frequency (rad/s)": f"{fn:.2f}",
        "Max Displacement": f"{max_disp:.4f} m",
        "Mid-span Collision Risk": "YES" if max_disp > collision_threshold else "NO",
        "Wear Contact Events": str(wear_events),
        "Noise Level": f"{noise_level_db} dB",
        "Pressure Drop": f"{pressure_drop} kPa",
        "Stress Corrosion Cracking Risk": scc_risk
    })

    st.success(f"Max Displacement: {max_disp:.4f} m")

    fig, ax = plt.subplots()
    ax.plot(time, displacement)
    ax.set_title("Tube Vibration Response")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Displacement (m)")
    ax.grid(True)
    st.pyplot(fig)

    from io import BytesIO
    buf = BytesIO()
    fig.savefig(buf, format="PDF")
    st.download_button("📥 Download Graph as PNG", buf.getvalue(), file_name="vibration_response.png", mime="image/png")

    if max_disp > collision_threshold:
        play_warning_sound()

# === TAB 8: Final Summary ===
with tabs[7]:
    st.header("📄 Download Final Report")
    result_text = "\n".join([f"{k}: {v}" for k, v in results.items()])
    st.text_area("🔎 Full Summary", result_text, height=300)
    st.download_button("📥 Download Results as PDF", result_text, file_name="final_results.txt", mime="text/plain")

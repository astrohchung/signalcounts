import streamlit as st
import numpy as np

# Constants
PLANCK_ERG_S = 6.62607015e-27  # erg·s
LIGHT_CM_S = 2.99792458e10     # cm/s
RAD_TO_ARCSEC = 180 * 3600 / np.pi

st.set_page_config(
    page_title="Signal Count Calculator",
    # page_icon="./eos_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔭 Signal Count Calculator")
st.markdown("[https://signalcounts.astrohchung.com](https://signalcounts.astrohchung.com)")

st.sidebar.markdown("[https://signalcounts.astrohchung.com](https://signalcounts.astrohchung.com)")

# --- Sidebar Inputs ---
st.sidebar.header("Input Parameters")

source_type = st.sidebar.radio("Select Source Type", ["Extended Source", "Point Source"])

if source_type == "Point Source":
    flux = st.sidebar.number_input("Flux (erg/s/cm²)", min_value=0.0, value=1e-15, format="%.2e")
else:
    surface_brightness = st.sidebar.number_input("Surface Brightness (erg/s/cm²/arcsec²)", min_value=0.0, value=1e-19, format="%.2e")

wavelength_nm = st.sidebar.number_input("Wavelength (nm)", min_value=90.0, max_value=4000.0, value=121.6)
exposure_sec = st.sidebar.number_input("Exposure Time (sec)", min_value=0.0, value=36000.0)
diameter_cm = st.sidebar.number_input("Telescope Diameter (cm)", min_value=0.0, value=900.0)
f_ratio = st.sidebar.number_input("Telescope F-ratio", min_value=0.0, value=19.0)
res_x = st.sidebar.number_input("Resolution Element X (pixels)", min_value=1, value=1, step=1)
res_y = st.sidebar.number_input("Resolution Element Y (pixels)", min_value=1, value=2, step=1)
pixel_size_um = st.sidebar.number_input("Pixel Size (µm)", min_value=0.0, value=100.0)
throughput_percent = st.sidebar.number_input("Throughput (%)", min_value=0.0, max_value=100.0, value=5.0)

# --- Calculations ---
# Convert units
wavelength_cm = wavelength_nm * 1e-7
pixel_size_mm = pixel_size_um * 1e-3
throughput_frac = throughput_percent / 100.0

# Photon energy in erg
photon_energy = PLANCK_ERG_S * LIGHT_CM_S / wavelength_cm

# Effective collecting area
radius_cm = diameter_cm / 2.0
area_cm2 = np.pi * radius_cm**2
a_eff = area_cm2 * throughput_frac

# Field of view and flux input
if source_type == "Point Source":
    fov_arcsec2 = 1.0
    flux_input = flux
else:
    focal_length_mm = diameter_cm * f_ratio * 10  # in mm
    arcsec_per_mm = (1 / focal_length_mm) * RAD_TO_ARCSEC
    arcsec_per_pixel = arcsec_per_mm * pixel_size_mm
    arcsec_per_res_x = arcsec_per_pixel * res_x
    arcsec_per_res_y = arcsec_per_pixel * res_y
    pixel_area_mm2 = res_x * res_y * pixel_size_mm**2
    fov_arcsec2 = (arcsec_per_mm**2) * pixel_area_mm2
    flux_input = surface_brightness

# Signal counts
signal_counts = flux_input / photon_energy * exposure_sec * a_eff * fov_arcsec2

# Exposure time formatting
days = int(exposure_sec // 86400)
hours = int((exposure_sec % 86400) // 3600)
seconds = int(exposure_sec % 3600)

# --- Output ---
st.markdown("## 📊 Results")

# Signal counts always at the top
st.metric(label="🔹 Signal Counts", value=f"{signal_counts:.1f} photons")

# Optional outputs
st.write(f"**Photon Energy:** {photon_energy:.3e} erg")
st.write(f"**Effective Area (A_eff):** {a_eff:.3f} cm²")

if source_type == "Extended Source":
    st.write(f"**Arcsec per Pixel:** {arcsec_per_pixel:.3f} arcsec/pixel")
    st.write(f"**Arcsec per Resolution Element X:** {arcsec_per_res_x:.3f} arcsec")
    st.write(f"**Arcsec per Resolution Element Y:** {arcsec_per_res_y:.3f} arcsec")
    st.write(f"**Field of View:** {fov_arcsec2:.3f} arcsec²")

# Exposure breakdown
time_str = ""
if days > 0:
    time_str += f"{days} days "
if hours > 0:
    time_str += f"{hours} hours "
time_str += f"{seconds} seconds"
st.write(f"**Exposure Time:** {time_str}")


st.write("By default, this calculator estimates signal counts from a diffuse source at around Lyman alpha, per single HWO EAC5 MOS shutter.")
st.write("Note that this is only signal counts. No other noise included.")
st.write("Target diffuse emission line sensitivity is set as 1e-19 erg/s/cm²/arcsec².")
st.write("Default numbers from HWO EAC5: F/#=19, focal length = 171 m. -> Sets diameter as 900 mm in this calculator")
st.write("Also from HWO EAC5: Single UV MSA shutter size is 100 um x 200 um")
st.write("-> For the signal count calculation purpose, pixel size of 100 micron with resolution element pixel numbers as 1 and 2 for X and Y is used.")
st.write("Optimistic throughput of 5\% is assumed here, which makes effective area size as ~30,000 cm²")
st.write("To check the counts with shutter binning, increase the X or Y pixel numbers. This is euivalent to sacrifice spectral resolution or spatial resolution accordingly.")



st.sidebar.markdown("#### Revisions")
st.sidebar.markdown("Aug. 4, 2025: Signal Count Calculator is released.  Haeun Chung")

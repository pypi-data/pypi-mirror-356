# NautiloPy: An open-source Python framework for the Gironda Underwater Cave Sonar And vision data set
**Authors:** Thomas Guilment, Gabriele Morra, Leonardo Macelloni, and Marco D'Emidio

![](./img/Logo_nautilopy_tiny_v2.png)

## Run the Project

### 1. Install UV

This project uses [UV](https://docs.astral.sh/uv/) for dependency management and environment setup.

- **Linux/Mac OS**  
  Use `curl` or `wget` to download and execute the script:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  or
  ```bash
  wget -qO- https://astral.sh/uv/install.sh | sh
  ```

- **Windows**  
  Use PowerShell:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### 2. Run the Demonstration Notebook

After installing UV, download/clone this repository:
```bash
git clone https://github.com/20KUTS/nautilopy-uace2025.git
```

Then, open a shell/terminal/command prompt inside the folder and run:
```bash
uv run jupyter lab Nautilopy.ipynb
```
This will open Jupyter Lab with the `Nautilopy.ipynb` demonstration notebook.

## Project Overview

**Nautilopy** is a Python module for 3D underwater cave mapping using sonar technology. It provides tools and algorithms to:

- Process sonar data
- Generate 3D models of underwater cave systems
- Visualize data from the “[Underwater caves sonar and vision dataset](https://cirs.udg.edu/caves-dataset/)”

A demonstration notebook, `Nautilopy.ipynb`, is included to help you get started.

## Dataset Description

The dataset, provided by *Angelos Maillos et al. (2017)*, includes sensor data collected during an AUV mission in July 2013. Because of the caves’ spatial complexity, a diver guided the AUV. For this project, the original ROS bag data have been processed with [`bagpy`](https://jmscslgroup.github.io/bagpy/) to convert the ROS messages into CSV files.

### Sensor Suite

- **Two mechanically scanned imaging sonars (MSIS)**
- **Doppler velocity log (DVL)**
- **Two inertial measurement units (IMUs)**
- **Depth sensor**
- **Vertically mounted camera** (for ground truth validation)

### Available Data Topics (from CSV)

1. `/depth_sensor` &nbsp;— DS2806 HPS-A pressure sensor data  
2. `/dvl_linkquest` &nbsp;— LinkQuest NavQuest 600 sensor data  
3. `/imu_adis` &nbsp;— Analog Devices ADIS16480 sensor data  
4. `/imu_adis_ros` &nbsp;— ADIS16480 orientation in standard ROS format  
5. `/imu_xsens_mti` &nbsp;— Xsens MTi sensor data  
6. `/odometry` &nbsp;— Robot pose estimation  
7. `/sonar_micron` &nbsp;— Tritech Micron DST sensor beam data  
8. `/sonar_micron_ros` &nbsp;— Micron data in standard ROS `LaserScan` format  
9. `/sonar_seaking` &nbsp;— Tritech Super SeaKing DFP profiler sensor beam data  
10. `/tf` &nbsp;— Sensor offset transformations  

<!-- 
REMOVED (FILE TOO LARGE):
    11. /sonar_seaking_ros : Profiler data in standard ROS LaserScan format
    12. /imu_xsens_mti_ros: Xsens MTi orientation in standard ROS format
-->

## Sonar Specifications

| Specification                  | **Imaging sonar** <br>Tritech Micron DST | **Profiling sonar** <br>Tritech Super SeaKing DFP |
|:------------------------------:|:----------------------------------------:|:-------------------------------------------------:|
| **Frequency**                  | Chirped 650 to 750 kHz                   | 0.6 MHz \| 1.1 MHz                                |
| **Max range**                  | 75 m (20 m used)                         | 80 m \| 40 m (10 m used)                          |
| **Horizontal beamwidth**       | 3°                                       | 2° \| 1°                                          |
| **Vertical beamwidth**         | 35°                                      | 2° \| 1°                                          |
| **Scan rate (360° sector)**    | 5 − 20 sec                                | 4 − 25 sec                                        |

## Available Data in Python

During pre-processing, CSV sensor data are loaded, interpolated, and saved into Python-friendly formats. These variables are stored in a Pickle folder. The variables have the following new names:

### 1. Horizontal (Micron) Sonar Data
- `v_timestamp_micron`: Timestamps of Micron sonar  
- `m_beam_data_micron`: Beam intensity data (range vs. time)  
- `m_ypr_micron`: (Yaw, Pitch, Roll) over time  
- `m_xyz_pos_micron`: (x, y, z) Cartesian positions over time  
- `v_angles_rad_micron`: Scanning angles over time (radians)  
- `v_range_micron`: Range values (0 to 20 meters)  
- `v_offset_ypr_micron`: Yaw, Pitch, Roll offsets relative to AUV reference  
- `v_offset_xyz_pos_micron`: Position offsets relative to AUV reference  

### 2. Vertical (SeaKing) Sonar Data
- `v_timestamp_seaking`: Timestamps of SeaKing sonar  
- `m_beam_data_seaking`: Beam intensity data (range vs. time)  
- `m_ypr_seaking`: (Yaw, Pitch, Roll) over time  
- `m_xyz_pos_seaking`: (x, y, z) Cartesian positions over time  
- `v_angles_rad_seaking`: Scanning angles over time (radians)  
- `v_range_seaking`: Range values (0 to 20 meters)  
- `v_offset_ypr_seaking`: Yaw, Pitch, Roll offsets relative to AUV reference  
- `v_offset_xyz_pos_seaking`: Position offsets relative to AUV reference  

### 3. Other Processed Sensor Data
- `v_timestamp`: General timestamps (e.g., unified or reference timeline)  
- `v_timestamp_dvl`: Timestamps for DVL readings  
- `v_altitude_dvl`: Altitude from DVL  
- `m_xyz_velocity_dvl`: (x, y, z) velocity data from DVL  
- `v_timestamp_depth`: Timestamps for depth sensor  
- `v_depth`: Depth measurements  

### 4. Cleaned Beam Data
- `m_beam_data_micron_clean` / `m_beam_data_micron_clean_hyst`: Filtered or hysteresis-cleaned Micron sonar data  
- `m_beam_data_seaking_clean` / `m_beam_data_seaking_clean_hyst`: Filtered or hysteresis-cleaned SeaKing sonar data  

### 5. General AUV Position/Orientation
- `m_xyz_pos`: Overall 3D position estimates of the AUV  
- `m_ypr`: Overall yaw, pitch, roll estimates of the AUV  

## Current/Future Work

1. **Walls segmentation**  
   - Automatic extraction of cave walls from sonar and sensor data.  
   - Potential approach: annotation + AI/ML algorithms.

2. **3D confidence map**  
   - From wall segmentation, create an initial 3D map and assign confidence to each point.

3. **3D map extension**  
   - Interpolate or extrapolate the map to unmeasured areas.  
   - Assign a confidence level to interpolated points.

4. **Photogrammetry**  
   - Use video data combined with altitude estimations for 3D photogrammetry.  
   - Correlate visually detected features with the sonar-based 3D map.

5. **SLAM**  
   - Integrate SLAM for better localization and mapping accuracy.

6. **Real-time mapping & optimization**  
   - Eventually adapt the pipeline for real-time processing if SLAM and segmentation are reliable.

## Project Folder Architecture

Below is an example of the core folder layout when using this UV-based project:

```
project_root/
├── data/
├── img/
├── nautilopy/
├── 01_Preprocessing.ipynb
├── Nautilopy.ipynb
├── ROSbag2csv.ipynb
├── pyproject.toml
├── uv.lock
└── README.md
```
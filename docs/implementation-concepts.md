<!--
SPDX-FileCopyrightText: 2026 sint project contributors

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# sint — Implementation Concepts & Design Options

This document captures specific technical solutions, candidate architectures, and implementation ideas explored during the project. These are not rigid requirements but proposed paths to fulfill the [Project Specification](spec.md).

---

## 1. Kinematics & Actuation

### 1.1. Symmetric Walking Kinematics (Canadarm2/ERA Style)
- **Concept**: A symmetric arm with identical "wrists" and interfaces on both ends.
- **Advantages**: Natural "walking" between docking points; zero-G heritage.
- **Trade-offs**: Requires dual-purpose interfaces (acting as both base and EE mount); increased complexity in power/data routing.

### 1.2. Drive Systems
- **BLDC + FOC (Field Oriented Control)**:
    - **Candidate**: Using high-pole count BLDC motors (e.g., gimbal motors or drone motors) with controllers like SimpleFOC or ODrive.
    - **Goal**: Achieve ultra-quiet operation (>20kHz PWM) to allow clean audio diagnostics.
- **Gearbox Options**:
    - **3D Printed Cycloidal**: High reduction in a compact volume, but sensitive to printing tolerances.
    - **Planetary**: Easier to print and assemble, but higher backlash.
    - **Strain Wave (Harmonic)**: High precision, but difficult to implement purely with COTS/3D printing.

---

## 2. Interface & Docking Mechanisms

### 2.1. Base Anchor Docks (PDGF-style)
- **Mechanical**: Ball-screw latches or wedge-based locking for high rigidity.
- **Electrical**: Spring-loaded pogo pins or co-axial connectors for high-current power and high-speed data (Ethernet/USB3).

### 2.2. Universal Quick-Change EE Interface
- **Magnetic-Mechanical Hybrid**: Using permanent magnets for initial alignment and a motorized latch for rigid locking.
- **Pass-through**: Integrated 8-12 pin connector for I2C/CAN bus and power.

---

## 3. Sensing & Perception

### 3.1. Acoustic Diagnostics
- **Implementation**: MEMS microphone arrays integrated into joints or the wrist.
- **Processing**: Real-time FFT analysis on the LLM/VLA edge compute to detect mechanical anomalies or assembly state (e.g., "click" of a successful latch).

### 3.2. Tactile Sensing
- **Vision-based (GelSight style)**: Using a camera and a soft gel pad for high-resolution tactile maps.
- **Resistive/Capacitive Matrix**: Flexible PCB with pressure-sensitive material for basic force distribution.

---

## 4. Electronics & Compute

### 4.1. Edge Compute
- **Candidates**: NVIDIA Jetson Orin Nano, Raspberry Pi 5, or high-end ESP32/STM32 for real-time motor control.
- **Distribution**: Central "brain" in a link, or distributed micro-controllers per joint communicating via CAN-FD or RS485.

---

## 5. Candidate COTS Stack (Example)
- **Motors**: 2212 - 5208 BLDC Gimbal/Drone motors.
- **Drivers**: SimpleFOC Shield / BGC drivers.
- **Control**: ESP32-S3 or STM32G4.
- **Sensing**: IMU (MPU6050), Magnetic Encoders (AS5600/AS5048A).

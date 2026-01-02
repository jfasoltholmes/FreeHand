# FreeHand Overview:
FreeHand is a real-time hand tracking system using OpenCV and MediaPipe, designed to eventually control a motorized 3D-printed hand via Raspberry Pi.

## Project Status:
### Implemented - 
 - Real-time hand tracking using webcam input
 - Hand landmark detection via MediaPipe

### In progress - 
 - Mapping hand landmarks to motor control signals
 - Raspberry Pi integration
 - Motor driver and 3D-printed hand control

## Run Instructions:
### Prerequisites -
- Install [mise-en-place](https://mise.jdx.dev/) (manages project Python version)
- Install [uv](https://github.com/astral-sh/uv) (fast venv + dependency sync)
- A working built-in webcam

### Setup - 
#### 1. Clone the repo and enter it: 
```bash
git clone https://github.com/jfasoltholmes/FreeHand
cd FreeHand
```
#### 2. Install/use the project’s Python version:
```bash
mise install
mise use -g python@$(cat .python-version)  # optional if you want it global
```
*(If you already have mise configured, mise install is usually enough.)*

#### 3. Create the virtual environment + install deps from lockfile:
```bash
uv sync
```
#### 4. Run: 
```bash
uv run python main.py
```
#### Notes: 
 - Ensure hand_landmarker.task remains in the project root (or update the path in main.py).
 - Press q to quit the webcam window.
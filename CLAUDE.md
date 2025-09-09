# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<<<<<<< HEAD
## Common Development Commands

### Data Collection and Task Running
- **Collect data for a task**: `bash collect_data.sh ${task_name} ${task_config} ${gpu_id}`
  - Example: `bash collect_data.sh beat_block_hammer demo_randomized 0`
  - This runs the task with specified configuration and collects training data
  - GPU ID is required for CUDA device selection

### Policy Training and Evaluation
- **Run policy evaluation**: `python script/eval_policy.py`
- **Start policy model server**: `python script/policy_model_server.py`
- **Run policy client**: `python script/eval_policy_client.py`

### Environment Setup and Installation
- **Install dependencies**: `bash script/_install.sh`
- **Download assets**: `bash script/_download_assets.sh`
- **Update environment paths**: `bash script/.update_path.sh` (run automatically by collect_data.sh)

### Python Environment
- Install dependencies with: `pip install -r script/requirements.txt`
- Key dependencies: torch==2.4.1, sapien==3.0.0b1, gymnasium==0.29.1, transforms3d==0.4.2

## Code Architecture Overview

### Core Task Structure
- **Base Environment**: `envs/_base_task.py` contains the `Base_Task` class that all task environments inherit from
- **Task Environments**: Individual task implementations in `envs/` (e.g., `beat_block_hammer.py`, `handover_block.py`)
- **Global Configuration**: `envs/_GLOBAL_CONFIGS.py` defines paths, grasp directions, and coordinate systems

### Task Configuration System
- **Configuration Files**: Located in `task_config/` with YAML format
- **Template Configuration**: `task_config/_config_template.yml` shows available options
- **Demo Configurations**: `demo_clean.yml` and `demo_randomized.yml` for different data collection modes
- **Key Configuration Sections**:
  - `domain_randomization`: Controls environmental randomization (background, lighting, table height)
  - `camera`: Camera types and data collection settings
  - `data_type`: Specifies what data to collect (rgb, depth, pointcloud, endpose, qpos)
  - `embodiment`: Robot embodiment selection (e.g., aloha-agilex)

### Policy Framework
- **Policy Implementations**: Each policy type has its own directory under `policy/`
  - `ACT/`: Action Chunking with Transformers implementation
  - `DP/`: Diffusion Policy implementation
  - `DP3/`: 3D Diffusion Policy implementation
  - `RDT/`: Robotic Diffusion Transformer
  - `pi0/`: Pi0 policy implementation
  - `openvla-oft/`: OpenVLA with online fine-tuning
  - `TinyVLA/`, `DexVLA/`: Vision-Language-Action models
- **Policy Deployment**: Each policy directory contains `deploy_policy.py` for running trained models

### Data and Asset Management
- **Assets**: Robot embodiments and textures stored in `assets/`
- **Data Storage**: Training data saved to `data/` directory by default
- **Task Descriptions**: Human-readable task descriptions in `description/`
- **Contact Point Tracking**: 3D contact points and 2D projections to camera images
  - Enable with `contact_point: true` in config for 3D world coordinates
  - Enable with `contact_point_2d: true` in config for 2D image coordinates
  - See `demo_with_contact_points.yml` for example configuration

### Code Generation
- **LLM Task Generation**: `code_gen/` contains utilities for generating new tasks using LLMs
- **GPT Agent**: `code_gen/gpt_agent.py` interfaces with language models
- **Task Templates**: Automated task creation and code generation tools

### Key Coordinate Systems and Constants
- **Grasp Directions**: Predefined in `GRASP_DIRECTION_DIC` for consistent object manipulation
- **World Directions**: Standard coordinate transformations in `WORLD_DIRECTION_DIC`
- **Path Constants**: All major paths defined in `_GLOBAL_CONFIGS.py` for consistency

### Environment Features
- **Dual-Arm Support**: Built-in bimanual robot manipulation capabilities
- **Domain Randomization**: Extensive randomization options for lighting, background, table height
- **Multi-Camera Support**: Head and wrist camera configurations with various sensor types
- **Evaluation Modes**: Separate configuration for training vs evaluation data collection

## Development Guidelines

- Tasks inherit from `Base_Task` class and implement required abstract methods
- Configuration files use YAML format with clear section organization
- All file paths use the constants defined in `_GLOBAL_CONFIGS.py`
- Policy implementations follow a standard `deploy_policy.py` interface pattern
- Data collection respects the `save_freq` and `render_freq` parameters for performance
=======
## Repository Overview

RoboTwin is a bimanual robotic manipulation platform and benchmark suite featuring 50+ tasks with domain randomization capabilities. The repository contains:

- **Robotic environments and tasks** (`envs/`) - 50+ bimanual manipulation tasks with SAPIEN simulation
- **Policy implementations** (`policy/`) - Multiple policy frameworks including ACT, DP, DP3, RDT, PI0, TinyVLA, DexVLA, LLaVA-VLA, OpenVLA-OFT
- **Data collection and evaluation scripts** (`script/`) - Core functionality for data collection and policy evaluation
- **Task configurations** (`task_config/`) - YAML configs for different experimental setups
- **Code generation utilities** (`code_gen/`) - GPT-based task and observation code generation
- **Asset management** (`assets/`) - 3D models, textures, and embodiment definitions

## Core Commands

### Data Collection
```bash
# Collect data for a specific task
bash collect_data.sh <task_name> <task_config> <gpu_id>
# Example: bash collect_data.sh beat_block_hammer demo_randomized 0
```

### Policy Evaluation
```bash
# Evaluate policies (run from policy subdirectories)
cd policy/ACT && bash eval.sh <task_name> <task_config> <ckpt_setting> <expert_data_num> <seed> <gpu_id>
cd policy/DP && bash eval.sh <task_name> <task_config> <ckpt_setting> <expert_data_num> <seed> <gpu_id>
```

### Environment Setup
```bash
# Install dependencies
pip install -r script/requirements.txt

# Update system paths (called automatically by collect_data.sh)
./script/.update_path.sh
```

## Architecture Overview

### Task System
- **Base Task Class**: `envs/_base_task.py` - Core environment interface extending gymnasium.Env
- **Individual Tasks**: Each file in `envs/` implements a specific manipulation task (e.g., `beat_block_hammer.py`, `stack_blocks_two.py`)
- **Global Configurations**: `envs/_GLOBAL_CONFIGS.py` - Defines paths, grasp directions, and world coordinates
- **Utilities**: `envs/utils/` - Action processing, actor creation, camera configs, transforms

### Policy Framework
The repository supports multiple policy architectures, each in its own subdirectory under `policy/`:
- **ACT** - Action Chunking with Transformers
- **DP** - Diffusion Policy  
- **DP3** - 3D Diffusion Policy
- **RDT** - Robot Diffusion Transformer
- **PI0** - Policy model with JAX/Flax implementation
- **TinyVLA/DexVLA** - Vision-Language-Action models
- **LLaVA-VLA** - LLaVA-based VLA implementation
- **OpenVLA-OFT** - OpenVLA Online Fine-Tuning

Each policy directory contains:
- `deploy_policy.py` - Policy deployment interface
- `deploy_policy.yml` - Configuration for evaluation
- `eval.sh` - Evaluation script
- Policy-specific training and data processing scripts

### Configuration System
- **Task Configs** (`task_config/`): YAML files defining experimental parameters
  - `demo_randomized.yml` - Standard config with domain randomization
  - `demo_clean.yml` - Clean environment config
  - `_camera_config.yml` - Camera setup configurations
  - `_embodiment_config.yml` - Robot embodiment definitions

### Data Collection Pipeline
1. **Script Entry**: `collect_data.sh` calls `script/collect_data.py`
2. **Task Loading**: Dynamic import of task classes from `envs/` module
3. **Environment Setup**: Configuration loading, robot/camera initialization
4. **Data Generation**: Episode collection with domain randomization
5. **Storage**: HDF5 format in specified save directory

## Development Guidelines

### Adding New Tasks
1. Create new task file in `envs/` inheriting from `Base_Task`
2. Implement required methods: `_init_task_env_`, `reset`, `step`
3. Add task description in `description/task_instruction/`
4. Test with data collection: `bash collect_data.sh new_task demo_randomized 0`

### Adding New Policies
1. Create policy directory under `policy/`
2. Implement `deploy_policy.py` with standard interface
3. Create `deploy_policy.yml` configuration
4. Add `eval.sh` script following existing patterns
5. Document in policy-specific README if complex setup required

### Key File Locations
- **Main evaluation script**: `script/eval_policy.py`
- **Core environment utils**: `envs/utils/create_actor.py`, `envs/utils/action.py`
- **Robot control**: `envs/robot/robot.py`
- **Camera handling**: `envs/camera/camera.py`

### Development Environment
- **Python**: 3.8+ with PyTorch 2.4.1
- **Simulation**: SAPIEN 3.0.0b1 for physics simulation
- **GPU**: CUDA support required for training/evaluation
- **Dependencies**: See `script/requirements.txt` for full list

## Important Notes

- Tasks are dynamically loaded using importlib - ensure new tasks follow naming conventions
- Domain randomization is controlled via task config YAML files
- GPU memory management is critical due to SAPIEN rendering - use `clear_cache_freq` setting
- The platform supports multiple robot embodiments (Aloha, Agilex configurations)
- All evaluation scripts expect to run from their respective policy directories
- Data is stored in HDF5 format with RGB images, depth, point clouds, and action trajectories
>>>>>>> 01e25a4 (collect contact point traj)

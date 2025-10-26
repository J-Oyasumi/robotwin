# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

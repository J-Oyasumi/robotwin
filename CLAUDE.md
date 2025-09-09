# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
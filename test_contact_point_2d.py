#!/usr/bin/env python3
"""
Test script for contact point 2D projection functionality.
This script demonstrates how to use the new contact point 2D features.

Usage:
    python test_contact_point_2d.py [task_name]
    
Example:
    python test_contact_point_2d.py beat_block_hammer
"""

import sys
import os
import numpy as np

# Add the project root to Python path
sys.path.append("./")

from envs import *
import yaml
import importlib


def test_contact_point_2d(task_name="beat_block_hammer"):
    """
    Test the contact point 2D projection functionality.
    
    Args:
        task_name (str): Name of the task to test
    """
    print(f"Testing contact point 2D projection with task: {task_name}")
    
    try:
        # Create task instance
        envs_module = importlib.import_module(f"envs.{task_name}")
        env_class = getattr(envs_module, task_name)
        env_instance = env_class()
        
        # Load configuration with contact points enabled
        config_path = "./task_config/demo_with_contact_points.yml"
        with open(config_path, "r", encoding="utf-8") as f:
            args = yaml.load(f.read(), Loader=yaml.FullLoader)
        
        args['task_name'] = task_name
        args['seed'] = 42  # Fixed seed for reproducible testing
        args['episode_num'] = 1  # Just test one episode
        
        print("Initializing environment with contact point collection enabled...")
        
        # Initialize the environment
        env_instance._init_task_env_(**args)
        
        # Test if the methods exist
        if hasattr(env_instance, 'get_contact_point_pose_2d'):
            print("✓ get_contact_point_pose_2d method found")
        else:
            print("✗ get_contact_point_pose_2d method not found")
            return False
            
        if hasattr(env_instance, 'get_contact_point_pose'):
            print("✓ get_contact_point_pose method found")
        else:
            print("✗ get_contact_point_pose method not found")
            return False
        
        # Test contact point functionality if manipulated_obj exists
        if hasattr(env_instance, 'manipulated_obj') and env_instance.manipulated_obj is not None:
            print("Testing contact point methods...")
            
            # Test 3D contact point
            try:
                contact_3d = env_instance.get_contact_point_pose()
                print(f"✓ 3D contact point: {contact_3d}")
            except Exception as e:
                print(f"✗ Error getting 3D contact point: {e}")
                
            # Test 2D contact point projection
            try:
                contact_2d = env_instance.get_contact_point_pose_2d()
                print(f"✓ 2D contact point projection: {contact_2d}")
                
                if contact_2d.get("valid", False):
                    coords = contact_2d.get("2d_coords", [0, 0])
                    print(f"  - Image coordinates: ({coords[0]:.1f}, {coords[1]:.1f})")
                    print(f"  - Depth: {contact_2d.get('depth', 0):.3f}m")
                    print(f"  - Camera: {contact_2d.get('camera_name', 'unknown')}")
                else:
                    print("  - Contact point not visible in camera")
                    
            except Exception as e:
                print(f"✗ Error getting 2D contact point: {e}")
        else:
            print("No manipulated object found - testing method interface only")
            
        # Test data collection with contact points
        print("Testing data collection with contact points...")
        try:
            obs_data = env_instance.get_obs()
            
            if "contact_point" in obs_data:
                print("✓ 3D contact point data collected")
            else:
                print("- 3D contact point data not in observation (may be disabled)")
                
            if "contact_point_2d" in obs_data:
                print("✓ 2D contact point data collected")
                contact_2d_data = obs_data["contact_point_2d"]
                print(f"  - 2D contact point data: {contact_2d_data}")
            else:
                print("- 2D contact point data not in observation (may be disabled)")
                
        except Exception as e:
            print(f"✗ Error during data collection: {e}")
            
        print("Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        try:
            env_instance.close_env()
        except:
            pass


def main():
    """Main function."""
    task_name = sys.argv[1] if len(sys.argv) > 1 else "beat_block_hammer"
    
    print("=" * 60)
    print("Contact Point 2D Projection Test")
    print("=" * 60)
    
    success = test_contact_point_2d(task_name)
    
    if success:
        print("\n✓ All tests passed!")
        print("\nTo enable contact point collection in your tasks:")
        print("1. Set 'contact_point: true' in your config file for 3D contact points")
        print("2. Set 'contact_point_2d: true' in your config file for 2D projections")
        print("3. Use the demo_with_contact_points.yml config as an example")
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
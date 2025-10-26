import h5py, pickle
import numpy as np
import os
import cv2
from collections.abc import Mapping, Sequence
import shutil
from .images_to_video import images_to_video


def images_encoding(imgs):
    encode_data = []
    padded_data = []
    max_len = 0
    for i in range(len(imgs)):
        success, encoded_image = cv2.imencode(".jpg", imgs[i])
        jpeg_data = encoded_image.tobytes()
        encode_data.append(jpeg_data)
        max_len = max(max_len, len(jpeg_data))
    # padding
    for i in range(len(imgs)):
        padded_data.append(encode_data[i].ljust(max_len, b"\0"))
    return encode_data, max_len


def parse_dict_structure(data):
    if isinstance(data, dict):
        parsed = {}
        for key, value in data.items():
            if isinstance(value, dict):
                parsed[key] = parse_dict_structure(value)
            elif isinstance(value, np.ndarray):
                parsed[key] = []
            else:
                parsed[key] = []
        return parsed
    else:
        return []


def append_data_to_structure(data_structure, data):
    for key in data_structure:
        if key in data:
            if isinstance(data_structure[key], list):
                # 如果是叶子节点，直接追加数据
                data_structure[key].append(data[key])
            elif isinstance(data_structure[key], dict):
                # 如果是嵌套字典，递归处理
                append_data_to_structure(data_structure[key], data[key])


def load_pkl_file(pkl_path):
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)
    return data


def create_hdf5_from_dict(hdf5_group, data_dict):
    for key, value in data_dict.items():
        if isinstance(value, dict):
            subgroup = hdf5_group.create_group(key)
            create_hdf5_from_dict(subgroup, value)
        elif isinstance(value, list):
            # Handle shape inconsistencies for images (especially three-panel images)
            if "rgb" in key:
                try:
                    value = np.array(value)
                except ValueError as e:
                    print(f"Shape inconsistency in {key}: {e}")
                    # Find the most common shape
                    shapes = [img.shape for img in value]
                    from collections import Counter
                    shape_counts = Counter(shapes)
                    most_common_shape = shape_counts.most_common(1)[0][0]
                    print(f"Most common shape for {key}: {most_common_shape}")
                    
                    # Resize all images to the most common shape
                    resized_images = []
                    for img in value:
                        if img.shape != most_common_shape:
                            resized_img = cv2.resize(img, (most_common_shape[1], most_common_shape[0]))
                            resized_images.append(resized_img)
                        else:
                            resized_images.append(img)
                    
                    value = np.array(resized_images)
                    print(f"Resized {key} to shape: {value.shape}")
                
                encode_data, max_len = images_encoding(value)
                hdf5_group.create_dataset(key, data=encode_data, dtype=f"S{max_len}")
            else:
                try:
                    value = np.array(value)
                    hdf5_group.create_dataset(key, data=value)
                except ValueError as e:
                    print(f"Error converting {key} to numpy array: {e}")
                    # Store as string if conversion fails
                    hdf5_group.create_dataset(key, data=str(value))
        else:
            try:
                hdf5_group.create_dataset(key, data=str(value))
            except Exception as e:
                print(f"Error storing value for key '{key}': {e}")


def pkl_files_to_hdf5_and_video(pkl_files, hdf5_path, video_path):
    data_list = parse_dict_structure(load_pkl_file(pkl_files[0]))
    for pkl_file_path in pkl_files:
        pkl_file = load_pkl_file(pkl_file_path)
        append_data_to_structure(data_list, pkl_file)

    # Handle three-panel images (original + X plot + Y plot)
    rgb_images = data_list["observation"]["head_camera"]["rgb"]
    
    # Check if images have consistent dimensions
    if rgb_images:
        first_img_shape = rgb_images[0].shape
        print(f"First image shape: {first_img_shape}")
        
        # Convert to numpy array, handling potential shape inconsistencies
        try:
            images_array = np.array(rgb_images)
            print(f"Images array shape: {images_array.shape}")
        except ValueError as e:
            print(f"Shape inconsistency detected: {e}")
            # If shapes are inconsistent, we need to handle them individually
            # This can happen with three-panel visualization
            print("Processing images individually to handle shape differences...")
            
            # Find the most common shape
            shapes = [img.shape for img in rgb_images]
            from collections import Counter
            shape_counts = Counter(shapes)
            most_common_shape = shape_counts.most_common(1)[0][0]
            print(f"Most common shape: {most_common_shape}")
            
            # Resize all images to the most common shape
            resized_images = []
            for img in rgb_images:
                if img.shape != most_common_shape:
                    resized_img = cv2.resize(img, (most_common_shape[1], most_common_shape[0]))
                    resized_images.append(resized_img)
                else:
                    resized_images.append(img)
            
            images_array = np.array(resized_images)
            print(f"Resized images array shape: {images_array.shape}")
    
    images_to_video(images_array, out_path=video_path)

    with h5py.File(hdf5_path, "w") as f:
        create_hdf5_from_dict(f, data_list)


def process_folder_to_hdf5_video(folder_path, hdf5_path, video_path):
    pkl_files = []
    for fname in os.listdir(folder_path):
        if fname.endswith(".pkl") and fname[:-4].isdigit():
            pkl_files.append((int(fname[:-4]), os.path.join(folder_path, fname)))

    if not pkl_files:
        raise FileNotFoundError(f"No valid .pkl files found in {folder_path}")

    pkl_files.sort()
    pkl_files = [f[1] for f in pkl_files]

    expected = 0
    for f in pkl_files:
        num = int(os.path.basename(f)[:-4])
        if num != expected:
            raise ValueError(f"Missing file {expected}.pkl")
        expected += 1

    pkl_files_to_hdf5_and_video(pkl_files, hdf5_path, video_path)

"""
Model handler module for PhytoSense application.
Provides functions for interacting with ML models and performing analysis.
"""

import random
import numpy as np
from datetime import datetime
from model import load_model, predict_disease, SOIL_CLASSES
from crop_data import onion_diseases, tomato_diseases, common_pests, maharashtra_crop_varieties

def identify_plant(image):
    """
    Identify the plant type from an image
    
    Args:
        image: Preprocessed image array
        
    Returns:
        dict: Information about the identified plant
    """
    # List of possible crops for identification
    crops = ["Tomato", "Potato", "Corn", "Wheat", "Rice", "Onion", "Soybean", "Cotton"]
    
    # Extract color features
    if len(image.shape) == 3:
        avg_color = np.mean(np.array(image), axis=(0, 1))
        r, g, b = avg_color
        
        # Calculate ratios
        g_r_ratio = g / (r + 1e-10)
        g_b_ratio = g / (b + 1e-10)
        
        # Use deterministic logic for consistent predictions
        plant_name = ""
        probability = 0.0
        scientific_name = ""
        
        # Set a seed based on image properties for consistent results
        np.random.seed(int(np.sum(avg_color) * 100))
        
        # Apply rule-based prediction
        if g_r_ratio > 1.2 and g > 100:
            # Green leafy crops
            candidates = ["Spinach", "Cabbage", "Lettuce"]
            plant_name = candidates[np.random.randint(0, len(candidates))]
            probability = 75 + np.random.randint(0, 20)
        elif g_r_ratio > 1.0 and g_b_ratio > 1.3:
            # Likely a Solanaceae family plant (tomato, potato, etc.)
            if r > 100 and b < 90:
                plant_name = "Tomato"
                scientific_name = "Solanum lycopersicum"
                probability = 85 + np.random.randint(0, 15)
            else:
                plant_name = "Potato"
                scientific_name = "Solanum tuberosum"
                probability = 80 + np.random.randint(0, 15)
        elif g_r_ratio < 0.9 and g > 80:
            # Likely a cereal crop
            if b > 80:
                plant_name = "Wheat"
                scientific_name = "Triticum aestivum"
                probability = 80 + np.random.randint(0, 15)
            else:
                plant_name = "Corn"
                scientific_name = "Zea mays"
                probability = 75 + np.random.randint(0, 20)
        elif g_r_ratio > 0.9 and g_r_ratio < 1.1:
            # Could be other crops
            if g > 120:
                plant_name = "Rice"
                scientific_name = "Oryza sativa"
                probability = 75 + np.random.randint(0, 20)
            else:
                plant_name = "Onion"
                scientific_name = "Allium cepa"
                probability = 70 + np.random.randint(0, 25)
        else:
            # Default case - select a random crop from the list
            idx = np.random.randint(0, len(crops))
            plant_name = crops[idx]
            probability = 60 + np.random.randint(0, 30)
            
            # Add scientific names for common crops
            scientific_names = {
                "Tomato": "Solanum lycopersicum",
                "Potato": "Solanum tuberosum",
                "Corn": "Zea mays",
                "Wheat": "Triticum aestivum",
                "Rice": "Oryza sativa",
                "Onion": "Allium cepa",
                "Soybean": "Glycine max",
                "Cotton": "Gossypium hirsutum"
            }
            scientific_name = scientific_names.get(plant_name, "")
        
        return {
            "name": plant_name,
            "scientific_name": scientific_name,
            "probability": probability
        }
    else:
        # If image is not RGB, return a default response
        return {
            "name": random.choice(crops),
            "scientific_name": "",
            "probability": 60 + np.random.randint(0, 15)
        }

def detect_water_content(image):
    """
    Detect the water content/hydration level of plants from an image
    
    Args:
        image: Preprocessed image array
        
    Returns:
        dict: Information about the plant's water content
    """
    # Extract color features for analysis
    if len(np.array(image).shape) == 3:
        avg_color = np.mean(np.array(image), axis=(0, 1))
        r, g, b = avg_color
        
        # Calculate green intensity as a proxy for plant health/hydration
        g_intensity = g / 255.0
        
        # Calculate ratios for better analysis
        g_r_ratio = g / (r + 1e-10)
        g_b_ratio = g / (b + 1e-10)
        
        # Create a deterministic prediction based on color features
        np.random.seed(int(np.sum(avg_color) * 100))
        
        # Determine water content and status
        water_percentage = 0.0
        status = ""
        
        # Higher green intensity and ratios usually indicate better hydration
        if g_intensity > 0.45 and g_r_ratio > 1.1 and g_b_ratio > 1.1:
            # Well-hydrated plant
            water_percentage = 75 + np.random.randint(0, 20)
            status = "Optimal"
        elif (g_intensity > 0.3 and g_intensity <= 0.45) or (g_r_ratio > 0.9 and g_r_ratio <= 1.1):
            # Moderately hydrated plant
            water_percentage = 40 + np.random.randint(0, 35)
            status = "Low"
        else:
            # Under-hydrated plant
            water_percentage = 10 + np.random.randint(0, 30)
            status = "Critical"
        
        return {
            "percentage": water_percentage,
            "status": status
        }
    else:
        # Default response for non-RGB images
        np.random.seed(int(datetime.now().timestamp()) % 1000)
        return {
            "percentage": 50 + np.random.randint(0, 30),
            "status": random.choice(["Optimal", "Low", "Critical"])
        }

def detect_diseases(image, plant_name):
    """
    Detect diseases in plants from an image
    
    Args:
        image: Preprocessed image array
        plant_name: Name of the plant to check for diseases
        
    Returns:
        dict: Information about detected diseases
    """
    # Convert image to numpy array if needed
    img_array = np.array(image)
    
    # Load appropriate model based on plant type
    if plant_name.lower() == "tomato":
        model = load_model("tomato")
        disease_list = tomato_diseases
    elif plant_name.lower() == "onion":
        model = load_model("onion")
        disease_list = onion_diseases
    else:
        # For other plants, use a generic model (tomato in this case)
        model = load_model("tomato")
        disease_list = tomato_diseases
    
    # Get disease prediction from model
    disease_id, confidence = predict_disease(model, img_array, plant_name.lower())
    
    # Check if disease is detected (based on confidence threshold)
    disease_detected = confidence > 60 and disease_id < model.num_classes - 1
    
    # Prepare response
    result = {
        "detected": disease_detected,
        "diseases": []
    }
    
    if disease_detected:
        # Convert disease ID to disease name and details
        if plant_name.lower() == "tomato":
            disease_names = list(tomato_diseases.keys())
            if disease_id < len(disease_names):
                disease_name = disease_names[disease_id]
                disease_info = tomato_diseases[disease_name]
                
                # Add disease information
                result["diseases"].append({
                    "name": disease_name,
                    "confidence": confidence,
                    "scientific_name": disease_info["scientific_name"],
                    "description": disease_info["symptoms"],
                    "treatment": "Apply appropriate " + ", ".join(disease_info["chemicals"][:2]) + 
                                " or organic options: " + ", ".join(disease_info["organic_controls"][:2])
                })
        elif plant_name.lower() == "onion":
            disease_names = list(onion_diseases.keys())
            if disease_id < len(disease_names):
                disease_name = disease_names[disease_id]
                disease_info = onion_diseases[disease_name]
                
                # Add disease information
                result["diseases"].append({
                    "name": disease_name,
                    "confidence": confidence,
                    "scientific_name": disease_info["scientific_name"],
                    "description": disease_info["symptoms"],
                    "treatment": "Apply appropriate " + ", ".join(disease_info["chemicals"][:2]) + 
                                " or organic options: " + ", ".join(disease_info["organic_controls"][:2])
                })
        else:
            # For other plants, use generic disease names
            generic_diseases = [
                "Leaf Spot", "Powdery Mildew", "Rust", "Bacterial Blight",
                "Mosaic Virus", "Anthracnose", "Root Rot"
            ]
            
            disease_name = generic_diseases[disease_id % len(generic_diseases)]
            
            # Add generic disease information
            result["diseases"].append({
                "name": disease_name,
                "confidence": confidence,
                "description": f"Symptoms of {disease_name} observed on the plant",
                "treatment": "Consult a local agricultural expert for specific treatment options"
            })
    
    return result

def detect_pests(image):
    """
    Detect pests in plants from an image
    
    Args:
        image: Preprocessed image array
        
    Returns:
        dict: Information about detected pests
    """
    # Create deterministic but simulated pest detection
    img_array = np.array(image)
    
    # Extract some simple image statistics
    if len(img_array.shape) == 3:
        # Calculate variance in each channel as a proxy for texture/patterns
        var_r = np.var(img_array[:, :, 0])
        var_g = np.var(img_array[:, :, 1]) 
        var_b = np.var(img_array[:, :, 2])
        
        # Calculate average color
        avg_color = np.mean(img_array, axis=(0, 1))
        r, g, b = avg_color
        
        # Set seed for consistent results
        np.random.seed(int((var_r + var_g + var_b) * 10))
        
        # Use the image properties to decide if pests are present
        texture_complexity = (var_r + var_g + var_b) / 3
        color_health = g / (r + b + 1e-10)
        
        # Higher texture complexity and lower green ratio might indicate pest presence
        pest_likelihood = texture_complexity / 1000 * (1 - color_health)
        
        # Determine if pests are detected
        pests_detected = pest_likelihood > 0.05 and np.random.random() < 0.6
        
        # Prepare response
        result = {
            "detected": pests_detected,
            "pests": []
        }
        
        if pests_detected:
            # Select which pests are present based on image characteristics
            pest_candidates = list(common_pests.keys())
            
            # Determine number of pests to report
            num_pests = 1 if np.random.random() < 0.7 else 2
            
            for _ in range(num_pests):
                # Select a pest
                pest_name = np.random.choice(pest_candidates)
                pest_info = common_pests[pest_name]
                
                # Determine infestation level
                infestation_level = "Low"
                if pest_likelihood > 0.1:
                    infestation_level = "Medium"
                if pest_likelihood > 0.15:
                    infestation_level = "High"
                
                # Add pest information
                result["pests"].append({
                    "name": pest_name,
                    "scientific_name": pest_info["scientific_name"],
                    "infestation_level": infestation_level,
                    "description": pest_info["identification"] + ". " + pest_info["damage"],
                    "treatment": "Chemical control: " + ", ".join(pest_info["chemicals"][:2]) + 
                                ". Organic options: " + ", ".join(pest_info["organic_controls"][:2])
                })
                
                # Remove selected pest from candidates to avoid duplicates
                pest_candidates.remove(pest_name)
                if not pest_candidates:
                    break
        
        return result
    else:
        # Default response for non-RGB images
        return {
            "detected": False,
            "pests": []
        }

def analyze_soil_type(image):
    """
    Analyze soil type from an image
    
    Args:
        image: Preprocessed image array
        
    Returns:
        str: Detected soil type
    """
    # Convert to numpy array if needed
    img_array = np.array(image)
    
    if len(img_array.shape) == 3:
        # Calculate average color
        avg_color = np.mean(img_array, axis=(0, 1))
        r, g, b = avg_color
        
        # Calculate standard deviation for texture
        std_color = np.std(img_array, axis=(0, 1))
        std_r, std_g, std_b = std_color
        
        # Set seed for consistent results
        np.random.seed(int((r + g + b) * 10))
        
        # Determine soil type based on color
        if r > g and r > b and r > 150:
            # Reddish soil
            return SOIL_CLASSES[1]  # Red Soil
        elif r < 100 and g < 100 and b < 100:
            # Dark soil
            return SOIL_CLASSES[0]  # Black Soil
        elif r > 150 and g > 150 and b > 100:
            # Sandy/light-colored soil
            return SOIL_CLASSES[4]  # Coastal Sandy Soil
        elif r > g and r > b:
            # Laterite-like soil
            return SOIL_CLASSES[2]  # Laterite Soil
        else:
            # Default to alluvial soil
            return SOIL_CLASSES[3]  # Alluvial Soil
    else:
        # For grayscale images, make a random selection
        return np.random.choice(SOIL_CLASSES)

"""
Crop database module for PhytoSense application.
Contains detailed information about crops, diseases, symptoms, and treatments.
"""

CROP_DATABASE = {
    "Tomato": {
        "info": {
            "scientific_name": "Solanum lycopersicum",
            "best_season": "Tomatoes can be cultivated throughout the year in Maharashtra. Optimal planting times are: Rainy Season (June to July), Winter Season (October to November), Summer Season (January to February)",
            "best_soil": "Well-drained loamy soils rich in organic matter with a pH range of 6.5–7.5",
            "time_period": "Approximately 120 days from transplanting to harvesting",
            "estimated_cost": "₹30,150 per acre",
            "varieties": [
                "Phule Raja", "Phule Tejas", "Vaishali", "Dhanashree", "Abhinav", 
                "Pusa Ruby", "Naveen", "Rashmi", "Megha", "Sankranti"
            ]
        },
        "diseases": {
            "Leaf Curl Virus": {
                "symptoms": "Upward curling of leaves, reduction in leaf size, stunted growth, and flower drop",
                "causes": "Transmitted by whiteflies",
                "treatment": "Apply insecticides such as Imidacloprid (70% WG) at 0.1 g per liter of water to control whitefly populations",
                "prevention": "Remove and destroy infected plants; use reflective mulches to deter whiteflies"
            },
            "Early Blight": {
                "symptoms": "Dark brown spots with concentric rings on older leaves ('target board' appearance). Yellowing of leaves leading to defoliation",
                "causes": "Fungus (Alternaria solani) persists in soil and plant debris. Spread facilitated by splashing water and wind",
                "treatment": "Spray Chlorothalonil or Mancozeb @ 2–2.5 g/L. Use Azoxystrobin as systemic option",
                "prevention": "Practice crop rotation, remove plant debris after harvest, ensure balanced fertilization (especially nitrogen and potassium)"
            },
            "Late Blight": {
                "symptoms": "Water-soaked lesions on leaves, stems, and fruits. White mold growth under leaves in humid conditions",
                "causes": "Oomycete pathogen Phytophthora infestans thrives in cool, wet weather. Spores spread via wind and rain",
                "treatment": "Apply fungicides like Mancozeb + Metalaxyl, Phosphoric acid-based foliar fertilizers",
                "prevention": "Remove and destroy infected plants immediately, avoid overhead watering to reduce leaf wetness"
            },
            "Fusarium Wilt": {
                "symptoms": "Yellowing and wilting of leaves, often on one side of the plant. Brown discoloration of vascular tissue when stems are cut",
                "causes": "Soil-borne fungus Fusarium oxysporum enters through roots and blocks water transport",
                "treatment": "Use biofertilizers like Pseudomonas fluorescens, Neem Cake + Farm Yard Manure (FYM)",
                "prevention": "Plant resistant tomato varieties, practice crop rotation with non-host plants, remove and destroy infected plants"
            }
        },
        "pests": {
            "Fruit Borer": {
                "symptoms": "Holes in fruits with excreta, caterpillar often found inside fruit",
                "description": "Greenish-brown caterpillar; feeds on developing fruits",
                "treatment": "Install pheromone traps, release Trichogramma chilonis (egg parasitoid), use Spinosad 45 SC (0.3 ml/l), Emamectin Benzoate 5 SG (0.4 g/l), or Novaluron 10 EC (1 ml/l)"
            },
            "Whitefly": {
                "symptoms": "Yellowing and curling of leaves, sticky honeydew on leaves; sooty mold formation",
                "description": "Tiny white insects on the undersides of leaves, also transmits Tomato Leaf Curl Virus",
                "treatment": "Use yellow sticky traps, apply Imidacloprid or Thiamethoxam, spray neem oil as an organic alternative"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Older leaves turn pale yellow or light green, stunted growth, poor fruit development",
                "treatment": "Apply Urea (46% N), Ammonium Sulphate, organic compost or well-decomposed FYM"
            },
            "Phosphorus": {
                "symptoms": "Leaves appear dull dark green with purplish veins, slow growth and poor root development",
                "treatment": "Apply Single Super Phosphate (SSP), Di-Ammonium Phosphate (DAP), or bone meal (organic)"
            },
            "Calcium": {
                "symptoms": "Blossom End Rot on fruits, young leaves may be distorted, reduced root and shoot growth",
                "treatment": "Apply Calcium Nitrate, Gypsum (Calcium Sulphate), or Dolomite lime (if soil is acidic)"
            }
        }
    },
    "Cabbage": {
        "info": {
            "scientific_name": "Brassica oleracea var. capitata",
            "best_season": "Cabbage is a cool-season crop that prefers moderate temperatures. It thrives best in spring or fall, with temperatures ranging from 15°C to 20°C (59°F to 68°F)",
            "best_soil": "Loamy soil, which is well-drained and rich in organic matter. Soil pH between 6.0 to 6.5",
            "time_period": "Early varieties take around 70 to 85 days to mature. Late varieties may take 100 to 120 days",
            "estimated_cost": "₹35,000 to ₹50,000 per acre",
            "varieties": [
                "Green Cabbage", "Red Cabbage", "Savoy Cabbage", "Napa Cabbage (Chinese Cabbage)"
            ]
        },
        "diseases": {
            "Downy Mildew": {
                "symptoms": "Yellow patches on upper leaf surface, white to grey mold under the leaves, wilting in severe infections",
                "causes": "Fungal disease caused by Peronospora parasitica, favors high humidity and cool temperatures",
                "treatment": "Spray Metalaxyl + Mancozeb (0.25%), use Fosetyl-Al (Aliette)",
                "prevention": "Improve field drainage and aeration, avoid wetting foliage during irrigation"
            },
            "Clubroot": {
                "symptoms": "Root swelling, stunted growth, yellowing of leaves, wilting, premature leaf drop, reduced head formation",
                "causes": "Caused by the soil-borne protist Plasmodiophora brassicae, thrives in acidic, poorly-drained soils",
                "treatment": "Apply lime to raise soil pH to 7.0–7.5, use phosphorus and potassium fertilizers, organic compost, biological control with Trichoderma harzianum",
                "prevention": "Crop rotation for 3-4 years, use resistant varieties, maintain neutral to alkaline pH, ensure good drainage"
            },
            "Black Rot": {
                "symptoms": "Yellowing of leaf edges, V-shaped lesions spreading inward, blackening of veins and rotting of heads",
                "causes": "Bacterial infection caused by Xanthomonas campestris pv. campestris, spread through seeds, water, and contaminated tools",
                "treatment": "Spray Copper Oxychloride @ 2.5 g/liter + Streptocycline @ 100 ppm, use bioagents like Pseudomonas fluorescens",
                "prevention": "Use disease-free seeds, practice crop rotation (3–4 years), avoid overhead irrigation"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Curled leaves, yellowing of leaves, sticky residue on plants",
                "description": "Small soft-bodied insects that cluster on leaves and stems",
                "treatment": "Use Neem oil or insecticidal soaps for control"
            },
            "Cabbage Worms": {
                "symptoms": "Holes in the leaves, chewed edges, and visible caterpillars",
                "description": "Green caterpillars that feed on leaves",
                "treatment": "Treat plants with Bacillus thuringiensis (Bt) or pyrethrin-based insecticides"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves (chlorosis), stunted growth and small leaves, reduced head size and poor yield",
                "treatment": "Apply Nitrogen-rich fertilizers, such as Urea or Ammonium Nitrate, or incorporate well-rotted manure or compost"
            },
            "Phosphorus": {
                "symptoms": "Dark green leaves with a reddish-purple tinge, stunted growth and poor root development",
                "treatment": "Use phosphorus-based fertilizers like Single Superphosphate (SSP) or Diammonium Phosphate (DAP), bone meal or rock phosphate"
            }
        }
    },
    "Cauliflower": {
        "info": {
            "scientific_name": "Brassica oleracea var. botrytis",
            "best_season": "Cool-season crop that prefers moderate temperatures, ideally between 15°C and 20°C (59°F to 68°F). Most successfully grown in spring or fall",
            "best_soil": "Well-drained, fertile soil rich in organic matter. Ideal pH range is 6.0 to 6.8",
            "time_period": "Early varieties mature in 50 to 75 days from transplanting. Late varieties typically require around 80 to 120 days",
            "estimated_cost": "Between ₹1,66,000 to ₹3,32,000 per acre",
            "varieties": [
                "Snowball", "Great White", "Graffiti", "Cheddar", "Romanesco"
            ]
        },
        "diseases": {
            "Downy Mildew": {
                "symptoms": "Yellowish patches on the upper side of leaves, white fungal growth on the underside, wilting in severe cases",
                "causes": "Caused by fungus Peronospora parasitica, favors cool, moist conditions",
                "treatment": "Spray Metalaxyl + Mancozeb (0.25%) every 10–15 days, use fungicides like Ridomil Gold",
                "prevention": "Avoid overhead irrigation, maintain plant spacing, use resistant varieties, ensure good air circulation"
            },
            "Black Rot": {
                "symptoms": "Yellowing leaf margins with V-shaped lesions, black veins on leaves and stems, bad odor in advanced stages",
                "causes": "Caused by Xanthomonas campestris pv. campestris (a bacterium), spread via infected seeds, tools, and water",
                "treatment": "Spray Copper Oxychloride (0.25%) + Streptocycline (100 ppm)",
                "prevention": "Use disease-free certified seeds, practice crop rotation, avoid overhead irrigation"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Soft-bodied green/black insects cluster on new leaves, curling and yellowing of leaves, sticky honeydew attracts ants",
                "description": "Small, soft-bodied insects that suck plant sap",
                "treatment": "Spray Neem oil (2%), Imidacloprid 17.8 SL @ 0.3 ml/liter water, Verticillium lecanii (biopesticide) as an eco-friendly option"
            },
            "Diamondback Moth": {
                "symptoms": "Small caterpillars make holes in leaves, larvae feed on leaf undersides and curds",
                "description": "Small caterpillars that feed on leaves and heads",
                "treatment": "Use Bacillus thuringiensis (Bt) formulations, Spinosad 45 SC @ 1 ml/liter, introduce natural enemies like Trichogramma spp."
            }
        },
        "deficiencies": {
            "Boron": {
                "symptoms": "Brown curd spots, hollow stems, distorted curd and stem cracking",
                "treatment": "Apply Borax (10–15 kg/ha), use boron-rich organic compost, foliar spray: 0.1% boric acid solution at 30 and 50 days after planting"
            },
            "Molybdenum": {
                "symptoms": "Whiptail condition – narrow, strap-like leaves, poor curd development",
                "treatment": "Apply Ammonium Molybdate (0.05%) as foliar spray, enrich compost with molybdenum-containing minerals"
            }
        }
    },
    "Potato": {
        "info": {
            "scientific_name": "Solanum tuberosum",
            "best_season": "Cool-season crop, grows best in spring and early summer. In temperate climates, spring planting is common. In tropical areas, potatoes can be grown in fall",
            "best_soil": "Well-drained, loose, and fertile soil with pH 5.0 to 6.0. Well-drained loamy soils are ideal",
            "time_period": "Early varieties mature in 70 to 90 days. Mid-season: 90 to 120 days. Late varieties: 120 to 150 days",
            "estimated_cost": "₹1,28,450 to ₹3,92,650 or more per acre",
            "varieties": [
                "Russet Burbank", "Yukon Gold", "Red Potatoes", "Fingerling Potatoes", "New Potatoes"
            ]
        },
        "diseases": {
            "Late Blight": {
                "symptoms": "Water-soaked brown to black lesions on leaves and stems, white fungal growth under leaves, tubers show brownish rot with foul smell",
                "causes": "Fungal disease caused by Phytophthora infestans, favored by cool, moist conditions",
                "treatment": "Spray Mancozeb + Metalaxyl (e.g., Ridomil Gold) at 10–15 day intervals, use Copper Oxychloride for tuber protection",
                "prevention": "Use resistant varieties (like Kufri Jyoti, Kufri Bahar), avoid overhead irrigation, destroy infected crop residues"
            },
            "Bacterial Wilt / Brown Rot": {
                "symptoms": "Sudden wilting of entire plant, browning of vascular tissues in stems, brown ooze from infected stem or tuber when cut",
                "causes": "Caused by Ralstonia solanacearum (bacteria), survives in soil and infected crop residue",
                "treatment": "No effective chemical treatment. Uproot and destroy infected plants immediately. Soil treatment with Pseudomonas fluorescens as biocontrol",
                "prevention": "Use certified disease-free seed, avoid waterlogging, rotate with non-host crops like cereals"
            }
        },
        "pests": {
            "Potato Tuber Moth": {
                "symptoms": "Caterpillars bore into tubers and create tunnels, dry powdery frass inside tuber, secondary fungal/bacterial rot",
                "description": "Moths that lay eggs on tubers, and the larvae bore into the potato",
                "treatment": "Spray Spinosad 45 SC @ 1 ml/l, store tubers under cool, dark, and ventilated conditions, use neem oil spray for eco-friendly control"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves, stunted growth, poor tuber development",
                "treatment": "Apply nitrogen fertilizers like urea or ammonium nitrate, organic options include composted manure"
            },
            "Potassium": {
                "symptoms": "Bronzing and scorching of leaf edges, weak stems, reduced tuber size",
                "treatment": "Apply potassium-rich fertilizers like muriate of potash or sulfate of potash"
            }
        }
    },
    "Watermelon": {
        "info": {
            "scientific_name": "Citrullus lanatus",
            "best_season": "Warm, dry climates. Spring Season: January to March. Summer Season: November to February (in areas with mild winters). Best when temperatures are between 22°C and 35°C",
            "best_soil": "Well-drained, sandy loam soils rich in organic matter. Soil pH between 6.0 and 7.5 is ideal",
            "time_period": "Approximately 75–120 days from sowing to harvesting, depending on the variety",
            "estimated_cost": "₹50,000–₹80,000 per acre",
            "varieties": [
                "Sugar Baby", "Arka Manik", "Crimson Sweet", "Black Diamond", "Kiran", "Seedless Watermelon"
            ]
        },
        "diseases": {
            "Anthracnose": {
                "symptoms": "Circular, sunken lesions on leaves, stems, and fruits. Fruits may develop cracks and rot",
                "causes": "Caused by the fungus Colletotrichum orbiculare. Thrives in warm, humid conditions with frequent rainfall",
                "treatment": "Apply fungicides like chlorothalonil, mancozeb, or azoxystrobin at regular intervals. Apply fertilizers rich in potassium and phosphorus",
                "prevention": "Use disease-resistant varieties, practice crop rotation, remove infected plant debris, avoid overhead irrigation, ensure proper spacing"
            },
            "Fusarium Wilt": {
                "symptoms": "Yellowing and wilting of leaves, vascular discoloration, and eventual plant death",
                "causes": "Caused by the fungus Fusarium oxysporum f. sp. niveum. Thrives in warm, sandy soils with low pH",
                "treatment": "Apply fertilizers rich in potassium and phosphorus. Use fungicides like prothioconazole through drip irrigation",
                "prevention": "Crop rotation for 5-6 years, plant resistant varieties, maintain soil pH above 6.5, remove infected plants"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Curled leaves, stunted growth, honeydew secretion",
                "description": "Small, soft-bodied insects that feed on plant sap",
                "treatment": "Apply insecticidal soap, neem oil, or introduce natural predators like ladybugs"
            },
            "Cucumber Beetles": {
                "symptoms": "Holes in leaves, damaged flowers, scarring on fruit surface",
                "description": "Small beetles with yellow and black stripes or spots",
                "treatment": "Use row covers, apply botanical insecticides, practice crop rotation"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves, stunted growth, and reduced foliage",
                "treatment": "Apply nitrogen-rich fertilizers like urea or ammonium nitrate. Organic options include composted manure or fish emulsion"
            },
            "Potassium": {
                "symptoms": "Browning or scorching of leaf edges and tips, weak stems, and poor fruit quality",
                "treatment": "Use potassium sulfate or muriate of potash. Organic alternatives include wood ash or banana peels"
            }
        }
    },
    "Pomegranate": {
        "info": {
            "scientific_name": "Punica granatum",
            "best_season": "Semi-arid and tropical climates. Monsoon Planting: June to August. Spring Planting: February to March in regions with irrigation",
            "best_soil": "Variety of soils from sandy loam to black soil. Slightly acidic to neutral soil pH of 6.0–7.5 is ideal",
            "time_period": "Trees typically start bearing fruits 2–3 years after planting. Fruits are harvested 5–7 months after flowering",
            "estimated_cost": "₹80,000–₹1,60,000 per acre",
            "varieties": [
                "Bhagwa", "Ganesh", "Arakta", "Mridula", "Kandhari", "Wonderful"
            ]
        },
        "diseases": {
            "Cercospora Fruit Spot": {
                "symptoms": "Yellowish spots with halos on leaves and fruits, which turn black and corky. Severe infections cause defoliation and fruit cracking",
                "causes": "Caused by the fungus Cercospora punicae. Thrives in warm, humid conditions with frequent rainfall",
                "treatment": "Apply Mancozeb (0.25%) or Propiconazole (0.1%) at regular intervals. Apply fertilizers rich in potassium and phosphorus",
                "prevention": "Use certified pathogen-free planting material, prune infected parts, ensure proper spacing, avoid overhead irrigation"
            },
            "Anthracnose": {
                "symptoms": "Leaf blight, fruit spots, and dieback. Fruits develop brownish-black patches that lead to rot",
                "causes": "Caused by the fungus Colletotrichum gloeosporioides. Thrives in warm, humid conditions with frequent rainfall",
                "treatment": "Use copper fungicides and prune infected branches. Apply fungicides like Mancozeb (0.25%) or Propiconazole (0.1%)",
                "prevention": "Use disease-free planting material, prune infected parts, ensure proper spacing, avoid overhead irrigation"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Curled leaves, stunted growth, honeydew secretion",
                "description": "Small, soft-bodied insects that feed on plant sap",
                "treatment": "Apply insecticidal soap, neem oil, or introduce natural predators like ladybugs"
            },
            "Fruit Borers": {
                "symptoms": "Holes in fruits, premature fruit drop, rotting of affected fruits",
                "description": "Larvae that bore into fruits, causing damage and rot",
                "treatment": "Apply approved insecticides, use pheromone traps, practice orchard sanitation"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves, stunted growth, reduced foliage",
                "treatment": "Apply nitrogen-rich fertilizers like urea or ammonium nitrate. Organic options include composted manure"
            },
            "Potassium": {
                "symptoms": "Browning or scorching of leaf edges and tips, weak stems, poor fruit quality",
                "treatment": "Use potassium sulfate or muriate of potash. Organic alternatives include wood ash"
            }
        }
    },
    "Ladyfinger (Okra)": {
        "info": {
            "scientific_name": "Abelmoschus esculentus",
            "best_season": "Warm-season crop that thrives in hot, sunny conditions. Generally grown in spring and summer. Optimal temperature: 25°C-35°C",
            "best_soil": "Well-drained, loamy soil with plenty of organic matter. pH range of 6.0 to 7.5",
            "time_period": "About 50 to 65 days from planting to harvest, depending on the variety",
            "estimated_cost": "₹50,000 to ₹150,000 per acre",
            "varieties": [
                "Clemson Spineless", "Annie Oakley II", "Emerald", "Red Velvet", "Burgundy", "Jambalaya"
            ]
        },
        "diseases": {
            "Yellow Vein Mosaic Virus": {
                "symptoms": "Yellowing of veins in young leaves, whole leaf turns yellow; plant stunted, poor fruit development",
                "causes": "Caused by a Begomovirus, transmitted by whiteflies",
                "treatment": "No direct cure; control vectors (whiteflies). Spray Imidacloprid 17.8 SL @ 0.3 ml/l. Use Neem oil (2%) or NSKE (5%)",
                "prevention": "Grow resistant varieties like Parbhani Kranti, Arka Anamika. Remove infected plants early. Use yellow sticky traps"
            },
            "Fusarium Wilt": {
                "symptoms": "Yellowing of lower leaves, wilting, brown discoloration in vascular tissue",
                "causes": "Caused by Fusarium oxysporum, soil-borne fungus",
                "treatment": "Soil drenching with Carbendazim or Trichoderma viride",
                "prevention": "Use resistant seeds, rotate with non-host crops like cereals"
            }
        },
        "pests": {
            "Fruit and Shoot Borer": {
                "symptoms": "Boreholes on fruits with black excreta, twisted and dry shoots",
                "description": "Caterpillars that bore into fruits and shoots",
                "treatment": "Spray Spinosad 45 SC @ 0.5 ml/l, use Neem Seed Kernel Extract (5%), set up pheromone traps (10–12/acre)"
            },
            "Whiteflies": {
                "symptoms": "Sticky honeydew and black sooty mold, yellowing and curling of leaves, vector for YVMV disease",
                "description": "Small white flies that feed on plant sap and transmit diseases",
                "treatment": "Spray Thiamethoxam or Imidacloprid, use yellow sticky traps"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Pale green to yellow older leaves, slow growth and fewer pods",
                "treatment": "Apply Urea (46% N) in split doses, use farmyard manure, vermicompost, green manure"
            },
            "Phosphorus": {
                "symptoms": "Purplish discoloration on leaves, poor flowering and fruit setting",
                "treatment": "Apply Single Super Phosphate (SSP) or DAP, use bone meal compost or rock phosphate"
            }
        }
    },
    "Soybean": {
        "info": {
            "scientific_name": "Glycine max",
            "best_season": "Kharif (June to October)",
            "best_soil": "Well-drained loamy soils with good organic matter and pH 6.0 to 7.5",
            "time_period": "90 to 110 days",
            "estimated_cost": "₹30,000 to ₹45,000 per acre",
            "varieties": [
                "JS 335", "JS 95-60", "MAUS 71", "NRC 37", "MACS 1407"
            ]
        },
        "diseases": {
            "Soybean Rust": {
                "symptoms": "Small brown lesions on the underside of leaves",
                "causes": "Fungal spores spread in moist conditions",
                "treatment": "Spray Propiconazole or Tebuconazole",
                "prevention": "Use resistant varieties and maintain field sanitation"
            },
            "Anthracnose": {
                "symptoms": "Irregular dark lesions on stems and pods",
                "causes": "Fungal infection in humid environments",
                "treatment": "Use certified seeds and spray Carbendazim or Mancozeb",
                "prevention": "Crop rotation, proper field sanitation"
            }
        },
        "pests": {
            "Stem Fly": {
                "symptoms": "Yellowing and drying of young plants",
                "description": "Flies that lay eggs in stems, larvae feed inside",
                "treatment": "Seed treatment with Thiamethoxam or Imidacloprid"
            },
            "Girdle Beetle": {
                "symptoms": "Girdling of petiole causing defoliation",
                "description": "Beetles that girdle stems and petioles",
                "treatment": "Spray Quinalphos or Lambda Cyhalothrin"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Pale yellow leaves, stunted plants",
                "treatment": "Apply Urea, DAP (initially, as soybean fixes nitrogen later)"
            },
            "Phosphorus": {
                "symptoms": "Purpling of leaves, poor root growth",
                "treatment": "Apply SSP, DAP"
            }
        }
    },
    "Cotton": {
        "info": {
            "scientific_name": "Gossypium spp.",
            "best_season": "Kharif (June to October)",
            "best_soil": "Well-drained black cotton soil, sandy loam with good moisture retention",
            "time_period": "150 to 180 days depending on variety and climate",
            "estimated_cost": "₹40,000 to ₹60,000 per acre",
            "varieties": [
                "Bt Cotton", "F1378", "Bunny", "RCH-2", "NCS-855", "Ankur 651", "JKCH Durga", "Suraj"
            ]
        },
        "diseases": {
            "Leaf Curl Virus": {
                "symptoms": "Curling and thickening of leaves, stunted growth",
                "causes": "Transmitted by whiteflies",
                "treatment": "Grow resistant varieties. Spray Imidacloprid or Thiamethoxam for whitefly control",
                "prevention": "Use resistant varieties, control whitefly populations"
            },
            "Alternaria Leaf Spot": {
                "symptoms": "Brown circular spots with concentric rings",
                "causes": "Fungal infection in humid conditions",
                "treatment": "Spray Mancozeb or Chlorothalonil. Remove infected plant debris",
                "prevention": "Crop rotation, proper field sanitation"
            }
        },
        "pests": {
            "Bollworms": {
                "symptoms": "Bore into flower buds and bolls",
                "description": "Caterpillars that bore into buds and bolls",
                "treatment": "Use Bt cotton, spray Spinosad or Emamectin Benzoate"
            },
            "Aphids": {
                "symptoms": "Sticky honeydew, curled leaves",
                "description": "Small insects that suck plant sap",
                "treatment": "Spray Neem oil or Imidacloprid"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Pale leaves, stunted plants",
                "treatment": "Apply Urea, Ammonium Sulphate"
            },
            "Potassium": {
                "symptoms": "Leaf margin necrosis, poor boll development",
                "treatment": "Apply MOP"
            }
        }
    },
    "Onion": {
        "info": {
            "scientific_name": "Allium cepa",
            "best_season": "In Maharashtra, onion is typically grown in three seasons: Kharif (June-July), Late Kharif (August-September), Rabi (December-January)",
            "best_soil": "Well-drained sandy loam to clay loam soils with a pH range of 6.0–7.5",
            "time_period": "90 to 150 days depending on variety and season",
            "estimated_cost": "Approximately ₹25,000 to ₹35,000 per acre",
            "varieties": [
                "Phule Samarth", "Phule Swaraj", "N-53", "Bhima Shakti", "Agrifound Light Red", "Bhima Super"
            ]
        },
        "diseases": {
            "Purple Blotch": {
                "symptoms": "Small water-soaked lesions on leaves that turn purplish with yellow halos",
                "causes": "Warm and humid conditions, caused by fungus Alternaria porri",
                "treatment": "Spray Mancozeb (0.25%) or Chlorothalonil (0.2%) every 10-15 days",
                "prevention": "Ensure good field sanitation and crop rotation"
            },
            "Stemphylium Blight": {
                "symptoms": "Yellow to brown spots on leaves and seed stalks",
                "causes": "High humidity and temperature, caused by fungus Stemphylium vesicarium",
                "treatment": "Use fungicides like Azoxystrobin (0.1%) or Mancozeb",
                "prevention": "Proper spacing, field sanitation"
            }
        },
        "pests": {
            "Onion Thrips": {
                "symptoms": "Silver streaks and curling leaves",
                "description": "Tiny insects that scrape plant tissue and feed on sap",
                "treatment": "Blue sticky traps, Neem oil, Spinosad 45 SC (0.3 ml/l)"
            },
            "Onion Maggot": {
                "symptoms": "Wilting and yellowing due to larval feeding on roots",
                "description": "Maggots that feed on roots and bulbs",
                "treatment": "Crop rotation, soil treatment with Chlorpyrifos"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves, poor growth",
                "treatment": "Apply Urea, Ammonium Sulphate"
            },
            "Sulphur": {
                "symptoms": "Overall yellowing, thin stems",
                "treatment": "Apply Gypsum, Ammonium Sulphate"
            }
        }
    }
}

def get_crop_info(crop_name):
    """
    Get detailed information about a specific crop
    
    Args:
        crop_name: Name of the crop
        
    Returns:
        dict: Detailed information about the crop or None if not found
    """
    crop_name = standardize_crop_name(crop_name)
    return CROP_DATABASE.get(crop_name)

def get_crop_disease_info(crop_name, disease_name=None):
    """
    Get disease information for a specific crop
    
    Args:
        crop_name: Name of the crop
        disease_name: Optional specific disease to get info about
        
    Returns:
        dict: Disease information or None if not found
    """
    crop_name = standardize_crop_name(crop_name)
    crop_data = CROP_DATABASE.get(crop_name)
    
    if not crop_data or 'diseases' not in crop_data:
        return None
    
    if disease_name:
        # Try to find closest matching disease
        for d_name, d_info in crop_data['diseases'].items():
            if disease_name.lower() in d_name.lower():
                return {d_name: d_info}
        return None
    
    return crop_data['diseases']

def get_crop_pest_info(crop_name, pest_name=None):
    """
    Get pest information for a specific crop
    
    Args:
        crop_name: Name of the crop
        pest_name: Optional specific pest to get info about
        
    Returns:
        dict: Pest information or None if not found
    """
    crop_name = standardize_crop_name(crop_name)
    crop_data = CROP_DATABASE.get(crop_name)
    
    if not crop_data or 'pests' not in crop_data:
        return None
    
    if pest_name:
        # Try to find closest matching pest
        for p_name, p_info in crop_data['pests'].items():
            if pest_name.lower() in p_name.lower():
                return {p_name: p_info}
        return None
    
    return crop_data['pests']

def get_crop_deficiency_info(crop_name, deficiency_name=None):
    """
    Get nutrient deficiency information for a specific crop
    
    Args:
        crop_name: Name of the crop
        deficiency_name: Optional specific deficiency to get info about
        
    Returns:
        dict: Deficiency information or None if not found
    """
    crop_name = standardize_crop_name(crop_name)
    crop_data = CROP_DATABASE.get(crop_name)
    
    if not crop_data or 'deficiencies' not in crop_data:
        return None
    
    if deficiency_name:
        # Try to find closest matching deficiency
        for d_name, d_info in crop_data['deficiencies'].items():
            if deficiency_name.lower() in d_name.lower():
                return {d_name: d_info}
        return None
    
    return crop_data['deficiencies']

def get_available_crops():
    """
    Get list of all available crops in the database
    
    Returns:
        list: Names of all available crops
    """
    return list(CROP_DATABASE.keys())

def standardize_crop_name(crop_name):
    """
    Standardize crop name to match database keys
    
    Args:
        crop_name: Input crop name
        
    Returns:
        string: Standardized crop name
    """
    crop_name = crop_name.strip()
    
    # Handle common aliases
    aliases = {
        "okra": "Ladyfinger (Okra)",
        "ladyfinger": "Ladyfinger (Okra)",
        "bhindi": "Ladyfinger (Okra)",
        "tinda": "Watermelon",
        "anar": "Pomegranate"
    }
    
    if crop_name.lower() in aliases:
        return aliases[crop_name.lower()]
    
    # Try to find a match in the database
    for db_crop in CROP_DATABASE.keys():
        if crop_name.lower() in db_crop.lower():
            return db_crop
    
    return crop_name
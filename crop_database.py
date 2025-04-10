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
                "causes": "Caused by the fungus Colletotrichum orbiculare, thrives in warm, humid conditions",
                "treatment": "Apply fungicides like chlorothalonil, mancozeb, or azoxystrobin at regular intervals during the growing season",
                "prevention": "Use disease-resistant varieties, practice crop rotation, avoid overhead irrigation"
            },
            "Fusarium Wilt": {
                "symptoms": "Yellowing and wilting of leaves, vascular discoloration, and eventual plant death",
                "causes": "Caused by the fungus Fusarium oxysporum f. sp. niveum, thrives in warm, sandy soils with low pH",
                "treatment": "Apply fungicides like prothioconazole through drip irrigation to reduce disease severity",
                "prevention": "Rotate with non-cucurbit crops for 5-6 years, plant resistant varieties, maintain soil pH above 6.5"
            },
            "Powdery Mildew": {
                "symptoms": "White powdery spots on leaves and stems, leads to leaf distortion and reduced photosynthesis",
                "causes": "Caused by the fungus Podosphaera xanthii, thrives in warm, dry conditions with high humidity",
                "treatment": "Use sulfur-based fungicides or systemic fungicides like azoxystrobin or myclobutanil",
                "prevention": "Plant resistant varieties, ensure proper spacing for airflow, avoid overhead irrigation"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Sticky honeydew secretions on leaves, curled or distorted leaves",
                "description": "Small soft-bodied insects that suck plant sap",
                "treatment": "Apply neem-based organic fertilizers, systemic insecticides like imidacloprid, introduce beneficial insects"
            },
            "Spider Mites": {
                "symptoms": "Fine webbing on leaves, yellow speckling or bronzing of leaves, leaf drop in severe cases",
                "description": "Tiny spider-like pests that suck plant juices, often found on leaf undersides",
                "treatment": "Apply miticides, horticultural oils, or insecticidal soaps, maintain adequate humidity"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves, stunted growth, and reduced foliage",
                "treatment": "Apply nitrogen-rich fertilizers like urea or ammonium nitrate, or organic options like composted manure"
            },
            "Potassium": {
                "symptoms": "Browning or scorching of leaf edges and tips, weak stems, and poor fruit quality",
                "treatment": "Use potassium sulfate or muriate of potash, or organic alternatives like wood ash or banana peels"
            },
            "Calcium": {
                "symptoms": "Distorted young leaves, yellow or brown spots, and cracking of fruits",
                "treatment": "Add lime, gypsum, or crushed eggshells to the soil, use calcium-rich compost"
            }
        }
    },
    "Pomegranate": {
        "info": {
            "scientific_name": "Punica granatum",
            "best_season": "Thrives in semi-arid and tropical climates. Best planted during monsoon (June to August) or spring (February to March) with irrigation",
            "best_soil": "Grows well in sandy loam to black soil with pH 6.0-7.5. Well-drained soil is essential to avoid waterlogging",
            "time_period": "Starts bearing fruits 2-3 years after planting. Fruits are harvested 5-7 months after flowering",
            "estimated_cost": "₹80,000–₹1,60,000 per acre",
            "varieties": [
                "Bhagwa", "Ganesh", "Arakta", "Mridula", "Kandhari", "Wonderful"
            ]
        },
        "diseases": {
            "Cercospora Fruit Spot": {
                "symptoms": "Yellowish spots with halos on leaves and fruits, which turn black and corky. Severe infections cause defoliation",
                "causes": "Caused by the fungus Cercospora punicae, thrives in warm, humid conditions",
                "treatment": "Apply fungicides like Hexaconazole (0.1%) or Carbendazim (0.1%), use Mancozeb (0.25%) or Propiconazole (0.1%)",
                "prevention": "Use pathogen-free planting material, prune infected parts, ensure proper spacing and airflow"
            },
            "Anthracnose": {
                "symptoms": "Leaf blight, dark brown lesions on fruits with concentric rings, dieback of twigs",
                "causes": "Caused by the fungus Colletotrichum gloeosporioides, spreads through wind, rain, and infected plant debris",
                "treatment": "Apply copper fungicides, use Mancozeb (0.25%) or Propiconazole (0.1%)",
                "prevention": "Use disease-free planting material, remove infected plant parts, improve airflow"
            },
            "Alternaria Leaf Spot": {
                "symptoms": "Circular brown spots with concentric rings on leaves, leading to defoliation",
                "causes": "Caused by the fungus Alternaria alternata, thrives in warm, humid conditions",
                "treatment": "Apply fungicides like Mancozeb or Chlorothalonil at recommended doses",
                "prevention": "Use certified disease-free material, avoid overhead irrigation, remove infected debris"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Curled leaves, stunted growth, honeydew secretion on leaves",
                "description": "Small soft-bodied insects that suck plant sap",
                "treatment": "Apply neem oil, insecticidal soap, or imidacloprid. Encourage natural predators like ladybugs"
            },
            "Fruit Borer": {
                "symptoms": "Holes in fruits, larval feeding damage, fruit drop",
                "description": "Caterpillars that bore into fruits and feed on the pulp",
                "treatment": "Apply Bacillus thuringiensis (Bt), spinosad, or carbaryl. Use pheromone traps for monitoring"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves, stunted growth, reduced foliage and fruit yield",
                "treatment": "Apply nitrogen-rich fertilizers like urea or ammonium nitrate, or organic alternatives like compost"
            },
            "Zinc": {
                "symptoms": "Small, narrow leaves, shortened internodes, chlorosis between veins",
                "treatment": "Apply zinc sulfate as foliar spray or soil application, use organic composts with zinc additives"
            },
            "Iron": {
                "symptoms": "Interveinal chlorosis in young leaves while veins remain green",
                "treatment": "Apply iron chelates or ferrous sulfate as foliar spray, improve soil organic matter"
            }
        }
    },
    "Bottle Gourd": {
        "info": {
            "scientific_name": "Lagenaria siceraria",
            "best_season": "Summer season crop that grows well in warm temperatures between 25°C to 35°C. Best planted from February to July in most regions",
            "best_soil": "Well-drained sandy loam to loamy soil with good organic matter content. Soil pH of 6.5-7.5 is ideal",
            "time_period": "Flowering begins 40-45 days after planting. Fruits are ready for harvest in 60-70 days from sowing",
            "estimated_cost": "₹40,000 to ₹60,000 per acre",
            "varieties": [
                "Pusa Naveen", "Pusa Sandesh", "Pusa Summer Prolific Long", "Punjab Komal", "Arka Bahar"
            ]
        },
        "diseases": {
            "Powdery Mildew": {
                "symptoms": "White powdery patches on leaves and stems that gradually cover entire surfaces. Leads to leaf yellowing, withering, and reduced yield",
                "causes": "Fungal disease caused by Erysiphe cichoracearum, favored by warm, dry days and cool, humid nights",
                "treatment": "Apply sulfur-based fungicides or systemic fungicides like Myclobutanil. Organic options include neem oil or potassium bicarbonate sprays",
                "prevention": "Proper plant spacing, avoid overhead irrigation, remove infected plants, and practice crop rotation"
            },
            "Downy Mildew": {
                "symptoms": "Yellow or pale green spots on upper leaf surfaces with grayish-white fungal growth on the undersides. Leaves eventually turn brown and die",
                "causes": "Caused by Pseudoperonospora cubensis, favored by cool, wet conditions with high humidity",
                "treatment": "Apply copper-based fungicides or specific downy mildew fungicides like Mancozeb or Metalaxyl",
                "prevention": "Provide good air circulation, avoid overhead irrigation, remove crop debris after harvest"
            },
            "Fusarium Wilt": {
                "symptoms": "Yellowing and wilting of leaves, brown discoloration of vascular tissue, stunted growth, and eventual plant death",
                "causes": "Soil-borne fungal pathogen Fusarium oxysporum that invades through roots and blocks water transport",
                "treatment": "No effective chemical treatment once infected. Use resistant varieties and soil solarization",
                "prevention": "Use disease-free seeds, practice crop rotation with non-host crops, manage soil pH and drainage"
            }
        },
        "pests": {
            "Red Pumpkin Beetle": {
                "symptoms": "Holes in leaves, damaged seedlings, reduced plant vigor",
                "description": "Small red-brown beetles that feed on leaves and flowers",
                "treatment": "Apply neem oil, spinosad, or carbaryl. Use row covers for young plants"
            },
            "Fruit Fly": {
                "symptoms": "Small punctures on fruits, maggots inside fruits, fruit rotting",
                "description": "Small flies that lay eggs in young fruits, larvae feed inside fruit causing rot",
                "treatment": "Use fruit fly traps with methyl eugenol, cover young fruits with paper bags, apply malathion or spinosad as needed"
            },
            "Aphids": {
                "symptoms": "Curled leaves, stunted growth, sticky honeydew on leaves",
                "description": "Small soft-bodied insects that suck plant sap, often clustered on new growth",
                "treatment": "Spray insecticidal soap, neem oil, or imidacloprid. Encourage natural predators like ladybugs"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves, stunted growth, thin stems, and poor fruit development",
                "treatment": "Apply nitrogen-rich fertilizers like urea or ammonium sulfate. Organic alternatives include compost or well-rotted manure"
            },
            "Calcium": {
                "symptoms": "Blossom end rot in fruits, distorted new leaves, poor root development",
                "treatment": "Apply calcium nitrate as foliar spray or soil application. Add lime or gypsum to calcium-deficient soils"
            },
            "Boron": {
                "symptoms": "Cracked fruits, hollow stems, stunted growth, and thickened leaves",
                "treatment": "Apply borax or solubor as foliar spray at very low concentrations (0.1-0.2%)"
            }
        }
    },
    "Cluster Beans": {
        "info": {
            "scientific_name": "Cyamopsis tetragonoloba",
            "best_season": "Summer season crop, preferably grown from March to July. Requires warm weather with temperatures between 25°C to 35°C",
            "best_soil": "Well-drained sandy loam to medium black soils. Tolerates slight salinity and alkalinity. Ideal pH range of 7.0-8.0",
            "time_period": "First picking starts 45-60 days after sowing. Harvesting period extends for about 3-4 months",
            "estimated_cost": "₹25,000 to ₹35,000 per acre",
            "varieties": [
                "Pusa Navbahar", "Pusa Sadabahar", "Durgapura Safed", "Durgapura Kanti", "HG-75"
            ]
        },
        "diseases": {
            "Bacterial Blight": {
                "symptoms": "Water-soaked lesions on leaves that turn brown with yellow halos. Severe infections cause defoliation",
                "causes": "Caused by Xanthomonas axonopodis pv. cyamopsidis, spreads through wind, rain, and infected seeds",
                "treatment": "Apply copper-based bactericides like copper oxychloride. Streptocycline can be effective when applied early",
                "prevention": "Use disease-free seeds, practice crop rotation, avoid overhead irrigation, remove infected plants"
            },
            "Powdery Mildew": {
                "symptoms": "White powdery growth on leaves, stems, and pods. Affected leaves become yellow and may fall prematurely",
                "causes": "Fungal disease caused by Leveillula taurica or Erysiphe polygoni, favored by moderate temperatures and high humidity",
                "treatment": "Apply sulfur-based fungicides or wettable sulfur. Organic options include neem oil or potassium bicarbonate",
                "prevention": "Provide adequate spacing between plants, avoid excessive nitrogen fertilization"
            },
            "Alternaria Leaf Spot": {
                "symptoms": "Brown circular spots with concentric rings on leaves. Severe cases lead to defoliation",
                "causes": "Caused by Alternaria cucumerina, thrives in warm, humid conditions with alternating wet and dry periods",
                "treatment": "Apply mancozeb or copper oxychloride at recommended doses",
                "prevention": "Crop rotation, proper field sanitation, use of disease-free seeds"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Curled leaves, stunted growth, honeydew secretion, and black sooty mold",
                "description": "Small soft-bodied insects that suck plant sap from tender shoots and leaves",
                "treatment": "Apply neem oil, insecticidal soap, or imidacloprid. Encourage natural predators like ladybugs"
            },
            "Pod Borer": {
                "symptoms": "Holes in pods, damaged seeds, frass (excrement) visible near entry holes",
                "description": "Caterpillars that bore into pods and feed on developing seeds",
                "treatment": "Apply Bacillus thuringiensis (Bt), spinosad, or neem-based insecticides. Use pheromone traps for monitoring"
            },
            "Jassids": {
                "symptoms": "Yellowing of leaf margins, leaf curling, 'hopper burn' where leaf edges turn brown",
                "description": "Small, wedge-shaped green insects that hop or fly when disturbed",
                "treatment": "Apply imidacloprid, thiamethoxam, or neem oil. Avoid water stress as it increases susceptibility"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Pale green or yellow older leaves, stunted growth, reduced branching and yield",
                "treatment": "Apply nitrogen fertilizers like urea, ammonium sulfate, or organic sources like compost and well-rotted manure"
            },
            "Iron": {
                "symptoms": "Interveinal chlorosis (yellowing between veins) in young leaves while veins remain green",
                "treatment": "Apply ferrous sulfate as foliar spray or use iron chelates for soil application"
            },
            "Zinc": {
                "symptoms": "Small, narrow leaves, shortened internodes, rosetting of terminal leaves",
                "treatment": "Apply zinc sulfate as foliar spray or soil application. Organic alternatives include composted manure with zinc additives"
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
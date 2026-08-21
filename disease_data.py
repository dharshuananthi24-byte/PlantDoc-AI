# ============================================================
# disease_data.py
# Contains comprehensive information about all 38 PlantVillage
# disease classes: description, causes, and cure recommendations
# ============================================================

DISEASE_DATA = {
    "Apple___Apple_scab": {
        "name": "Apple Scab",
        "plant": "Apple",
        "description": "Apple scab is a common fungal disease caused by Venturia inaequalis. It creates dark, scaly lesions on leaves and fruit, causing significant crop loss if untreated.",
        "causes": [
            "Fungus Venturia inaequalis",
            "Cool, wet spring weather",
            "Poor air circulation",
            "Infected leaf debris left on ground"
        ],
        "organic_treatment": [
            "Apply neem oil spray every 7–14 days during wet weather",
            "Use sulfur-based fungicide (organic-approved)",
            "Remove and destroy infected leaves immediately",
            "Rake and compost fallen leaves away from the base"
        ],
        "chemical_treatment": [
            "Apply captan fungicide at bud break",
            "Use myclobutanil (Rally) or mancozeb",
            "Spray fungicide every 7 days during infection periods",
            "Rotate fungicide classes to prevent resistance"
        ],
        "prevention": [
            "Plant scab-resistant apple varieties (Liberty, Redfree)",
            "Prune trees for better air circulation",
            "Apply lime sulfur during dormant season",
            "Avoid overhead irrigation; use drip irrigation"
        ],
        "severity": "Medium",
        "icon": "🍎"
    },

    "Apple___Black_rot": {
        "name": "Apple Black Rot",
        "plant": "Apple",
        "description": "Black rot is a serious fungal disease caused by Botryosphaeria obtusa, causing frogeye leaf spots, rotting fruit, and limb cankers.",
        "causes": [
            "Fungus Botryosphaeria obtusa",
            "Warm, humid weather (75–85°F)",
            "Wounds from insects or pruning",
            "Infected mummified fruit left on tree"
        ],
        "organic_treatment": [
            "Prune out and destroy all infected wood",
            "Remove mummified fruit from the tree and ground",
            "Apply copper-based fungicide",
            "Use neem oil as a preventive spray"
        ],
        "chemical_treatment": [
            "Apply thiophanate-methyl at petal fall",
            "Use captan + mancozeb combination",
            "Spray ziram during early fruit development",
            "Apply systemic fungicides to canker areas"
        ],
        "prevention": [
            "Remove all dead wood and mummified fruits annually",
            "Disinfect pruning tools between cuts",
            "Maintain tree vigor through proper fertilization",
            "Avoid injuring bark during cultivation"
        ],
        "severity": "High",
        "icon": "🍎"
    },

    "Apple___Cedar_apple_rust": {
        "name": "Cedar Apple Rust",
        "plant": "Apple",
        "description": "A fungal disease requiring two host plants (cedar/juniper and apple) to complete its lifecycle. Creates bright orange-yellow spots on apple leaves and fruit.",
        "causes": [
            "Fungus Gymnosporangium juniperi-virginianae",
            "Nearby cedar or juniper trees",
            "Warm temperatures (46–75°F) with moisture",
            "Wind spreading spores from cedars to apples"
        ],
        "organic_treatment": [
            "Remove nearby eastern red cedar trees if feasible",
            "Apply sulfur-based fungicide from pink stage through 3rd cover",
            "Use neem oil starting at green tip stage",
            "Remove galls from cedar trees in late winter"
        ],
        "chemical_treatment": [
            "Apply myclobutanil from pink bud through 2nd cover spray",
            "Use propiconazole or triadimefon fungicide",
            "Spray at 7–10 day intervals during wet springs",
            "Use trifloxystrobin (Flint) for systemic protection"
        ],
        "prevention": [
            "Plant rust-resistant apple varieties",
            "Remove cedar galls before they mature (late winter)",
            "Plant apples far from cedar/juniper trees",
            "Apply dormant season spray"
        ],
        "severity": "Medium",
        "icon": "🍎"
    },

    "Apple___healthy": {
        "name": "Healthy Apple",
        "plant": "Apple",
        "description": "Your apple plant appears healthy with no signs of disease. Continue your current care routine.",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Maintain regular watering schedule",
            "Fertilize appropriately in spring",
            "Monitor regularly for early signs of disease",
            "Prune annually for good air circulation"
        ],
        "severity": "None",
        "icon": "✅"
    },

    "Blueberry___healthy": {
        "name": "Healthy Blueberry",
        "plant": "Blueberry",
        "description": "Your blueberry plant is healthy! Keep up the good work with your current care practices.",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Maintain soil pH between 4.5–5.5",
            "Mulch to retain moisture",
            "Prune old canes after harvest",
            "Water consistently, avoid waterlogging"
        ],
        "severity": "None",
        "icon": "✅"
    },

    "Cherry_(including_sour)___Powdery_mildew": {
        "name": "Cherry Powdery Mildew",
        "plant": "Cherry",
        "description": "Powdery mildew appears as white powdery spots on leaves, shoots, and fruit. It stunts growth and reduces fruit quality.",
        "causes": [
            "Fungus Podosphaera clandestina",
            "High humidity with dry conditions",
            "Moderate temperatures (60–80°F)",
            "Overcrowded plants with poor air flow"
        ],
        "organic_treatment": [
            "Spray with baking soda solution (1 tbsp per gallon water)",
            "Apply potassium bicarbonate spray",
            "Use neem oil every 7–14 days",
            "Apply sulfur-based organic fungicide"
        ],
        "chemical_treatment": [
            "Apply trifloxystrobin at first sign of disease",
            "Use myclobutanil or propiconazole",
            "Spray difenoconazole before infection",
            "Apply systemic fungicide at 10–14 day intervals"
        ],
        "prevention": [
            "Prune to improve air circulation",
            "Plant resistant cherry varieties",
            "Avoid excess nitrogen fertilization",
            "Apply dormant oil spray in early spring"
        ],
        "severity": "Medium",
        "icon": "🍒"
    },

    "Cherry_(including_sour)___healthy": {
        "name": "Healthy Cherry",
        "plant": "Cherry",
        "description": "Your cherry plant looks perfectly healthy! No disease detected.",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Water at base to keep foliage dry",
            "Thin fruit to reduce disease pressure",
            "Annual dormant pruning",
            "Apply balanced fertilizer in spring"
        ],
        "severity": "None",
        "icon": "✅"
    },

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "name": "Corn Gray Leaf Spot",
        "plant": "Corn (Maize)",
        "description": "Gray leaf spot is one of the most significant yield-limiting diseases of corn. It creates rectangular gray-to-brown lesions on leaves, reducing photosynthesis.",
        "causes": [
            "Fungus Cercospora zeae-maydis",
            "Warm temperatures (75–95°F) with high humidity",
            "Corn residue left in field",
            "Continuous corn cropping"
        ],
        "organic_treatment": [
            "Remove and destroy infected plant material",
            "Rotate crops — avoid continuous corn",
            "Apply copper-based fungicide",
            "Use resistant hybrid varieties"
        ],
        "chemical_treatment": [
            "Apply strobilurin fungicide (azoxystrobin) at silking",
            "Use propiconazole at VT/R1 growth stage",
            "Apply trifloxystrobin + propiconazole combination",
            "Spray preventively when disease pressure is high"
        ],
        "prevention": [
            "Choose resistant corn hybrids",
            "Rotate with soybeans or other non-host crops",
            "Till residue to reduce inoculum",
            "Avoid planting in poorly drained fields"
        ],
        "severity": "High",
        "icon": "🌽"
    },

    "Corn_(maize)___Common_rust_": {
        "name": "Corn Common Rust",
        "plant": "Corn (Maize)",
        "description": "Common rust produces brick-red to brown pustules on both leaf surfaces. Severe infections cause premature leaf death and yield loss.",
        "causes": [
            "Fungus Puccinia sorghi",
            "Cool temperatures (60–77°F)",
            "High humidity and wet weather",
            "Wind-dispersed spores"
        ],
        "organic_treatment": [
            "Apply neem oil spray on affected plants",
            "Use sulfur-based fungicide as organic option",
            "Remove heavily infected leaves",
            "Improve field air circulation through proper spacing"
        ],
        "chemical_treatment": [
            "Apply azoxystrobin at first sign of rust",
            "Use trifloxystrobin fungicide",
            "Spray propiconazole preventively",
            "Apply fungicide at VT stage for best protection"
        ],
        "prevention": [
            "Plant rust-resistant corn hybrids",
            "Monitor fields from V6 stage onward",
            "Avoid planting when cool wet weather is forecast",
            "Maintain proper plant spacing"
        ],
        "severity": "Medium",
        "icon": "🌽"
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "name": "Corn Northern Leaf Blight",
        "plant": "Corn (Maize)",
        "description": "Northern Leaf Blight creates long, cigar-shaped gray-green lesions on corn leaves. It can cause up to 50% yield loss in severe cases.",
        "causes": [
            "Fungus Exserohilum turcicum",
            "Moderate temperatures (65–80°F)",
            "Extended wet periods (leaf wetness >6 hrs)",
            "Infected crop residue in soil"
        ],
        "organic_treatment": [
            "Remove and destroy infected leaves",
            "Crop rotation with non-host crops",
            "Apply copper hydroxide fungicide",
            "Ensure proper field drainage"
        ],
        "chemical_treatment": [
            "Apply propiconazole or tebuconazole",
            "Use azoxystrobin + propiconazole (Quilt)",
            "Spray at VT/R1 stage when disease is present",
            "Apply every 14 days if conditions favor disease"
        ],
        "prevention": [
            "Use NLB-resistant hybrid varieties",
            "Rotate crops every 1–2 seasons",
            "Plow under residue after harvest",
            "Apply balanced nitrogen — avoid excess"
        ],
        "severity": "High",
        "icon": "🌽"
    },

    "Corn_(maize)___healthy": {
        "name": "Healthy Corn",
        "plant": "Corn (Maize)",
        "description": "Your corn plant appears healthy and vigorous. No disease detected.",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Maintain proper plant spacing (8–12 inches)",
            "Fertilize based on soil test",
            "Scout regularly for pests and disease",
            "Rotate crops each season"
        ],
        "severity": "None",
        "icon": "✅"
    },

    "Grape___Black_rot": {
        "name": "Grape Black Rot",
        "plant": "Grape",
        "description": "Black rot is the most destructive grape disease in humid regions. It destroys fruit and creates reddish-brown leaf lesions with black dots.",
        "causes": [
            "Fungus Guignardia bidwellii",
            "Warm temperatures (60–90°F)",
            "Wet weather during early fruit development",
            "Infected mummified berries"
        ],
        "organic_treatment": [
            "Remove all mummified berries from vines and ground",
            "Apply copper-based fungicide in early spring",
            "Use sulfur spray at 10-day intervals",
            "Improve canopy airflow through pruning"
        ],
        "chemical_treatment": [
            "Apply myclobutanil (Rally) from pre-bloom through berry set",
            "Use mancozeb preventively",
            "Apply thiophanate-methyl at bloom",
            "Spray ziram or captan during wet periods"
        ],
        "prevention": [
            "Prune vines to allow air and sunlight penetration",
            "Remove and destroy all infected material",
            "Train vines on trellises for better airflow",
            "Apply dormant copper spray before bud break"
        ],
        "severity": "High",
        "icon": "🍇"
    },

    "Grape___Esca_(Black_Measles)": {
        "name": "Grape Esca (Black Measles)",
        "plant": "Grape",
        "description": "Esca is a complex grapevine trunk disease causing tiger-striped leaves, shriveled berries (black measles), and eventual vine death.",
        "causes": [
            "Multiple fungi (Phaeomoniella, Phaeoacremonium)",
            "Pruning wounds that are not sealed",
            "Old vines (>10 years)",
            "Stressful weather conditions"
        ],
        "organic_treatment": [
            "Apply Trichoderma-based biological fungicide to pruning wounds",
            "Remove and destroy infected wood",
            "Paint pruning cuts with wound sealant",
            "Avoid pruning during wet weather"
        ],
        "chemical_treatment": [
            "Apply thiophanate-methyl to fresh pruning cuts",
            "Use tebuconazole as a wound protectant",
            "Inject trunk with phosphorous acid (severe cases)",
            "Apply systemic fungicide at dormant stage"
        ],
        "prevention": [
            "Seal all pruning wounds immediately",
            "Prune during dry weather",
            "Replace old, infected vines",
            "Use sharp, sterilized pruning tools"
        ],
        "severity": "High",
        "icon": "🍇"
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "name": "Grape Leaf Blight",
        "plant": "Grape",
        "description": "Isariopsis leaf spot creates dark brown spots with yellow halos on upper leaf surfaces, causing premature defoliation and reduced fruit quality.",
        "causes": [
            "Fungus Isariopsis clavispora",
            "Warm, humid conditions",
            "Poor air circulation in canopy",
            "Water splashing infected soil onto leaves"
        ],
        "organic_treatment": [
            "Apply copper-based organic fungicide",
            "Remove infected leaves and destroy them",
            "Use neem oil spray every 7–10 days",
            "Apply sulfur dust on affected areas"
        ],
        "chemical_treatment": [
            "Spray mancozeb or ziram",
            "Apply tebuconazole at disease onset",
            "Use foliar fungicide at 10-day intervals",
            "Apply captan + sulfur combination"
        ],
        "prevention": [
            "Ensure proper vine spacing for air circulation",
            "Avoid overhead irrigation",
            "Apply mulch to reduce soil splash",
            "Scout vines weekly during growing season"
        ],
        "severity": "Medium",
        "icon": "🍇"
    },

    "Grape___healthy": {
        "name": "Healthy Grape",
        "plant": "Grape",
        "description": "Your grapevine is healthy! No disease detected. Maintain your current care routine.",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Annual dormant pruning",
            "Train vines on trellis system",
            "Monitor for pest pressure",
            "Fertilize moderately in spring"
        ],
        "severity": "None",
        "icon": "✅"
    },

    "Orange___Haunglongbing_(Citrus_greening)": {
        "name": "Citrus Greening (HLB)",
        "plant": "Orange",
        "description": "Huanglongbing (HLB) is the most devastating citrus disease worldwide. It causes yellowing (blotchy mottle), misshapen bitter fruit, and eventual tree death. Currently has no cure.",
        "causes": [
            "Bacteria Candidatus Liberibacter asiaticus",
            "Asian citrus psyllid insect vector",
            "Infected planting material",
            "Spread through grafting"
        ],
        "organic_treatment": [
            "Control psyllid populations with organic insecticidal soap",
            "Apply kaolin clay to deter psyllids",
            "Remove and destroy infected trees immediately",
            "Release beneficial insects to control psyllid populations"
        ],
        "chemical_treatment": [
            "Apply imidacloprid systemic insecticide for psyllid control",
            "Use drenching with thermotherapy (trunk injection)",
            "Apply antimicrobial compounds (oxytetracycline) — slows disease",
            "Spray abamectin for psyllid management"
        ],
        "prevention": [
            "Only plant certified disease-free nursery stock",
            "Install psyllid monitoring traps",
            "Quarantine new plant material before planting",
            "Report suspected HLB trees to local agriculture authority immediately"
        ],
        "severity": "Critical",
        "icon": "🍊"
    },

    "Peach___Bacterial_spot": {
        "name": "Peach Bacterial Spot",
        "plant": "Peach",
        "description": "Bacterial spot causes water-soaked lesions on leaves, fruit, and twigs. It leads to defoliation, cracked fruit, and reduced yield.",
        "causes": [
            "Bacteria Xanthomonas arboricola pv. pruni",
            "Warm, rainy weather (65–90°F)",
            "High humidity and wind",
            "Wounds from insects or hail"
        ],
        "organic_treatment": [
            "Apply copper-based bactericide in early spring",
            "Remove infected twigs and leaves",
            "Avoid overhead irrigation",
            "Apply Bacillus subtilis biological spray"
        ],
        "chemical_treatment": [
            "Apply oxytetracycline at petal fall and through summer",
            "Use copper hydroxide during dormant season",
            "Spray copper + mancozeb combination",
            "Apply every 7–10 days during wet, warm weather"
        ],
        "prevention": [
            "Plant resistant peach varieties",
            "Prune to improve air circulation",
            "Avoid overhead irrigation systems",
            "Apply dormant copper spray annually"
        ],
        "severity": "Medium",
        "icon": "🍑"
    },

    "Peach___healthy": {
        "name": "Healthy Peach",
        "plant": "Peach",
        "description": "Your peach tree is healthy with no signs of disease!",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Annual dormant pruning",
            "Apply balanced fertilizer in spring",
            "Thin fruit for better sizing",
            "Monitor for peach borers and aphids"
        ],
        "severity": "None",
        "icon": "✅"
    },

    "Pepper,_bell___Bacterial_spot": {
        "name": "Bell Pepper Bacterial Spot",
        "plant": "Bell Pepper",
        "description": "Bacterial spot creates water-soaked, greasy-looking lesions on leaves and raised, scab-like spots on fruit, causing defoliation and fruit loss.",
        "causes": [
            "Bacteria Xanthomonas campestris pv. vesicatoria",
            "Warm, wet weather",
            "Infected seed or transplants",
            "Splashing water"
        ],
        "organic_treatment": [
            "Apply copper-based bactericide at first symptoms",
            "Remove and destroy infected plant material",
            "Use drip irrigation to keep leaves dry",
            "Spray Bacillus subtilis biological control"
        ],
        "chemical_treatment": [
            "Apply copper hydroxide + mancozeb",
            "Use copper octanoate spray",
            "Spray at 5–7 day intervals during wet weather",
            "Apply acibenzolar-S-methyl (Actigard) as plant activator"
        ],
        "prevention": [
            "Use certified disease-free seed",
            "Avoid working in field when plants are wet",
            "Rotate crops — no peppers or tomatoes for 2–3 years",
            "Mulch to reduce soil splash"
        ],
        "severity": "Medium",
        "icon": "🫑"
    },

    "Pepper,_bell___healthy": {
        "name": "Healthy Bell Pepper",
        "plant": "Bell Pepper",
        "description": "Your bell pepper plant looks perfectly healthy!",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Water at base, not on leaves",
            "Stake plants to prevent stem breakage",
            "Fertilize every 3–4 weeks",
            "Monitor for aphids and spider mites"
        ],
        "severity": "None",
        "icon": "✅"
    },

    "Potato___Early_blight": {
        "name": "Potato Early Blight",
        "plant": "Potato",
        "description": "Early blight causes dark brown concentric ring lesions (target-board pattern) on lower leaves first. It reduces yield and tuber quality significantly.",
        "causes": [
            "Fungus Alternaria solani",
            "Warm temperatures (75–85°F)",
            "Alternating wet and dry conditions",
            "Plant stress from nutrient deficiency"
        ],
        "organic_treatment": [
            "Apply copper-based fungicide at first sign",
            "Use neem oil spray every 7–10 days",
            "Remove infected lower leaves promptly",
            "Apply compost tea as foliar spray"
        ],
        "chemical_treatment": [
            "Apply chlorothalonil (Bravo) preventively",
            "Use mancozeb + metalaxyl combination",
            "Spray azoxystrobin for systemic protection",
            "Apply every 7–10 days during wet weather"
        ],
        "prevention": [
            "Rotate potatoes with non-solanaceous crops (3-year rotation)",
            "Use certified disease-free seed potatoes",
            "Avoid overhead irrigation",
            "Ensure adequate potassium and calcium nutrition"
        ],
        "severity": "Medium",
        "icon": "🥔"
    },

    "Potato___Late_blight": {
        "name": "Potato Late Blight",
        "plant": "Potato",
        "description": "Late blight is the disease that caused the Irish Potato Famine. It creates large, water-soaked lesions with white mold and can destroy an entire crop in days.",
        "causes": [
            "Oomycete Phytophthora infestans",
            "Cool temperatures (50–70°F) with high humidity",
            "Extended leaf wetness periods",
            "Infected seed tubers or volunteer plants"
        ],
        "organic_treatment": [
            "Apply copper-based fungicide (copper sulfate) immediately",
            "Remove and destroy all infected plant material",
            "Avoid overhead watering completely",
            "Apply Bacillus subtilis-based biological spray"
        ],
        "chemical_treatment": [
            "Apply mancozeb + metalaxyl (Ridomil Gold)",
            "Use cymoxanil + mancozeb combination",
            "Spray chlorothalonil every 5–7 days",
            "Apply dimethomorph for systemic control"
        ],
        "prevention": [
            "Plant resistant varieties (Sarpo Mira, Cara)",
            "Use only certified disease-free seed tubers",
            "Hill soil over tubers to protect them",
            "Monitor local blight forecasting services"
        ],
        "severity": "Critical",
        "icon": "🥔"
    },

    "Potato___healthy": {
        "name": "Healthy Potato",
        "plant": "Potato",
        "description": "Your potato plant is healthy with no signs of disease!",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Use certified seed potatoes",
            "Hill soil every 2–3 weeks",
            "Maintain adequate moisture",
            "Rotate crops annually"
        ],
        "severity": "None",
        "icon": "✅"
    },

    "Raspberry___healthy": {
        "name": "Healthy Raspberry",
        "plant": "Raspberry",
        "description": "Your raspberry plant is healthy! No disease detected.",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Remove old floricanes after fruiting",
            "Provide proper trellis support",
            "Mulch heavily around base",
            "Water consistently but avoid waterlogging"
        ],
        "severity": "None",
        "icon": "✅"
    },

    "Soybean___healthy": {
        "name": "Healthy Soybean",
        "plant": "Soybean",
        "description": "Your soybean plant appears healthy with no signs of disease.",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Rotate with corn or small grains",
            "Scout fields regularly for pests",
            "Use inoculated seed for nitrogen fixation",
            "Maintain proper row spacing"
        ],
        "severity": "None",
        "icon": "✅"
    },

    "Squash___Powdery_mildew": {
        "name": "Squash Powdery Mildew",
        "plant": "Squash",
        "description": "Powdery mildew covers squash leaves with white, talcum-like powder. It weakens plants and reduces fruit production.",
        "causes": [
            "Fungus Podosphaera xanthii or Erysiphe cichoracearum",
            "Warm dry days with cool humid nights",
            "Dense plant growth with poor airflow",
            "High nitrogen fertilization"
        ],
        "organic_treatment": [
            "Spray baking soda solution (1 tbsp + 1 tsp liquid soap per gallon)",
            "Apply diluted milk spray (40% milk, 60% water)",
            "Use neem oil every 7 days",
            "Apply potassium bicarbonate spray"
        ],
        "chemical_treatment": [
            "Apply myclobutanil or trifloxystrobin",
            "Use sulfur-based fungicide (not in heat >90°F)",
            "Spray azoxystrobin at first sign of infection",
            "Apply every 7–14 days as needed"
        ],
        "prevention": [
            "Plant resistant varieties when possible",
            "Space plants for good air circulation",
            "Avoid excessive nitrogen fertilization",
            "Water in the morning so leaves dry quickly"
        ],
        "severity": "Medium",
        "icon": "🥒"
    },

    "Strawberry___Leaf_scorch": {
        "name": "Strawberry Leaf Scorch",
        "plant": "Strawberry",
        "description": "Leaf scorch creates small, dark purple spots that enlarge and merge, giving leaves a 'scorched' appearance. It weakens plants over multiple seasons.",
        "causes": [
            "Fungus Diplocarpon earlianum",
            "Cool, wet spring weather",
            "Infected plant material",
            "Overhead irrigation"
        ],
        "organic_treatment": [
            "Remove and destroy infected leaves",
            "Apply copper-based fungicide",
            "Use neem oil spray every 10 days",
            "Renovate planting after harvest"
        ],
        "chemical_treatment": [
            "Apply captan fungicide from bloom to harvest",
            "Use myclobutanil during renovation",
            "Spray thiram at bloom time",
            "Apply every 7–10 days during wet conditions"
        ],
        "prevention": [
            "Plant disease-resistant strawberry varieties",
            "Renovate beds annually after harvest",
            "Mulch to reduce soil splash",
            "Use drip irrigation instead of overhead"
        ],
        "severity": "Medium",
        "icon": "🍓"
    },

    "Strawberry___healthy": {
        "name": "Healthy Strawberry",
        "plant": "Strawberry",
        "description": "Your strawberry plant is healthy! Keep up the good care.",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Renovate beds after harvest",
            "Mulch in winter to protect crowns",
            "Remove runners to focus energy on berries",
            "Fertilize lightly after harvest"
        ],
        "severity": "None",
        "icon": "✅"
    },

    "Tomato___Bacterial_spot": {
        "name": "Tomato Bacterial Spot",
        "plant": "Tomato",
        "description": "Bacterial spot causes water-soaked spots on leaves, stems, and fruit. It's one of the most common and destructive tomato diseases in warm, wet climates.",
        "causes": [
            "Bacteria Xanthomonas vesicatoria",
            "Warm, wet weather (75–86°F)",
            "Infected seed or transplants",
            "Rain, wind, or irrigation splash"
        ],
        "organic_treatment": [
            "Apply copper-based bactericide at first symptom",
            "Remove infected lower leaves",
            "Avoid overhead watering",
            "Use Bacillus subtilis spray (Serenade)"
        ],
        "chemical_treatment": [
            "Spray copper hydroxide + mancozeb weekly",
            "Apply acibenzolar-S-methyl (Actigard) as plant activator",
            "Use fixed copper compounds every 5–7 days",
            "Combine copper with antibiotics in severe cases"
        ],
        "prevention": [
            "Use certified disease-free seeds or transplants",
            "Rotate tomatoes with non-solanaceous crops",
            "Stake and prune for air circulation",
            "Mulch to reduce soil splash onto leaves"
        ],
        "severity": "High",
        "icon": "🍅"
    },

    "Tomato___Early_blight": {
        "name": "Tomato Early Blight",
        "plant": "Tomato",
        "description": "Early blight creates dark concentric ring spots (bullseye pattern) on older leaves first, causing defoliation and reducing fruit yield.",
        "causes": [
            "Fungus Alternaria solani",
            "Warm temperatures (75–85°F)",
            "High humidity",
            "Plant stress or senescence"
        ],
        "organic_treatment": [
            "Apply copper fungicide at first sign",
            "Remove infected lower leaves",
            "Spray neem oil every 7 days",
            "Use compost mulch to reduce soil splash"
        ],
        "chemical_treatment": [
            "Apply chlorothalonil (Daconil) preventively",
            "Use mancozeb from transplanting onward",
            "Spray azoxystrobin (Quadris) for systemic control",
            "Apply at 7–10 day intervals"
        ],
        "prevention": [
            "Rotate crops (3-year rotation)",
            "Stake plants for airflow",
            "Use drip irrigation",
            "Remove all infected debris after season"
        ],
        "severity": "Medium",
        "icon": "🍅"
    },

    "Tomato___Late_blight": {
        "name": "Tomato Late Blight",
        "plant": "Tomato",
        "description": "Late blight is an extremely destructive disease causing large, greasy, gray-green lesions on leaves and brown rot on fruit. It can destroy a crop in days.",
        "causes": [
            "Oomycete Phytophthora infestans",
            "Cool, wet weather (50–70°F)",
            "High humidity and fog",
            "Infected tomato or potato debris"
        ],
        "organic_treatment": [
            "Apply copper sulfate immediately at first sign",
            "Remove and dispose of infected plants in sealed bags",
            "Never compost infected material",
            "Apply Bacillus subtilis spray as early preventive"
        ],
        "chemical_treatment": [
            "Apply mancozeb + cymoxanil combination",
            "Use metalaxyl (Ridomil) for systemic control",
            "Spray chlorothalonil every 5–7 days",
            "Apply mandipropamid (Revus) for advanced protection"
        ],
        "prevention": [
            "Plant late blight-resistant varieties (Iron Lady, Defiant)",
            "Avoid planting near potatoes",
            "Stake and prune for excellent air circulation",
            "Monitor blight forecast alerts in your region"
        ],
        "severity": "Critical",
        "icon": "🍅"
    },

    "Tomato___Leaf_Mold": {
        "name": "Tomato Leaf Mold",
        "plant": "Tomato",
        "description": "Leaf mold creates pale green-yellow spots on upper leaf surfaces with olive-green to brown mold on lower surfaces. Common in greenhouse tomatoes.",
        "causes": [
            "Fungus Passalora fulva (Cladosporium fulvum)",
            "High humidity (>85%)",
            "Temperatures 71–75°F",
            "Poor air circulation"
        ],
        "organic_treatment": [
            "Improve ventilation in greenhouse immediately",
            "Apply copper-based fungicide",
            "Remove affected lower leaves",
            "Reduce humidity with better spacing"
        ],
        "chemical_treatment": [
            "Apply chlorothalonil preventively",
            "Use mancozeb at 7–10 day intervals",
            "Spray fenhexamid for specific control",
            "Apply trifloxystrobin in severe cases"
        ],
        "prevention": [
            "Maintain humidity below 85% in greenhouse",
            "Space plants adequately",
            "Use resistant varieties (Dotmaster, Shirley)",
            "Avoid wetting foliage during irrigation"
        ],
        "severity": "Medium",
        "icon": "🍅"
    },

    "Tomato___Septoria_leaf_spot": {
        "name": "Tomato Septoria Leaf Spot",
        "plant": "Tomato",
        "description": "Septoria leaf spot creates small circular spots with dark borders and tan centers. It starts on lower leaves and moves upward, causing severe defoliation.",
        "causes": [
            "Fungus Septoria lycopersici",
            "Warm, wet weather (60–80°F)",
            "Rain and overhead irrigation",
            "Infected crop debris in soil"
        ],
        "organic_treatment": [
            "Remove and destroy infected leaves immediately",
            "Apply copper-based fungicide every 7–10 days",
            "Mulch heavily to prevent soil splash",
            "Use neem oil as protective spray"
        ],
        "chemical_treatment": [
            "Apply chlorothalonil at first sign",
            "Use mancozeb + cymoxanil",
            "Spray azoxystrobin for systemic control",
            "Apply every 7 days in wet weather"
        ],
        "prevention": [
            "Rotate crops — no tomatoes in same bed for 3 years",
            "Remove all crop debris after harvest",
            "Stake plants to keep foliage off soil",
            "Water at base only"
        ],
        "severity": "Medium",
        "icon": "🍅"
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "name": "Tomato Spider Mites",
        "plant": "Tomato",
        "description": "Two-spotted spider mites cause yellow stippling on leaves, fine webbing on undersides, and premature leaf drop. They thrive in hot, dry conditions.",
        "causes": [
            "Pest: Tetranychus urticae (Spider Mite)",
            "Hot, dry, dusty conditions",
            "Over-use of broad-spectrum insecticides killing predators",
            "Plant stress from drought"
        ],
        "organic_treatment": [
            "Spray plants forcefully with water to dislodge mites",
            "Apply insecticidal soap every 3–5 days",
            "Use neem oil spray on leaf undersides",
            "Release predatory mites (Phytoseiidae) as biological control"
        ],
        "chemical_treatment": [
            "Apply abamectin (Agri-Mek) miticide",
            "Use bifenazate (Acramite) for contact kill",
            "Spray spiromesifen (Oberon) for eggs and adults",
            "Rotate miticide classes to prevent resistance"
        ],
        "prevention": [
            "Maintain adequate soil moisture — stressed plants attract mites",
            "Avoid broad-spectrum insecticides",
            "Install reflective mulch to disorient mites",
            "Scout leaf undersides weekly in hot weather"
        ],
        "severity": "Medium",
        "icon": "🍅"
    },

    "Tomato___Target_Spot": {
        "name": "Tomato Target Spot",
        "plant": "Tomato",
        "description": "Target spot creates brown lesions with concentric rings and yellow halos on leaves. It can also affect fruit and stems, causing significant defoliation.",
        "causes": [
            "Fungus Corynespora cassiicola",
            "High humidity and temperatures above 68°F",
            "Extended leaf wetness",
            "Dense canopy with poor air movement"
        ],
        "organic_treatment": [
            "Apply copper-based fungicide at first symptom",
            "Prune lower leaves to improve air circulation",
            "Remove infected plant material immediately",
            "Use neem oil as protective spray"
        ],
        "chemical_treatment": [
            "Apply azoxystrobin or boscalid",
            "Use tebuconazole + trifloxystrobin",
            "Spray chlorothalonil preventively",
            "Apply at 7–14 day intervals"
        ],
        "prevention": [
            "Maintain well-pruned, open canopy",
            "Use drip irrigation exclusively",
            "Rotate with non-solanaceous crops",
            "Avoid late afternoon irrigation"
        ],
        "severity": "Medium",
        "icon": "🍅"
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "name": "Tomato Yellow Leaf Curl Virus",
        "plant": "Tomato",
        "description": "TYLCV causes upward leaf curling, yellowing, stunting, and flower drop. Transmitted by whiteflies, it can completely destroy a crop with no direct cure.",
        "causes": [
            "Tomato Yellow Leaf Curl Virus (TYLCV)",
            "Bemisia tabaci (whitefly) as vector",
            "Infected transplants",
            "Neighboring infected plants"
        ],
        "organic_treatment": [
            "Control whitefly with yellow sticky traps",
            "Apply insecticidal soap to kill whiteflies",
            "Use neem oil to repel whitefly",
            "Remove and destroy infected plants immediately"
        ],
        "chemical_treatment": [
            "Apply imidacloprid systemic insecticide for whitefly control",
            "Use thiamethoxam at transplanting",
            "Spray spirotetramat for immature whitefly stages",
            "Apply reflective mulch to deter whiteflies"
        ],
        "prevention": [
            "Plant TYLCV-resistant varieties",
            "Use floating row covers on transplants",
            "Plant away from other tomato/pepper fields",
            "Eradicate weeds that host whiteflies"
        ],
        "severity": "Critical",
        "icon": "🍅"
    },

    "Tomato___Tomato_mosaic_virus": {
        "name": "Tomato Mosaic Virus",
        "plant": "Tomato",
        "description": "Tomato Mosaic Virus creates a mosaic of light and dark green patches on leaves, distortion, stunting, and internal fruit browning.",
        "causes": [
            "Tomato Mosaic Virus (ToMV)",
            "Mechanical transmission (tools, hands)",
            "Infected seeds",
            "Tobacco products handling"
        ],
        "organic_treatment": [
            "Remove and destroy infected plants",
            "Wash hands thoroughly before handling plants",
            "Disinfect all tools with 10% bleach solution",
            "Control aphid vectors with insecticidal soap"
        ],
        "chemical_treatment": [
            "No direct chemical cure exists for the virus",
            "Control aphid vectors with imidacloprid",
            "Apply reflective mulch to deter aphids",
            "Use mineral oil sprays to reduce aphid transmission"
        ],
        "prevention": [
            "Use certified virus-free seed",
            "Plant resistant varieties (tm-2 gene resistance)",
            "Wash hands after smoking before touching plants",
            "Disinfect all equipment between plants"
        ],
        "severity": "High",
        "icon": "🍅"
    },

    "Tomato___healthy": {
        "name": "Healthy Tomato",
        "plant": "Tomato",
        "description": "Your tomato plant is perfectly healthy with no disease signs!",
        "causes": [],
        "organic_treatment": ["No treatment needed"],
        "chemical_treatment": ["No treatment needed"],
        "prevention": [
            "Stake or cage plants early",
            "Water consistently at base",
            "Fertilize with balanced tomato fertilizer",
            "Pinch suckers for better fruit production"
        ],
        "severity": "None",
        "icon": "✅"
    }
}

# Helper function to get disease info by class name
def get_disease_info(class_name):
    """Return disease data for a given class name, or a default if not found."""
    return DISEASE_DATA.get(class_name, {
        "name": "Unknown Condition",
        "plant": "Unknown",
        "description": "Disease information not available for this condition.",
        "causes": ["Unknown"],
        "organic_treatment": ["Consult a local agricultural extension service"],
        "chemical_treatment": ["Consult a local agricultural extension service"],
        "prevention": ["Regular monitoring and good plant hygiene"],
        "severity": "Unknown",
        "icon": "❓"
    })

# List of all 38 class names (matches PlantVillage dataset order)
CLASS_NAMES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

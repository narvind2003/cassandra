export interface CommodityDossier {
    title: string;
    description: string;
    critical_node: string;
    top_producers: string[];
    top_traders: string[];
    strategic_flows: string[];
    vulnerabilities: string[];
    node_guide: {
        resource: string;
        transformation: string;
        logistic: string;
        retail: string;
    };
}

export const COMMODITY_MANIFEST: Record<string, CommodityDossier> = {
    // ==========================================
    // ENERGY
    // ==========================================
    "Crude Oil": {
        title: "The Industrial Lifeblood",
        description: "The world's most traded commodity flows from mega-fields in the Middle East, US Permian Basin, and Russia. It travels via VLCC tankers through critical chokepoints like Hormuz and Malacca to reach refining hubs.",
        critical_node: "Strait of Hormuz",
        top_producers: ["Saudi Aramco", "ExxonMobil", "Chevron", "Shell", "Gazprom"],
        top_traders: ["Vitol", "Trafigura", "Glencore", "Mercuria"],
        strategic_flows: [
            "Ghawar (Saudi) → Ras Tanura",
            "Permian Basin (USA) → Corpus Christi (USA)",
            "Urals/Siberia (Russia) → Novorossiysk",
            "Lula (Brazil) → Ningbo-Zhoushan",
            "Strait of Hormuz → Jamnagar (India)"
        ],
        vulnerabilities: ["Hormuz Blockade", "Suez Transit Risk", "OPEC+ Policy Shifts"],
        node_guide: {
            resource: "Extraction from onshore/offshore reservoirs (Ghawar, Permian).",
            transformation: "Stabilization (Abqaiq) and Complex Refining (Cracking/Distillation).",
            logistic: "Pipeline transport and VLCC Supertanker shipping.",
            retail: "Strategic Storage Hubs (Cushing, ARA) and distribution."
        }
    },
    "Natural Gas (LNG)": {
        title: "The Bridge Fuel",
        description: "Supercooled to -162°C to become liquid (LNG). Connects Qatar/US reserves to power-hungry East Asia and Europe. Requires specialized cryogenic infrastructure.",
        critical_node: "Ras Laffan Terminal",
        top_producers: ["QatarEnergy", "ExxonMobil", "Shell", "Cheniere", "Gazprom"],
        top_traders: ["Vitol", "Gunvor", "TotalEnergies"],
        strategic_flows: [
            "North Field (Qatar) → Ras Laffan LNG",
            "Marcellus Shale (USA) → Sabine Pass LNG",
            "Yamal LNG → Zeebrugge Hub (EU)",
            "Strait of Hormuz → Futtsu LNG (Japan)",
            "Suez Canal → Gate Terminal (NL)"
        ],
        vulnerabilities: ["Cryogenic Infrastructure Failure", "Panama Canal Drought", "Seasonal Demand Spikes"],
        node_guide: {
            resource: "Gas field extraction (North Field, Marcellus).",
            transformation: "Liquefaction Trains (Gas to Liquid) at export terminals.",
            logistic: "Q-Flex/Q-Max LNG Carrier transport.",
            retail: "Regasification Terminals feeding national power grids."
        }
    },
    "Thermal Coal": {
        title: "Baseload Power",
        description: "The backbone of electricity in China and India. High-energy fuel mined at scale and moved by massive unit trains and bulk carriers.",
        critical_node: "Port of Newcastle",
        top_producers: ["Adani", "BHP", "Glencore", "Coal India", "China Shenhua"],
        top_traders: ["Glencore", "Noble Group", "Trafigura"],
        strategic_flows: [
            "Hunter Valley (Aus) → Port of Newcastle",
            "Kaltim Prima (Indonesia) → Shanghai Port",
            "Richards Bay Coal (SA) → Mundra Port (India)",
            "Port of Newcastle → Hekinan Power (Japan)",
            "Samarinda/Balikpapan → Guangzhou Power"
        ],
        vulnerabilities: ["Indonesian Export Bans", "Australian Cyclone Season", "Global Carbon Pricing"],
        node_guide: {
            resource: "Open-cut or underground coal mining operations.",
            transformation: "Washing, crushing, and blending for quality.",
            logistic: "Heavy haul rail lines and dry bulk ocean shipping.",
            retail: "Ultra-supercritical power stations and industrial boilers."
        }
    },
    "Uranium": {
        title: "The Nuclear Core",
        description: "Unprecedented energy density. Highly regulated and concentrated chain involving ore, yellowcake, conversion, and enrichment.",
        critical_node: "Rosatom Enrichment",
        top_producers: ["Kazatomprom", "Cameco", "Orano", "BHP"],
        top_traders: ["Traxys", "Yellow Cake PLC"],
        strategic_flows: [
            "Inkai (Kazakhstan) → St. Petersburg Port",
            "Cigar Lake (Canada) → Blind River Refinery",
            "Olympic Dam (Aus) → Port Adelaide",
            "Rosatom Enrichment → EU Nuclear Fleet",
            "ConverDyn (USA) → Vogtle NPP (USA)"
        ],
        vulnerabilities: ["Kazakh Political Instability", "Enrichment Sanctions", "Type-B Cask Logistics"],
        node_guide: {
            resource: "In-situ recovery (ISR) or deep shaft mining.",
            transformation: "Conversion to UF6 and Centrifuge Enrichment.",
            logistic: "High-security transport of casks and rods.",
            retail: "Nuclear reactors generating base-load power."
        }
    },

    // ==========================================
    // METALS (Industrial)
    // ==========================================
    "Iron Ore": {
        title: "Backbone of Steel",
        description: "The primary ingredient for global infrastructure. Dominated by massive operations in Australia and Brazil that feed the blast furnaces of Asia.",
        critical_node: "Port Hedland",
        top_producers: ["Vale", "Rio Tinto", "BHP", "Fortescue", "Anglo American"],
        top_traders: ["Glencore", "Trafigura"],
        strategic_flows: [
            "Pilbara (BHP/Rio) → Port Hedland",
            "Carajás S11D (Vale) → Ponta da Madeira",
            "Port Hedland → Shougang Caofeidian",
            "Ponta da Madeira → Rotterdam Coal Terminal",
            "Minas-Rio (Anglo) → Port of Açu"
        ],
        vulnerabilities: ["Pilbara Cyclones", "Brazilian Dam Failures", "Suez Canal Transit"],
        node_guide: {
            resource: "Open-pit extraction and crushing at scale.",
            transformation: "Sintering, Pelletizing, and Blast Furnace smelting.",
            logistic: "Unit trains and Valemax class bulk carriers.",
            retail: "Steel mills producing HRC, Rebar, and Auto sheets."
        }
    },
    "Copper": {
        title: "The Electrification Metal",
        description: "Essential for EVs and grids. High-grade deposits in the Andes are concentrated and shipped across the Pacific for refining.",
        critical_node: "Antofagasta Port",
        top_producers: ["Codelco", "Freeport-McMoRan", "BHP", "Glencore", "Ivanhoe"],
        top_traders: ["Trafigura", "Glencore", "IXM"],
        strategic_flows: [
            "Escondida (Chile) → Port of Antofagasta",
            "Grasberg (Indonesia) → Guixi Smelter (Jiangxi)",
            "Kamoa-Kakula (DRC) → Port of Lobito (Angola)",
            "Cerro Verde (Peru) → Matarani Port",
            "Port of Antofagasta → Ningbo-Zhoushan"
        ],
        vulnerabilities: ["Andean Water Scarcity", "DRC Conflict Risk", "Refining Capacity Bottlenecks"],
        node_guide: {
            resource: "Porphyry deposit mining and milling to concentrate.",
            transformation: "Smelting to blister copper and electrolytic refining.",
            logistic: "Concentrate shipping and cathode container trade.",
            retail: "Wire rod factories and electronics assembly."
        }
    },
    "Aluminum": {
        title: "Frozen Electricity",
        description: "Lightweight and recyclable. Production requires massive bauxite mining in Guinea and extreme electricity for smelting.",
        critical_node: "Port of Kamsar",
        top_producers: ["Rio Tinto", "Alcoa", "UC Rusal", "Chalco", "Emirates Global"],
        top_traders: ["Glencore", "Trafigura"],
        strategic_flows: [
            "Boké (Guinea) → Port of Kamsar",
            "Port of Kamsar → Alunorte (Brazil)",
            "Port of Weipa → Gladstone Refineries",
            "Port of Kamsar → Port of Qingdao",
            "EGA Jebel Ali (UAE) → Global Auto Hubs"
        ],
        vulnerabilities: ["Guinea Coup Risks", "Energy Price Spikes", "Carbon Border Adjustments (CBAM)"],
        node_guide: {
            resource: "Bauxite strip mining and refining to Alumina.",
            transformation: "Cryolite electrolysis smelting to liquid metal.",
            logistic: "Bulk bauxite carriers and aluminum ingot shipping.",
            retail: "Aerospace plants, Can makers, and Auto body mills."
        }
    },
    "Zinc": {
        title: "The Galvanizer",
        description: "Protects the world's steel from rust. Mined in remote Alaska and the Andes, then refined in complex electrolytic smelters.",
        critical_node: "Red Dog Port",
        top_producers: ["Teck Resources", "Glencore", "Vedanta", "Korea Zinc", "Nyrstar"],
        top_traders: ["Trafigura", "Glencore"],
        strategic_flows: [
            "Red Dog Mine (Alaska) → Trail Smelter",
            "Antamina (Peru) → Port of Callao",
            "Rampura Agucha (India) → Chanderiya (India)",
            "Red Dog Mine (Alaska) → Korea Zinc (Onsan)",
            "Port of Callao → Nyrstar Budel (NL)"
        ],
        vulnerabilities: ["Arctic Shipping Seasons", "Smelter Margin Squeeze", "Power Rationing in EU"],
        node_guide: {
            resource: "Mining and production of zinc-lead concentrates.",
            transformation: "Roasting, leaching, and electrowinning.",
            logistic: "Concentrate shipping in bulk or bags.",
            retail: "Galvanizing lines at integrated steel works."
        }
    },
    "Lead": {
        title: "The Battery Link",
        description: "Highly recycled and critical for every vehicle's 12V starter battery. Mined in Australia/China and refined globally.",
        critical_node: "Port Pirie Smelter",
        top_producers: ["Glencore", "South32", "Vedanta", "Nyrstar", "Clarios (Recycling)"],
        top_traders: ["Trafigura", "Glencore"],
        strategic_flows: [
            "Mount Isa (Aus) → Nyrstar Port Pirie",
            "Cannington (Aus) → Port of Townsville",
            "Nyrstar Port Pirie → Tianneng Battery",
            "Clarios (USA) → VW Wolfsburg",
            "Port of Townsville → Korea Zinc (Onsan)"
        ],
        vulnerabilities: ["Environmental Lead Bans", "Secondary Recycling Scrap Supply", "Auto Lead-Acid Demand Shift"],
        node_guide: {
            resource: "Lead-zinc-silver mining and concentrating.",
            transformation: "Smelting and refining of primary/secondary lead.",
            logistic: "Heavy metal ingot transport and scrap collection.",
            retail: "Lead-acid battery manufacturing (Clarios, GS Yuasa)."
        }
    },
    "Nickel": {
        title: "Stainless & Electric",
        description: "Dual-purpose metal for high-end steel and EV batteries. Indonesia has become the global hub via industrial parks.",
        critical_node: "Morowali (Indo)",
        top_producers: ["Vale", "Norilsk Nickel", "Tsingshan", "Glencore", "BHP"],
        top_traders: ["Trafigura", "Glencore"],
        strategic_flows: [
            "Morowali IMIP (Indo) → IMIP Port",
            "Norilsk (Russia) → Rotterdam Coal Terminal",
            "Sudbury Basin (Can) → Thompson",
            "IMIP Port → CATL Ningde",
            "Tianqi Kwinana (Aus) → Tesla Fremont"
        ],
        vulnerabilities: ["Indonesian Export Restrictions", "HPAL Tech Execution Risk", "LME Liquidity Shocks"],
        node_guide: {
            resource: "Laterite ore mining (Indo) or Sulfide (Canada/Russia).",
            transformation: "RKEF (Stainless) or HPAL (Battery Grade) refining.",
            logistic: "Bulk ore barges and class 1 nickel containers.",
            retail: "Stainless steel mills and battery precursor plants."
        }
    },

    // ==========================================
    // METALS (Precious & Strategic)
    // ==========================================
    "Gold": {
        title: "The Ultimate Asset",
        description: "Safeguard against inflation and war. Mined deep in the earth, refined to extreme purity, and vaulted in the world's financial hubs.",
        critical_node: "Valcambi Swiss",
        top_producers: ["Newmont", "Barrick Gold", "AngloGold Ashanti", "Polyus", "Freeport"],
        top_traders: ["JPMorgan", "HSBC", "MKS PAMP"],
        strategic_flows: [
            "Grasberg (Indonesia) → Metalor (Swiss)",
            "Carlin (USA) → Valcambi (Swiss)",
            "Muruntau (Uzbekistan) → SGE (Shanghai)",
            "Swiss Refineries → LBMA Vaults",
            "London Vaults → RBI (India)"
        ],
        vulnerabilities: ["Mining Resource Depletion", "Central Bank Policy Shifts", "Illegal Refining Infiltration"],
        node_guide: {
            resource: "Deep underground or open-pit leaching of gold ore.",
            transformation: "Refining to .9999 purity bars (Swiss standard).",
            logistic: "High-security air freight and armored transport.",
            retail: "Central Bank vaults and luxury jewelry fabrication."
        }
    },
    "Silver": {
        title: "The Solar Metal",
        description: "Precious and industrial. High conductivity makes it irreplaceable for solar panels and electronics. Mined primarily in Mexico.",
        critical_node: "Fresnillo MX",
        top_producers: ["Fresnillo", "Newmont", "Glencore", "Pan American Silver", "Hochschild"],
        top_traders: ["Trafigura", "Samsung (Offtake)"],
        strategic_flows: [
            "Fresnillo (Mexico) → Met-Mex Peñoles (MX)",
            "Met-Mex Peñoles (MX) → Port of Manzanillo",
            "Port of Manzanillo → Shanghai Port",
            "Port of Callao → Korea Zinc (Onsan)",
            "Tianqi Kwinana (Aus) → Global Solar Hubs"
        ],
        vulnerabilities: ["Solar Cell Substitution", "Mexican Mining Reforms", "Byproduct Supply Elasticity"],
        node_guide: {
            resource: "Primary silver mining or byproduct of Lead/Zinc.",
            transformation: "Refining to investment grade and industrial paste.",
            logistic: "Secure containerized sea and air freight.",
            retail: "Solar panel manufacturers and electronic OEMs."
        }
    },
    "Platinum": {
        title: "The Hydrogen Metal",
        description: "Essential for catalytic converters and fuel cells. Production is geographically hyper-concentrated in South Africa.",
        critical_node: "Bushveld Complex",
        top_producers: ["Anglo American Platinum", "Impala Platinum", "Sibanye-Stillwater"],
        top_traders: ["Johnson Matthey", "BASF"],
        strategic_flows: [
            "Bushveld Complex (SA) → Rustenburg Smelter",
            "Rustenburg → Zurich Vaults",
            "Zurich Airport → VW Wolfsburg",
            "Sibanye (USA) → Ford Rouge Complex",
            "SA Refineries → Shanghai PGM Market"
        ],
        vulnerabilities: ["SA Power Grid (Eskom) Failure", "Hydrogen Tech Adoption Speed", "Labor Strikes in Rustenburg"],
        node_guide: {
            resource: "Ultra-deep mining of PGM reef deposits.",
            transformation: "Complex smelting and precious metal separation.",
            logistic: "High-security air freight and secure depots.",
            retail: "Auto catalyst plants and PEM fuel cell makers."
        }
    },
    "Palladium": {
        title: "The Gasoline Scrubber",
        description: "The duopoly of Russia and South Africa controls the world's supply of this essential anti-pollution metal for gasoline engines.",
        critical_node: "Norilsk Nickel",
        top_producers: ["Norilsk Nickel", "Sibanye-Stillwater", "Impala Platinum"],
        top_traders: ["Johnson Matthey", "Traxys"],
        strategic_flows: [
            "Norilsk (Russia) → Helsinki Port",
            "Helsinki → BASF (Germany)",
            "Stillwater (USA) → Detroit Auto Hub",
            "Rustenburg → Toyota City",
            "Norilsk (Russia) → Shanghai PGM Hub"
        ],
        vulnerabilities: ["Russian Sanctions", "Electric Vehicle Transition", "Supply Concentration Risk"],
        node_guide: {
            resource: "Byproduct of nickel mining or PGM reef mining.",
            transformation: "Chemical separation and refining to sponge/ingot.",
            logistic: "Secure, insured air and sea freight.",
            retail: "Catalytic converter coating and sensor makers."
        }
    },
    "Cobalt": {
        title: "The Blue Metal",
        description: "Critical for battery stability. The supply chain runs from the DRC Copperbelt through the Kasumbalesa border to China.",
        critical_node: "Kasumbalesa Border",
        top_producers: ["Glencore", "CMOC Group", "ERG", "Huayou Cobalt"],
        top_traders: ["Glencore", "Trafigura"],
        strategic_flows: [
            "Mutanda (Glencore) → Kasumbalesa Border",
            "Tenke Fungurume (CMOC) → Port of Durban",
            "Kasumbalesa Border → Port of Lobito (Angola)",
            "Port of Durban → Ningbo-Zhoushan",
            "Huayou Refined → CATL Gigafactories"
        ],
        vulnerabilities: ["Artisanal Mining Ethics", "Kasumbalesa Congestion", "LFP Battery Substitution"],
        node_guide: {
            resource: "Mining of copper-cobalt ores in the Katanga region.",
            transformation: "Refining to Cobalt Hydroxide and Battery Sulfate.",
            logistic: "Long-haul trucking through the Copperbelt corridors.",
            retail: "Battery cathode and aerospace superalloy makers."
        }
    },
    "Lithium-Ion Battery": {
        title: "The EV Revolution",
        description: "The bottleneck of the energy transition. A complex chain moving from Australian rock and Chilean brine to Chinese refining dominance.",
        critical_node: "Malacca Strait",
        top_producers: ["Albemarle", "SQM", "Ganfeng", "Tianqi", "Pilbara Minerals"],
        top_traders: ["Glencore (Offtake)", "Trafigura"],
        strategic_flows: [
            "Greenbushes (Aus) → Port of Bunbury",
            "Albemarle Atacama (Chile) → Port of Antofagasta",
            "Pilgangoora (Aus) → Port Hedland",
            "Port of Bunbury → Ningbo Magnet Hub",
            "Port of Antofagasta → Shanghai Port"
        ],
        vulnerabilities: ["Chinese Midstream Dominance", "Water Scarcity in Atacama", "Solid-State Tech Disruption"],
        node_guide: {
            resource: "Brine evaporation or spodumene rock mining.",
            transformation: "Conversion to Carbonate or Hydroxide chemicals.",
            logistic: "Class 9 dangerous goods shipping.",
            retail: "Gigafactories producing cells for Tesla, BYD, etc."
        }
    },
    "Rare Earths": {
        title: "Strategic Magnets",
        description: "Small volumes, massive impact. Irreplaceable for EV motors and defense. Processing is almost entirely concentrated in China.",
        critical_node: "Baotou Hub",
        top_producers: ["China Rare Earth Group", "MP Materials", "Lynas"],
        top_traders: ["Shenghe Resources"],
        strategic_flows: [
            "Bayan Obo (China) → Baotou Steel RE",
            "Mountain Pass (USA) → Port of LA",
            "Port of LA → Shenghe Resources",
            "Mount Weld (Aus) → Kuantan Port",
            "Kuantan Port → Toyota City"
        ],
        vulnerabilities: ["Export Quotas by China", "Processing Environmental Impact", "Single-point-of-failure in Baotou"],
        node_guide: {
            resource: "Mining and production of RE concentrate.",
            transformation: "Solvent extraction for individual oxide separation.",
            logistic: "Sensitive chemical container transport.",
            retail: "NdFeB magnet manufacturing for motors and sensors."
        }
    },
    "Semiconductors": {
        title: "The Brains of Modernity",
        description: "The most complex supply chain ever built. Spans continents from specialized sand in the US to lithography in the EU and fabs in Taiwan.",
        critical_node: "TSMC Fab 18",
        top_producers: ["TSMC", "Samsung", "Intel", "SMIC", "SK Hynix"],
        top_traders: ["Arrow Electronics", "Avnet", "WPG Holdings"],
        strategic_flows: [
            "Spruce Pine Mines (USA) → Hemlock Semi (USA)",
            "ASML (NL) → TSMC Fab 18 (Tainan)",
            "Shin-Etsu Handotai (Japan) → TSMC Fab 18 (Tainan)",
            "TSMC Fab 18 (Tainan) → Foxconn Shenzhen",
            "Samsung Electronics → Apple Cupertino"
        ],
        vulnerabilities: ["Taiwan Strait Conflict", "ASML Machine Lead Times", "Pure-play Foundry Capacity"],
        node_guide: {
            resource: "High-purity quartz mining and silicon purification.",
            transformation: "Poly-Si, Wafer Slicing, and Nanoscale Lithography.",
            logistic: "Ultra-clean, shock-proof air freight.",
            retail: "Electronics assembly for Apple, Tesla, Servers."
        }
    },

    // ==========================================
    // GRAINS & SOFT AGRI
    // ==========================================
    "Wheat": {
        title: "The Staff of Life",
        description: "The primary calorie source for much of the world. Global trade is hypersensitive to Black Sea geopolitics and Australian/US climate patterns.",
        critical_node: "Bosphorus Strait",
        top_producers: ["Cargill", "ADM", "Bunge", "COFCO", "Viterra"],
        top_traders: ["ABCD Group", "Olam"],
        strategic_flows: [
            "Georgia/Arkansas → Port of NOLA",
            "Novorossiysk → Bosphorus Strait",
            "Greater Odessa (UA) → Bosphorus Strait",
            "Bosphorus Strait → Port Said",
            "Tianqi Kwinana (Aus) → Bulog Jakarta"
        ],
        vulnerabilities: ["Black Sea Grain Corridor Blockage", "MENA Food Insecurity", "La Niña Wheat Droughts"],
        node_guide: {
            resource: "Broadacre cultivation of winter and spring wheat.",
            transformation: "Grain elevator storage and flour milling.",
            logistic: "River barges, unit trains, and bulk carriers.",
            retail: "Industrial bakeries and food manufacturing plants."
        }
    },
    "Corn (Maize)": {
        title: "Feed, Fuel & Food",
        description: "A dual-use crop for livestock feed and ethanol. The US and Brazil form an export duopoly that drives global energy and protein prices.",
        critical_node: "Panama Canal",
        top_producers: ["ADM", "Cargill", "Bunge", "AMAGGI", "Corteva"],
        top_traders: ["ABCD Group", "COFCO"],
        strategic_flows: [
            "CF Industries (Iowa) → Mississippi River",
            "Mato Grosso (BR) → Port of Santos",
            "Mississippi River → Panama Canal",
            "Port of Santos → Nagoya (Japan)",
            "Port of NOLA → Nescafé Veracruz"
        ],
        vulnerabilities: ["Mississippi River Draft Levels", "US Ethanol Mandates", "Nitrogen Fertilizer Price Spikes"],
        node_guide: {
            resource: "Row crop farming of yellow and white corn.",
            transformation: "Crushing for feed or wet-milling for ethanol/syrup.",
            logistic: "Massive barge and dry bulk shipping networks.",
            retail: "Feedlots, ethanol blenders, and starch makers."
        }
    },
    "Rice": {
        title: "The Foundation of Asia",
        description: "The world's most consumed staple. Unlike wheat, only 10% is traded globally, making export bans from India or Thailand highly disruptive.",
        critical_node: "Mekong Delta",
        top_producers: ["India State Corp", "COFCO", "Olam", "Wilmar"],
        top_traders: ["Olam", "Louis Dreyfus", "Wilmar"],
        strategic_flows: [
            "Central Plains (Thai) → Bangkok Port",
            "Mekong Delta (VN) → Cat Lai Port",
            "Andhra Pradesh (Ind) → Kakinada Port",
            "Bangkok Canneries → Manila (Philippines)",
            "Kakinada Anchorage → Port of Lagos (Nigeria)"
        ],
        vulnerabilities: ["Indian Export Bans", "Mekong Saltwater Intrusion", "Fertilizer Subsidy Risks"],
        node_guide: {
            resource: "Paddy field cultivation and monsoon-fed irrigation.",
            transformation: "Milling, husking, and polishing to white rice.",
            logistic: "Bagged break-bulk and containerized shipping.",
            retail: "Domestic markets and grocery retail channels."
        }
    },
    "Soybeans": {
        title: "The Global Protein Link",
        description: "The engine of the world's meat industry. A massive flow of protein moves from the Americas to China's crushing plants.",
        critical_node: "Port of Santos",
        top_producers: ["AMAGGI", "Cargill", "ADM", "Bunge", "Louis Dreyfus"],
        top_traders: ["ABCD Group", "COFCO"],
        strategic_flows: [
            "Mato Grosso (BR) → Port of Santos",
            "Illinois/Iowa (USA) → Port of NOLA",
            "Port of Santos → Rizhao Crush (China)",
            "Port of Santos → Port of Amsterdam",
            "Port of NOLA → SGE (Shanghai)"
        ],
        vulnerabilities: ["Amazon Deforestation Regulations", "Chinese Swine Herd Fluctuations", "Mississippi Logistics Bottlenecks"],
        node_guide: {
            resource: "Large-scale mechanized oilseed farming.",
            transformation: "Crushing into soybean meal (protein) and oil.",
            logistic: "Intermodal rail, barge, and Panamax carriers.",
            retail: "Livestock feed mixers and vegetable oil packers."
        }
    },
    "Cane Sugar": {
        title: "The Sweet Pivot",
        description: "Brazil dominates the market, with the ability to pivot production between sugar (food) and ethanol (fuel) based on crude oil prices.",
        critical_node: "Santos Terminal",
        top_producers: ["Raízen", "Copersucar", "Tereos", "Wilmar", "Mitre Phol"],
        top_traders: ["Alvean", "Wilmar", "Czarnikow"],
        strategic_flows: [
            "Sao Paulo Groves → Port of Santos",
            "Port of Santos → Dubai Gold Souk",
            "Port of Santos → Tate & Lyle (London)",
            "Uttar Pradesh (India) → Kandla Port",
            "Kandla Port → Port Sudan"
        ],
        vulnerabilities: ["Brazilian Ethanol/Sugar Parity", "Indian Export Quotas", "Port of Santos Congestion"],
        node_guide: {
            resource: "Sugarcane plantation and mechanized harvesting.",
            transformation: "Milling, centrifugation, and white sugar refining.",
            logistic: "Bulk sugar terminals and specialized carriers.",
            retail: "FMCG manufacturers and beverage bottling plants."
        }
    },

    // ==========================================
    // FERTILIZER & INDUSTRIAL
    // ==========================================
    "Fertilizer": {
        title: "The Yield Engine",
        description: "A composite chain of Nitrogen, Phosphate, and Potash. Essential for the green revolution and the avoidance of global famine.",
        critical_node: "Suez Canal",
        top_producers: ["Nutrien", "Yara", "Mosaic", "OCP", "EuroChem"],
        top_traders: ["Trafigura", "Ameropa", "Trammo"],
        strategic_flows: [
            "OCP Boucraa (Morocco) → Brazil Soy Belt",
            "Olimpiada (Russia) → EU Agriculture",
            "Teck Trail (Canada) → China Hubs",
            "Suez Canal → Global Agri Belts",
            "Yara Porsgrunn (Norway) → Amsterdam Hub"
        ],
        vulnerabilities: ["Natural Gas Feedstock Spikes", "Russian Export Blockades", "Moroccan Resource Monopolies"],
        node_guide: {
            resource: "Extraction of Phosphate Rock and Potash salts.",
            transformation: "Chemical synthesis (Nitrogen) and acidulation.",
            logistic: "Bulk chemical carriers and specialized storage.",
            retail: "Farm cooperatives and fertilizer blenders."
        }
    },
    "Urea (Nitrogen)": {
        title: "Solid Gas",
        description: "Natural gas turned into solid pellets. The primary nitrogen source for crops, moving from gas-rich nations to agricultural giants.",
        critical_node: "Port of Yuzhny",
        top_producers: ["Yara", "CF Industries", "Nutrien", "QAFCO", "SABIC"],
        top_traders: ["Trammo", "Keytrade"],
        strategic_flows: [
            "North Field (Qatar) → Brazil Soy Farms",
            "Louisiana (USA) → Mississippi River",
            "Novorossiysk → Global Markets",
            "Port Said → JNPT Mumbai",
            "Yuzhny (Ukraine) → EU Hubs"
        ],
        vulnerabilities: ["Natural Gas Curtailments", "Russian Ammonia Pipeline Risks", "Indian Subsidy Policy"],
        node_guide: {
            resource: "Natural gas feedstock extraction and reforming.",
            transformation: "Haber-Bosch Ammonia synthesis and Prilling.",
            logistic: "Bulk solid carriers and moisture-controlled silos.",
            retail: "On-farm application for high-yield grains."
        }
    },
    "Phosphate": {
        title: "The Root Builder",
        description: "Irreplaceable nutrient for plant root development. Morocco's OCP Group holds a dominant position in the world's phosphate rock reserves.",
        critical_node: "Casablanca Port",
        top_producers: ["OCP Group", "Mosaic", "Nutrien", "PhosAgro", "Ma'aden"],
        top_traders: ["Trafigura", "Indorama"],
        strategic_flows: [
            "OCP Khouribga → Jorf Lasfar",
            "Mosaic Florida → Port of Tampa",
            "Jorf Lasfar → Brazil Soy Belt",
            "Tampa → Mississippi River",
            "Ma'aden (Saudi) → JNPT Mumbai"
        ],
        vulnerabilities: ["Moroccan Geopolitical Leverage", "Florida Environmental Regulations", "Byproduct Phosphogypsum Disposal"],
        node_guide: {
            resource: "Phosphate rock mining and beneficiation.",
            transformation: "Phosphoric acid production and DAP/MAP synthesis.",
            logistic: "Bulk phosphate carriers and terminal handling.",
            retail: "Direct application or NPK blending plants."
        }
    },
    "Potash": {
        title: "The Resilience Salt",
        description: "Enhances plant water retention and disease resistance. Trade is dominated by a few players in Canada, Russia, and Belarus.",
        critical_node: "Port of Vancouver",
        top_producers: ["Nutrien", "Uralkali", "Belaruskali", "Mosaic", "K+S"],
        top_traders: ["Canpotex", "BPC"],
        strategic_flows: [
            "Saskatchewan (CAN) → Westridge Marine (Vancouver)",
            "Soligorsk (Belarus) → Klaipeda (Lithuania)",
            "Berezniki (RU) → St. Petersburg",
            "Westridge Marine (Vancouver) → Port of Qinhuangdao",
            "Westridge Marine (Vancouver) → Port of Santos"
        ],
        vulnerabilities: ["Belarusian Sanctions", "Canadian Rail Strikes", "Deep-shaft Mining Flooding"],
        node_guide: {
            resource: "Deep underground or solution mining of potash salts.",
            transformation: "Flotation, crystallization, and compaction.",
            logistic: "Unit trains (Canpotex) and deep-water terminals.",
            retail: "Global agricultural blenders and cooperatives."
        }
    },
    "Silicon": {
        title: "The Industrial Base",
        description: "The starting point for both the Aluminum alloy and Semiconductor industries. China dominates global smelting capacity.",
        critical_node: "Xinjiang Hub",
        top_producers: ["Ferroglobe", "Elkem", "Dow", "Hoshine Silicon", "Wacker Chemie"],
        top_traders: ["Traxys", "Glencore"],
        strategic_flows: [
            "Xinjiang XPCC (China) → Ningbo-Zhoushan",
            "Helsinki → Wacker Chemie (Germany)",
            "Ningbo Magnet Hub → Port of LA",
            "Elkem (Norway) → EU Foundries",
            "Xinjiang XPCC (China) → Hemlock Semi (USA)"
        ],
        vulnerabilities: ["Energy-Intensive Smelting Costs", "Xinjiang Human Rights Sanctions", "Solar Grade vs Semi Grade Purity"],
        node_guide: {
            resource: "High-purity quartz and silica sand mining.",
            transformation: "Arc furnace smelting and chemical purification.",
            logistic: "Solid bulk or containerized chemical transport.",
            retail: "Aluminum smelters, Solar firms, and Chip fabs."
        }
    },
    "Cement": {
        title: "Urban Foundation",
        description: "The literal building block of civilization. Heavy and low-value, it has the most localized supply chain but is essential for growth.",
        critical_node: "Yangtze River",
        top_producers: ["Holcim", "Heidelberg Materials", "Cemex", "Anhui Conch", "UltraTech"],
        top_traders: ["Bulk trading is minimal; mostly localized."],
        strategic_flows: [
            "Anhui Conch (China) → Shanghai Hub",
            "plant_cemex (MX) → Port of Houston",
            "UltraTech (India) → Mumbai Metro",
            "Holcim (EU) → London Gateway",
            "Cat Lai Port → NEOM (Saudi)"
        ],
        vulnerabilities: ["Limestone Quarry Depletion", "Extreme Carbon Footprint", "High Energy Cost Sensitivity"],
        node_guide: {
            resource: "Limestone quarrying and clay extraction.",
            transformation: "Clinker production in high-temperature kilns.",
            logistic: "Short-haul barge, truck, and specialized rail.",
            retail: "Construction sites and ready-mix concrete plants."
        }
    },

    // ==========================================
    // SOFTS & PERISHABLES
    // ==========================================
    "Coffee": {
        title: "The Global Caffeine Chain",
        description: "A dual market of Arabica (flavor) and Robusta (body). Mined in the tropical highlands and roasted in the consumer hubs of the West.",
        critical_node: "Santos Port",
        top_producers: ["Neumann Kaffee", "ECOM", "Sucafina", "Louis Dreyfus", "Olam"],
        top_traders: ["Nestle", "Starbucks", "JDE Peet's"],
        strategic_flows: [
            "Minas Gerais (Brazil) → Port of Santos",
            "Dak Lak (Vietnam) → Cat Lai Port",
            "Port of Santos → Aurubis Hamburg (DE)",
            "Cat Lai Port → Port of LA",
            "Port of Antwerp → Nestle Refineries"
        ],
        vulnerabilities: ["Frost in Brazil Highlands", "Climate-driven Highland Retreat", "Vietnam Water Management"],
        node_guide: {
            resource: "Cherry picking and wet/dry milling at origin.",
            transformation: "Hulling, grading, and industrial scale roasting.",
            logistic: "Ventilated container shipping in jute bags or bulk liners.",
            retail: "Café chains, grocery retail, and instant coffee plants."
        }
    },
    "Cocoa": {
        title: "The Chocolate Belt",
        description: "Hyper-concentrated production in West Africa. A fragile chain involving millions of smallholders and massive grinding hubs in Europe.",
        critical_node: "Abidjan Port",
        top_producers: ["Barry Callebaut", "Cargill", "Olam", "ECOM", "Touton"],
        top_traders: ["Nestle", "Mars", "Ferrero", "Hershey"],
        strategic_flows: [
            "Ivory Coast Farms → Port of Abidjan",
            "Ghana Farms → Port of Tema",
            "Port of Abidjan → Port of Amsterdam",
            "Port of Amsterdam → Barry Callebaut (BE)",
            "Tema → Hershey (USA)"
        ],
        vulnerabilities: ["West African Labor Ethics", "Swollen Shoot Virus outbreaks", "Amsterdam Grinding Bottlenecks"],
        node_guide: {
            resource: "Smallholder pod harvesting and on-farm fermentation.",
            transformation: "Drying, cleaning, and grinding into butter and powder.",
            logistic: "Temperature-monitored bulk or bagged shipping.",
            retail: "Confectionery manufacturing and luxury chocolatiers."
        }
    },
    "Palm Oil": {
        title: "The Invisible Ingredient",
        description: "The world's most efficient oilseed. Irreplaceable for food, soap, and biofuels, but under intense environmental scrutiny.",
        critical_node: "Malacca Strait",
        top_producers: ["Wilmar International", "Sime Darby", "Golden Agri", "Musim Mas", "IOI Group"],
        top_traders: ["Wilmar", "Cargill", "ADOP"],
        strategic_flows: [
            "North Sumatra (Indo) → Port of Dumai",
            "Sabah (Malaysia) → Sandakan",
            "Port of Dumai → Malacca Strait",
            "Strait of Malacca → Kandla Port",
            "Strait of Malacca → Rotterdam Coal Terminal"
        ],
        vulnerabilities: ["Indonesian Export Levies", "EU Deforestation Regulations (EUDR)", "Monsoon Logistics Disruption"],
        node_guide: {
            resource: "Fresh fruit bunch harvesting and sterilization.",
            transformation: "Crude oil extraction and fractionation (Olein/Stearin).",
            logistic: "Heated tanker transport and specialized tank farms.",
            retail: "FMCG giants (Unilever, P&G) and food processors."
        }
    },
    "Tea": {
        title: "The Ancient Brew",
        description: "A labor-intensive chain spanning from Kenyan highlands to Chinese gardens. Value is added at the great auction houses and blending hubs.",
        critical_node: "Mombasa Auction",
        top_producers: ["James Finlay", "McLeod Russel", "Lipton Teas", "China Tea Co"],
        top_traders: ["Unilever", "Tata Consumer", "Associated British Foods"],
        strategic_flows: [
            "Kericho (Kenya) → Port of Mombasa",
            "Assam (India) → Port of Kolkata",
            "Port of Mombasa → Dubai Gold Souk",
            "Dubai Gold Souk → London Tea Hub",
            "Kolkata → Karachi Tea Mkt"
        ],
        vulnerabilities: ["Highland Labor Shortages", "Monetary Crisis in Sri Lanka", "Mombasa Port Congestion"],
        node_guide: {
            resource: "Plucking of fresh leaves and on-estate withering.",
            transformation: "Rolling, oxidation (CTC or Orthodox), and drying.",
            logistic: "Bagged tea in dry, odor-free containers.",
            retail: "Blending houses, tea-bagging plants, and retail."
        }
    },
    "Cotton": {
        title: "The Global Fiber",
        description: "The backbone of the apparel industry. Mined from the fields of Texas and Xinjiang and spun in the mega-factories of SE Asia.",
        critical_node: "Ho Chi Minh Port",
        top_producers: ["Cargill", "Louis Dreyfus", "Olam", "Glencore"],
        top_traders: ["ABCD Group", "Noble"],
        strategic_flows: [
            "West Texas (USA) → Port of LA",
            "Xinjiang XPCC (China) → Port of Qingdao",
            "Port of LA → Cat Lai Port",
            "Port of LA → Chittagong (Bangladesh)",
            "Cat Lai Port → Dong Nai Garments"
        ],
        vulnerabilities: ["Xinjiang Forced Labor Sanctions", "Water Scarcity in Texas", "Bangladesh Energy Shortages"],
        node_guide: {
            resource: "Mechanized or manual picking and local ginning.",
            transformation: "Fiber separation, spinning to yarn, and weaving.",
            logistic: "Compressed bales in standard containers.",
            retail: "Garment factories and fast-fashion retail (H&M, Zara)."
        }
    },
    "Rubber": {
        title: "The Logistics Enabler",
        description: "Without rubber, the world's trucks stop. A biological product concentrated in Southeast Asia that keeps global trade moving.",
        critical_node: "Laem Chabang",
        top_producers: ["Halcyon Agri", "Sri Trang", "Thai Hua Rubber"],
        top_traders: ["Bridgestone", "Michelin", "Continental"],
        strategic_flows: [
            "Southern Thailand → Laem Chabang (Thai)",
            "North Sumatra (Indo) → Port of Belawan",
            "Laem Chabang (Thai) → Port of Nagoya (JP)",
            "Port of Belawan → Port of Savannah",
            "Laem Chabang (Thai) → Port of Qingdao"
        ],
        vulnerabilities: ["Leaf Fall Disease outbreaks", "Smallholder Tapping Elasticity", "Tire Industry Demand Shocks"],
        node_guide: {
            resource: "Latex tapping from Hevea trees and coagulation.",
            transformation: "Processing into Technically Specified Rubber (TSR).",
            logistic: "Palletized blocks in standard containers.",
            retail: "Tire manufacturing plants and industrial part makers."
        }
    },
    "Lumber": {
        title: "The Housing Framework",
        description: "The primary construction material for the North American and Chinese housing markets. Driven by interest rates and forestry health.",
        critical_node: "Vancouver Port",
        top_producers: ["West Fraser", "Canfor", "Weyerhaeuser", "Interfor", "Rayonier"],
        top_traders: ["Localized sawmills and distributors."],
        strategic_flows: [
            "British Columbia (Can) → Port of Vancouver",
            "Westridge Marine (Vancouver) → Port of Tokyo",
            "Urals/Siberia (Russia) → Manzhouli Rail",
            "US South (Yellow Pine) → Home Depot Distribution",
            "Westridge Marine (Vancouver) → Port of LA"
        ],
        vulnerabilities: ["Mountain Pine Beetle infestations", "US-Canada Softwood Lumber Duties", "Siberian Logging Restrictions"],
        node_guide: {
            resource: "Sustainable forestry logging and transport to mills.",
            transformation: "Sawmilling, kiln-drying, and planing into boards.",
            logistic: "Flatbed rail and break-bulk specialized shipping.",
            retail: "Construction sites and big-box home improvement retail."
        }
    },
    "Beef": {
        title: "The Premium Protein",
        description: "A land and resource-intensive chain. Brazil, the US, and Australia dominate the export of frozen and chilled beef to the world.",
        critical_node: "Shanghai Cold Chain",
        top_producers: ["JBS S.A.", "Tyson Foods", "Marfrig", "Minerva", "Cargill"],
        top_traders: ["JBS", "NH Foods"],
        strategic_flows: [
            "Mato Grosso (BR) → Port of Santos",
            "Queensland Cattle → Port of Brisbane",
            "Port of Santos → SGE (Shanghai)",
            "Port of Brisbane → Tokyo Port",
            "Georgia/Arkansas → Port of Long Beach"
        ],
        vulnerabilities: ["Foot and Mouth Disease outbreaks", "Amazon Deforestation pressure", "Methane Emissions regulations"],
        node_guide: {
            resource: "Cow-calf operations, grazing, and feedlot finishing.",
            transformation: "Slaughter, fabrication, and vacuum packing.",
            logistic: "Continuous cold-chain reefer container transport.",
            retail: "Supermarkets and premium food service/steakhouses."
        }
    },
    "Poultry": {
        title: "The Universal Meat",
        description: "The most efficient land-based protein. Highly industrialized and globally traded in frozen parts (wings, feet, breasts).",
        critical_node: "Savannah Port",
        top_producers: ["JBS (Seara)", "Tyson Foods", "BRF", "CP Foods", "Wens Foodstuff"],
        top_traders: ["Cargill", "BRF"],
        strategic_flows: [
            "Port of Paranaguá → Port of Paranagua",
            "SK On Georgia → Port of Savannah",
            "Port of Paranagua → Port of Jeddah (KSA)",
            "Port of Savannah → Port of Qingdao",
            "CP Foods (Thai) → Tokyo Port"
        ],
        vulnerabilities: ["Avian Influenza (H5N1) outbreaks", "Corn/Soy Feed Price volatility", "Halal Certification barriers"],
        node_guide: {
            resource: "Hatcheries and climate-controlled grow-out houses.",
            transformation: "Automated processing, chilling, and portioning.",
            logistic: "Reefer containers and cold-storage distribution.",
            retail: "QSR (Fast Food) chains and grocery retail."
        }
    },
    "Pork": {
        title: "Asia's Red Meat",
        description: "China is both the largest producer and consumer. Global trade fills the gaps left by disease outbreaks and demand spikes.",
        critical_node: "WH Group Logistics",
        top_producers: ["WH Group (Smithfield)", "Wens Foodstuff", "JBS", "CP Foods", "Danish Crown"],
        top_traders: ["Cargill", "Smithfield"],
        strategic_flows: [
            "CF Industries (Iowa) → Port of Long Beach",
            "Denmark → Port of Hamburg",
            "Port of LA/Long Beach → Port of Shanghai",
            "Aurubis Hamburg (DE) → Port of Shanghai",
            "Smithfield (NC) → US Domestic Hubs"
        ],
        vulnerabilities: ["African Swine Fever (ASF) risks", "Chinese State Reserve interventions", "Feed conversion ratio efficiency"],
        node_guide: {
            resource: "Intensive hog farming and breeding operations.",
            transformation: "Slaughter, primal cutting, and curing/processing.",
            logistic: "Strictly monitored cold-chain reefer shipping.",
            retail: "Fresh markets in Asia and processed meat retail."
        }
    },
    "Dairy": {
        title: "The White Gold",
        description: "Highly perishable in liquid form, but traded globally as milk powder and butter. New Zealand's Fonterra is the undisputed titan.",
        critical_node: "Fonterra Hub",
        top_producers: ["Fonterra", "Nestle", "Lactalis", "Danone", "Dairy Farmers of America"],
        top_traders: ["Fonterra", "GDT (Global Dairy Trade)"],
        strategic_flows: [
            "Waikato (NZ) → Port of Tauranga",
            "Brittany (FR) → Port of Le Havre",
            "Port of Tauranga → Port of Shanghai",
            "Le Havre (FR) → Port Said",
            "California Dairies → Port of Oakland"
        ],
        vulnerabilities: ["Milk Powder Price volatility", "Drought in New Zealand", "Chinese Infant Formula regulations"],
        node_guide: {
            resource: "Dairy herd milking and raw milk collection.",
            transformation: "Pasteurization, spray-drying, and butter churning.",
            logistic: "Reefer (Butter) and Dry (Powder) containers.",
            retail: "Infant formula plants and grocery dairy aisles."
        }
    },
    "Salmon": {
        title: "The Cold Chain Gold",
        description: "A high-value aquaculture product. Flown fresh around the world to sushi markets from the fjords of Norway and Chile.",
        critical_node: "Oslo Airport",
        top_producers: ["Mowi", "Leroy Seafood", "SalMar", "AquaChile", "Bakkafrost"],
        top_traders: ["Mitsubishi (Cermaq)"],
        strategic_flows: [
            "Norway Fjords → Oslo Airport",
            "Oslo Airport → Narita Airport (Japan)",
            "Puerto Montt (Chile) → Miami Airport",
            "Miami Airport → New York JFK",
            "Oslo Airport → Shanghai Pudong"
        ],
        vulnerabilities: ["Sea Lice and Algae Blooms", "Air Freight Fuel Costs", "Chilean Coastal Regulations"],
        node_guide: {
            resource: "Ocean-based net pen aquaculture and harvesting.",
            transformation: "Gutting, filleting, and specialized ice-packing.",
            logistic: "High-priority, temperature-controlled air freight.",
            retail: "High-end sushi restaurants and seafood retail."
        }
    },
    "Tuna": {
        title: "Harvest of the High Seas",
        description: "The world's most popular canned protein. Caught in the Pacific and processed in Thailand for global distribution.",
        critical_node: "Bangkok Cannery",
        top_producers: ["Thai Union", "Dongwon", "Bolton Group", "Itouchu"],
        top_traders: ["Mitsubishi", "Maruha Nichiro"],
        strategic_flows: [
            "Western Pacific → Bangkok Port",
            "Central Pacific → Port of Manta (EC)",
            "Bangkok Canneries → Port of LA",
            "Bangkok Canneries → Port of Rotterdam",
            "C. Kalimantan (Indo) → US East Coast"
        ],
        vulnerabilities: ["FAD Fishing Bans", "Illegal, Unreported, and Unregulated (IUU) fishing", "Can metal price spikes"],
        node_guide: {
            resource: "Purse seine and longline vessel operations.",
            transformation: "Cooking, cleaning, and canning in oil/brine.",
            logistic: "Reefer vessel (raw fish) and Dry container (cans).",
            retail: "Mass-market grocery retail and food service."
        }
    },
    "Tomatoes": {
        title: "The Industrial Red",
        description: "Processed into paste for the world's pizza and pasta. China and California dominate the industrial-scale production.",
        critical_node: "Tianjin Port",
        top_producers: ["Morning Star", "COFCO Tunhe", "The Kraft Heinz Co", "Sugal", "Conagra"],
        top_traders: ["Olam", "Cargill"],
        strategic_flows: [
            "Central Valley (USA) → Port of Oakland",
            "Xinjiang XPCC (China) → Tianjin Port",
            "Tianjin Port → Port of Lagos (Nigeria)",
            "Tianjin Port → Port of Naples (Italy)",
            "Port of Oakland → Tokyo Port"
        ],
        vulnerabilities: ["Water allocations in California", "Chinese Paste Sanctions", "Pest and Drought outbreaks"],
        node_guide: {
            resource: "Mechanized row crop harvesting for processing.",
            transformation: "Evaporation into high-brix tomato paste.",
            logistic: "Aseptic bags in drums and standard containers.",
            retail: "Food service (Pizza/Pasta) and sauce manufacturers."
        }
    },
    "Potatoes": {
        title: "The Global Fry",
        description: "The foundation of the global fast-food industry. Frozen French Fries are a high-value traded commodity.",
        critical_node: "Rotterdam Cold",
        top_producers: ["Lamb Weston", "McCain Foods", "Simplot", "Aviko", "Kraft Heinz"],
        top_traders: ["Sysco", "US Foods"],
        strategic_flows: [
            "Idaho (USA) → Port of Tacoma",
            "Netherlands Seed → Port of Rotterdam",
            "PNW (Portland) → Tokyo Port",
            "Rotterdam Coal Terminal → Port of Dumai",
            "Rotterdam Coal Terminal → Shanghai Port"
        ],
        vulnerabilities: ["Potato Late Blight disease", "Cold Storage Energy Costs", "QSR (Fast Food) Demand Shifts"],
        node_guide: {
            resource: "Mechanized potato harvesting and sorting.",
            transformation: "Washing, cutting, par-frying, and freezing.",
            logistic: "Strict -18°C cold-chain reefer transport.",
            retail: "Quick Service Restaurants (McDonald's, etc.) and retail."
        }
    },
    "Wine": {
        title: "The Liquid Culture",
        description: "A fragmented and premium market. Value is driven by origin (terroir), brand, and the unbroken chain from vineyard to table.",
        critical_node: "Le Havre Port",
        top_producers: ["Castel Group", "Constellation Brands", "E&J Gallo", "Treasury Wine Estates", "Pernod Ricard"],
        top_traders: ["LVMH", "Diageo"],
        strategic_flows: [
            "Bordeaux (France) → Port of Le Havre",
            "Napa Valley (USA) → Port of Oakland",
            "Mendoza (Argentina) → Port of Valparaiso",
            "Le Havre (FR) → Port of New York",
            "Port of Oakland → Shanghai Port"
        ],
        vulnerabilities: ["Extreme Weather (Frost/Fire) at origin", "Glass Bottle shortages", "Luxury Consumption trends"],
        node_guide: {
            resource: "Viticulture, harvesting, and on-estate vinification.",
            transformation: "Aging, blending, bottling, and labeling.",
            logistic: "Climate-controlled reefer or insulated containers.",
            retail: "Hospitality, specialized retail, and duty-free."
        }
    },
    "Orange Juice": {
        title: "Liquid Sunshine",
        description: "A highly concentrated market. Brazil's São Paulo state is the world's orchard, shipping frozen juice via specialized tankers.",
        critical_node: "Santos Juice",
        top_producers: ["Citrosuco", "Cutrale", "Louis Dreyfus", "Coca-Cola (Minute Maid)", "PepsiCo (Tropicana)"],
        top_traders: ["Cargill", "ADM"],
        strategic_flows: [
            "Sao Paulo Groves → Port of Santos",
            "Port of Santos → Port of Rotterdam",
            "Port of Santos → Port Newark",
            "Mosaic Florida → US Domestic Hubs",
            "Rotterdam Coal Terminal → EU Bottling Plants"
        ],
        vulnerabilities: ["Citrus Greening (HLB) disease", "Frost in Florida", "High Juice Tanker specificity"],
        node_guide: {
            resource: "Orange grove harvesting and extraction.",
            transformation: "Pasteurization, concentration, and freezing (FCOJ).",
            logistic: "Specialized juice tankers and bulk tank terminals.",
            retail: "Bottling plants and supermarket grocery aisles."
        }
    },
    "Bananas": {
        title: "The Perishable Titan",
        description: "The world's most traded fruit. A logistics marvel that moves green fruit at exactly 13°C across oceans to ripening rooms.",
        critical_node: "Guayaquil Port",
        top_producers: ["Chiquita", "Dole", "Del Monte", "Fyffes", "Noboa"],
        top_traders: ["Chiquita", "Dole"],
        strategic_flows: [
            "Port of Guayaquil → Panama Canal",
            "Panama Canal → Port of Rotterdam",
            "Panama Canal → Port of St. Petersburg (RU)",
            "Davao (Philippines) → SGE (Shanghai)",
            "Rotterdam Coal Terminal → EU Ripening Rooms"
        ],
        vulnerabilities: ["Tropical Race 4 (TR4) soil fungus", "Panama Canal Draft Restrictions", "Ripening Room Energy Costs"],
        node_guide: {
            resource: "Plantation harvesting, washing, and palletizing.",
            transformation: "Ripening room ethylene exposure at destination.",
            logistic: "Atmosphere-controlled reefer vessels and containers.",
            retail: "Supermarket fresh produce displays."
        }
    }
};
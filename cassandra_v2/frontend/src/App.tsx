import React, { useEffect, useState, useMemo } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import L from 'leaflet';
import { MapContainer, TileLayer, Marker, CircleMarker, Polyline, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { 
    Search, MapPin, Info, AlertTriangle, ShieldCheck, Play, Pause, Rewind, DollarSign, Activity, ChevronRight, ChevronDown, Filter, 
    Hammer, Factory, Ship, ShoppingCart, 
    Droplets, Flame, Zap, Gem, Coins, Sparkles, BrickWall, Trees, Cpu, FlaskConical,
    Wheat, Bean, Sprout, Banana, Wine, Fish, Milk, Beef, Drumstick, Apple, Leaf,
    CircleDot, Nut, Shirt, Grape, Citrus, GlassWater,
    Mountain, Anvil, Car, Construction, Fuel, ShieldAlert
} from 'lucide-react';
import clsx from 'clsx';
import { COMMODITY_MANIFEST } from './data/commodity_manifest';
import { CommodityFilter } from './components/CommodityFilter';
import { InspectionPanel } from './components/InspectionPanel';
import { FinancialDashboard } from './components/FinancialDashboard';
import { ScenarioControl } from './components/ScenarioControl';
import { NewsFeed } from './components/NewsFeed';
import { CommodityDossier } from './components/CommodityDossier';

const MapController = ({ selectedNode, selectedEdge, nodes }: { selectedNode: any, selectedEdge: any, nodes: any[] }) => {
    const map = useMap();
    useEffect(() => {
        if (selectedNode) {
            map.flyTo([selectedNode.location.lat, selectedNode.location.lng], 6, { duration: 1.5 });
        } else if (selectedEdge && nodes) {
            const src = nodes.find((n: any) => n.id === selectedEdge.source_id);
            const tgt = nodes.find((n: any) => n.id === selectedEdge.target_id);
            if (src && tgt) {
                let lng1 = src.location.lng;
                let lng2 = tgt.location.lng;
                
                // Handle Antimeridian
                if (Math.abs(lng1 - lng2) > 180) {
                    if (lng1 > 0) lng1 -= 360;
                    else lng2 -= 360;
                }

                const midLat = (src.location.lat + tgt.location.lat) / 2;
                const midLng = (lng1 + lng2) / 2;
                
                // Dynamic Zoom based on distance
                const dist = Math.sqrt(Math.pow(src.location.lat - tgt.location.lat, 2) + Math.pow(lng1 - lng2, 2));
                const zoom = dist > 50 ? 3 : (dist > 20 ? 4 : 5);

                map.flyTo([midLat, midLng], zoom, { duration: 1.5 });
            }
        }
    }, [selectedNode, selectedEdge, nodes, map]);
    return null;
};

// Deterministic Jitter
const getJitteredPosition = (lat: number, lng: number, id: string) => {
    const seed = id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    const angle = (seed % 360) * (Math.PI / 180);
    const distance = 0.5 + (seed % 10) * 0.05; 
    return [lat + Math.cos(angle) * distance, lng + Math.sin(angle) * distance] as [number, number];
};

const getCommodityIcon = (commodity: string, type: string) => {
    const c = commodity.toLowerCase();
    const t = type.toLowerCase();

    // Global Overrides for Stage
    if (t === 'logistic') return Ship;
    
    // --- NON-FOOD ---

    // Energy
    if (c.includes('oil') || c.includes('gas') || c.includes('fuel')) {
        if (t === 'resource') return Fuel; // Extraction
        if (t === 'transformation') return Factory; // Refinery
        return Droplets;
    }
    if (c.includes('coal')) return Mountain;
    if (c.includes('uranium')) return Zap;
    if (c.includes('battery') || c.includes('lithium')) {
        if (t === 'resource') return Mountain; // Spodumene/Brine
        if (t === 'transformation') return FlaskConical; // Chemical Processing
        if (t === 'retail') return Car; // EV
        return Zap;
    }
    
    // Metals (Precious & Industrial)
    if (c.includes('gold') || c.includes('silver') || c.includes('platinum') || c.includes('palladium') || 
        c.includes('copper') || c.includes('iron') || c.includes('aluminum') || c.includes('zinc') || 
        c.includes('nickel') || c.includes('lead') || c.includes('cobalt') || c.includes('tin')) {
        
        if (t === 'resource') return Mountain; // Mine
        if (t === 'transformation') return Anvil; // Smelter/Forge
        return Hammer;
    }
    
    if (c.includes('rare')) return Sparkles;
    
    // Industrial Materials
    if (c.includes('cement')) return BrickWall;
    if (c.includes('lumber') || c.includes('rubber')) return Trees;
    if (c.includes('cotton')) return Shirt;
    if (c.includes('silicon') || c.includes('semi')) {
        if (t === 'resource') return Mountain; // Silica Mine
        return Cpu; // Fab
    }
    if (c.includes('potash') || c.includes('phosphate') || c.includes('urea')) {
        if (t === 'resource') return Mountain;
        return FlaskConical; // Fertilizer Plant
    }
    
    // --- FOOD (Simplified) ---
    // Agri (Crops)
    if (c.includes('wheat') || c.includes('corn') || c.includes('rice') || c.includes('soy')) return Wheat;
    if (c.includes('potato')) return Nut;
    
    // Agri (Plantation)
    if (c.includes('coffee') || c.includes('cocoa')) return Bean;
    if (c.includes('tea')) return Leaf;
    if (c.includes('sugar')) return Sprout;
    if (c.includes('banana')) return Banana;
    if (c.includes('orange')) return Citrus;
    if (c.includes('tomato')) return Apple;
    if (c.includes('wine') || c.includes('grape')) return Grape;
    
    // Animal
    if (c.includes('beef') || c.includes('pork')) return Beef;
    if (c.includes('poultry')) return Drumstick;
    if (c.includes('dairy')) return Milk;
    if (c.includes('salmon') || c.includes('tuna')) return Fish;

    // Fallback based on Type
    switch (t) {
        case 'resource': return Mountain;
        case 'transformation': return Factory;
        case 'logistic': return Ship;
        case 'retail': return ShoppingCart;
        default: return CircleDot;
    }
};

// Visual Harmony Plan: Semantic Shapes & Colors
const getTypeVisuals = (type: string) => {
    switch (type) {
        case 'resource': return { shape: 'hexagon', fill: '#064e3b', stroke: '#10b981', color: '#34d399' }; // Emerald-900/500/400
        case 'transformation': return { shape: 'square', fill: '#451a03', stroke: '#f59e0b', color: '#fbbf24' }; // Amber-950/500/400
        case 'logistic': return { shape: 'triangle', fill: '#083344', stroke: '#06b6d4', color: '#22d3ee' }; // Cyan-950/500/400
        case 'retail': return { shape: 'circle', fill: '#4a044e', stroke: '#d946ef', color: '#e879f9' }; // Fuchsia-950/500/400
        default: return { shape: 'circle', fill: '#0f172a', stroke: '#64748b', color: '#94a3b8' };
    }
};

const createNodeIcon = (node: any, isSelected: boolean, riskView: boolean = false) => {
    const tension = node.tension_score || 0;
    const isStressed = tension > 50;
    const isHighRisk = node.risk_level > 0.5;
    const v = getTypeVisuals(node.type);
    
    // Override colors for Stress or Risk
    let fill = isStressed ? '#450a0a' : v.fill;
    let stroke = isStressed ? '#ef4444' : v.stroke;
    let iconColor = isStressed ? '#ef4444' : v.color;

    if (riskView && isHighRisk) {
        fill = '#7f1d1d'; // Dark Red
        stroke = '#f87171'; // Lighter Red
        iconColor = '#fee2e2'; 
    }

    // Size & Z-Index Logic (Visual Polish)
    // ...
    
    let size = 32;
    let iconSize = 16;
    let zIndex = 100;

    if (isSelected) {
        size = 48;
        iconSize = 24;
        zIndex = 1000;
    } else {
        switch (node.type) {
            case 'resource': size = 28; iconSize = 14; zIndex = 10; break;
            case 'transformation': size = 30; iconSize = 15; zIndex = 20; break;
            case 'retail': size = 28; iconSize = 14; zIndex = 30; break;
            case 'logistic': size = 26; iconSize = 12; zIndex = 50; break;
        }
        if (isStressed || (riskView && isHighRisk)) {
            zIndex = 500;
            size += 4;
        }
    }
    
    const center = size / 2;

    // ... (rest of SVG generation)
    let shapeSvg = '';
    if (v.shape === 'hexagon') {
        const r = size / 2 - 2;
        const p = `
            ${center - r},${center} 
            ${center - r/2},${center - r*0.866} 
            ${center + r/2},${center - r*0.866} 
            ${center + r},${center} 
            ${center + r/2},${center + r*0.866} 
            ${center - r/2},${center + r*0.866}
        `;
        shapeSvg = `<polygon points="${p}" fill="${fill}" stroke="${stroke}" stroke-width="${isSelected ? 3 : 2}" />`;
    } else if (v.shape === 'triangle') {
        const p = `${center},${2} ${size-2},${size-2} ${2},${size-2}`;
        shapeSvg = `<polygon points="${p}" fill="${fill}" stroke="${stroke}" stroke-width="${isSelected ? 3 : 2}" />`;
    } else if (v.shape === 'square') {
        const s = size - 6;
        shapeSvg = `<rect x="3" y="3" width="${s}" height="${s}" rx="4" fill="${fill}" stroke="${stroke}" stroke-width="${isSelected ? 3 : 2}" />`;
    } else {
        const r = size / 2 - 3;
        shapeSvg = `<circle cx="${center}" cy="${center}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${isSelected ? 3 : 2}" />`;
    }

    const iconMarkup = renderToStaticMarkup(
        React.createElement(getCommodityIcon(node.commodity, node.type), { 
            size: iconSize, 
            color: iconColor, 
            strokeWidth: 2.5 
        })
    );

    const pulseClass = (isStressed || (riskView && isHighRisk)) ? 'animate-pulse-ring' : '';
    const shadowFilter = isSelected ? 'drop-shadow(0 0 8px rgba(0,0,0,0.8))' : 'drop-shadow(0 0 4px rgba(0,0,0,0.5))';

    const html = `
        <div class="${pulseClass}" style="width: ${size}px; height: ${size}px; position: relative; filter: ${shadowFilter}; transition: all 0.3s ease;">
            <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" style="position: absolute; top: 0; left: 0; z-index: 0;">
                ${shapeSvg}
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); display: flex; align-items: center; justify-content: center; z-index: 10;">
                ${iconMarkup}
            </div>
        </div>
    `;
    
    return L.divIcon({
        html: html,
        className: 'bg-transparent', 
        iconSize: [size, size],
        iconAnchor: [center, center],
        popupAnchor: [0, -center]
    });
};

const createVesselIcon = (vessel: any) => {
    const iconMarkup = renderToStaticMarkup(<Ship size={14} color="#06b6d4" strokeWidth={2.5} />);
    return L.divIcon({
        className: 'vessel-marker',
        html: `<div style="
            background-color: #083344; 
            width: 24px; 
            height: 24px; 
            border-radius: 4px; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            border: 1px solid #06b6d4;
            box-shadow: 0 0 10px rgba(6,182,212,0.5);
            transform: rotate(45deg);
        "><div style="transform: rotate(-45deg)">${iconMarkup}</div></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });
};

export default function App() {
  const [timeline, setTimeline] = useState<any[]>([]);
  const [day, setDay] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [selectedEdge, setSelectedEdge] = useState<any>(null);
  const [traceData, setTraceData] = useState<any>(null);
  const [actors, setActors] = useState<any[]>([]);

  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedCommodity, setSelectedCommodity] = useState<string | null>(null);
  const [expandedCategories, setExpandedCategories] = useState<string[]>(['Food', 'Non-Food']);
  const [showLogistics, setShowLogistics] = useState(true);
  const [riskView, setRiskView] = useState(false);
  const [showDossier, setShowDossier] = useState(false);

  const data = timeline.length > 0 ? timeline[day] : null;

  useEffect(() => {
    // Initial Simulation (Normal Ops)
    fetch('http://localhost:8002/api/simulate_timeline', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify([]) // No injections
    })
      .then(res => res.json())
      .then(newTimeline => {
          setTimeline(newTimeline);
          setDay(0);
          setIsPlaying(true); // Auto-play on load
      })
      .catch(console.error);

    // Sprint 1 (v7.0): Load Actors
    fetch('http://localhost:8002/api/actors')
        .then(res => res.json())
        .then(setActors)
        .catch(console.error);
  }, []);

  useEffect(() => {
    let interval: any;
    if (isPlaying && timeline.length > 1) {
        interval = setInterval(() => {
            setDay(d => {
                if (d >= timeline.length - 1) {
                    setIsPlaying(false);
                    return d;
                }
                return d + 1;
            });
        }, 150); 
    }
    return () => clearInterval(interval);
}, [isPlaying, timeline]);

  useEffect(() => {
      if (selectedNode) {
          fetch(`http://localhost:8002/api/trace/${selectedNode.id}`)
            .then(res => res.json())
            .then(setTraceData);
      } else {
          setTraceData(null);
      }
  }, [selectedNode]);

  const handleSim = (targetId: string | null, type: string = 'blockage', severity: number = 1.0) => {
    if (!targetId) return;
    fetch('http://localhost:8002/api/simulate_timeline', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify([{ target_id: targetId, type, severity }])
    })
    .then(res => res.json())
    .then(newTimeline => {
        setTimeline(newTimeline);
        setDay(0);
        setIsPlaying(true);
    });
  };

  const handlePlaybook = (injections: any[]) => {
    fetch('http://localhost:8002/api/simulate_timeline', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(injections)
    })
    .then(res => res.json())
    .then(newTimeline => {
        setTimeline(newTimeline);
        setDay(0);
        setIsPlaying(true);
    });
  };

  const handleFlowClick = (flow: string) => {
      if (!data) return;
      
      // Split "Ghawar (Saudi) → Ras Tanura"
      const parts = flow.split('→');
      const srcRaw = parts[0].trim();
      const tgtRaw = parts.length > 1 ? parts[1].trim() : "";
      
      const clean = (s: string) => s.split('(')[0].trim().toLowerCase();
      
      const s = clean(srcRaw); // "ghawar"
      const t = tgtRaw ? clean(tgtRaw) : ""; // "ras tanura"
      
      let foundEdge = null;
      let foundNode = null;
      
      if (t) {
        // Look for Edge
        foundEdge = data.edges.find((e: any) => {
            const srcNode = data.nodes.find((n: any) => n.id === e.source_id);
            const tgtNode = data.nodes.find((n: any) => n.id === e.target_id);
            if (!srcNode || !tgtNode) return false;
            
            const srcMatch = srcNode.label.toLowerCase().includes(s);
            const tgtMatch = tgtNode.label.toLowerCase().includes(t);
            
            return srcMatch && tgtMatch;
        });
      }
      
      if (foundEdge) {
          setSelectedEdge(foundEdge);
          setSelectedNode(null);
      } else {
          // Fallback: Find Node (Source or Target)
          // Try Source first
          foundNode = data.nodes.find((n: any) => n.label.toLowerCase().includes(s));
          if (!foundNode && t) {
              foundNode = data.nodes.find((n: any) => n.label.toLowerCase().includes(t));
          }
          
          if (foundNode) {
              setSelectedNode(foundNode);
              setSelectedEdge(null);
          }
      }
  };

  const categories = useMemo(() => {
      if (!data) return {};
      const cats: Record<string, Set<string>> = {};
      data.nodes.forEach((n: any) => {
          if (!n.category) return;
          if (!cats[n.category]) cats[n.category] = new Set();
          if (n.commodity) cats[n.category].add(n.commodity);
      });
      return cats;
  }, [data]);

  const searchResults = useMemo(() => {
      if (!data || !searchQuery) return [];
      const lowerQuery = searchQuery.toLowerCase();
      
      const nodes = data.nodes.filter((n: any) => n.label.toLowerCase().includes(lowerQuery)).map((n: any) => ({
          type: 'node',
          data: n,
          label: n.label,
          subLabel: `${n.type} • ${n.commodity}`
      }));

      const allCommodities = new Set<string>();
      data.nodes.forEach((n: any) => {
          if (n.commodity) allCommodities.add(n.commodity);
      });
      
      const commodities = Array.from(allCommodities)
          .filter(c => c.toLowerCase().includes(lowerQuery))
          .map(c => ({
              type: 'commodity',
              data: c,
              label: c,
              subLabel: 'Commodity Filter'
          }));

      return [...commodities, ...nodes];
  }, [data, searchQuery]);

  const toggleCategory = (cat: string) => {
      if (expandedCategories.includes(cat)) {
          setExpandedCategories(expandedCategories.filter(c => c !== cat));
      } else {
          setExpandedCategories([...expandedCategories, cat]);
      }
  };

  const filteredMapNodes = useMemo(() => {
    if (!data) return [];
    return data.nodes.filter((n: any) => {
        if (selectedCommodity && n.commodity !== selectedCommodity) return false;
        if (selectedCategory && n.category !== selectedCategory) return false;
        return true;
    });
  }, [data, selectedCategory, selectedCommodity]);

  const filteredMapEdges = useMemo(() => {
      if (!data) return [];
      const visibleNodeIds = new Set(filteredMapNodes.map((n: any) => n.id));
      return data.edges.filter((e: any) => visibleNodeIds.has(e.source_id) && visibleNodeIds.has(e.target_id));
  }, [data, filteredMapNodes]);

  const NEWS = [
      { id: 1, text: "LME Lithium opens at $13,500.", stress: 0.0, target: null },
      { id: 2, text: "ALERT: Sichuan Earthquake reported.", stress: 2.0, target: 'refinery_tianqi' },
      { id: 3, text: "Typhoon warning in Malacca Strait.", stress: 1.5, target: 'choke_malacca' },
  ];

  if (!data) return <div className="p-10 text-white font-mono flex items-center justify-center h-screen bg-slate-950">INITIALIZING GLOBAL TWIN...</div>;

  const totalLoss = timeline.slice(0, day + 1).reduce((acc, curr) => acc + (curr.global_loss || 0), 0);
  const cumulativeBreakdown = timeline.slice(0, day + 1).reduce((acc, curr) => {
      const b = curr.systemic_risk_breakdown || {};
      acc.unmet_value += b.unmet_value || 0;
      acc.revenue_loss += b.revenue_loss || 0;
      acc.choke_penalty += b.choke_penalty || 0;
      return acc;
  }, { unmet_value: 0, revenue_loss: 0, choke_penalty: 0 });
  const cumulativeSummary = {
      scenario: data?.systemic_risk_summary?.scenario,
      total: totalLoss,
      unmet: cumulativeBreakdown.unmet_value,
      revenue: cumulativeBreakdown.revenue_loss,
      choke: cumulativeBreakdown.choke_penalty,
      peak_total: data?.systemic_risk_summary?.peak_total,
      peak_day: data?.systemic_risk_summary?.peak_day
  };

  return (
    <div className="h-screen w-screen flex bg-slate-900 text-white font-sans overflow-hidden">
      
      {/* Sidebar (Left) - Navigation & Filters */}
      <div className="w-80 border-r border-slate-800 bg-slate-950 flex flex-col z-20 shadow-2xl shrink-0">
        <div className="p-4 border-b border-slate-800 bg-slate-900/50">
            <div className="flex items-center justify-between mb-4">
                <h1 className="text-lg font-bold text-cyan-400 tracking-tighter flex items-center gap-2">
                    <Activity className="text-cyan-500" size={20} /> CASSANDRA v7.5
                </h1>
                <button 
                    onClick={() => setShowLogistics(!showLogistics)}
                    className={clsx(
                        "p-1.5 rounded transition-all",
                        showLogistics ? "bg-cyan-500/20 text-cyan-400" : "bg-slate-800 text-slate-500 hover:text-slate-300"
                    )}
                    title="Toggle Logistics Layer"
                >
                    <Ship size={16} />
                </button>
                <button 
                    onClick={() => setRiskView(!riskView)}
                    className={clsx(
                        "p-1.5 rounded transition-all ml-1",
                        riskView ? "bg-red-500/20 text-red-400 border border-red-500/30" : "bg-slate-800 text-slate-500 hover:text-slate-300"
                    )}
                    title="Toggle Geopolitical Risk View"
                >
                    <ShieldAlert size={16} />
                </button>
            </div>
            <div className="relative group">
                <Search className="absolute left-3 top-2.5 text-slate-500" size={16} />
                <input 
                    type="text" 
                    placeholder="Search nodes or commodities..." 
                    className="w-full bg-slate-900 border border-slate-700 rounded pl-10 pr-4 py-2 text-xs text-white focus:border-cyan-500 outline-none transition-all"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                {searchQuery && (
                    <div className="absolute top-full left-0 w-full bg-slate-900 border border-slate-700 rounded-b mt-1 max-h-60 overflow-y-auto z-50 shadow-xl">
                        {searchResults.length === 0 ? (
                            <div className="p-2 text-xs text-slate-500">No results found.</div>
                        ) : (
                            searchResults.map((result: any, i: number) => (
                                <div 
                                    key={i}
                                    className="p-2 hover:bg-slate-800 cursor-pointer text-xs border-b border-slate-800 last:border-0"
                                    onClick={() => {
                                        if (result.type === 'node') {
                                            setSelectedNode(result.data);
                                            if (selectedCommodity && selectedCommodity !== result.data.commodity) {
                                                setSelectedCommodity(null);
                                                setSelectedCategory(null);
                                                setShowDossier(false);
                                            }
                                        } else {
                                            setSelectedCommodity(result.data);
                                            setSelectedCategory(null);
                                            setSelectedNode(null);
                                            setShowDossier(true);
                                        }
                                        setSearchQuery("");
                                    }}
                                >
                                    <div className="font-bold text-cyan-400">{result.label}</div>
                                    <div className="text-slate-500 flex justify-between">
                                        <span>{result.subLabel}</span>
                                        {result.type === 'commodity' && <Filter size={10} className="text-cyan-600"/>}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                )}
            </div>
        </div>

        {/* Commodity Filter Section - Now takes available space */}
        <div className="flex-1 overflow-y-auto min-h-0">
            <CommodityFilter 
                categories={categories}
                selectedCategory={selectedCategory}
                selectedCommodity={selectedCommodity}
                onSelectCategory={setSelectedCategory}
                onSelectCommodity={setSelectedCommodity}
                onShowDossier={setShowDossier}
            />
        </div>
      </div>

      {/* Main Content (Center) */}
      <div className="flex-1 relative flex flex-col min-w-0">
        {/* Commodity Dossier Overlay (v7.0 Sprint 4) */}
        {showDossier && selectedCommodity && COMMODITY_MANIFEST[selectedCommodity] && (
            <div className="absolute inset-y-0 right-0 w-[400px] z-[5000] shadow-[-20px_0_40px_rgba(0,0,0,0.5)]">
                <CommodityDossier 
                    commodity={selectedCommodity} 
                    dossier={COMMODITY_MANIFEST[selectedCommodity]} 
                    onClose={() => setShowDossier(false)} 
                    onFlowClick={handleFlowClick}
                />
            </div>
        )}

        <div className="flex-1 relative">
            <MapContainer center={[20, 100]} zoom={3} className="h-full w-full" style={{background:'#020617'}}>
              <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" />
              <MapController selectedNode={selectedNode} selectedEdge={selectedEdge} nodes={data.nodes} />
              
              {/* Sea Lanes Layer (Global Backbone) */}
              {showLogistics && data.sea_lanes && data.sea_lanes.edges.map((e: any, i: number) => {
                  const srcWp = data.sea_lanes.waypoints.find((w: any) => w.id === e.source);
                  const tgtWp = data.sea_lanes.waypoints.find((w: any) => w.id === e.target);
                  if (!srcWp || !tgtWp) return null;
                  
                  return <Polyline 
                    key={`lane-${i}`}
                    positions={[[srcWp.location.lat, srcWp.location.lng], [tgtWp.location.lat, tgtWp.location.lng]]}
                    pathOptions={{ 
                        color: '#0ea5e9', // Sky-500
                        weight: 1, 
                        dashArray: '3, 6',
                        className: 'flow-line-normal', 
                        opacity: 0.3 
                    }} 
                 />
              })}

              {filteredMapEdges.map((e: any, i: number) => {
                 const src = data.nodes.find((n: any) => n.id === e.source_id);
                 const tgt = data.nodes.find((n: any) => n.id === e.target_id);
                 if(!src || !tgt) return null;
                 const [srcLat, srcLng] = getJitteredPosition(src.location.lat, src.location.lng, src.id);
                 const [tgtLat, tgtLng] = getJitteredPosition(tgt.location.lat, tgt.location.lng, tgt.id);
                 
                 const isStressed = src.tension_score > 50;
                 const isSelected = selectedEdge === e;
                 
                 return <Polyline 
                    key={i} 
                    positions={[[srcLat, srcLng], [tgtLat, tgtLng]]} 
                    pathOptions={{ 
                        color: isSelected ? '#22d3ee' : (isStressed ? '#ef4444' : '#3b82f6'), 
                        weight: isSelected ? 5 : (isStressed ? 3 : 1.5), 
                        dashArray: '10, 10', 
                        className: isStressed ? 'flow-line-stressed' : 'flow-line-normal', 
                        opacity: isSelected ? 1.0 : (isStressed ? 1.0 : 0.6) 
                    }}
                    eventHandlers={{
                        click: () => {
                            setSelectedEdge(e);
                            setSelectedNode(null);
                        }
                    }}
                 />
              })}

              {filteredMapNodes.map((n: any) => {
                const isSelected = selectedNode && selectedNode.id === n.id;
                const [lat, lng] = getJitteredPosition(n.location.lat, n.location.lng, n.id);
                
                // Z-Index Logic
                let zIndex = 100;
                if (n.tension_score > 50) zIndex = 1000;
                else if (n.type === 'logistic') zIndex = 500; // Ports on top
                else if (n.type === 'retail') zIndex = 300;
                else if (n.type === 'transformation') zIndex = 200;
                else zIndex = 100; // Resources at bottom

                if (isSelected) zIndex = 2000;

                return (
                    <Marker 
                        key={n.id} 
                        position={[lat, lng]} 
                        icon={createNodeIcon(n, isSelected, riskView)}
                        zIndexOffset={zIndex}
                        eventHandlers={{
                            click: () => {
                                setSelectedNode(n);
                                setSelectedEdge(null);
                            }
                        }}
                    />
                );
              })}

              {/* Vessel Layer */}
              {data.vessels?.map((v: any, index: number) => {
                  // v5.1 Visual Queueing: Offset vessels at the same location
                  const otherVesselsAtSameLoc = data.vessels.slice(0, index).filter((ov: any) => 
                      ov.current_location.lat === v.current_location.lat && 
                      (ov.current_location.lng || ov.current_location.lon) === (v.current_location.lng || v.current_location.lon)
                  );
                  
                  const offsetScale = 0.005; // Degree offset for visual separation
                  const lat = v.current_location.lat + (otherVesselsAtSameLoc.length * offsetScale);
                  const lng = (v.current_location.lng || v.current_location.lon || 0) + (otherVesselsAtSameLoc.length * offsetScale);

                  return (
                    <React.Fragment key={`vessel-group-${v.id}`}>
                      {showLogistics && v.status === 'transit' && v.destination_location && (
                          <Polyline 
                              positions={[
                                  [v.current_location.lat, v.current_location.lng || v.current_location.lon || 0],
                                  ...(v.route_path || []).map((wp: any) => [wp.lat, wp.lng || wp.lon || 0]),
                                  [v.destination_location.lat, v.destination_location.lng || v.destination_location.lon || 0]
                              ]}
                              pathOptions={{ 
                                  color: '#06b6d4', 
                                  weight: 1, 
                                  dashArray: '5, 5', 
                                  opacity: 0.4,
                                  interactive: false
                              }}
                          />
                      )}
                      {showLogistics && (
                          <Marker
                            key={v.id}
                            position={[lat, lng]}
                            icon={createVesselIcon(v)}
                          >
                              <Popup>
                                  <div className="font-bold text-cyan-400">{v.name}</div>
                                  <div className="text-xs text-slate-400 uppercase">{v.vessel_class.name} Class</div>
                                  <div className="text-xs mt-1">Status: <span className="text-white font-bold">{v.status}</span></div>
                                  {v.distance_remaining > 0 && (
                                      <div className="text-[10px] text-slate-500 mt-1">Distance Remaining: {Math.round(v.distance_remaining)} nm</div>
                                  )}
                              </Popup>
                          </Marker>
                      )}
                    </React.Fragment>
                  );
              })}
            </MapContainer>

            {/* Overlays (Rendered last to stay on top) */}
            {data.global_loss > 0 && (
                <div className="absolute top-0 left-0 w-full z-[3000] bg-red-600/90 backdrop-blur text-white text-center py-1 text-[10px] font-bold tracking-[0.2em] uppercase animate-pulse">
                    Critical Supply Disruption Detected — Day {day}
                </div>
            )}

            <InspectionPanel 
                node={selectedNode} 
                edge={selectedEdge}
                traceData={traceData} 
                actors={actors}
                onClose={() => { setSelectedNode(null); setSelectedEdge(null); }}
            />
        </div>

        <div className="h-20 bg-slate-950 border-t border-slate-800 flex items-center px-8 gap-6 z-30 shadow-[0_-10px_20px_rgba(0,0,0,0.5)]">
            <div className="flex flex-col">
                <div className="text-[10px] text-slate-500 uppercase font-bold tracking-widest mb-1">Causal Horizon</div>
                <div className="text-xl font-mono font-bold text-cyan-400">DAY {day.toString().padStart(2, '0')}</div>
            </div>
            <button onClick={() => setIsPlaying(!isPlaying)} className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-slate-700 text-white transition-colors">
                {isPlaying ? <Pause size={16} /> : <Play size={16} />}
            </button>
            <div className="flex-1 relative group">
                <input type="range" min="0" max={timeline.length - 1 || 0} value={day} onChange={(e) => setDay(parseInt(e.target.value))} className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500 hover:accent-cyan-400" />
            </div>
            <button onClick={() => {setDay(0); setIsPlaying(false);}} className="p-2 text-slate-500 hover:text-white"><Rewind size={16} /></button>
        </div>
      </div>

      {/* Sidebar (Right) - Ops & Analysis */}
      <div className="w-80 border-l border-slate-800 bg-slate-950 flex flex-col z-20 shadow-2xl shrink-0">
        <FinancialDashboard 
            totalLoss={totalLoss} 
            currentPrices={data.prices} 
            selectedCommodity={selectedCommodity}
            systemicBreakdown={{ ...cumulativeBreakdown, blocked_chokes: data.systemic_risk_breakdown?.blocked_chokes || [] }}
            systemicSummary={cumulativeSummary}
        />
        
        <div className="flex-1 overflow-hidden flex flex-col min-h-0">
            <div className="h-1/3 overflow-y-auto border-b border-slate-800 shrink-0">
                <NewsFeed onSimulate={handleSim} />
            </div>
            <div className="flex-1 overflow-y-auto">
                <ScenarioControl selectedNode={selectedNode} onInject={handleSim} onPlaybook={handlePlaybook} />
            </div>
        </div>
        
        <div className="p-4 border-t border-slate-800 bg-slate-900/50 mt-auto">
            <button onClick={() => { 
                fetch('http://localhost:8002/api/reset', { method: 'POST' })
                .then(() => window.location.reload()); 
            }} className="w-full bg-slate-800 p-2 rounded text-[10px] font-bold uppercase tracking-widest hover:bg-slate-700 transition-colors text-slate-400 hover:text-white">
                REBOOT SYSTEM
            </button>
        </div>
      </div>
    </div>
  );
}

import React from 'react';
import clsx from 'clsx';
import { Activity, Anchor, MapPin, Share2, AlertOctagon, Ship, ArrowRight, Truck } from 'lucide-react';

interface InspectionPanelProps {
    node: any;
    edge: any;
    traceData: any;
    actors: any[];
    onClose: () => void;
}

export const InspectionPanel: React.FC<InspectionPanelProps> = ({ node, edge, traceData, actors, onClose }) => {
    if (!node && !edge) return null;

    if (edge) {
        const carrier = actors.find(a => a.id === edge.carrier_id);
        const modeIcon = edge.transport_mode === 'sea' ? <Ship size={14} /> : <Truck size={14} />;
        
        return (
            <div className="absolute top-6 right-6 w-80 bg-slate-950/90 backdrop-blur-xl border border-slate-800 rounded-2xl p-0 z-[4000] shadow-2xl animate-in fade-in slide-in-from-right-4 pointer-events-auto overflow-hidden">
                {/* Edge Header */}
                <div className="relative h-24 bg-gradient-to-br from-slate-900 to-slate-950 border-b border-slate-800 p-5 flex flex-col justify-end">
                    <button 
                        onClick={onClose} 
                        className="absolute top-3 right-3 w-8 h-8 rounded-full bg-black/20 hover:bg-white/10 flex items-center justify-center text-slate-400 hover:text-white transition-colors"
                    >
                        ✕
                    </button>
                    <div className="flex items-center gap-2 mb-1">
                        <span className="text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full border bg-cyan-500/10 text-cyan-400 border-cyan-500/20 flex items-center gap-1">
                            {modeIcon} {edge.transport_mode} Route
                        </span>
                    </div>
                    <div className="flex items-center gap-2 text-white font-bold text-lg leading-none tracking-tight">
                        <span className="truncate max-w-[100px]">{edge.source_id.split('_').slice(2).join(' ')}</span>
                        <ArrowRight size={16} className="text-slate-500" />
                        <span className="truncate max-w-[100px]">{edge.target_id.split('_').slice(2).join(' ')}</span>
                    </div>
                </div>

                {/* Content */}
                <div className="p-5 space-y-6">
                    {/* Logistics Card */}
                    <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 space-y-3">
                        <div className="flex justify-between items-center border-b border-slate-800 pb-2">
                            <div className="text-[10px] uppercase text-slate-500 font-bold tracking-widest">Transit Time</div>
                            <div className="text-sm font-mono font-bold text-white">{edge.lag_days} DAYS</div>
                        </div>
                        <div className="flex justify-between items-center border-b border-slate-800 pb-2">
                             <div className="text-[10px] uppercase text-slate-500 font-bold tracking-widest">Distance</div>
                             <div className="text-sm font-mono font-bold text-white">{edge.distance_km ? edge.distance_km.toFixed(0) : "N/A"} km</div>
                        </div>
                        <div className="flex justify-between items-center">
                             <div className="text-[10px] uppercase text-slate-500 font-bold tracking-widest">Route Risk</div>
                             <div className={clsx("text-sm font-mono font-bold", edge.risk_level > 0.5 ? "text-red-400" : "text-emerald-400")}>
                                {(edge.risk_level * 100).toFixed(0)}%
                             </div>
                        </div>
                    </div>

                    {/* Carrier Card */}
                    {carrier ? (
                        <div className="bg-slate-900 border border-slate-800 rounded-lg p-3 flex items-center gap-3">
                            <div className="w-10 h-10 rounded bg-slate-800 flex items-center justify-center text-xl font-bold text-cyan-500 uppercase">
                                {carrier.name.substring(0, 2)}
                            </div>
                            <div>
                                <div className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">LOGISTICS OPERATOR</div>
                                <div className="text-sm font-bold text-white">{carrier.name}</div>
                                <div className="text-[9px] text-slate-400">{carrier.hq_country} • {carrier.attributes?.fleet || "Logistics"}</div>
                            </div>
                        </div>
                    ) : (
                        <div className="p-3 border border-dashed border-slate-800 rounded text-center text-xs text-slate-600">
                            No Specific Carrier Assigned
                        </div>
                    )}

                    {/* Infrastructure Info */}
                    {edge.infrastructure_id && (
                        <div className="p-3 bg-indigo-950/20 border border-indigo-500/20 rounded-lg">
                            <div className="text-[9px] font-bold text-indigo-400 uppercase tracking-widest mb-1">Infrastructure</div>
                            <div className="text-sm font-bold text-indigo-200">{edge.infrastructure_id.replace('infra_', '').replace(/_/g, ' ').toUpperCase()}</div>
                        </div>
                    )}
                </div>
            </div>
        );
    }

    const owner = actors.find(a => a.id === node.owner_id);
    const isCritical = node.inventory < 30;
    const isStressed = node.tension_score > 50;

    const maxInv = node.specs?.max_inventory || 10000;
    const invPct = Math.min((node.inventory / maxInv) * 100, 100);

    return (
        <div className="absolute top-6 right-6 w-80 bg-slate-950/90 backdrop-blur-xl border border-slate-800 rounded-2xl p-0 z-[4000] shadow-2xl animate-in fade-in slide-in-from-right-4 pointer-events-auto overflow-hidden">
            {/* Header */}
            <div className="relative h-24 bg-gradient-to-br from-slate-900 to-slate-950 border-b border-slate-800 p-5 flex flex-col justify-end">
                <button 
                    onClick={onClose} 
                    className="absolute top-3 right-3 w-8 h-8 rounded-full bg-black/20 hover:bg-white/10 flex items-center justify-center text-slate-400 hover:text-white transition-colors"
                >
                    ✕
                </button>
                <div className="flex items-center gap-2 mb-1">
                    <span className={clsx(
                        "text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full border",
                        node.type === 'resource' ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
                        node.type === 'transformation' ? "bg-amber-500/10 text-amber-400 border-amber-500/20" :
                        node.type === 'logistic' ? "bg-blue-500/10 text-blue-400 border-blue-500/20" :
                        "bg-purple-500/10 text-purple-400 border-purple-500/20"
                    )}>
                        {node.type}
                    </span>
                    <span className="text-[10px] font-bold uppercase tracking-widest text-slate-500 flex items-center gap-1">
                        <MapPin size={10} />
                        {node.location.lat.toFixed(1)}, {node.location.lng.toFixed(1)}
                    </span>
                </div>
                <h2 className="font-bold text-xl text-white leading-none tracking-tight">{node.label}</h2>
            </div>

            {/* Content */}
            <div className="p-5 space-y-6">
                
                {/* Ownership Card (v7.0) */}
                {owner && (
                    <div className="bg-slate-900 border border-slate-800 rounded-lg p-3 flex items-center gap-3">
                        <div className="w-10 h-10 rounded bg-slate-800 flex items-center justify-center text-xl font-bold text-slate-500 uppercase">
                            {owner.name.substring(0, 2)}
                        </div>
                        <div>
                            <div className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">OWNED BY</div>
                            <div className="text-sm font-bold text-white">{owner.name}</div>
                            <div className="text-[9px] text-slate-400">{owner.hq_country} • {owner.type}</div>
                        </div>
                    </div>
                )}

                {/* Geopolitical Risk (v7.0) */}
                <div className="bg-slate-900 border border-slate-800 rounded-lg p-3 space-y-2">
                    <div className="flex justify-between items-center">
                        <div className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">Jurisdiction</div>
                        <div className="text-[10px] font-bold text-white">{node.jurisdiction}</div>
                    </div>
                    <div className="flex justify-between items-center">
                        <div className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">Geopolitical Risk</div>
                        <div className={clsx(
                            "text-[10px] font-bold font-mono",
                            node.risk_level > 0.5 ? "text-red-400" : "text-emerald-400"
                        )}>
                            {(node.risk_level * 100).toFixed(0)}%
                        </div>
                    </div>
                    {(node.is_sanctioned || node.conflict_zone) && (
                        <div className="pt-2 border-t border-slate-800 flex gap-2">
                            {node.is_sanctioned && (
                                <span className="px-1.5 py-0.5 bg-red-500/20 text-red-400 text-[8px] font-bold rounded border border-red-500/30 uppercase tracking-tighter">
                                    Sanctioned
                                </span>
                            )}
                            {node.conflict_zone && (
                                <span className="px-1.5 py-0.5 bg-orange-500/20 text-orange-400 text-[8px] font-bold rounded border border-orange-500/30 uppercase tracking-tighter">
                                    Conflict Zone
                                </span>
                            )}
                        </div>
                    )}
                </div>

                {/* Status Card */}
                <div className={clsx(
                    "p-4 rounded-xl border flex items-center justify-between",
                    isCritical ? "bg-red-500/5 border-red-500/20" : "bg-slate-900 border-slate-800"
                )}>
                    <div>
                        <div className="text-[10px] uppercase text-slate-500 font-bold tracking-widest mb-1">Operational Status</div>
                        <div className={clsx(
                            "font-bold text-lg flex items-center gap-2",
                            isCritical ? "text-red-400" : (isStressed ? "text-amber-400" : "text-emerald-400")
                        )}>
                            {isCritical ? <AlertOctagon size={18} /> : <Activity size={18} />}
                            {isCritical ? "CRITICAL" : (isStressed ? "STRESSED" : "OPTIMAL")}
                        </div>
                    </div>
                    <div className="text-right">
                        <div className="text-[10px] uppercase text-slate-500 font-bold tracking-widest mb-1">Storage Depth</div>
                        <div className="font-mono text-xl font-bold text-white">{invPct.toFixed(0)}%</div>
                        <div className="text-[9px] text-slate-500 font-mono">
                            {node.inventory.toLocaleString()} / {maxInv.toLocaleString()}
                        </div>
                    </div>
                </div>

                {/* Storage Economics (v7.5) */}
                <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-3 space-y-1">
                    <div className="flex justify-between text-[9px] text-slate-500 uppercase tracking-widest">
                        <span>Daily Storage Cost</span>
                        <span className="text-white font-mono">${(node.inventory * (node.specs?.storage_cost_per_unit_day || 0.1)).toLocaleString()}</span>
                    </div>
                    {node.specs?.is_benchmark_hub && (
                        <div className="flex items-center gap-1.5 mt-1 text-cyan-400">
                            <Anchor size={10} />
                            <span className="text-[9px] font-bold uppercase">Strategic Benchmark Hub</span>
                        </div>
                    )}
                </div>

                {/* Metrics Grid */}
                <div className="grid grid-cols-2 gap-3">
                    <div className="bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                        <div className="text-[10px] uppercase text-slate-500 font-bold mb-1">Commodity</div>
                        <div className="text-sm font-bold text-cyan-400 truncate" title={node.commodity}>{node.commodity}</div>
                    </div>
                    <div className="bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                         <div className="text-[10px] uppercase text-slate-500 font-bold mb-1">Revenue Risk</div>
                         <div className="text-sm font-bold text-slate-300">$ {(node.revenue_per_day || 0).toLocaleString()}/day</div>
                    </div>
                </div>

                {/* Trace Data (Upstream/Downstream) */}
                {traceData && (
                    <div className="space-y-3">
                        <div className="flex items-center gap-2 text-[10px] uppercase text-slate-500 font-bold tracking-widest border-b border-slate-800 pb-2">
                            <Share2 size={12} /> Network Topology
                        </div>
                        <div className="space-y-2">
                            <div className="flex justify-between text-xs">
                                <span className="text-slate-400 font-bold uppercase text-[9px]">Upstream Dependencies</span>
                                <span className="text-white font-mono">{traceData.ancestors?.length || 0}</span>
                            </div>
                            <div className="flex justify-between text-xs">
                                <span className="text-slate-400 font-bold uppercase text-[9px]">Downstream Impact</span>
                                <span className="text-cyan-400 font-mono font-bold">{traceData.descendants?.length || 0}</span>
                            </div>
                        </div>
                    </div>
                )}

                {/* AI Insight Placeholder */}
                <div className="p-3 bg-cyan-950/20 border border-cyan-900/30 rounded-lg">
                     <p className="text-xs text-cyan-200/80 leading-relaxed italic">
                        "Market volatility detected. Downstream demand for {node.commodity} is spiking due to supply shocks in the Asian sector."
                     </p>
                </div>
            </div>
        </div>
    );
};

import React from 'react';
import { Book, ShieldAlert, Users, TrendingUp, AlertTriangle, X } from 'lucide-react';
import { CommodityDossier as DossierType } from '../data/commodity_manifest';

interface CommodityDossierProps {
    commodity: string;
    dossier: DossierType;
    onClose: () => void;
    onFlowClick: (flow: string) => void;
}

export const CommodityDossier: React.FC<CommodityDossierProps> = ({ commodity, dossier, onClose, onFlowClick }) => {
    return (
        <div className="flex flex-col h-full bg-slate-950/95 backdrop-blur-xl border-l border-slate-800 shadow-2xl animate-in slide-in-from-right-full duration-300">
            {/* Header */}
            <div className="p-6 border-b border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 relative">
                <button 
                    onClick={onClose}
                    className="absolute top-4 right-4 p-2 text-slate-500 hover:text-white transition-colors"
                >
                    <X size={20} />
                </button>
                <div className="flex items-center gap-2 text-cyan-400 font-bold uppercase tracking-widest text-[10px] mb-2">
                    <Book size={14} /> Global Commodity Dossier
                </div>
                <h1 className="text-3xl font-bold text-white mb-2 leading-none">{commodity}</h1>
                <p className="text-sm text-cyan-400 font-medium italic">{dossier.title}</p>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-8">
                
                {/* Description */}
                <div className="space-y-3">
                    <div className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">Summary</div>
                    <p className="text-slate-300 text-sm leading-relaxed">
                        {dossier.description}
                    </p>
                </div>

                {/* Top Producers & Traders */}
                <div className="grid grid-cols-2 gap-6">
                    <div className="space-y-3">
                        <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">
                            <Users size={12} /> Key Producers
                        </div>
                        <div className="space-y-1.5">
                            {dossier.top_producers.map((p, i) => (
                                <div key={i} className="text-xs text-slate-200 py-1 border-b border-slate-800/50 last:border-0">{p}</div>
                            ))}
                        </div>
                    </div>
                    <div className="space-y-3">
                        <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">
                            <TrendingUp size={12} /> Dominant Traders
                        </div>
                        <div className="space-y-1.5">
                            {dossier.top_traders.map((t, i) => (
                                <div key={i} className="text-xs text-slate-200 py-1 border-b border-slate-800/50 last:border-0">{t}</div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Strategic Flows */}
                <div className="space-y-3">
                    <div className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">Strategic Map Flows</div>
                    <div className="space-y-2">
                        {dossier.strategic_flows.map((flow, i) => (
                            <button 
                                key={i} 
                                onClick={() => onFlowClick(flow)}
                                className="w-full text-left p-2 bg-slate-900/50 border border-slate-800 rounded-lg flex items-center gap-3 group hover:border-cyan-500/50 hover:bg-cyan-950/20 transition-all cursor-pointer"
                            >
                                <div className="text-cyan-500 font-mono text-[10px] font-bold group-hover:text-cyan-400">0{i+1}</div>
                                <div className="text-xs text-slate-300 group-hover:text-white transition-colors truncate">{flow}</div>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Vulnerabilities */}
                <div className="space-y-3">
                    <div className="flex items-center gap-2 text-[10px] font-bold text-red-500 uppercase tracking-[0.2em]">
                        <AlertTriangle size={12} /> Systemic Risks
                    </div>
                    <div className="flex flex-wrap gap-2">
                        {dossier.vulnerabilities.map((v, i) => (
                            <span key={i} className="px-2 py-1 bg-red-500/10 border border-red-500/20 rounded text-[10px] text-red-400 font-bold uppercase">
                                {v}
                            </span>
                        ))}
                    </div>
                </div>

                {/* Supply Chain Guide */}
                <div className="space-y-3 pt-6 border-t border-slate-800">
                    <div className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">Digital Twin Guide</div>
                    <div className="grid grid-cols-1 gap-3">
                        {Object.entries(dossier.node_guide).map(([type, desc]) => (
                            <div key={type} className="flex gap-3">
                                <div className={`w-1 h-auto rounded ${
                                    type === 'resource' ? 'bg-emerald-500' :
                                    type === 'transformation' ? 'bg-amber-500' :
                                    type === 'logistic' ? 'bg-blue-500' : 'bg-purple-500'
                                }`} />
                                <div>
                                    <div className="text-[9px] font-bold text-slate-500 uppercase">{type}</div>
                                    <div className="text-[10px] text-slate-400">{desc}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

            </div>

            {/* Footer */}
            <div className="p-4 bg-slate-900 border-t border-slate-800 flex justify-between items-center">
                <div className="text-[9px] text-slate-500 font-mono italic">DATA SOURCE: CASSANDRA INTEL</div>
                <div className="flex items-center gap-1 text-[9px] font-bold text-cyan-500 uppercase">
                    <ShieldAlert size={10} /> Verified Path
                </div>
            </div>
        </div>
    );
};

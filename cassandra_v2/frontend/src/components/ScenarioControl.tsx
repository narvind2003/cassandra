import React from 'react';
import { ShieldAlert, Zap, Lock, Activity, Ban } from 'lucide-react';

import React, { useEffect, useState } from 'react';
import { ShieldAlert, Zap, Lock, Activity, Ban, BookOpen, Play } from 'lucide-react';

interface ScenarioControlProps {
    selectedNode: any | null;
    onInject: (targetId: string, type: string, severity: number) => void;
    onPlaybook: (injections: any[]) => void;
}

export const ScenarioControl: React.FC<ScenarioControlProps> = ({ selectedNode, onInject, onPlaybook }) => {
    const [scenarios, setScenarios] = useState<any[]>([]);

    useEffect(() => {
        fetch('http://localhost:8002/api/playbook')
            .then(res => res.json())
            .then(setScenarios)
            .catch(console.error);
    }, []);

    return (
        <div className="p-4 border-t border-slate-800 bg-slate-950/50 space-y-4">
            {/* ... Existing Manual Controls ... */}
            
            {selectedNode && (
                <div className="p-2 bg-slate-900 border border-slate-800 rounded mb-2">
                    <div className="text-[9px] text-slate-500 uppercase font-bold mb-1">Target: {selectedNode.label}</div>
                    <div className="grid grid-cols-3 gap-1">
                        <button 
                            onClick={() => onInject(selectedNode.id, 'blockage', 1.0)}
                            className="bg-red-500/10 border border-red-500/20 hover:bg-red-500/20 text-red-400 p-1.5 rounded text-[8px] font-bold flex flex-col items-center justify-center gap-1 transition-all"
                        >
                            <Lock size={10} /> BLKADE
                        </button>
                        <button 
                            onClick={() => onInject(selectedNode.id, 'strike', 0.8)}
                            className="bg-amber-500/10 border border-amber-500/20 hover:bg-amber-500/20 text-amber-400 p-1.5 rounded text-[8px] font-bold flex flex-col items-center justify-center gap-1 transition-all"
                        >
                            <ShieldAlert size={10} /> STRIKE
                        </button>
                        <button 
                            onClick={() => onInject(selectedNode.id, 'embargo', 1.0)}
                            className="bg-purple-500/10 border border-purple-500/20 hover:bg-purple-500/20 text-purple-400 p-1.5 rounded text-[8px] font-bold flex flex-col items-center justify-center gap-1 transition-all"
                        >
                            <Ban size={10} /> EMBARGO
                        </button>
                    </div>
                </div>
            )}

            <div className="space-y-2">
                <div className="text-[10px] text-slate-500 font-bold uppercase tracking-widest flex items-center gap-2">
                    <BookOpen size={12} /> The Crisis Playbook
                </div>
                <div className="space-y-1 max-h-48 overflow-y-auto custom-scrollbar">
                    {scenarios.map((s, i) => (
                        <button 
                            key={i}
                            onClick={() => onPlaybook(s.injections)}
                            className="w-full text-left p-2 bg-slate-900 border border-slate-800 hover:border-cyan-500/50 hover:bg-slate-800 rounded group transition-all"
                        >
                            <div className="text-[10px] font-bold text-cyan-400 group-hover:text-cyan-300 flex items-center justify-between">
                                {s.title}
                                <Play size={10} className="opacity-0 group-hover:opacity-100 transition-opacity" />
                            </div>
                            <div className="text-[9px] text-slate-500 mt-1 leading-tight">{s.description}</div>
                        </button>
                    ))}
                </div>
            </div>

            <div className="text-[9px] text-slate-600 font-bold uppercase mb-1">Strategic Choke Points</div>
            <div className="grid grid-cols-2 gap-2">
                <button 
                    onClick={() => onInject('choke_suez', 'blockage', 1.0)}
                    className="bg-slate-800 border border-slate-700 hover:border-red-500/50 text-slate-400 hover:text-red-400 p-2 rounded text-[10px] font-bold flex flex-col items-center gap-1 transition-all"
                >
                    <Lock size={12} /> SUEZ
                </button>
                <button 
                    onClick={() => onInject('choke_panama', 'blockage', 1.0)}
                    className="bg-slate-800 border border-slate-700 hover:border-red-500/50 text-slate-400 hover:text-red-400 p-2 rounded text-[10px] font-bold flex flex-col items-center gap-1 transition-all"
                >
                    <Lock size={12} /> PANAMA
                </button>
                <button 
                    onClick={() => onInject('choke_malacca', 'blockage', 1.0)}
                    className="bg-slate-800 border border-slate-700 hover:border-red-500/50 text-slate-400 hover:text-red-400 p-2 rounded text-[10px] font-bold flex flex-col items-center gap-1 transition-all"
                >
                    <Lock size={12} /> MALACCA
                </button>
                <button 
                    onClick={() => onInject('choke_hormuz', 'blockage', 1.0)}
                    className="bg-slate-800 border border-slate-700 hover:border-red-500/50 text-slate-400 hover:text-red-400 p-2 rounded text-[10px] font-bold flex flex-col items-center gap-1 transition-all"
                >
                    <Lock size={12} /> HORMUZ
                </button>
            </div>
        </div>
    );
};

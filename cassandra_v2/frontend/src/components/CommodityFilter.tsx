import React, { useState } from 'react';
import { Filter, ChevronRight, ChevronDown, Check, Circle } from 'lucide-react';
import clsx from 'clsx';

interface CommodityFilterProps {
    categories: Record<string, Set<string>>;
    selectedCategory: string | null;
    selectedCommodity: string | null;
    onSelectCategory: (cat: string | null) => void;
    onSelectCommodity: (comm: string | null) => void;
    onShowDossier: (show: boolean) => void;
}

export const CommodityFilter: React.FC<CommodityFilterProps> = ({
    categories,
    selectedCategory,
    selectedCommodity,
    onSelectCategory,
    onSelectCommodity,
    onShowDossier
}) => {
    const [expandedCategories, setExpandedCategories] = useState<string[]>(['Food', 'Non-Food']);

    const toggleCategory = (cat: string) => {
        if (expandedCategories.includes(cat)) {
            setExpandedCategories(expandedCategories.filter(c => c !== cat));
        } else {
            setExpandedCategories([...expandedCategories, cat]);
        }
    };

    return (
        <div className="flex-1 overflow-y-auto p-2 space-y-1 custom-scrollbar">
            <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest px-2 py-2 flex items-center gap-2 sticky top-0 bg-slate-950/90 backdrop-blur z-10 border-b border-slate-800/50 mb-2">
                <Filter size={12} /> Commodity Filter
            </div>

            <button 
                onClick={() => { onSelectCommodity(null); onSelectCategory(null); }}
                className={clsx(
                    "w-full text-left px-3 py-2 text-xs rounded transition-all duration-200 flex items-center justify-between group",
                    !selectedCommodity && !selectedCategory 
                        ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-[0_0_10px_rgba(6,182,212,0.1)]" 
                        : "text-slate-400 hover:bg-slate-900 hover:text-slate-200"
                )}
            >
                <span className="font-bold flex items-center gap-2">
                    <div className={clsx("w-1.5 h-1.5 rounded-full transition-colors", !selectedCommodity && !selectedCategory ? "bg-cyan-500" : "bg-slate-600")} />
                    ALL COMMODITIES
                </span>
                {(!selectedCommodity && !selectedCategory) && <Check size={12} className="text-cyan-500" />}
            </button>

            {Object.entries(categories).map(([cat, commodities]) => {
                const isCatSelected = selectedCategory === cat && !selectedCommodity;
                const isChildSelected = Array.from(commodities).includes(selectedCommodity || '');
                const isOpen = expandedCategories.includes(cat);

                return (
                    <div key={cat} className="space-y-0.5">
                        <button 
                            onClick={() => toggleCategory(cat)}
                            className={clsx(
                                "w-full flex items-center justify-between text-left px-3 py-2 text-xs font-bold rounded hover:bg-slate-900 transition-colors",
                                (isCatSelected || isChildSelected) ? "text-slate-200" : "text-slate-500"
                            )}
                        >
                            <span className="flex items-center gap-2">
                                {isOpen ? <ChevronDown size={12} className="text-slate-600"/> : <ChevronRight size={12} className="text-slate-600"/>}
                                {cat}
                            </span>
                            <span className="text-[10px] bg-slate-900 px-1.5 py-0.5 rounded text-slate-600 border border-slate-800">
                                {commodities.size}
                            </span>
                        </button>
                        
                        <div className={clsx(
                            "overflow-hidden transition-all duration-300 ease-in-out border-l border-slate-800 ml-4 pl-1 space-y-0.5",
                            isOpen ? "max-h-[1000px] opacity-100" : "max-h-0 opacity-0"
                        )}>
                            <button
                                onClick={() => { onSelectCategory(cat); onSelectCommodity(null); }}
                                className={clsx(
                                    "w-full text-left px-2 py-1.5 text-xs rounded transition-all flex items-center gap-2",
                                    isCatSelected 
                                        ? "bg-cyan-500/10 text-cyan-400 font-medium" 
                                        : "text-slate-500 hover:text-slate-300 hover:bg-slate-900/50"
                                )}
                            >
                                <div className={clsx("w-1 h-1 rounded-full", isCatSelected ? "bg-cyan-500" : "bg-transparent border border-slate-600")} />
                                All {cat}
                            </button>

                            {Array.from(commodities).sort().map((comm: any) => {
                                const isCommSelected = selectedCommodity === comm;
                                return (
                                    <button
                                        key={comm}
                                        onClick={() => { onSelectCategory(null); onSelectCommodity(comm); onShowDossier(true); }}
                                        className={clsx(
                                            "w-full text-left px-2 py-1.5 text-xs rounded transition-all flex items-center justify-between group",
                                            isCommSelected 
                                                ? "bg-cyan-500/10 text-cyan-400 font-medium border-l-2 border-cyan-500" 
                                                : "text-slate-500 hover:text-slate-300 hover:bg-slate-900/50 border-l-2 border-transparent"
                                        )}
                                    >
                                        <span className="truncate">{comm}</span>
                                        {isCommSelected && <div className="w-1.5 h-1.5 rounded-full bg-cyan-500 shadow-[0_0_5px_rgba(6,182,212,0.8)]" />}
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

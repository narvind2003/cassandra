import React from 'react';
import { DollarSign, TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react';
import clsx from 'clsx';

interface FinancialDashboardProps {
    totalLoss: number;
    currentPrices: Record<string, number>;
    selectedCommodity: string | null;
    systemicBreakdown?: {
        unmet_value?: number;
        revenue_loss?: number;
        choke_penalty?: number;
        blocked_chokes?: string[];
    };
    systemicSummary?: {
        scenario?: string;
        total?: number;
        unmet?: number;
        revenue?: number;
        choke?: number;
        peak_total?: number;
        peak_day?: number;
    };
}

export const FinancialDashboard: React.FC<FinancialDashboardProps> = ({ totalLoss, currentPrices, selectedCommodity, systemicBreakdown, systemicSummary }) => {
    // Determine market sentiment based on price (random logic for demo until historical data is passed)
    // In a real app, we'd compare vs yesterday.
    
    const price = selectedCommodity && currentPrices ? currentPrices[selectedCommodity] : null;
    const formatCompact = (value: number) => {
        const abs = Math.abs(value);
        if (abs >= 1_000_000_000) return `$${(value / 1_000_000_000).toFixed(2)}B`;
        if (abs >= 1_000_000) return `$${(value / 1_000_000).toFixed(2)}M`;
        if (abs >= 1_000) return `$${(value / 1_000).toFixed(2)}K`;
        return `$${Math.round(value).toLocaleString()}`;
    };
    
    return (
        <div className="p-4 border-t border-slate-800 bg-slate-900/50 space-y-4">
            
            {/* Global Risk Meter */}
            <div>
                <div className="flex justify-between items-center mb-1">
                    <div className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Systemic Risk</div>
                    {totalLoss > 500 && (
                        <div className="flex items-center gap-1 text-[10px] text-red-500 font-bold animate-pulse">
                            <AlertTriangle size={10} /> MARGIN CALL
                        </div>
                    )}
                </div>
                <div className="text-2xl font-mono font-bold text-white flex items-center gap-1">
                    {formatCompact(totalLoss)}
                </div>
                {/* Visual Risk Bar */}
                <div className="w-full h-1.5 bg-slate-800 rounded-full mt-2 overflow-hidden">
                    <div 
                        className={clsx("h-full transition-all duration-500", totalLoss > 1000 ? "bg-red-500" : (totalLoss > 200 ? "bg-amber-500" : "bg-emerald-500"))} 
                        style={{ width: `${Math.min(100, (totalLoss / 2000) * 100)}%` }}
                    />
                </div>
            </div>

            {/* Systemic Risk Breakdown (Cumulative) */}
            {systemicBreakdown && (
                <div className="bg-slate-950 p-3 rounded border border-slate-800">
                    <div className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-2">Cumulative Breakdown</div>
                    <div className="flex items-center justify-between text-[11px] text-slate-300 mb-1">
                        <span>Unmet Demand Value</span>
                        <span className="font-mono text-slate-200">{formatCompact(systemicBreakdown.unmet_value || 0)}</span>
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-slate-300 mb-1">
                        <span>Revenue Loss</span>
                        <span className="font-mono text-slate-200">{formatCompact(systemicBreakdown.revenue_loss || 0)}</span>
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-slate-300 mb-1">
                        <span>Choke Penalty</span>
                        <span className="font-mono text-slate-200">{formatCompact(systemicBreakdown.choke_penalty || 0)}</span>
                    </div>
                    {systemicBreakdown.blocked_chokes && systemicBreakdown.blocked_chokes.length > 0 && (
                        <div className="mt-2 text-[10px] text-amber-400 font-mono uppercase tracking-wider">
                            Blocked: {systemicBreakdown.blocked_chokes.join(', ')}
                        </div>
                    )}
                </div>
            )}

            {/* Systemic Risk Summary */}
            {systemicSummary && (
                <div className="bg-slate-950 p-3 rounded border border-slate-800">
                    <div className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-2">Scenario Summary</div>
                    {systemicSummary.scenario && (
                        <div className="text-[10px] text-slate-400 font-mono mb-2">{systemicSummary.scenario}</div>
                    )}
                    <div className="flex items-center justify-between text-[11px] text-slate-300 mb-1">
                        <span>Cumulative Total Risk</span>
                        <span className="font-mono text-slate-200">{formatCompact(systemicSummary.total || 0)}</span>
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-slate-300 mb-1">
                        <span>Cumulative Unmet Value</span>
                        <span className="font-mono text-slate-200">{formatCompact(systemicSummary.unmet || 0)}</span>
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-slate-300 mb-1">
                        <span>Cumulative Revenue Loss</span>
                        <span className="font-mono text-slate-200">{formatCompact(systemicSummary.revenue || 0)}</span>
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-slate-300 mb-1">
                        <span>Cumulative Choke Penalty</span>
                        <span className="font-mono text-slate-200">{formatCompact(systemicSummary.choke || 0)}</span>
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-slate-300 mt-2">
                        <span>Peak Risk</span>
                        <span className="font-mono text-amber-300">{formatCompact(systemicSummary.peak_total || 0)}</span>
                    </div>
                    <div className="text-[10px] text-slate-500">Peak Day: {systemicSummary.peak_day ?? 0}</div>
                </div>
            )}

            {/* Selected Commodity Price Ticker */}
            {selectedCommodity && price && (
                <div className="bg-slate-950 p-3 rounded border border-slate-800 animate-in fade-in slide-in-from-bottom-2">
                    <div className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-1 flex justify-between">
                        <span>{selectedCommodity} Spot</span>
                        <span className="text-emerald-500 flex items-center gap-1">LIVE <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"/></span>
                    </div>
                    <div className="flex items-end justify-between">
                        <div className="text-lg font-mono font-bold text-cyan-400">
                            ${price.toFixed(2)}
                        </div>
                        <div className="text-xs font-bold text-emerald-400 flex items-center">
                            <TrendingUp size={12} className="mr-1" /> +1.2%
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

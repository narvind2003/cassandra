import React, { useEffect, useState } from 'react';
import { Newspaper, Radio, AlertTriangle, ExternalLink, Zap } from 'lucide-react';

interface NewsItem {
    id: string;
    title: string;
    summary: string;
    source: string;
    published: string;
    timestamp: number;
    impact_assessment?: {
        target_id: string;
        type: string;
        severity: number;
    };
}

interface NewsFeedProps {
    onSimulate: (targetId: string, type: string, severity: number) => void;
}

export const NewsFeed: React.FC<NewsFeedProps> = ({ onSimulate }) => {
    const [news, setNews] = useState<NewsItem[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchNews = () => {
            fetch('http://localhost:8002/api/news')
                .then(res => res.json())
                .then(data => {
                    setNews(data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error("Failed to fetch news:", err);
                    setLoading(false);
                });
        };

        fetchNews();
        const interval = setInterval(fetchNews, 30000); // Poll every 30s
        return () => clearInterval(interval);
    }, []);

    // Ticker Logic (Derived from latest news)
    const latestNews = news.length > 0 ? news[0] : null;

    return (
        <div className="flex flex-col h-full bg-slate-950 border-t border-slate-800">
            {/* Header */}
            <div className="p-3 border-b border-slate-800 bg-slate-900/50 flex items-center justify-between">
                <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-widest">
                    <Radio size={14} className="animate-pulse text-red-500" />
                    Global Intelligence
                </div>
                <div className="text-[10px] text-slate-500 font-mono">LIVE</div>
            </div>

            {/* Scrollable Feed */}
            <div className="flex-1 overflow-y-auto custom-scrollbar p-0">
                {loading && <div className="p-4 text-center text-[10px] text-slate-500 animate-pulse">Scanning Global Feeds...</div>}
                
                {!loading && news.length === 0 && (
                    <div className="p-4 text-center text-[10px] text-slate-500">No active alerts detected.</div>
                )}

                {news.map((item) => (
                    <div key={item.id} className="p-3 border-b border-slate-800/50 hover:bg-slate-900/30 transition-colors group">
                        <div className="flex justify-between items-start mb-1">
                            <span className="text-[9px] font-bold text-slate-500 uppercase tracking-wider">{item.source}</span>
                            <span className="text-[9px] text-slate-600 font-mono">{new Date(item.timestamp * 1000).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                        </div>
                        
                        <div className="text-xs font-bold text-slate-200 mb-1 leading-snug group-hover:text-cyan-300 transition-colors">
                            {item.title}
                        </div>
                        
                        {/* Impact Assessment Card */}
                        {item.impact_assessment && (
                            <div className="mt-2 bg-slate-900/80 border border-red-900/30 rounded p-2 flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                    <AlertTriangle size={12} className="text-amber-500" />
                                    <div className="flex flex-col">
                                        <span className="text-[9px] font-bold text-amber-500 uppercase">System Shock Detected</span>
                                        <span className="text-[9px] text-slate-400">Target: {item.impact_assessment.target_id}</span>
                                    </div>
                                </div>
                                <button 
                                    onClick={() => onSimulate(
                                        item.impact_assessment!.target_id, 
                                        item.impact_assessment!.type, 
                                        item.impact_assessment!.severity
                                    )}
                                    className="px-2 py-1 bg-red-900/20 border border-red-900/50 rounded text-[9px] font-bold text-red-400 hover:bg-red-900/40 hover:text-white transition-all flex items-center gap-1"
                                >
                                    <Zap size={8} /> SIMULATE
                                </button>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

import feedparser
import time
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class NewsItem(BaseModel):
    id: str
    title: str
    summary: str
    source: str
    published: str
    timestamp: float
    impact_assessment: Optional[dict] = None # {target_id, type, severity}

class NewsIngestor:
    """
    Fetches real-world news from RSS feeds and maps them to simulation injections.
    Part of Project Cassandra v7.0 "Reality Engine".
    """
    
    RSS_FEEDS = [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
        "https://www.aljazeera.com/xml/rss/all.xml"
    ]

    # simple keyword mapping for v7 prototype
    KEYWORD_MAP = {
        "strike": "strike",
        "protest": "strike",
        "union": "strike",
        "blockade": "blockage",
        "halt": "blockage",
        "suspended": "blockage",
        "fire": "fire",
        "explosion": "fire",
        "storm": "disaster",
        "hurricane": "disaster",
        "earthquake": "disaster",
        "flood": "disaster"
    }
    
    # target mapping (very basic for prototype)
    TARGET_MAP = {
        "china": "mkt_china",
        "usa": "mkt_usa",
        "eu": "mkt_eu",
        "rotterdam": "hub_rotterdam",
        "suez": "choke_suez",
        "panama": "choke_panama",
        "hormuz": "choke_hormuz",
        "malacca": "choke_malacca",
        "taiwan": "fab_tsmc_hsinchu"
    }

    @staticmethod
    def fetch_latest_news() -> List[NewsItem]:
        news_items = []
        try:
            # For prototype, just fetch from one or mock if failed
            # combining feeds
            for url in NewsIngestor.RSS_FEEDS:
                try:
                    feed = feedparser.parse(url)
                    for entry in feed.entries[:5]: # Top 5 from each
                        item = NewsItem(
                            id=entry.link,
                            title=entry.title,
                            summary=entry.summary if 'summary' in entry else "",
                            source=feed.feed.title if 'title' in feed.feed else "Unknown",
                            published=entry.published if 'published' in entry else str(datetime.now()),
                            timestamp=time.mktime(entry.published_parsed) if 'published_parsed' in entry else time.time()
                        )
                        
                        # Assess Impact
                        item.impact_assessment = NewsIngestor._assess_impact(item.title + " " + item.summary)
                        news_items.append(item)
                except Exception as e:
                    print(f"Error fetching {url}: {e}")
                    continue
                    
            # Sort by newest
            news_items.sort(key=lambda x: x.timestamp, reverse=True)
            return news_items[:20]
            
        except Exception as e:
            print(f"NewsIngestor Error: {e}")
            return []

    @staticmethod
    def _assess_impact(text: str) -> Optional[dict]:
        text_lower = text.lower()
        
        detected_type = None
        for key, impact_type in NewsIngestor.KEYWORD_MAP.items():
            if key in text_lower:
                detected_type = impact_type
                break
        
        if not detected_type:
            return None
            
        detected_target = None
        for key, target_id in NewsIngestor.TARGET_MAP.items():
            if key in text_lower:
                detected_target = target_id
                break
                
        if detected_type and detected_target:
            return {
                "target_id": detected_target,
                "type": detected_type,
                "severity": 0.7 # Default severity
            }
        
        return None

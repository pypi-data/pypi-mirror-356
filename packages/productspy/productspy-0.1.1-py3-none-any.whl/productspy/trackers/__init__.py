from productspy.trackers.amazon import AmazonTracker
from productspy.trackers.noon import NoonTracker
from productspy.trackers.extra import ExtraTracker
from productspy.trackers.carrefour import CarrefourTracker
from productspy.trackers.aliexpress import AliExpressTracker
from productspy.utils.url_tools import extract_domain
from productspy.exceptions import UnsupportedSiteError

def get_product_info(url: str):
    domain = extract_domain(url).lower()

    if "amazon" in domain:
        return AmazonTracker(url).fetch_info()
    elif "noon" in domain:
        return NoonTracker(url).fetch_info()
    elif "extra" in domain:
        return ExtraTracker(url).fetch_info()
    elif "carrefour" in domain:
        return CarrefourTracker(url).fetch_info()
    elif "aliexpress" in domain or "ali" in domain:
        return AliExpressTracker(url).fetch_info()
    
    raise UnsupportedSiteError(f"Unsupported domain: {domain}")

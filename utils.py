def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

def clean_text(text):
    return text.replace('\n', '').replace('\xa0', '').strip()

def extract_data(soup, fsin):
    try:
        title = soup.select_one('span.VU-ZEz')
        title = clean_text(title.text) if title else "N/A"

        # Brand and Category from r2CdBx divs
        r2cd_divs = soup.select('div.r2CdBx')
        category = clean_text(r2cd_divs[3].text) if len(r2cd_divs) >= 4 else "N/A"
        brand = clean_text(r2cd_divs[4].text) if len(r2cd_divs) >= 5 else "N/A"

        # Price (as number)
        price_tag = soup.select_one('div.Nx9bqj.CxhGGd')
        price = None
        if price_tag:
            try:
                price = int(clean_text(price_tag.text.replace("₹", "").replace(",", "")))
            except Exception:
                price = None

        # Seller (unchanged)
        seller_tag = soup.select_one('div.yeLeBC span')
        seller = clean_text(seller_tag.text) if seller_tag else "N/A"

        # Rating (as float)
        rating_tag = soup.select_one('div.XQDdHH')
        rating = None
        if rating_tag:
            import re
            match = re.search(r"[0-9.]+", rating_tag.text)
            if match:
                try:
                    rating = float(match.group(0))
                except Exception:
                    rating = None

        # Rating number (same as rating, for clarity)
        rating_number = rating

        # Reviews and Ratings count (as int)
        reviews = 0
        ratings = 0
        reviews_block = soup.select_one('span.Wphh3N')
        if reviews_block:
            spans = reviews_block.find_all('span')
            if len(spans) >= 2:
                import re
                ratings_match = re.search(r"([\d,]+) Ratings", spans[0].text)
                reviews_match = re.search(r"([\d,]+) Reviews", spans[-1].text)
                if ratings_match:
                    try:
                        ratings = int(ratings_match.group(1).replace(",", ""))
                    except Exception:
                        ratings = 0
                if reviews_match:
                    try:
                        reviews = int(reviews_match.group(1).replace(",", ""))
                    except Exception:
                        reviews = 0

        return {
            "fsin": fsin,
            "title": title,
            "brand": brand,
            "category": category,
            "price": price,
            "seller": seller,
            "rating": rating,
            "rating_number": rating_number,
            "ratings_count": ratings,
            "review_count": reviews
        }
    except Exception as e:
        print(f"Error parsing FSIN {fsin}: {e}")
        return None

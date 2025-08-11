import requests
from bs4 import BeautifulSoup
import json
import time


def get_clash_royale_card_urls():
    """Scrape Clash Royale card images from wiki"""

    # List of popular Clash Royale cards
    card_names = ["P.E.K.K.A.", "Royal_Giant", "Prince", "Dark_Prince", "Miner", "Bandit", "Ice_Spirit", "Electro_Dragon", "Baby_Dragon", "Skeleton_Dragons", "Night_Witch", "Witch", "Executioner", "Hunter", "Bowler", "Magic_Archer", "Dart_Goblin", "Royal_Recruits", "Royal_Ghost", "Cannon_Cart", "Flying_Machine", "Mega_Knight", "Lumberjack", "Ram_Rider", "Elite_Barbarians", "Barbarians", "Guards", "Fisherman", "Tornado",
                  "Lightning", "Arrows", "Rocket", "Zap", "Furnace", "Zappies", "Minions", "Goblin_Hut", "Hog_Rider", "Skeleton_Army", "Skeletons", "Monk", "Little_Prince", "Goblin_Drill", "Goblin_Barrel", "Knight", "Bomber", "Electro_Spirit", "Spear_Goblins", "Mini_P.E.K.K.A.", "Mega_Minion", "Berserker", "Wizard", "Ice_Wizard", "Firecracker", "Valkyrie", "Battle_Healer", "Mother_Witch", "Heal_Spirit", "Archers", "Musketeer"]

    base_url = "https://clashroyale.fandom.com"
    card_image_urls = []

    for card_name in card_names:
        try:
            print(f"Fetching {card_name}...")

            # Get the card's wiki page
            page_url = f"{base_url}/wiki/{card_name}"
            response = requests.get(page_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for card image - try multiple selectors
            card_image = None

            # Try to find the card image in infobox
            selectors = [
                'img[alt*="Card"]',
                'img[src*="Card.png"]',
                'img[data-src*="Card.png"]',
                '.image img',
                '.infobox img'
            ]

            for selector in selectors:
                images = soup.select(selector)
                for img in images:
                    src = img.get('src') or img.get('data-src')
                    if isinstance(src, list):
                        src = src[0] if src else None
                    if src and 'Card.png' in src:
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            src = base_url + src

                        # Scale up the image
                        if 'scale-to-width-down' in src:
                            src = src.replace(
                                'scale-to-width-down/100', 'scale-to-width-down/500')
                            src = src.replace(
                                'scale-to-width-down/150', 'scale-to-width-down/500')

                        card_image = src
                        break

                if card_image:
                    break

            if card_image:
                card_image_urls.append(card_image)
                print(f"Found: {card_image}")
            else:
                print(f"No card image found for {card_name}")

            # Be respectful to the server
            time.sleep(0.5)

        except Exception as e:
            print(f"Error processing {card_name}: {e}")

    return card_image_urls


def main():
    """Main function to scrape and save card URLs"""
    print("Starting Clash Royale card image scraping...")

    card_urls = get_clash_royale_card_urls()

    # Save to JSON file
    output_file = 'clash_royale_card_urls.json'
    with open(output_file, 'w') as f:
        json.dump(card_urls, f, indent=4)

    print(f"\nScraping complete!")
    print(f"Found {len(card_urls)} card images")
    print(f"URLs saved to {output_file}")


if __name__ == "__main__":
    main()

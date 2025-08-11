import requests
from bs4 import BeautifulSoup
import json
import time


def get_clash_royale_card_urls():
    """Scrape Clash Royale card images from wiki"""

    # List of popular Clash Royale cards
    card_names = [
        "Archers", "Knight", "Goblins", "Giant", "Wizard", "Dragon", "Princess",
        "Prince", "Musketeer", "Fireball", "Arrows", "Barbarians", "Minions",
        "Skeleton_Army", "Valkyrie", "Hog_Rider", "Freeze", "Mirror", "Rage",
        "Ice_Wizard", "Balloon", "Witch", "Barbarian_Hut", "Lightning", "Golem",
        "Poison", "Baby_Dragon", "Dark_Prince", "Three_Musketeers", "Guards",
        "Miner", "Sparky", "Bowler", "Graveyard", "Ice_Golem", "Mega_Minion",
        "Ice_Spirit", "Elite_Barbarians", "Electro_Wizard", "Inferno_Dragon",
        "Bandit", "Royal_Ghost", "Zappies", "Hunter", "Magic_Archer", "Rascals",
        "Royal_Hogs", "Goblin_Giant", "Electro_Dragon", "Ram_Rider", "Wall_Breakers",
        "Battle_Healer", "Elixir_Golem", "Firecracker", "Earthquake", "Goblin_Cage"
    ]

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

import requests
from bs4 import BeautifulSoup
import json
import time


def get_clash_royale_card_data():
    """Scrape Clash Royale card images and rarities from wiki"""

    # List of popular Clash Royale cards
    card_names = ["P.E.K.K.A.", "Royal_Giant", "Prince", "Dark_Prince", "Miner", "Bandit", "Ice_Spirit", "Electro_Dragon", "Baby_Dragon", "Skeleton_Dragons", "Night_Witch", "Witch", "Executioner", "Hunter", "Bowler", "Magic_Archer", "Dart_Goblin", "Royal_Recruits", "Royal_Ghost", "Cannon_Cart", "Flying_Machine", "Mega_Knight", "Lumberjack", "Ram_Rider", "Elite_Barbarians", "Barbarians", "Guards", "Fisherman", "Tornado",
                  "Lightning", "Arrows", "Rocket", "Zap", "Furnace", "Zappies", "Minions", "Goblin_Hut", "Hog_Rider", "Skeleton_Army", "Skeletons", "Monk", "Little_Prince", "Goblin_Drill", "Goblin_Barrel", "Knight", "Bomber", "Electro_Spirit", "Spear_Goblins", "Mini_P.E.K.K.A.", "Mega_Minion", "Berserker", "Wizard", "Ice_Wizard", "Firecracker", "Valkyrie", "Battle_Healer", "Mother_Witch", "Heal_Spirit", "Archers", "Musketeer"]

    base_url = "https://clashroyale.fandom.com"
    card_data = []

    for card_name in card_names:
        try:
            print(f"Fetching {card_name}...")

            # Get the card's wiki page
            page_url = f"{base_url}/wiki/{card_name}"
            response = requests.get(page_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for card image
            card_image = None
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

            # Look for rarity information
            rarity = "common"  # default

            # Try multiple ways to find rarity
            rarity_selectors = [
                '.infobox tr:contains("Rarity") td',
                '.infobox-data',
                'td:contains("Common")',
                'td:contains("Rare")',
                'td:contains("Epic")',
                'td:contains("Legendary")',
                'td:contains("Champion")'
            ]

            for selector in rarity_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text().lower().strip()
                    if any(r in text for r in ['common', 'rare', 'epic', 'legendary', 'champion']):
                        if 'champion' in text:
                            rarity = 'champion'
                        elif 'legendary' in text:
                            rarity = 'legendary'
                        elif 'epic' in text:
                            rarity = 'epic'
                        elif 'rare' in text:
                            rarity = 'rare'
                        else:
                            rarity = 'common'
                        break
                if rarity != 'common':
                    break

            # Manual rarity mapping for known cards
            rarity_mapping = {
                'P.E.K.K.A.': 'epic',
                'Royal_Giant': 'common',
                'Prince': 'epic',
                'Dark_Prince': 'epic',
                'Miner': 'legendary',
                'Bandit': 'legendary',
                'Ice_Spirit': 'common',
                'Electro_Dragon': 'epic',
                'Baby_Dragon': 'epic',
                'Skeleton_Dragons': 'epic',
                'Night_Witch': 'legendary',
                'Witch': 'epic',
                'Executioner': 'epic',
                'Hunter': 'epic',
                'Bowler': 'epic',
                'Magic_Archer': 'legendary',
                'Dart_Goblin': 'rare',
                'Royal_Recruits': 'common',
                'Royal_Ghost': 'legendary',
                'Cannon_Cart': 'epic',
                'Flying_Machine': 'rare',
                'Mega_Knight': 'legendary',
                'Lumberjack': 'legendary',
                'Ram_Rider': 'legendary',
                'Elite_Barbarians': 'common',
                'Barbarians': 'common',
                'Guards': 'epic',
                'Fisherman': 'legendary',
                'Tornado': 'epic',
                'Lightning': 'epic',
                'Arrows': 'common',
                'Rocket': 'rare',
                'Zap': 'common',
                'Furnace': 'rare',
                'Zappies': 'rare',
                'Minions': 'common',
                'Goblin_Hut': 'rare',
                'Hog_Rider': 'rare',
                'Skeleton_Army': 'epic',
                'Skeletons': 'common',
                'Monk': 'champion',
                'Little_Prince': 'champion',
                'Goblin_Drill': 'epic',
                'Goblin_Barrel': 'epic',
                'Knight': 'common',
                'Bomber': 'common',
                'Electro_Spirit': 'common',
                'Spear_Goblins': 'common',
                'Mini_P.E.K.K.A.': 'rare',
                'Mega_Minion': 'rare',
                'Berserker': 'epic',
                'Wizard': 'rare',
                'Ice_Wizard': 'legendary',
                'Firecracker': 'common',
                'Valkyrie': 'rare',
                'Battle_Healer': 'rare',
                'Mother_Witch': 'legendary',
                'Heal_Spirit': 'common',
                'Archers': 'common',
                'Musketeer': 'rare'
            }

            if card_name in rarity_mapping:
                rarity = rarity_mapping[card_name]

            if card_image:
                card_data.append({
                    'name': card_name,
                    'image_url': card_image,
                    'rarity': rarity
                })
                print(f"Found: {card_name} - {rarity} - {card_image}")
            else:
                print(f"No card image found for {card_name}")

            # Be respectful to the server
            time.sleep(0.5)

        except Exception as e:
            print(f"Error processing {card_name}: {e}")

    return card_data


def main():
    """Main function to scrape and save card data"""
    print("Starting Clash Royale card data scraping...")

    card_data = get_clash_royale_card_data()

    # Save to JSON file
    output_file = 'clash_royale_card_data.json'
    with open(output_file, 'w') as f:
        json.dump(card_data, f, indent=4)

    print(f"\nScraping complete!")
    print(f"Found {len(card_data)} cards")
    print(f"Data saved to {output_file}")


if __name__ == "__main__":
    main()

# ezDoorDecks

An easy way to generate door decks for Resident Advisors (RAs). This tool automates the creation of PowerPoint presentations featuring resident information and images, making it simple to create professional-looking door decorations.

## Features

- Automatically scrapes and downloads resident images from Animal Crossing Wiki
- Generates a PowerPoint presentation with:
  - 3 residents per slide
  - Individual cards for each resident
  - Resident name and room number
  - High-quality images (500px width)
- Saves all downloaded images locally
- Generates a CSV file mapping resident names to image paths

## Prerequisites

- Poetry (for dependency management)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ezDoorDecks.git
cd ezDoorDecks
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Usage

1. Prepare your residents data in a CSV file named `residents.csv` with the following columns:
   - Name
   - Room

2. Run the image scraper to collect villager images:
```bash
poetry run python get_villager_images.py
```

3. Generate the presentation:
```bash
poetry run python main.py
```

The script will:
- Create an `images` directory and download all resident images
- Generate a PowerPoint presentation named `Residents_Presentation.pptx`
- Create `image_paths.csv` containing the mapping of resident names to their image files

## Project Structure

```
ezDoorDecks/
├── main.py                    # Main script for generating presentations
├── get_villager_images.py     # Script for scraping villager images
├── residents.csv              # Input file with resident information
├── image_paths.csv           # Output file mapping names to image paths
├── pyproject.toml            # Poetry dependency management
└── README.md                 # This file
```

## Dependencies

- pandas: Data manipulation and CSV handling
- requests: HTTP requests for image downloading
- python-pptx: PowerPoint presentation generation
- Pillow: Image processing
- beautifulsoup4: Web scraping
- poetry: Dependency management

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT

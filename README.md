# istoe-news-scrapper

## About

This program was developed as part of an extension program at the Neologism's Laboratory at UFES, with non-commercial goals. Its main objective is to create a corpus for identifying neologisms in the Brazilian Portuguese language.

## Instalation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/MiguelPim01/istoe-news-scrapper.git
   ```
2. Change to the project root directory:
   ```bash
   cd istoe-news-scrapper
   ```
3. Create a conda enviroment and activate it:
   ```bash
   conda create -n istoe-scrapper python=3.13.2
   conda activate istoe-scrapper
   ```
4. Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Collect links in internet archive

Run the `get_archive_links.py` script to collect links in internet archive.

```bash
python src/get_archive_links.py start=mm/yyyy end=mm/yyyy --headless
```

- `start=mm/yyyy`: Specify the start date to collect links. For example, start=09/2024.
- `end=mm/yyyy`: Specify the end date to collect links. For example, end=12/2024.
- `--headless`: If this flag is set, the program will run without a GUI.

### Step 2: Collect IstoE links in internet archive

Run the `get_istoe_links.py` script to collect IstoE links.

```bash
python src/get_istoe_links.py start=mm/yyyy end=mm/yyyy --headless
```

- `start=mm/yyyy`: Specify the start date to collect links. For example, start=09/2024.
- `end=mm/yyyy`: Specify the end date to collect links. For example, end=12/2024.
- `--headless`: If this flag is set, the program will run without a GUI.

### Step 3: Collect news in IstoE web site

Run the `get_news.py` script to collect news in IstoE web site.

```bash
python src/get_news.py start=mm/yyyy end=mm/yyyy --headless
```

- `start=mm/yyyy`: Specify the start date to collect news. For example, start=09/2024.
- `end=mm/yyyy`: Specify the end date to collect news. For example, end=12/2024.
- `--headless`: If this flag is set, the program will run without a GUI.

### Step 4: Clean news

Run the `news_cleaner.py` script to clean all collected news.

```bash
python src/news_cleaner.py start=mm/yyyy end=mm/yyyy --headless
```

- `start=mm/yyyy`: Specify the start date to clean news. For example, start=09/2024.
- `end=mm/yyyy`: Specify the end date to clean news. For example, end=12/2024.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
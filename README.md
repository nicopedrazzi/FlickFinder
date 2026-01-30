Been scrolling for hours? Don't know what to watch and your little free time got consumed by deciding which film or tv series to watch? Well, this simple CLI tool help you by giving you discovery options, summary and finally taking little time to select a film.

Quick setup (if python doesn't work, use python3):
```bash
pip install -r requirements.txt
```

Current commands:

If you don't know what to watch... go pure random (note: this will fetch also unknown niche titles... NOICE)
```bash
python3 main.py random
```

If you want to know the most watched at the moment
```bash
python main.py discover
```

If you want to search for a specific movie or tv show
```bash
python main.py search "Inception"
```

Need help or wanna see all options?
```bash
python main.py -h
```

Other possible options (mix and match):

For search:
```bash
python main.py search "The Office" --type tv --language en-US
```

For discover:
```bash
python main.py discover --type movie --genre comedy --provider netflix --region US --language en-US
```

For random:
```bash
python main.py random --type tv --genre thriller --provider hbo --region US --language en-US
```

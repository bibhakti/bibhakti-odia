# Bibhakti

Odia case-marker (ବିଭକ୍ତି) utilities. Work in progress.

## Install

```bash
pip install bibhakti
```

## Usage

```python
from bibhakti import split, segment

split("କଟକରୁ")            # ('କଟକ', 'ରୁ')
segment("ମୋ ଠିକଣା କଟକରୁ ଭୁବନେଶ୍ୱରକୁ ବଦଳିଛି")
# ['ମୋ', 'ଠିକଣା', 'କଟକ', 'ରୁ', 'ଭୁବନେଶ୍ୱର', 'କୁ', 'ବଦଳିଛି']
```

This early release is a simple rule-based baseline. More to come.

## License

MIT

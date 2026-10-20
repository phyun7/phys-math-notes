import json, re, sys
from pathlib import Path
p = Path("zensical.toml")
p.write_text(re.sub(r'^site_url = .*$', 'site_url = ' + json.dumps(sys.argv[1]), p.read_text(), flags=re.M))

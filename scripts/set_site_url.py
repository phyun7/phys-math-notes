import json
from pathlib import Path
import re
import sys

path = Path("zensical.toml")
path.write_text(re.sub(r'^site_url = .*$', 'site_url = ' + json.dumps(sys.argv[1]),
                       path.read_text(), flags=re.M))

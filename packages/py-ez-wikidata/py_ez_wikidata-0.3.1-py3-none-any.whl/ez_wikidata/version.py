"""
Created on 2024-03-01

@author: wf
"""

from dataclasses import dataclass

import ez_wikidata


@dataclass
class Version(object):
    """
    Version handling for easy wikidata access
    """

    name = "py_ez_wikidata"
    version = ez_wikidata.__version__
    date = "2024-03-01"
    updated = "2025-06-18"
    description = "Mapping for Wikidata allows creation of wikidata entries from dicts"

    authors = "Tim Holzheim, Wolfgang Fahl"

    doc_url = "https://wiki.bitplan.com/index.php/Py_ez_wikidata"
    chat_url = "https://github.com/WolfgangFahl/py_ez_wikidata/discussions"
    cm_url = "https://github.com/WolfgangFahl/py_ez_wikidata"

    license = f"""Copyright 2024-2025 contributors. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied."""
    longDescription = f"""{name} version {version}
{description}

  Created by {authors} on {date} last updated {updated}"""

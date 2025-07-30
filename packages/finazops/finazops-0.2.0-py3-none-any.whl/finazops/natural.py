import subprocess
from difflib import get_close_matches
from typing import Optional


def run_natural_language(cmd: str) -> Optional[int]:
    """Execute a script based on a natural language command.

    The function dispatches known keywords to the matching shell script. If no
    direct keyword is found a fuzzy match is attempted on individual words.

    Parameters
    ----------
    cmd:
        Free form text describing the desired action.

    Returns
    -------
    Optional[int]
        The return code from the executed script or ``None`` if no match was
        found.
    """

    text = cmd.lower()

    if "budget" in text:
        script = "check-budgets.sh"
    elif "waste" in text:
        script = "detect-waste.sh"
    elif "saving" in text or "recommend" in text:
        script = "generate-recommendations.sh"
    else:
        keywords = {
            "budget": "check-budgets.sh",
            "waste": "detect-waste.sh",
            "savings": "generate-recommendations.sh",
        }
        script = None
        for word in text.split():
            match = get_close_matches(word, keywords.keys(), n=1, cutoff=0.8)
            if match:
                script = keywords[match[0]]
                break

    if script:
        return subprocess.call(["bash", script])
    return None

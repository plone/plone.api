import logging
import os
import re

logging.basicConfig(encoding='utf-8')  # Add encoding for proper character handling
logger = logging.getLogger("fix converted MyST documentation")
logger.setLevel(logging.INFO)

logger.info("Fix some MyST / markdown stuff.")
count_files = {
    "modified": 0,
    "unmodified": 0,
}


def replace_label_underscore(data):
    """Fix 'examples' reference in docstrings.

    :Example: :ref:`portal_get_tool_example`
    ->
    :Example: :ref:`portal-get-tool-example`
    """
    regex_label_underscore = "(?<=:ref:`)(.*)(?=`)"

    def _replace(mobj):
        return mobj.group(0).replace("_", "-")

    data = re.sub(regex_label_underscore, _replace, data)
    return data


def remove_github_warning(data):
    """Remove 'GitHub-only' warning"""
    regex_github_warning = r":::{admonition} GitHub-only([\S\s]*?):::\n\n"
    data = re.sub(regex_github_warning, "", data, flags=re.DOTALL)
    return data


for root, dirs, files in (*os.walk("./src"), *os.walk("./docs")):
    for name in files:
        if name.endswith(".py") or name.endswith(".md"):
            filename = os.path.join(root, name)
            try:
                with open(filename, "r+") as f:
                    original_data = f.read()
                    modified_data = replace_label_underscore(original_data)
                    modified_data = remove_github_warning(modified_data)

                    if modified_data != original_data:
                        f.seek(0)
                        f.write(modified_data)
                        f.truncate()
                        count_files["modified"] += 1
                        logger.info(f"{filename} modified.")
                    else:
                        count_files["unmodified"] += 1
                        logger.info(f"{filename} unmodified.")


            except IOError as e:
                logger.error(f"Error processing {filename}: {e}")

logger.info(f'MyST modified for {count_files["modified"]} files.')
logger.info(f'{count_files["unmodified"]} files unmodified.')

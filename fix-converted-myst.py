import logging
import os
import re

logging.basicConfig()
logger = logging.getLogger("fix converted myST documentation")
logger.setLevel(logging.INFO)

logger.info("Fix some myST / markdown stuff.")
count_files = {
    "modified": 0,
    "unmodified": 0,
}

regex_replace_example = '(?<=:ref:`)(.*)(?=`)'


def replace_label_underscore(mobj):
    return mobj.group(0).replace('_', '-')


regex_github_warning = r':::{admonition}([\S\s]*?):::'


for root, dirs, files in (*os.walk('./src'), *os.walk('./docs')):
    for name in files:
        if name.endswith(".py") or name.endswith(".md"):
            filename = os.path.join(root, name)
            with open(filename, 'r+') as f:
                data = f.read()
                data_new = re.sub(regex_replace_example, replace_label_underscore, data)
                # data_new = re.sub(regex_github_warning, '', data_new, flags=re.DOTALL)
                f.seek(0)
                f.write(data_new)
                count_files["modified"] += 1
                logger.info(f"{filename} modified.")


logger.info(f'myST modified for {count_files["modified"]} files.')
logger.info(f'{count_files["unmodified"]} files unmodified.')

# '\\1'.replace('_', '-')

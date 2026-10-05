import json
import os

from utils import generate_hash


COMMITS_DIR = "data/commits"
HEAD_FILE = "data/HEAD"
OBJECTS_DIR = "data/objects"


def save_commit(commit):

    os.makedirs(COMMITS_DIR, exist_ok=True)

    path = os.path.join(
        COMMITS_DIR,
        f"{commit.commit_id}.json"
    )

    with open(path, "w", encoding="utf-8") as file:

        json.dump(
            commit.to_dict(),
            file,
            indent=4
        )


def load_commit(commit_id):

    path = os.path.join(
        COMMITS_DIR,
        f"{commit_id}.json"
    )

    if not os.path.exists(path):

        return None

    with open(path, "r", encoding="utf-8") as file:

        return json.load(file)


def save_head(commit_id):

    os.makedirs("data", exist_ok=True)

    with open(
        HEAD_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(commit_id)


def load_head():

    if not os.path.exists(HEAD_FILE):

        return None

    with open(
        HEAD_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read().strip()


def save_object(content):

    os.makedirs(
        OBJECTS_DIR,
        exist_ok=True
    )

    object_id = generate_hash(content)

    path = os.path.join(
        OBJECTS_DIR,
        object_id
    )

    if not os.path.exists(path):

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

    return object_id


def load_object(object_id):

    path = os.path.join(
        OBJECTS_DIR,
        object_id
    )

    if not os.path.exists(path):

        return None

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()
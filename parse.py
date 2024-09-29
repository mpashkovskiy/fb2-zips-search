import os
import json


def get_files_from_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            yield f"{directory}/{file}"


def build_index():
    fields = ["authors", "genres", "title", "series", "series_num",
              "file_name", "file_size", "lib_id", "deleted", "ext", "date",
              "lang", "lib_rate", "keywords"]
    print("[")
    for file in get_files_from_directory("unzipped_inpx"):
        with open(file, "+rb") as file:
            for line in file:
                vals = [
                    (
                        part
                        .decode('UTF-8')
                        .replace('\r', '')
                        .replace('\n', '')
                        .strip(":")
                        .strip()
                    )
                    for part in line.split(b'\x04')
                ]

                d = dict(zip(fields, vals))
                if "authors" in d:
                    d["authors"] = [
                        " ".join(a.split(",")).strip()
                        for a in d["authors"].split(":")
                    ]
                if "genres" in d:
                    d["genres"] = d["genres"].split(":")
                if "keywords" in d:
                    d["keywords"] = d["keywords"].split(",")
                d["archive"] = file.name.split("/")[-1].replace(".inp", "")
                print(json.dumps(d, ensure_ascii=False) + ",")
    print("{}")
    print("]")


if __name__ == "__main__":
    build_index()

import os
import sys
import pickle
import zipfile
import re


def tokenize(line):
    """
    Convert a line into normalized tokens.
    Tokens contain letters, digits and underscore.
    """
    return re.findall(r'[A-Za-z0-9_]+', line.lower())


def build_index(folder, output_zip):
    """
    Scan all files in the folder and create an inverted index.
    """

    index = {}

    total_files = 0
    total_lines = 0

    # Temporary pickle file
    pickle_name = "log_index.pkl"

    # Scan folder
    for filename in sorted(os.listdir(folder)):

        filepath = os.path.join(folder, filename)

        # Process only regular files
        if not os.path.isfile(filepath):
            continue

        total_files += 1

        try:
            with open(
                filepath,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                for line_number, line in enumerate(
                    file,
                    start=1
                ):

                    total_lines += 1

                    tokens = tokenize(line)

                    # Avoid duplicate postings
                    # for the same token on the same line
                    for token in set(tokens):

                        if token not in index:
                            index[token] = []

                        index[token].append(
                            (filename, line_number)
                        )

        except OSError:
            continue

    # Number of unique tokens
    total_tokens = len(index)

    # Save index using pickle
    with open(
        pickle_name,
        "wb"
    ) as pickle_file:

        pickle.dump(
            index,
            pickle_file,
            protocol=pickle.HIGHEST_PROTOCOL
        )

    # Compress logs + pickle index
    with zipfile.ZipFile(
        output_zip,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as archive:

        # Add all original log files
        for filename in sorted(os.listdir(folder)):

            filepath = os.path.join(folder, filename)

            if os.path.isfile(filepath):
                archive.write(
                    filepath,
                    arcname=filename
                )

        # Add index
        archive.write(
            pickle_name,
            arcname=pickle_name
        )

    # Delete temporary pickle after compression
    try:
        os.remove(pickle_name)
    except OSError:
        pass

    print("FILES", total_files)
    print("LINES", total_lines)
    print("TOKENS", total_tokens)


def search_index(pickle_path, queries):
    """
    Load the pickle index and search for tokens.
    """

    with open(
        pickle_path,
        "rb"
    ) as file:

        index = pickle.load(file)

    for query in queries:

        token = query.lower()

        matches = index.get(
            token,
            []
        )

        # Print all file:line matches
        for filename, line_number in matches:
            print(
                f"{filename}:{line_number}"
            )


def main():

    if len(sys.argv) < 2:
        print("Usage:")
        print("BUILD folder output.zip")
        print("SEARCH index.pkl q token1 token2 ...")
        return

    mode = sys.argv[1].upper()

    if mode == "BUILD":

        if len(sys.argv) != 4:
            print(
                "Usage: BUILD folder output.zip"
            )
            return

        folder = sys.argv[2]
        output_zip = sys.argv[3]

        if not os.path.isdir(folder):
            print("Folder not found")
            return

        build_index(
            folder,
            output_zip
        )

    elif mode == "SEARCH":

        if len(sys.argv) < 4:
            print(
                "Usage: SEARCH index.pkl q token1 token2 ..."
            )
            return

        pickle_path = sys.argv[2]
        q = int(sys.argv[3])

        queries = sys.argv[
            4:4 + q
        ]

        if len(queries) != q:
            print("Invalid number of queries")
            return

        search_index(
            pickle_path,
            queries
        )

    else:
        print("Invalid mode")


if __name__ == "__main__":
    main()
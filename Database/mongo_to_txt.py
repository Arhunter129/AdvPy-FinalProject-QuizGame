from typing import Any, List, Iterator
from pymongo import MongoClient  # type: ignore
from pymongo.server_api import ServerApi  # type: ignore
from pymongo.errors import ConnectionFailure  # type: ignore
from pymongo.cursor import Cursor  # type: ignore


def get_mongodb_data(
        connection_string: str,
        path: str,
        db_name: str,
        collection_name: str) -> Cursor:
    client = MongoClient(
        connection_string,
        tls=True,
        tlsCertificateKeyFile=path,
        server_api=ServerApi('1'))

    try:
        client.admin.command('ismaster')
        print("MongoDB connection successful. Fetching documents...")
    except ConnectionFailure:
        print("MongoDB connection failed.")

    db = client[db_name]
    return db[collection_name].find()


def format_data(documents: Iterator[Any]) -> List[str]:
    formatted_data = []
    for doc in documents:
        formatted_data.append(doc["question"])
        formatted_data.extend(doc["options"])
        formatted_data.append(doc["answer"] + "\n")
    return formatted_data


def write_to_file(data: List[str], file_path: str) -> None:
    with open(file_path, "w") as file:
        for line in data:
            file.write(str(line) + "\n")


if __name__ == "__main__":
    path_to_certificate = "../X509-cert-4213624397857697800.pem"
    uri = (
        "mongodb+srv://cluster0.dgvxubp.mongodb.net/"
        "?authSource=%24external&authMechanism=MONGODB-X509&"
        "retryWrites=true&w=majority"
    )
    db_name = "Quiz"
    collection_name = "Questions"
    file_path = "output.txt"

    # Fetch documents
    documents = get_mongodb_data(
        uri,
        path_to_certificate,
        db_name,
        collection_name)

    print("Documents fetched. Now converting to txt...")

    # Format data
    data = format_data(documents)

    print("Data converted. Now writing to file...")

    # Write to file
    write_to_file(data, file_path)

    print("Done.")

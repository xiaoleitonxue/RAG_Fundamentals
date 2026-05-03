from gitdb.fun import chunk_size

md5_path = "./md5.txt"

#chroma
collection_name = "rag"
persist_directory = "./chroma_db"

#spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", r"(?<=\. )", " ", ""]
max_split_char_number = 1000
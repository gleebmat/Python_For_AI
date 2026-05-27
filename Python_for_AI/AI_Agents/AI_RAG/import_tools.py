from tools import grep, read_file, list_files


print("Files in notes/:")
for f in list_files():
    print(f" {f}")


print("\nGrep for 'connection pool':")
for hit in grep("connection pool"):
    print(f" {hit}")


print("\nFirst 200 chars of 04-architecture-desicions.md:")
print(read_file("04-architecture-decisions.md")[:200])


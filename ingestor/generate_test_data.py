import os

DATA_DIR = "test_data"
os.makedirs(DATA_DIR, exist_ok=True)

def create_dummy_file(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        # Create predictable content: "Line 0", "Line 1"...
        # This makes it easy to see if your chunker is skipping correctly.
        for i in range(lines):
            f.write(f"This is line number {i} in the document {filename}. It contains some padding text to make it look like a real paragraph.\n")
    print(f"Created {path} ({lines} lines)")

# 1. A small file (Quick test)
create_dummy_file("small_doc_1.txt", 100)

# 2. A massive file (Crash test dummy)
# You will use this to hit Ctrl+C midway.
create_dummy_file("massive_doc.txt", 50000)

# 3. A file you will manually edit later (Hash change test)
create_dummy_file("edit_me_later.txt", 500)

print("\n✅ Test Data Ready in /test_data folder.")
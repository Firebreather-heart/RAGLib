This is the "Final Exam" specification, **Lord fire breather**. Since you are going "dark" (no AI/Internet), this document is your only lifeline. Print it or save it locally.

### 🧱 Project: The Resilient Granular ETL Pipeline

**Objective:** Build a Python ingestion script that processes text files chunk-by-chunk. It must support **crashing at any moment** and resuming exactly where it left off, without skipping data or processing the same chunk twice.

**Tech Stack Constraints:**

* **Language:** Python 3.x (Standard Library only, except for `blake3` if you installed it, otherwise `hashlib`).
* **Database:** SQLite3 (Raw SQL queries only. No ORMs).
* **External Libs:** None required (use your existing `chunker`).

---

### 1. The Database Schema (The Truth Source)

You must implement a class `StateManager` that manages a SQLite database `pipeline.db` with this exact behavior:

**Table:** `ingestion_state`

* `file_path` (TEXT, Primary Key): Unique ID for the file.
* `file_hash` (TEXT): The fingerprint of the file content.
* `last_chunk_index` (INTEGER): The index of the last successfully processed chunk. Default is `-1` (nothing processed).
* `status` (TEXT): 'processing' or 'completed'.

---

### 2. The Logic Flow (The Orchestrator)

Your `main.py` must follow this exact decision tree for every file in the directory:

1. **Calculate Hash:** Read the file (streamed) and compute the BLAKE3/SHA256 hash.
2. **Query DB:** Check if this `file_path` exists in SQLite.
3. **The Decision:**
* **Scenario A (New File):** Path not found.
* *Action:* Insert new row. Start processing from Chunk 0.


* **Scenario B (Changed File):** Path found, but `stored_hash != current_hash`.
* *Action:* **Reset** the row (update hash, set `last_chunk_index = -1`). Start from Chunk 0.


* **Scenario C (Resuming):** Path found, `stored_hash == current_hash`, status is 'processing'.
* *Action:* Read `last_chunk_index` (e.g., 50). Skip chunks 0-50. Start processing at Chunk 51.


* **Scenario D (Done):** Path found, Hash matches, status is 'completed'.
* *Action:* Skip file entirely.




4. **The Loop (Processing):**
* For each chunk yielded by your generator:
* **Simulate Work:** `time.sleep(0.1)` (This allows you to hit Ctrl+C easily).
* **Print:** `Processing {file}: Chunk {i}`.
* **Commit:** Update `last_chunk_index` in SQLite to `i`. **(Critical: This must happen AFTER work is done).**




5. **Completion:**
* When the loop finishes, update `status` to 'completed'.



---

### 3. The Test Data (The Playground)

Since you cannot download data later, run this script **NOW** to generate your "dummy" dataset. It creates files that are easy to verify visually (line numbers match the text).

**Save as `generate_test_data.py` and run it once:**

```python
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
create_dummy_file("small_doc.txt", 100)

# 2. A massive file (Crash test dummy)
# You will use this to hit Ctrl+C midway.
create_dummy_file("massive_doc.txt", 50000)

# 3. A file you will manually edit later (Hash change test)
create_dummy_file("edit_me_later.txt", 500)

print("\n✅ Test Data Ready in /test_data folder.")

```

---

### 4. The Acceptance Criteria (Pass/Fail)

You pass the challenge if you can perform this sequence successfully without internet:

**Test 1: The Interrupt**

1. Run the pipeline on `massive_doc.txt`.
2. Watch it print "Processing Chunk 0... 1... 2...".
3. Hit `Ctrl+C` when it reaches roughly **Chunk 500**.
4. Restart the script.
5. **PASS Condition:** The script immediately prints "Resuming massive_doc.txt from Chunk 501..." (It must NOT process 0-500 again).

**Test 2: The Mutation**

1. Open `edit_me_later.txt` and change one character in the first line. Save it.
2. Run the pipeline.
3. **PASS Condition:** The script detects the hash mismatch, prints "File changed! Resetting...", and starts from **Chunk 0**.

**Test 3: The Completion**

1. Let `small_doc.txt` finish completely.
2. Run the script again.
3. **PASS Condition:** The script prints "Skipping small_doc.txt (Already Completed)".

Good luck, **Lord fire breather**. See you on the other side.
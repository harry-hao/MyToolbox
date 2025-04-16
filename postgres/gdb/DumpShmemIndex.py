import gdb

def print_shmemindex():
    # Check if ShmemIndex is valid
    shmemindex = gdb.parse_and_eval("ShmemIndex")
    if not shmemindex:
        print("ShmemIndex is NULL. Shared memory may not be initialized.")
        return

    # Check if hctl is valid
    hctl = shmemindex["hctl"]
    if hctl == 0:
        print("ShmemIndex->hctl is NULL. Invalid hash table.")
        return

    # Use dsize as the number of segments
    nsegs = int(hctl["dsize"])
    print("Number of segments (nsegs): %d" % nsegs)

    nbuckets = int(hctl["max_bucket"]) + 1
    print("Number of buckets (nbuckets): %d" % nbuckets)

    entries = []

    # Iterate through each segment and bucket
    for i in range(nsegs):
        segment = shmemindex["dir"][i]
        if not segment:
            continue

        for j in range(nbuckets):
            bucket = segment[j]

            if not bucket:
                continue

            element = bucket[0].address
            k = 0

            while element != gdb.Value(0):
                entry = element.cast(gdb.lookup_type("HASHELEMENT").pointer()) + 1
                entry = entry.cast(gdb.lookup_type("ShmemIndexEnt").pointer())

                key = str(entry["key"]).split(",")[0][:32]
                location = str(entry["location"])
                size = int(entry["size"])
                entries.append((key, location, size))

                element = element["link"]
                k += 1

    # Sort entries by size
    entries = sorted(entries, key=lambda x: x[2], reverse=True)

    # Print sorted entries
    for key, location, size in entries:
        print("Key: %32s, Location: %12s, Size: %12d" % (key, location, size))

# Register the command
class DumpShmemIndexCommand(gdb.Command):
    def __init__(self):
        super(DumpShmemIndexCommand, self).__init__("dump-shmemindex", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        print_shmemindex()

DumpShmemIndexCommand()

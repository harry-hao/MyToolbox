import gdb

class DumpBackgroundWorkerList(gdb.Command):
    """Print the BackgroundWorkerList."""

    def __init__(self):
        super(DumpBackgroundWorkerList, self).__init__("dump-bgw", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        # Get the head pointer of BackgroundWorkerList
        worker = gdb.parse_and_eval("BackgroundWorkerList.head.next")
        print("head is %s" % worker)

        # Ensure BackgroundWorkerList is valid
        if not worker:
            print("BackgroundWorkerList is NULL.")
            return

        # Traverse the BackgroundWorkerList
        registered_bgworker_type = gdb.lookup_type("RegisteredBgWorker")

        # Calculate the offset of slist_node within RegisteredBgWorker

        dummy_worker = gdb.Value(0).cast(registered_bgworker_type.pointer())


        slist_node_addr = dummy_worker["rw_lnode"].address
        slist_node_offset = slist_node_addr

        print("offset = %s"%slist_node_offset)
        while worker != 0:
            # Get the address of RegisteredBgWorker using the offset
            registered_worker = ((worker.cast(gdb.lookup_type("char").pointer()) -
                                 slist_node_offset.cast(gdb.lookup_type("char").pointer()))
                                 .cast(registered_bgworker_type.pointer()))

            # Print the attributes of RegisteredBgWorker
            print("Worker: {}".format(registered_worker))
            print("  PID: {}".format(registered_worker["rw_pid"]))
            print("  CrashAt: {}".format(registered_worker["rw_crashed_at"]))
            print("  Name: {}".format(registered_worker["rw_worker"]["bgw_name"].string()))
            print("  Library Name: {}".format(registered_worker["rw_worker"]["bgw_library_name"].string()))
            print("  Function Name: {}".format(registered_worker["rw_worker"]["bgw_function_name"].string()))

            # Get the next worker
            worker = worker["next"]

DumpBackgroundWorkerList()

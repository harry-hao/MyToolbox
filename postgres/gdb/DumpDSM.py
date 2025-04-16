import gdb

class DumpDsmSegmentList(gdb.Command):
    """Dump the contents of dsm_segment_list."""

    def __init__(self):
        super(DumpDsmSegmentList, self).__init__("dump-dsm", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        dsm_segment_list = gdb.parse_and_eval("dsm_segment_list")
        head = dsm_segment_list["head"]

        dsm_segment_type = gdb.lookup_type("dsm_segment")
        dsm_segment_ptr_type = dsm_segment_type.pointer()

        current = head["next"]
        while current != head.address:
            dsm_segment = current.cast(dsm_segment_ptr_type)

            print("dsm_segment: {} handle: {} mapped_address: {} mapped_size: {}".format(
                dsm_segment,
                dsm_segment["handle"],
                dsm_segment["mapped_address"],
                dsm_segment["mapped_size"]))

            current = current["next"]

DumpDsmSegmentList()

import gdb, csv, os

CSV_PATH = os.getcwd() + "/gdb-syscall/syscall_table.csv"

def load_syscall_csv(path):
    table = {}
    if not os.path.isfile(path):
        gdb.write(f"[sc] CSV not found: {path}\n", gdb.STDERR)
        return table
    try:
        with open(path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                num_str = row.get("syscall number", "").strip()
                if not num_str:
                    continue
                try:
                    num = int(num_str)
                except:
                    continue
                table[num] = row
    except Exception as e:
        gdb.write(f"[sc] load error: {e}\n", gdb.STDERR)
    return table

SYSCALL_TABLE = load_syscall_csv(CSV_PATH)


class SyscallInfo(gdb.Command):
    """Print syscall info using CSV (usage: sc [nr])"""

    def __init__(self):
        super(SyscallInfo, self).__init__("sc", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        arg = arg.strip()

        if arg:
            try:
                # 0xNN 형태도 지원
                if arg.lower().startswith("0x"):
                    nr = int(arg, 16)
                else:
                    nr = int(arg, 10)
            except Exception:
                gdb.write(f"[sc] invalid syscall number: '{arg}'\n", gdb.STDERR)
                return
        else:
            try:
                nr = int(gdb.parse_and_eval("$rax"))
            except Exception:
                gdb.write("[sc] Cannot read $rax\n", gdb.STDERR)
                return

        info = SYSCALL_TABLE.get(nr)
        name = info["syscall"] if info else "unknown"

        def reg(x):
            try:
                return gdb.parse_and_eval(f"${x}")
            except Exception:
                return None

        rdi = reg("rdi")
        rsi = reg("rsi")
        rdx = reg("rdx")
        r10 = reg("r10")
        r8  = reg("r8")
        r9  = reg("r9")

        gdb.write("\n───────────────[ SYSCALL ]───────────────\n")
        gdb.write(f"  #{nr}   {name}\n")

        if info:
            desc = {
                "rdi": info.get("%rdi", "").strip(),
                "rsi": info.get("%rsi", "").strip(),
                "rdx": info.get("%rdx", "").strip(),
                "r10": info.get("%rcx", "").strip(),
                "r8":  info.get("%r8", "").strip(),
                "r9":  info.get("%r9", "").strip(),
            }
        else:
            desc = {k: "" for k in ["rdi", "rsi", "rdx", "r10", "r8", "r9"]}

        def out(label, val, d):
            if val is None:
                return
            line = f"  {label:12s} = {val}"
            if d:
                line += f"    // {d}"
            gdb.write(line + "\n")

        out("rdi",      rdi, desc["rdi"])
        out("rsi",      rsi, desc["rsi"])
        out("rdx",      rdx, desc["rdx"])
        out("r10(rcx)", r10, desc["r10"])
        out("r8",       r8,  desc["r8"])
        out("r9",       r9,  desc["r9"])

        gdb.write("──────────────────────────────────────────\n")


SyscallInfo()

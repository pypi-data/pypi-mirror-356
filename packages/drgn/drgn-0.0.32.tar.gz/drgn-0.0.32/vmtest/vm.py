# Copyright (c) Meta Platforms, Inc. and affiliates.
# SPDX-License-Identifier: LGPL-2.1-or-later

import contextlib
import enum
import os
from pathlib import Path
import re
import shlex
import shutil
import socket
import subprocess
import sys
import tempfile
from typing import Any, Optional, Sequence

from util import nproc, out_of_date
from vmtest.config import HOST_ARCHITECTURE, Kernel, local_kernel
from vmtest.download import (
    DOWNLOAD_KERNEL_ARGPARSE_METAVAR,
    DownloadKernel,
    download,
    download_kernel_argparse_type,
)
from vmtest.kmod import build_kmod

# Script run as init in the virtual machine.
_INIT_TEMPLATE = r"""#!/bin/sh

# Having /proc from the host visible in the guest can confuse some commands. In
# particular, if BusyBox is configured with FEATURE_SH_STANDALONE, then busybox
# sh executes BusyBox applets using /proc/self/exe. So, before doing anything
# else, mount /proc (using the fully qualified executable path so that BusyBox
# doesn't use /proc/self/exe).
/bin/mount -t proc -o nosuid,nodev,noexec proc /proc

set -eu

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
export DRGN_TEST_DISK=/dev/vda
{kdump_needs_nosmp}

# On exit, power off. We don't use the poweroff command because very minimal
# installations don't have it (e.g., the debootstrap minbase variant). We don't
# use the "o" magic SysRq because it returns immediately. Since we run QEMU
# with -no-reboot, we can use the "b" magic SysRq, which is synchronous.
trap 'echo b > /proc/sysrq-trigger' exit

umask 022

HOSTNAME=vmtest
VPORT_NAME=com.osandov.vmtest.0
RELEASE=$(uname -r)

# Set up overlayfs.
if [ ! -w /tmp ]; then
	mount -t tmpfs tmpfs /tmp
fi
mkdir /tmp/upper /tmp/work /tmp/merged
mkdir /tmp/upper/dev /tmp/upper/etc /tmp/upper/mnt
mkdir -m 555 /tmp/upper/proc /tmp/upper/sys
mkdir -m 1777 /tmp/upper/tmp
if [ -e /tmp/host ]; then
	mkdir /tmp/host_upper /tmp/host_work /tmp/upper/host
fi

mount -t overlay -o lowerdir=/,upperdir=/tmp/upper,workdir=/tmp/work overlay /tmp/merged
if [ -e /tmp/host ]; then
	mount -t overlay -o lowerdir=/tmp/host,upperdir=/tmp/host_upper,workdir=/tmp/host_work overlay /tmp/merged/host
fi

# Mount core filesystems.
mount -t devtmpfs -o nosuid,noexec dev /tmp/merged/dev
mkdir /tmp/merged/dev/shm
mount -t tmpfs -o nosuid,nodev tmpfs /tmp/merged/dev/shm
mount -t proc -o nosuid,nodev,noexec proc /tmp/merged/proc
mount -t sysfs -o nosuid,nodev,noexec sys /tmp/merged/sys
# cgroup2 was added in Linux v4.5.
mount -t cgroup2 -o nosuid,nodev,noexec cgroup2 /tmp/merged/sys/fs/cgroup || true
# Ideally we'd just be able to create an opaque directory for /tmp on the upper
# layer. However, before Linux kernel commit 51f7e52dc943 ("ovl: share inode
# for hard link") (in v4.8), overlayfs doesn't handle hard links correctly,
# which breaks some tests.
mount -t tmpfs -o nosuid,nodev tmpfs /tmp/merged/tmp

# Pivot into the new root.
pivot_root /tmp/merged /tmp/merged/mnt
cd /
umount -n -l /mnt

# Load kernel modules.
mkdir -p "/lib/modules/$RELEASE"
mount --bind {kernel_dir} "/lib/modules/$RELEASE"
modprobe -a rng_core virtio_rng

# Create static device nodes.
grep -v '^#' "/lib/modules/$RELEASE/modules.devname" |
while read -r module name node; do
	name="/dev/$name"
	dev=${{node#?}}
	major=${{dev%%:*}}
	minor=${{dev##*:}}
	type=${{node%"${{dev}}"}}
	mkdir -p "$(dirname "$name")"
	mknod "$name" "$type" "$major" "$minor"
done
ln -s /proc/self/fd /dev/fd
ln -s /proc/self/fd/0 /dev/stdin
ln -s /proc/self/fd/1 /dev/stdout
ln -s /proc/self/fd/2 /dev/stderr

# Mount additional filesystems.
mount -t binfmt_misc -o nosuid,nodev,noexec binfmt_misc /proc/sys/fs/binfmt_misc
# We currently only enable tracefs if we have uprobes, which AArch64 only
# supports since Linux 4.10.
mount -t tracefs -o nosuid,nodev,noexec tracefs /sys/kernel/tracing || true

# Configure networking.
cat << EOF > /etc/hosts
127.0.0.1 localhost
::1 localhost
127.0.1.1 $HOSTNAME.localdomain $HOSTNAME
EOF
: > /etc/resolv.conf
hostname "$HOSTNAME"
ip link set lo up

# Find virtio port.
vport=
for vport_dir in /sys/class/virtio-ports/*; do
	if [ -r "$vport_dir/name" -a "$(cat "$vport_dir/name")" = "$VPORT_NAME" ]; then
		vport="${{vport_dir#/sys/class/virtio-ports/}}"
		break
	fi
done
if [ -z "$vport" ]; then
	echo "could not find virtio-port \"$VPORT_NAME\""
	exit 1
fi

cd {cwd}
{test_kmod}
set +e
{stty}
setsid -c sh -c {command}
rc=$?
set -e

echo "Exited with status $rc"
echo "$rc" > "/dev/$vport"
"""


def _compile(
    *args: str,
    CPPFLAGS: str = "",
    CFLAGS: str = "",
    LDFLAGS: str = "",
    LIBADD: str = "",
) -> None:
    # This mimics automake: the order of the arguments allows for the default
    # flags to be overridden by environment variables, and we use the same
    # default CFLAGS.
    cmd = [
        os.getenv("CC", "cc"),
        *shlex.split(CPPFLAGS),
        *shlex.split(os.getenv("CPPFLAGS", "")),
        *shlex.split(CFLAGS),
        *shlex.split(os.getenv("CFLAGS", "-g -O2")),
        *shlex.split(LDFLAGS),
        *shlex.split(os.getenv("LDFLAGS", "")),
        *args,
        *shlex.split(LIBADD),
        *shlex.split(os.getenv("LIBS", "")),
    ]
    print(" ".join([shlex.quote(arg) for arg in cmd]))
    subprocess.check_call(cmd)


def _build_onoatimehack(dir: Path) -> Path:
    dir.mkdir(parents=True, exist_ok=True)

    onoatimehack_so = dir / "onoatimehack.so"
    onoatimehack_c = (Path(__file__).parent / "onoatimehack.c").relative_to(Path.cwd())
    if out_of_date(onoatimehack_so, onoatimehack_c):
        _compile(
            "-o",
            str(onoatimehack_so),
            str(onoatimehack_c),
            CPPFLAGS="-D_GNU_SOURCE",
            CFLAGS="-fPIC",
            LDFLAGS="-shared",
            LIBADD="-ldl",
        )
    return onoatimehack_so


def _have_setpriv_pdeathsig() -> bool:
    # util-linux supports setpriv --pdeathsig since v2.33. BusyBox doesn't
    # support it as of v1.37.
    try:
        help = subprocess.run(
            ["setpriv", "--help"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ).stdout
    except FileNotFoundError:
        return False
    return b"--pdeathsig" in help


class TestKmodMode(enum.Enum):
    NONE = 0
    BUILD = 1
    INSERT = 2


class LostVMError(Exception):
    pass


def run_in_vm(
    command: str,
    kernel: Kernel,
    root_dir: Optional[Path],
    build_dir: Path,
    *,
    extra_qemu_options: Sequence[str] = (),
    test_kmod: TestKmodMode = TestKmodMode.NONE,
    interactive: bool = False,
) -> int:
    if root_dir is None:
        if kernel.arch is HOST_ARCHITECTURE:
            root_dir = Path("/")
        else:
            root_dir = build_dir / kernel.arch.name / "rootfs"

    if test_kmod != TestKmodMode.NONE:
        kmod = build_kmod(build_dir, kernel)

    qemu_exe = "qemu-system-" + kernel.arch.name
    match = re.search(
        r"QEMU emulator version ([0-9]+(?:\.[0-9]+)*)",
        subprocess.check_output([qemu_exe, "-version"], universal_newlines=True),
    )
    if not match:
        raise Exception("could not determine QEMU version")
    qemu_version = tuple(int(x) for x in match.group(1).split("."))

    # QEMU's 9pfs O_NOATIME handling was fixed in 5.1.0. The fix was backported
    # to 5.0.1.
    env = os.environ.copy()
    if qemu_version < (5, 0, 1):
        onoatimehack_so = _build_onoatimehack(build_dir)
        env["LD_PRELOAD"] = f"{str(onoatimehack_so)}:{env.get('LD_PRELOAD', '')}"

    # Kill the child QEMU process if we die. If we die between the fork() and
    # the prctl(PR_SET_PDEATHSIG), then the signal won't be delivered, but then
    # QEMU will fail to connect to our socket and exit.
    if _have_setpriv_pdeathsig():
        setpriv_args = ["setpriv", "--pdeathsig=TERM"]
    else:
        setpriv_args = []

    kvm_args = []
    if HOST_ARCHITECTURE is not None and kernel.arch.name == HOST_ARCHITECTURE.name:
        if os.access("/dev/kvm", os.R_OK | os.W_OK):
            kvm_args = ["-cpu", "host", "-enable-kvm"]
        else:
            print(
                "warning: /dev/kvm cannot be accessed; falling back to emulation",
                file=sys.stderr,
            )

    if interactive:
        serial_args = ["-serial", "mon:stdio"]
        infile = None
    else:
        serial_args = [
            "-chardev",
            "stdio,id=stdio,signal=off",
            "-serial",
            "chardev:stdio",
        ]
        infile = subprocess.DEVNULL

    virtfs_options = "security_model=none,readonly=on"
    # multidevs was added in QEMU 4.2.0.
    if qemu_version >= (4, 2):
        virtfs_options += ",multidevs=remap"
    _9pfs_mount_options = f"trans=virtio,cache=loose,msize={1024 * 1024}"

    with contextlib.ExitStack() as exit_stack:
        temp_path = Path(
            exit_stack.enter_context(tempfile.TemporaryDirectory(prefix="drgn-vmtest-"))
        )
        socket_path = temp_path / "socket"
        server_sock = exit_stack.enter_context(socket.socket(socket.AF_UNIX))
        server_sock.bind(str(socket_path))
        server_sock.listen()

        init_path = temp_path / "init"

        unshare_args = []
        if root_dir == Path("/"):
            host_virtfs_args = []
            init = str(init_path.resolve())
            host_dir_prefix = ""
        else:
            # Try to detect if the rootfs was created without privileges (e.g.,
            # by vmtest.rootfsbuild) and remap the UIDs/GIDs if so.
            if (root_dir / "bin" / "mount").stat().st_uid != 0:
                unshare_args = [
                    "unshare",
                    "--map-root-user",
                    "--map-users=auto",
                    "--map-groups=auto",
                ]
            host_virtfs_args = [
                "-virtfs",
                f"local,path=/,mount_tag=host,{virtfs_options}",
            ]
            init = f'/bin/sh -- -c "/bin/mount -t tmpfs tmpfs /tmp && /bin/mkdir /tmp/host && /bin/mount -t 9p -o {_9pfs_mount_options},ro host /tmp/host && . /tmp/host{init_path.resolve()}"'
            host_dir_prefix = "/host"

        if test_kmod == TestKmodMode.NONE:
            test_kmod_command = ""
        else:
            test_kmod_command = f"export DRGN_TEST_KMOD={shlex.quote(host_dir_prefix + str(kmod.resolve()))}"
            if test_kmod == TestKmodMode.INSERT:
                test_kmod_command += '\ninsmod "$DRGN_TEST_KMOD"'

        terminal_size = shutil.get_terminal_size((0, 0))
        if terminal_size.columns or terminal_size.lines:
            stty_command = (
                f"stty cols {terminal_size.columns} rows {terminal_size.lines}"
            )
        else:
            stty_command = ""

        init_path.write_text(
            _INIT_TEMPLATE.format(
                cwd=shlex.quote(host_dir_prefix + os.getcwd()),
                kernel_dir=shlex.quote(host_dir_prefix + str(kernel.path.resolve())),
                command=shlex.quote(command),
                kdump_needs_nosmp="" if kvm_args else "export KDUMP_NEEDS_NOSMP=1",
                test_kmod=test_kmod_command,
                stty=stty_command,
            )
        )
        init_path.chmod(0o755)

        disk_path = temp_path / "disk"
        with disk_path.open("wb") as f:
            os.ftruncate(f.fileno(), 1024 * 1024 * 1024)

        proc = subprocess.Popen(
            [
                # fmt: off
                *setpriv_args,
                *unshare_args,

                qemu_exe, *kvm_args,

                # Limit the number of cores to 8, otherwise we can reach an OOM troubles.
                "-smp", str(min(nproc(), 8)), "-m", "2G",

                "-display", "none", *serial_args,

                # This along with -append panic=-1 ensures that we exit on a
                # panic instead of hanging.
                "-no-reboot",

                "-virtfs",
                f"local,id=root,path={root_dir},mount_tag=/dev/root,{virtfs_options}",
                *host_virtfs_args,

                "-device", "virtio-rng",

                "-device", "virtio-serial",
                "-chardev", f"socket,id=vmtest,path={socket_path}",
                "-device",
                "virtserialport,chardev=vmtest,name=com.osandov.vmtest.0",

                "-drive", f"file={disk_path},if=virtio,media=disk,format=raw",

                *kernel.arch.qemu_options,

                "-kernel", str(kernel.path / "vmlinuz"),
                "-append",
                f"rootfstype=9p rootflags={_9pfs_mount_options} ro console={kernel.arch.qemu_console},115200 panic=-1 crashkernel=256M init={init}",

                *extra_qemu_options,
                # fmt: on
            ],
            env=env,
            stdin=infile,
        )
        try:
            server_sock.settimeout(5)
            try:
                sock = exit_stack.enter_context(server_sock.accept()[0])
            except socket.timeout:
                raise LostVMError(
                    f"QEMU did not connect within {server_sock.gettimeout()} seconds"
                )
            status_buf = bytearray()
            while True:
                try:
                    buf = sock.recv(4)
                except ConnectionResetError:
                    buf = b""
                if not buf:
                    break
                status_buf.extend(buf)
        except BaseException:
            proc.terminate()
            raise
        finally:
            proc.wait()
        if not status_buf:
            raise LostVMError("VM did not return status")
        if status_buf[-1] != ord("\n") or not status_buf[:-1].isdigit():
            raise LostVMError(f"VM returned invalid status: {repr(status_buf)[11:-1]}")
        return int(status_buf)


if __name__ == "__main__":
    import argparse
    import logging

    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", level=logging.INFO
    )

    class _StringSplitExtendAction(argparse.Action):
        def __call__(
            self, parser: Any, namespace: Any, values: Any, option_string: Any = None
        ) -> None:
            items = getattr(namespace, self.dest, None)
            if items is None:
                setattr(namespace, self.dest, values.split())
            else:
                items.extend(values.split())

    parser = argparse.ArgumentParser(
        description="run vmtest virtual machine",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--directory",
        metavar="DIR",
        type=Path,
        default="build/vmtest",
        help="directory for vmtest artifacts",
    )
    parser.add_argument(
        "--lost-status",
        metavar="STATUS",
        type=int,
        default=128,
        help="exit status if VM is lost",
    )
    parser.add_argument(
        "-k",
        "--kernel",
        metavar=DOWNLOAD_KERNEL_ARGPARSE_METAVAR,
        type=download_kernel_argparse_type,
        required=HOST_ARCHITECTURE is None,
        default=argparse.SUPPRESS,
        help="kernel to use"
        + ("" if HOST_ARCHITECTURE is None else " (default: latest available kernel)"),
    )
    parser.add_argument(
        "-r",
        "--root-directory",
        metavar="DIR",
        default=argparse.SUPPRESS,
        type=Path,
        help="directory to use as root directory in VM (default: / for the host architecture, $directory/$arch/rootfs otherwise)",
    )
    parser.add_argument(
        "--qemu-options",
        metavar="OPTIONS",
        action=_StringSplitExtendAction,
        default=argparse.SUPPRESS,
        help="additional options to pass to QEMU, split on spaces. May be given multiple times",
    )
    parser.add_argument(
        "-Xqemu",
        metavar="OPTION",
        action="append",
        dest="qemu_options",
        default=argparse.SUPPRESS,
        help="additional option to pass to QEMU (not split on spaces). May be given multiple times",
    )
    parser.add_argument(
        "--build-test-kmod",
        dest="test_kmod",
        action="store_const",
        const=TestKmodMode.BUILD,
        default=argparse.SUPPRESS,
        help="build the drgn test kernel module and define the DRGN_TEST_KMOD environment variable in the VM",
    )
    parser.add_argument(
        "--insert-test-kmod",
        dest="test_kmod",
        action="store_const",
        const=TestKmodMode.INSERT,
        default=argparse.SUPPRESS,
        help="insert the drgn test kernel module. Implies --build-test-kmod",
    )
    parser.add_argument(
        "command",
        type=str,
        nargs=argparse.REMAINDER,
        help="command to run in VM (default: sh -i)",
    )
    args = parser.parse_args()

    if not hasattr(args, "kernel"):
        assert HOST_ARCHITECTURE is not None
        args.kernel = DownloadKernel(HOST_ARCHITECTURE, "*")
    if not hasattr(args, "root_directory"):
        args.root_directory = None
    if not hasattr(args, "qemu_options"):
        args.qemu_options = []
    if not hasattr(args, "test_kmod"):
        args.test_kmod = TestKmodMode.NONE

    if args.kernel.pattern.startswith(".") or args.kernel.pattern.startswith("/"):
        kernel = local_kernel(args.kernel.arch, Path(args.kernel.pattern))
    else:
        kernel = next(download(args.directory, [args.kernel]))  # type: ignore[assignment]

    try:
        command = (
            " ".join([shlex.quote(arg) for arg in args.command])
            if args.command
            else "sh -i"
        )
        sys.exit(
            run_in_vm(
                command,
                kernel,
                args.root_directory,
                args.directory,
                extra_qemu_options=args.qemu_options,
                test_kmod=args.test_kmod,
                interactive=True,
            )
        )
    except LostVMError as e:
        print("error:", e, file=sys.stderr)
        sys.exit(args.lost_status)

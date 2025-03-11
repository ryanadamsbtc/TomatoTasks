from __future__ import annotations

import argparse
from . import __version__
from . import storage


def main() -> None:
    parser = argparse.ArgumentParser(prog="tomato", description="Pomodoro + task notes")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("title", help="task title")

    sub.add_parser("ls", help="list tasks")

    p_done = sub.add_parser("done", help="mark a task done")
    p_done.add_argument("id", help="task id")

    p_start = sub.add_parser("start", help="start a pomodoro session")
    p_start.add_argument("minutes", type=int, help="minutes")

    sub.add_parser("stop", help="stop current session")
    sub.add_parser("session", help="show current session")

    args = parser.parse_args()

    if args.cmd == "add":
        t = storage.add_task(args.title)
        print(f"added {t.id} - {t.title}")
    elif args.cmd == "ls":
        tasks = storage.list_tasks()
        for t in tasks:
            mark = "[x]" if t.done else "[ ]"
            print(f"{mark} {t.id}  {t.title}")
    elif args.cmd == "done":
        ok = storage.mark_done(args.id)
        print("ok" if ok else "not found")
    elif args.cmd == "start":
        storage.start_session(args.minutes)
        print(f"session started for {args.minutes} min")
    elif args.cmd == "stop":
        storage.stop_session()
        print("session stopped")
    elif args.cmd == "session":
        s = storage.current_session()
        print(s or "no session")


if __name__ == "__main__":
    main()


# mypackage/__main__.py
import argparse
from .Tools import run




def main():
    parser = argparse.ArgumentParser(description="My Package Command Line Tool")
    parser.add_argument('action', type=str,
                        choices=['create', 'update'],  # 限制可选值
                        help="Action to execute: start/stop/status")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    print('args=', args)

    # 根据动作执行不同逻辑
    if args.action == 'start':
        run(code=1)
    elif args.action == 'stop':
        run(1)
    else:
        run(1)






if __name__ == "__main__":
    main()
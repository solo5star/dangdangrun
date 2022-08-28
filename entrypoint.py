import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="당당런 프로그램")
    parser.add_argument("mode", choices=["server", "bot"])

    args = parser.parse_args()

    if args.mode == "server":
        import dangdangrun_server.main

    elif args.mode == "bot":
        import dangdangrun_bot.main

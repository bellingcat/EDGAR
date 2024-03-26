from edgar_tool.cli import SecEdgarScraperCli
import fire


def main_entrypoint():
    fire.Fire(SecEdgarScraperCli)


if __name__ == "__main__":
    main_entrypoint()

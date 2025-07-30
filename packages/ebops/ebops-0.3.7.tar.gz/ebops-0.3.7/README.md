# Ebops

Eborg is a tool designed for managing e-books and Org-mode files to facilitate analytical reading. With Eborg, you can load EPUB documents, update Org-mode files with table of contents (TOC), and export highlights from your e-books.

## Installing

You can install Eborg using pip:

```bash
pip install ebops
```

## Usage

After installing Eborg, you can use the command-line interface (CLI) to perform various tasks. The CLI is accessed via the `ebops` command.

### Commands

#### `load`

Mount an e-reader, upload an EPUB document, and update an Org-mode file with the TOC. This can be useful to be synced to Orgzly so you can add notes on the different document chapters.

```bash
ebops load [OPTIONS] EPUB_PATH [MOUNT_POINT] [BOOKS_ORGMODE_PATH]
```

- `EPUB_PATH`: Path to the EPUB document to load.
- `MOUNT_POINT` (optional): Directory where the e-reader should be mounted. Defaults to `/tmp/ebook`.
- `BOOKS_ORGMODE_PATH` (optional): Path to the Org-mode file to update. Defaults to the environment variable `BOOKS_ORGMODE_PATH` if not provided.

#### `export_highlights`

Export highlights from an EPUB to an Org-mode file.

```bash
ebops export_highlights [OPTIONS] EPUB_PATH [MOUNT_POINT] [LEARN_ORGMODE_PATH]
```

- `EPUB_PATH`: Path to the EPUB file inside the mount point.
- `MOUNT_POINT` (optional): Mount point where the e-reader is connected. Defaults to `/tmp/ebook`.
- `LEARN_ORGMODE_PATH` (optional): Path to the Org-mode file to save highlights. Defaults to the environment variable `LEARN_ORGMODE_PATH` if not provided.

### Options

- `--version`: Show the version of the tool.
- `--verbose`, `-v`: Enable verbose logging.

## License

This project is licensed under the GNU General Public License v3.0 (GPLv3).

## Authors

- **Lyz**

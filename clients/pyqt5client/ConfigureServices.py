from services.service_provider import ServiceProvider
from services.htmlparsers.all import ParserBase64
from services.storage.all import SqliteStorage
# from services.storage.all import FilesystemStorage

sp = ServiceProvider()

with open("./services/storage/sql_init/sqlite.sql", "r") as f:
    init_script = f.read()
with open("./services/storage/sql_destroy/sqlite.sql", "r") as f:
    destroy_script = f.read()
STORAGE = SqliteStorage("./root.db", init_script, destroy_script)
# STORAGE = FilesystemStorage("./root", "./misc")

HTML_PARSER = ParserBase64()
for misc_file_name in STORAGE.get_all_misc_file_names():
    rawData = STORAGE.get_misc_file(misc_file_name).raw_data
    HTML_PARSER.add_file_mapping(misc_file_name, rawData)

sp.register("storage")(STORAGE)
sp.register("html_parser")(HTML_PARSER)

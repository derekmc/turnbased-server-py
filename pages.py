
def read_file(name):
    return open(name).read()

index_html = read_file("templates/index.html")
new_game_tmpl = read_file("templates/new_game.html")
docs_html = read_file("templates/docs.html")

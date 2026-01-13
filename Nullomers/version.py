import typer

app = typer.Typer()


@app.command()
def version():
    print("NullomerGenerator Version 0.5")
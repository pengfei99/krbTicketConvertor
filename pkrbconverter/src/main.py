import typer

from krb.convertor import convert_kirbi

app = typer.Typer()


@app.command()
def main(
    kirbi_path: str = typer.Argument(..., help="Path to the input .kirbi ticket file"),
    ccache_path: str = typer.Argument(..., help="Path for the output .ccache file"),
):
    # Convert a Kerberos .kirbi ticket to .ccache format.
    try:
        convert_kirbi(kirbi_path, ccache_path)
        typer.echo(f"[+] Success: {ccache_path}")
    except Exception as e:
        typer.echo(f"[-] Error: {e}")


if __name__ == "__main__":
    app()

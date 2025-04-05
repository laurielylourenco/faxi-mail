import click

from services.email_fetcher import count_emails_by_sender
from services.email_deleter import delete_emails_by_sender

@click.command()
@click.option("-a", "--analisar", is_flag=True, help="Analisar e contar e-mails por remetente")
@click.option("-d", "--deletar", help="Deletar e-mails de um remetente específico. Ex: -d 'email@teste.com'")


def main(analisar,deletar):
    
    
    if analisar:
        click.echo(click.style("🔍 Analisando e-mails por remetente...\n", fg="green"))
        senders_count = count_emails_by_sender()

        if not senders_count:
            click.echo("Nenhum e-mail encontrado.")
            return

        click.echo("📩 Quantidade de e-mails por remetente:\n")
        for sender, count in sorted(senders_count.items(), key=lambda x: x[1], reverse=True):
            print(f"✉️ {sender}: {count} e-mails")
        
    if deletar:
        email = deletar
        confirm = click.confirm(f"Tem certeza que deseja deletar e-mails de {email}?", default=False)
        if confirm:
            deleted_count = delete_emails_by_sender(email)
            click.echo(click.style(f"✅ {deleted_count} e-mails movidos para a lixeira.", fg="green"))
        else:
            click.echo("❌ Operação cancelada.")


if __name__ == "__main__":
    main()

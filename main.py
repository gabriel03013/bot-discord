import discord
from discord.ext import commands
import psycopg2
from psycopg2 import sql
from random import randint as rd
import datetime
from discord import SelectOption
import asyncio

adm = 614548307187990651 # Eu gabriel (gabbzn)

try:
    conexao = psycopg2.connect(database = "discord", host = 'pg-198bee84-discord-gb.d.aivencloud.com', user = 'avnadmin', password = 'AVNS_BPnCotxyGQ_PZW7nyV8', port = '14647')
    bd = conexao.cursor()
    bd.execute("SELECT current_database();") 

    print("Banco conectado:", bd.fetchone()[0])

except Exception as e:
    print("Erro ao conectar:", e)


permissoes = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=permissoes)
permissoes.bans = True  
permissoes.members = True

#LOJA
class OpcoesLoja(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Escolha um item para comprar!", custom_id='itens',
        options=[
            SelectOption(label="Capacete Melancia do Gato Melancia", value="1"),
            SelectOption(label="Cargo: Companheiro do Gato Melancia", value="2"),
            SelectOption(label="Adicionar um comando novo", value="3")
        ]
    )
    async def selecao_item(self, interaction: discord.Interaction, select: discord.ui.Select):
        opcao_escolhida = int(select.values[0])
        usuario = interaction.user.id

        bd.execute("SELECT melancias FROM usuarios_moedas WHERE nome = %s", (usuario,))
        saldo_disponivel = bd.fetchone()

        if saldo_disponivel is None:
            await interaction.response.send_message("Você ainda não tem melancias!", ephemeral=True)
            await asyncio.sleep(5)
            try:
                await interaction.delete_original_response()
            except discord.NotFound:
                pass
            return
        
        saldo_atual = saldo_disponivel[0]

        if opcao_escolhida == 1:
            valor = 20000
        elif opcao_escolhida == 2:
            valor = 20000
        elif opcao_escolhida == 3:
            valor = 5000
        else:
            await interaction.response.send_message("Opção inválida!", ephemeral=True)
            await asyncio.sleep(5)
            try:
                await interaction.delete_original_response()
            except discord.NotFound:
                pass
            return

        view_confirmacao = ConfirmarCompra(usuario, valor)
        await interaction.response.send_message(f"Você tem certeza que deseja comprar este item por {valor} melancias?", view=view_confirmacao, ephemeral=True)
        await asyncio.sleep(5)
        try:
            await interaction.delete_original_response()
        except discord.NotFound:
            pass

class ConfirmarCompra(discord.ui.View):
    def __init__(self, usuario, valor):
        super().__init__()
        self.usuario = usuario
        self.valor = valor

    @discord.ui.button(label="Confirmar", style=discord.ButtonStyle.green)
    async def botao_confirmar(self, interaction: discord.Interaction, button: discord.ui.Button):
        bd.execute("UPDATE usuarios_moedas SET melancias = melancias - %s WHERE nome = %s", (self.valor, self.usuario))
        conexao.commit()
        await interaction.response.send_message("Compra confirmada! Melancias debitadas.", ephemeral=True)
        await asyncio.sleep(5)
        try:
            await interaction.delete_original_response()
        except discord.NotFound:
            pass

    @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.red)
    async def botao_cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Compra cancelada.", ephemeral=True)
        await asyncio.sleep(5)
        try:
            await interaction.delete_original_response()
        except discord.NotFound:
            pass

@bot.command()
async def loja(ctx):
    view = OpcoesLoja()
    await ctx.send("Bem-vindo à loja! Escolha um item para comprar:", view=view)

@bot.command()
async def embed_loja(ctx):
    canal = bot.get_channel(1349151077873750066)

    if canal is None:
        await ctx.send("❌ Erro: Não consegui encontrar o canal! Verifique o ID.")
        return

    if not canal.permissions_for(ctx.guild.me).send_messages:
        await ctx.send("❌ Erro: Não tenho permissão para enviar mensagens nesse canal!")
        return

    if not canal.permissions_for(ctx.guild.me).attach_files:
        await ctx.send("❌ Erro: Não tenho permissão para enviar imagens nesse canal!")
        return

    embed_loja = discord.Embed(
        title="LOJA DO GATO MELANCIA !!!! 🍉🍉",
        description=(
            "Veja as opções e o que mais te agrada!\n"
            "  • Chapéu do Gato Melancia -> 20.000 melancias\n"
            "  • Cargo: Companheiro do Gato Melancia -> 20.000 melancias\n"
            "  • Adicionar um novo comando (falar com o Gabriel) -> 5.000 melancias\n"
            "  • Mais em breve..."
        ),
        color=discord.Color.green()
    )

    embed_loja.set_image(url="https://i.pinimg.com/736x/b3/32/bb/b332bbc48b87ef31e7b305574ae0f698.jpg")
    embed_loja.set_author(name="Gato Melancia", icon_url="https://i.pinimg.com/736x/b3/32/bb/b332bbc48b87ef31e7b305574ae0f698.jpg")

    await canal.send(embed=embed_loja)
    await ctx.send("✅ Embed enviado com sucesso!")
#

# EVENTOS DO BOT
async def on_ready():
    if not hasattr(bot, 'view_registered'):
        bot.add_view(OpcoesLoja())
        bot.view_registered = True
    print('o gato colocou a melancia')

@bot.event
async def on_member_join(membro: discord.Member):
    canal = bot.get_channel(1348020151521378426)
    imagem = discord.File('img/gato melancia.jpeg', filename='foto_gato_melancia.jpeg')

    boas_vindas_embed = discord.Embed(
        title=f"SEJA BEM-VINDO AO NOSSO SERVIDOR {membro.display_name} ! 👋",
        description=f"Se divirta! Nosso servidor é livre, faz o que quiser ae!\n{membro.mention}"
    )

    boas_vindas_embed.set_image(url="https://i.pinimg.com/originals/cc/bb/d8/ccbbd88195e19edd53fddaa2ad25ce50.gif")

    boas_vindas_embed.set_author(
        name=f"{membro.display_name}",
        icon_url=f'{membro.avatar}'
    )
    
    boas_vindas_embed.color = discord.Color.dark_purple()
    
    await canal.send(embed=boas_vindas_embed)

@bot.event
async def on_member_remove(member):
    canal = bot.get_channel(1348044970468049016)
    if canal:
        await canal.send(f'O usuário {member.mention} foi **expulso** ou saiu do servidor.')

@bot.event
async def on_member_ban(guild, user):
    canal = bot.get_channel(1348044970468049016)
    if canal:
        await canal.send(f'O usuário {user.mention} foi **banido**! Se fudeu')

# COMANDOS DO BOT
@bot.command()
async def gatomelancia(ctx):
    await ctx.reply('eu sou um gato melancia eu sou um gato melancia eu sou um gato melancia')

@bot.command()
async def devorar_cu(ctx, membro:discord.Member):
    await ctx.reply(f'EU VOU DEVORAR O BUMBUM DO {membro.mention} EU VOU SIM')

@bot.command()
async def felipetraido(ctx:commands.Context, vezes:int):
    nome = ctx.author.mention
    for i in range(1, vezes + 1):
        await ctx.send(f'o Felipe foi traído {i} vezes hoje, {nome}.')  

@bot.command()
async def regras(ctx):
    canal = bot.get_channel(1337950420026265701)
    regras_embed = discord.Embed(
        title='📋 Regras !',
        description='O servidor é de todo mundo e todo mundo faz o que quiser, des de canais, calls, bots até adicionar pessoas, contanto que elas sejam legais.\n\nSiga o conselho do Gato Melancia !'
    )

    await canal.send(embed=regras_embed)

@bot.command()
async def membros(ctx):
    await ctx.reply(f'{ctx.guild.member_count} membros.')

@bot.command()
async def deletar_mensagens(ctx: commands.Context, quantidade: int):
    await ctx.channel.purge(limit=quantidade)
    await ctx.send(f'O Gato Melancia devorou {quantidade} mensagens desse canal!', delete_after=0.1)

@bot.command()
async def daily(ctx):
    nome = ctx.author.id
    melancias_diaria = rd(700, 1200)
    data_atual = datetime.date.today()

    bd.execute("SELECT melancias FROM usuarios_moedas WHERE nome = %s", (nome,))
    existe_saldo = bd.fetchone()

    bd.execute("SELECT ultima_recompensa FROM usuarios_moedas WHERE nome = %s", (nome,))
    ultima_recompensa = bd.fetchone()

    if existe_saldo:
        if ultima_recompensa[0] != data_atual:
            novo_saldo_melancias = existe_saldo[0] + melancias_diaria
            bd.execute("UPDATE usuarios_moedas SET melancias = %s WHERE nome = %s", (novo_saldo_melancias, nome))
            bd.execute("UPDATE usuarios_moedas SET ultima_recompensa = %s WHERE nome = %s", (data_atual, nome,))

            await ctx.reply(f'Parabéns! Você recebeu {melancias_diaria} melancias! Seu saldo atual é de {novo_saldo_melancias} melancias.')
            conexao.commit()
        elif ultima_recompensa[0] == data_atual:
            await ctx.reply("Você já pegou as melancias de hoje! Volte amanhã!")
    else:
        novo_saldo_melancias = melancias_diaria
        bd.execute("INSERT INTO usuarios_moedas (nome, melancias, ultima_recompensa) VALUES (%s, %s, %s)", (nome, novo_saldo_melancias, data_atual))
        await ctx.reply(f'Parabéns! Você recebeu {melancias_diaria} melancias e foi registrado no sistema! Seu saldo atual é de {novo_saldo_melancias} melancias.')
    conexao.commit()

@bot.command()
async def saldo(ctx):
    nome = ctx.author.id
    bd.execute("SELECT melancias FROM usuarios_moedas WHERE nome = %s", (nome,))
    saldo = bd.fetchone()

    if saldo:
        await ctx.reply(f'Seu saldo total é de: {saldo[0]} melancias.')
    else:
        await ctx.reply("Você ainda não tem melancias registradas.")

@bot.command()
async def adm_alterar(ctx, usuario: discord.User, novo_saldo: int):
    adm = 614548307187990651
    autor_msg = ctx.author.id
    bd.execute("SELECT melancias FROM usuarios_moedas WHERE nome = %s", (usuario.id,))
    existe = bd.fetchone()
    if existe:
        if autor_msg != adm:
            await ctx.reply('Você não pode usar esse comando seu merda')
        else:
            bd.execute("UPDATE usuarios_moedas SET melancias = %s WHERE nome = %s", (novo_saldo, usuario.id))
        conexao.commit()
    else:
        await ctx.reply("O usuário não está registrado no sistema.")

    await ctx.reply(f'O saldo do Usuário {usuario} foi atualizado para {novo_saldo} melancias.')

@bot.command()
async def consultar_id(ctx, usuario: discord.User):
    id_usuario = usuario.id
    await ctx.reply(f"O ID do usuário é: {id_usuario}")

@bot.command()
async def consultar_saldo(ctx, usuario: discord.User):
    bd.execute("SELECT melancias FROM usuarios_moedas WHERE nome = %s", (usuario.id,))
    existe = bd.fetchone()
    if existe:
        bd.execute("SELECT melancias FROM usuarios_moedas WHERE nome = %s", (usuario.id,))
        saldo = bd.fetchone()
        await ctx.reply(f"O saldo do usuário é de {saldo[0]} melancias.")
    else:
        await ctx.reply("O usuário ainda não tem nenhuma melancia 😓 e não está no sistema.")
    
@bot.command()
async def depositar(ctx, usuario:discord.Member, deposito:int):
    bd.execute("SELECT melancias FROM usuarios_moedas WHERE nome = %s", (usuario.id,))
    existe = bd.fetchone()
    depositante = ctx.author.id
    if existe:
        if depositante != usuario.id:
            bd.execute("SELECT melancias FROM usuarios_moedas WHERE nome = %s", (depositante,))
            saldo_depositante = bd.fetchone()
            if saldo_depositante[0] > deposito:
                bd.execute("SELECT melancias FROM usuarios_moedas WHERE nome = %s", (usuario.id,))
                saldo_usuario = bd.fetchone()
                novo_saldo_usuario = saldo_usuario[0] + deposito
                bd.execute("UPDATE usuarios_moedas SET melancias = %s WHERE nome = %s", (novo_saldo_usuario, usuario.id))

                novo_saldo_depositante = saldo_depositante[0] - deposito
                bd.execute("UPDATE usuarios_moedas SET melancias = %s WHERE nome = %s", (novo_saldo_depositante, depositante ))
                
                await ctx.reply(f"Você fez um depósito de {deposito} melancias para {usuario.mention}.")
                conexao.commit()
            else:
                await ctx.reply(f"Você não tem melancias suficiente para fazer esse depósito seu merda.")
        else:
            await ctx.reply(f"Você não pode depositar para si mesmo.")
    else:
        await ctx.reply(f"O usuário não está registrado no sistema.")
bot.run('MTM0Nzk4MjY2MjE5MDQ5NzkzNA.GFS8us.ZTWUrBaH8vuFdEUACKYeohGBS95cUjnag1cIbs')
import discord
from discord.ext import tasks, commands
import asyncio
import random
import pickle
import json
import os

every_single_word = ""
with open("./liste_francais.txt", "r") as f:
    every_single_word = f.read().lower().split("\n")


def is_in_every_single_word(word):
    return word.lower() in every_single_word


def are_the_same(word1, word2):
    return abs(len(word1) - len(word2)) < 4 and (word1.lower() in word2.lower() or word2.lower() in word1.lower())


def file_exist(filename):
    result = True
    try:
        f = open("./dict/dictionary_" + filename)
    except IOError:
        result = False
    else:
        f.close()
    return result


class Undercover(commands.Cog):

    def __init__(self, client, emojis, guild, category):
        self.client = client
        self.parties = dict()
        self.emojis = emojis
        self.players = set()
        self.guild_uc2 = guild
        self.category = category
        print("Undercover cog loaded")
        self.change_status.start()

    def cog_unload(self):
        self.parties.clear()
        self.change_status.cancel()
        print("Undercover cog unloaded.")

    @tasks.loop(seconds=5.0)
    async def change_status(self):
        await self.client.wait_until_ready()
        if len(self.parties.keys()) > 0:
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game("Undercover^2, " + str(len(self.parties.keys())) + " partie(s) en cours"))
        else:
            await self.client.change_presence(status=discord.Status.dnd, activity=discord.Game("Undercover^2"))

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):

        print("yop")

        if user == self.client.user:
            print("line 40")
            return

        for party in self.parties.keys():

            if self.parties[party]["Message"] is None:
                print("line 46")
                continue
            else:
                print("line 49")
                msg_vote = self.parties[party]["Message"]

            if reaction.message.id != msg_vote.id:
                print("line 53")
                continue

            if self.parties[party]["Actual players"] is not None:
                print("line 57")

                if str(user.id) not in self.parties[party]["Actual players"].keys():
                    print("line 60")
                    await reaction.remove(user)
                elif self.parties[party]["Actual players"][str(user.id)]["Vote"] is not None:
                    self.parties[party]["Actual players"][str(user.id)]["Vote"] = None
                """elif str(reaction.emoji) not in [str(self.parties[party]["Actual players"][player]["Emoji"]) for player in self.parties[party]["Actual players"].keys()]:
                    print("line 63")
                    await reaction.remove(user)
                elif self.parties[party]["Actual players"][str(user.id)]["Vote"] is None:
                    print("line 66")
                    await reaction.remove(user)
                    self.parties[party]["Actual players"][str(user.id)]["Vote"] = str(reaction.emoji)"""

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        print("yop")

        if user == self.client.user:
            print("line 40")
            return

        for party in self.parties.keys():

            if self.parties[party]["Message"] is None:
                print("line 46")
                continue
            else:
                print("line 49")
                msg_vote = self.parties[party]["Message"]

            if reaction.message.id != msg_vote.id:
                print("line 53")
                continue

            if self.parties[party]["Actual players"] is not None:
                print("line 57")

                if str(user.id) not in self.parties[party]["Actual players"].keys():
                    print("line 60")
                    await reaction.remove(user)
                elif str(reaction.emoji) not in [str(self.parties[party]["Actual players"][player]["Emoji"]) for player in self.parties[party]["Actual players"].keys()]:
                    print("line 63")
                    await reaction.remove(user)
                elif self.parties[party]["Actual players"][str(user.id)]["Can Vote"] is False:
                    await reaction.remove(user)
                elif self.parties[party]["Actual players"][str(user.id)]["Vote"] is None:
                    print("line 66")
                    self.parties[party]["Actual players"][str(user.id)]["Vote"] = str(reaction.emoji)
                else:
                    print("line 69")
                    await reaction.message.remove_reaction(self.parties[party]["Actual players"][str(user.id)]["Vote"], user)
                    self.parties[party]["Actual players"][str(user.id)]["Vote"] = str(reaction.emoji)

    @commands.command()
    async def link(self, ctx):
        await ctx.author.create_dm()
        if ctx.guild is not None:
            await ctx.send(str(ctx.author.mention) + ", je vous ai envoyé le lien en privé.")
            await ctx.author.dm_channel.send("Vous pouvez m'inviter sur votre serveur en suivant ce lien : https://discord.com/api/oauth2/authorize?client_id=746823712820559912&permissions=2048&scope=bot \n\n*Cliquez ici pour revenir dans le salon textuel où vous étiez : " + str(ctx.channel.mention) + "*")
        else:
            await ctx.author.dm_channel.send("Vous pouvez m'inviter sur votre serveur en suivant ce lien : https://discord.com/api/oauth2/authorize?client_id=746823712820559912&permissions=2048&scope=bot")

    """@commands.command()
    @commands.is_owner()
    async def icon(self, ctx):
        try:
            guild_icon_url = ctx.guild.icon_url
            b = await (ctx.guild.icon_url_as(static_format='jpg', size=4096)).read()
            await self.client.user.edit(avatar=b)
            await ctx.send("L'icône du bot est maintenant celui de ce serveur : " + guild_icon_url)
        except Exception:
            await ctx.send("Ce serveur n'a pas d'icône.")"""

    @commands.command(aliases=["règles", "regles"])
    async def rules(self, ctx):
        await ctx.author.create_dm()
        await ctx.author.dm_channel.send("L'\"Undercover^2\" est une recréation du jeu original \"Undercover^^\" créé par Yanstar Studio OU et disponible sur les smartphones et tablettes Android et Apple.\n\nLe jeu se base sur un set de paires de mots se ressemblant *(ex: Loup <> Chien, Abeille <> Frelon)*. De ce fait, il est impossible de créer tout seul un set rempli d'assez de mots pour pour jouer pendant plusieurs parties. Ainsi, il est possible d'en créer un ou d'en reprendre un (le dictionnaire sera demandé en début de session). Pour en créer un il faut que chaque joueur donne un mot assez vague qui permet de lui associer d'autres mots *(ex : Loup ==> Chien, Renard, Fennec, etc...)*. Après que chaque joueur est mis un mot dit \"principal\", chaque joueur sera invité a mettre un mot ressemblant pour chacun des mots pincipaux. Je répète, pour que le jeu fonctionne il faut que les mots aient des descriptions se ressemblant *(ex: un Loup et un Chien ont de la fourure, une queue, etc... Mais l'un est sauvage et l'autre non (enfin pas forcément mais vous avez compris, il y a une petit différence entre leurs descriptions!))*\n\nA partir de ces mots il est possible de jouer.")
        await ctx.author.dm_channel.send("Ainsi nous pouvons enfin parler du jeu :\n\n\tIl existe 3 types de joueur dans ce jeu :\n\nChaque joueur ne connais pas son rôle au début de paprtir (à part le white player)\n\n\t\t**Les citoyens :** ils ont tous le même mot et doivent coopérer ensemble pour gagner face à l'undercover et le white player.\n\n\t\t**L'undercover :** il a un mot différent des citoyens et doit rapidement comprendre si il est l'undercover et quel est le mot des citoyens pour pouvoir se faire passer comme un citoyen et pouvoir gagner sans que les joueurs ne pensent que ça soit un undercover.\n\n\t\t**Le white player :** il n'a pas de mot! Il doit se débrouiller pour connaître le mot des citoyens et pouvoir se faire passer pour un des leurs. Si il se fait éliminer il peut gagner si il dit le mot des citoyens (il devra envoyer le mot en privé au bot).\n\nAvant que la partie commence chaque joueur reçoit son mot/rôle en privé, mais la partie s'organise sur le salon textuel où la partie a été lancé.\n\nLe jeu s'organise en round chronométré (moins il ya de joueur en jeu, moins il y a du temps!), à chaque round chaque joueurs doivent donner un mot en rapport avec le mot qu'ils ont, le white player doit être attentif au mot que les autres joueurs laissent passer pour comprendre le mot des citoyens. Au début de partie un joueur est élu pour commencer le tour, en suite les joueurs doivent suivre l'ordre de la liste de joueurs. *(ex : Joueur A commence ! Liste : Joueur C puis Joueur B puis Joueur A puis Joueur D, après le joueur A c'est au tour du joueur D)*. Au cours d'un round les joueurs peuvent voter pour le joueur qu'ils souhaitent éliminer (avec des réactions), lorsque le temps s'est écoulé les joueurs n'ayant pas voté sont invité à voter définitivement pour un joueur.")
        await ctx.author.dm_channel.send("**N'hésitez pas à débattre entre vous pour voter, *mais* méfiez-vous des faux amis...**\n\nPour lancer une partie faites **U^**start *[liste de joueur mentionné par un @]* , amusez-vous bien!")
        if ctx.guild is not None:
            await ctx.author.dm_channel.send("~~~~~~~~~~~~~~~~~~~~\n\n*Cliquez ici pour revenir dans le salon textuel où vous étiez : " + str(ctx.channel.mention) + "*")
            await ctx.send(str(ctx.author.mention) + ", je vous ai envoyé les règles en privé!")

    @commands.command()
    @commands.guild_only()
    async def start(self, ctx, *args: discord.User):

        creator = str(ctx.author.id)
        if creator in self.players:
            await ctx.send("Tu es déjà en jeu !")
            return
        players_list = {str(player.id) for player in args if not player.bot}

        nb_base_players = len(players_list) + 1
        if nb_base_players < 4:
            await ctx.send("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nImpossible de lancer une partie, vous n'êtes pas assez nombreux (Nombre : " + int(nb_base_players) + "). (4 minimum)")
            return

        are_already_playing = False
        msg_player_playing = "Ce(s) joueur(s) est/sont déjà entrain de jouer :\n"
        for player in players_list:

            if player in self.players:
                players_list.remove(player)
                are_already_playing = True
                msg_player_playing += "\t" + (self.client.get_user(int(player))).name + "\n"

        if are_already_playing:
            await ctx.send(msg_player_playing)

        nb_base_players = len(players_list) + 1
        if nb_base_players < 4:
            await ctx.send("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nImpossible de lancer une partie, vous n'êtes pas assez nombreux (Nombre : " + str(nb_base_players) + "). (4 minimum)")
            return

        wont_play = set()

        async def dm_will_play(player):
            player_id = int(player)
            player_user = self.client.get_user(player_id)

            msg_will_play = None
            msg_cant_send = None
            times_tried = 0
            while times_tried < 5:
                try:
                    await player_user.create_dm()
                    msg_will_play = await player_user.dm_channel.send("Voulez-vous jouer ? (Vous avez 60 secondes pour répondre)")
                    await msg_will_play.add_reaction("👍")
                    await msg_will_play.add_reaction("👎")
                    break
                except Exception:
                    times_tried += 1
                    if times_tried != 5:
                        msg_cant_send = await ctx.send(player_user.mention + " je ne peux pas vous contacter, veuillez m'envoyer un message.\nNouvelle tentative dans 5 secondes... (Tentative " + str(times_tried + 1) + "/5)")
                    else:
                        msg_cant_send = await ctx.send(player_user.mention + " je ne peux pas vous contacter. Tentative 5/5, c'était la dernière tentative.")
                    asyncio.wait(5)
                    await msg_cant_send.delete()

            if msg_will_play is not None:

                def check(reaction, user):
                    return reaction.message.id == msg_will_play.id and str(reaction.emoji) in ("👍", "👎") and user == player_user

                try:
                    reaction_will_play, user_will_play = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                    if str(reaction_will_play.emoji) == "👎":
                        wont_play.add(player)
                    await player_user.dm_channel.send("Merci pour la réponse !")
                except asyncio.TimeoutError:
                    wont_play.add(player)
                    await msg_will_play.delete()
                    await player_user.dm_channel.send(str(ctx.author.mention) + " a essayé de lancer une partie avec vous.")

            else:
                wont_play.add(player)

        await asyncio.wait([dm_will_play(str(player)) for player in players_list])

        if len(wont_play) > 0:
            msg_player_wont_play = "Ce(s) joueur(s) n'a/ont pas accepté de jouer :\n"
            for player in wont_play:
                players_list.remove(player)
                msg_player_wont_play += "\t" + (self.client.get_user(int(player))).name + "\n"

            await ctx.send(msg_player_wont_play)

        players_list.add(creator)

        nb_base_players = len(players_list)
        players_list = list(players_list)

        if nb_base_players < 4:
            await ctx.send("Impossible de lancer une partie, vous n'êtes pas assez nombreux (Nombre : " + str(nb_base_players) + "). (4 minimum)")
            return

        self.players.union(set(players_list))

        party_no = str(len(self.parties) + 1)

        self.parties[party_no] = dict()

        dictionary = dict()
        base_players = dict()

        party_channel = await self.guild_uc2.create_text_channel(category=self.category, name=ctx.author.name)
        party_channel_invite = await party_channel.create_invite()

        to_delete = []
        to_kick = []
        to_remove_invite = []

        async def invite_player(player):
            invite_player_user = self.client.get_user(int(player))
            await invite_player_user.create_dm()
            invite_player_msg = await invite_player_user.send("Veuillez rejoindre la partie en suivant ce lien : \n" + str(party_channel_invite))

            if self.guild_uc2.get_member(int(player)) is None:

                def check_if_join(member):
                    if str(member.id) not in [str(player_var) for player_var in players_list]:
                        to_kick.append(member)
                    return member == invite_player_user

                new_member = await self.client.wait_for('member_join', check=check_if_join)
                """while new_member != invite_player_user:
                    await self.guild_uc2.kick(new_member, reason="Vous n'appartenez pas à cette partie.")
                    new_member = await self.client.wait_for('member_join', check=check_if_join)"""

                await invite_player_msg.delete()

            else:
                to_remove_invite.append(invite_player_msg)

            await party_channel.set_permissions(invite_player_user, read_messages=True, read_message_history=True)
            to_delete.append(await party_channel.send(invite_player_user.mention + " est arrivé!"))

        await asyncio.wait([invite_player(str(player_var)) for player_var in players_list])

        for player in to_kick:
            await self.guild_uc2.kick(player, reason="Vous n'appartenez pas à cette partie.")

        for invite_msg in to_remove_invite:
            await invite_msg.delete()

        await party_channel_invite.delete()

        to_delete.append(await party_channel.send("Tout le monde est connecté !\nNettoyage du salon..."))
        await asyncio.sleep(5)
        for message in to_delete:
            await message.delete()

        party = self.parties[party_no]

        party["Creator"] = creator
        party["Players"] = base_players
        party["Actual players"] = None
        party["Players No"] = nb_base_players
        party["Dictionary"] = dictionary
        party["Message"] = None
        party["Channel"] = party_channel

        pass_save = True

        for player in players_list:
            base_players[str(player)] = {"Word": ""}

        await ctx.author.create_dm()
        msg_save = await ctx.author.dm_channel.send("Utiliser un dictionnaire de mot ?")
        await msg_save.add_reaction("👍")
        await msg_save.add_reaction("👎")
        """await asyncio.wait([msg_save.add_reaction(emoji) for emoji in ("👎", "👍")])"""

        def check_pass_save(reaction, user):
            print(str(reaction.emoji) in ("👍", "👎") and user == ctx.author and reaction.message.id == msg_save.id)
            return str(reaction.emoji) in ("👍", "👎") and user == ctx.author and reaction.message.id == msg_save.id

        reaction_ask, user_reaction_ask = await self.client.wait_for('reaction_add', check=check_pass_save)

        if str(reaction_ask.emoji) == "👍":
            msg_ask_dict_content = "\n".join(["::\t" + dict_name[11:] for dict_name in os.listdir("./dict")])
            msg_ask_dict = await ctx.author.dm_channel.send(msg_ask_dict_content + "\nQuel dictionnaire voulez-vous utiliser ? (N = abandon)")

            def check_dict(message):
                return message.author == ctx.author and message.channel == msg_ask_dict.channel

            save_dict = (await self.client.wait_for('message', check=check_dict)).content
            pass_save = False
            if save_dict == "N":
                pass_save = True
            while file_exist(save_dict) is False and pass_save is False:
                await ctx.author.dm_channel.send("Ce dictionnaire n'existe pas !\nDonnez un nom de dictionnaire existant : ")
                save_dict = (await self.client.wait_for('message', check=check_dict)).content
                if save_dict == "N":
                    pass_save = True

            if pass_save is False:
                with open("./dict/dictionary_" + save_dict, 'rb') as file:
                    dictionary = pickle.load(file)

        if pass_save is True:

            async def dm_word1(player):
                player_id = player
                player_user = self.client.get_user(int(player_id))
                base_players[str(player_id)] = {"Word": ""}

                while True:
                    try:
                        await player_user.create_dm()
                        await player_user.dm_channel.send("Entrez un mot :")
                        break
                    except Exception:
                        await ctx.send(player_user.mention + " je ne peux pas vous contacter, veuillez m'envoyer un message.\nNouvelle tentative dans 5 secondes...")
                        asyncio.wait(5)

                def check(word):
                    return word.channel == player_user.dm_channel and word.author == player_user

                word = (await self.client.wait_for('message', check=check)).content
                while word in dictionary.keys() or not is_in_every_single_word(word):
                    if word in dictionary.keys():
                        await player_user.dm_channel.send("Mot déjà mis. Donnez un autre mot :")
                    else:
                        await player_user.dm_channel.send("Ce mot n'existe pas. Donnez un mot existant :")
                    word = (await self.client.wait_for('message', check=check)).content

                dictionary[word] = set()

                await player_user.dm_channel.send("Merci !")

            await asyncio.wait([dm_word1(player) for player in players_list])

            to_remove = set()
            for word in dictionary.keys():

                test_set = set(dictionary.keys())
                test_set.remove(word)

                for another_word in test_set:
                    word_to_remove = None

                    if are_the_same(word, another_word):
                        word_to_remove = word

                        if another_word > word_to_remove:
                            word_to_remove = another_word

                    if word_to_remove is not None:
                        to_remove.add(word_to_remove)

            for word in to_remove:
                dictionary.pop(word)

            """for player in players_list:
                player_id = player.id
                player_user = self.client.get_user(int(player_id))
                base_players[str(player_id)] = {"Word": ""}

                while True:
                    try:
                        await player_user.dm_channel.send("Entrez un mot :")
                        break
                    except:
                        await ctx.send(player_user.mention + " je ne peux pas vous contacter, veuillez m'envoyer un message.\nNouvelle tentative dans 5 secondes...")
                        asyncio.wait(5)

                def check(word):
                    return word.channel == player_user.dm_channel

                word = await self.client.wait_for('message', check=check)
                while word in dictionary.keys():
                    await player_user.dm_channel.send("Mot déjà mis. Donnez un autre mot :")
                    word = await self.client.wait_for('message', check=check)

                dictionary[word] = set()

                await player_user.dm_channel.send("Merci !")"""

            players_with_words = []
            for word in dictionary.keys():

                temp_list = []

                for player in base_players.keys():

                    temp_list.append((player, word))

                players_with_words.append(list(temp_list))

            async def dm_word2(word_and_player):

                player_user = self.client.get_user(int(word_and_player[0]))

                await player_user.dm_channel.send("A ton tour !\nDonnez un mot presque en rapport avec le mot __**\"" + word_and_player[1] + "\"**__ : ")

                def check(word):
                    return word.channel == player_user.dm_channel and word.author == player_user

                new_word = (await self.client.wait_for('message', check=check)).content
                while new_word in dictionary.keys() or not is_in_every_single_word(new_word):
                    if new_word not in dictionary.keys():
                        await player_user.dm_channel.send("Ce mot n'existe pas.\nDonnez un mot presque en rapport avec le mot __**\"" + word_and_player[1] + "\"**__ : ")
                    else:
                        await player_user.dm_channel.send("Mot déjà mis dans les mots principaux.\nDonnez un autre mot presque en rapport avec le mot __**\"" + word_and_player[1] + "\"**__ : ")
                    new_word = (await self.client.wait_for('message', check=check)).content

                dictionary[word_and_player[1]].add(new_word)

            to_remove_from_dictionary = dict()
            for word_and_player in temp_list:
                to_remove_from_dictionary[word_and_player[1]] = set()

                for word in dictionary[word_and_player[1]]:
                    test_set = set(dictionary[word_and_player[1]])
                    test_set.remove(word)

                    for another_word in test_set:
                        word_to_remove = None

                        if are_the_same(word, another_word):
                            word_to_remove = word

                            if another_word > word_to_remove:
                                word_to_remove = another_word

                        if word_to_remove is not None:
                            to_remove_from_dictionary[word_and_player[1]].add(word_to_remove)

                dictionary[word_and_player[1]] = dictionary[word_and_player[1]] - to_remove_from_dictionary[word_and_player[1]]

            for temp_list in players_with_words:
                await asyncio.wait([dm_word2(word_and_player) for word_and_player in temp_list])

            """for word_and_player in players_with_words:

                player = await self.client.get_user(int(word_and_player[0]))

                await player.dm_channel.send("A ton tour !\nDonnez un mot presque en rapport avec le mot \"" + word_and_player[1] + "\" : ")

                def check(word):
                    return word.channel == player_user.dm_channel

                new_word = await self.client.wait_for('message', check=check)
                while word in dictionary.keys():
                    await player_user.dm_channel.send("Mot déjà mis dans les mots principaux.\nDonnez un autre mot presque en rapport avec le mot \"" + word_and_player[1] + "\" : ")
                    new_word = await self.client.wait_for('message', check=check)

                dictionary[word_and_player[1]].add(new_word)"""

            await ctx.author.create_dm()
            msg_name_dict = await ctx.author.dm_channel.send("Donner un nom au dictionnaire ?")
            await msg_name_dict.add_reaction("👍")
            await msg_name_dict.add_reaction("👎")

            def check_name_dict(reaction, user):
                print(str(reaction.emoji) in ("👍", "👎") and user == ctx.author and reaction.message.id == msg_name_dict.id)
                return str(reaction.emoji) in ("👍", "👎") and user == ctx.author and reaction.message.id == msg_name_dict.id

            reaction_name_dict, user_reaction_name_dict = await self.client.wait_for('reaction_add', check=check_name_dict)

            if str(reaction_name_dict.emoji) == "👍":
                msg_name_dict_ask = await ctx.author.dm_channel.send("Comment voulez-vous nommer votre dictionnaire ? (N = abandon)")

                def check_dict_name(message):
                    return message.author == ctx.author and message.channel == msg_name_dict_ask.channel

                dict_name = (await self.client.wait_for('message', check=check_dict_name)).content
                pass_name = False
                if dict_name == "N":
                    pass_name = True
                while file_exist(dict_name) is True and pass_name is False:
                    await ctx.author.dm_channel.send("Ce dictionnaire existe déjà !\nDonnez un nom de dictionnaire valide : ")
                    dict_name = (await self.client.wait_for('message', check=check_dict_name)).content

                    if dict_name == "N":
                        pass_name = True

                if pass_name:
                    dict_no = 1
                    while file_exist(str(dict_no)):
                        dict_no += 1
                    with open("./dict/dictionary_" + str(dict_no), 'wb') as file:
                        pickle.dump(dictionary, file)
                    await ctx.author.dm_channel.send("Dictionnaire enregistré.\nNom : dict" + str(dict_no) + "\n\n*Cliquez ici pour revenir dans le salon textuel de la partie : " + ctx.channel.mention + "*")
                else:
                    with open("./dict/dictionary_" + str("".join(c for c in dict_name if c.isalnum())), 'wb') as file:
                        pickle.dump(dictionary, file)

                    await ctx.author.dm_channel.send("Dictionnaire enregistré.\nNom : " + str("".join(c for c in dict_name if c.isalnum())) + "\n\n*Cliquez ici pour revenir dans le salon textuel de la partie : " + ctx.channel.mention + "*")

            else:
                dict_no = 1
                while file_exist(str(dict_no)):
                    dict_no += 1
                with open("./dict/dictionary_" + str(dict_no), 'wb') as file:
                    pickle.dump(dictionary, file)
                await ctx.author.dm_channel.send("Dictionnaire enregistré.\nNom : dict" + str(dict_no) + "\n\n*Cliquez ici pour revenir dans le salon textuel de la partie : " + ctx.channel.mention + "*")

        wanna_play = True

        actual_emojis = list(self.emojis)
        for player in base_players.keys():
            base_players[player]["Vote"] = None
            base_players[player]["Can Vote"] = True
            base_players[player]["Emoji"] = actual_emojis.pop(random.randint(0, len(actual_emojis)))

        while wanna_play:

            players = dict(base_players)
            party["Actual players"] = players
            party["Already said"] = set()

            play = True
            round = 0

            list_players_random = list(players.keys())
            random.shuffle(list_players_random)

            key_words = list(dictionary[random.choice(list(dictionary.keys()))])

            while len(key_words) < 2:
                key_words = list(dictionary[random.choice(list(dictionary.keys()))])

            citizen_word = random.choice(key_words)
            key_words.remove(citizen_word)
            undercover_word = random.choice(key_words)

            print(list(players.keys()))

            white_player = random.choice(list_players_random)
            print("white_player = " + white_player)

            undercover = random.choice(list_players_random)
            while undercover == white_player:
                undercover = random.choice(list_players_random)

            print("undercover = " + undercover)

            players_random = list(players.keys())
            random.shuffle(players_random)
            for player in players_random:

                if player != undercover and player != white_player:
                    players[player]["Word"] = citizen_word
                    print("\n" + player)

            players[undercover]["Word"] = undercover_word
            undercover_user = self.client.get_user(int(undercover))
            white_player_user = self.client.get_user(int(white_player))

            await party_channel.send("C'est parti . . . \n" + self.client.user.mention)

            async def dm_game_word(player):
                player_user = self.client.get_user(int(player))
                print(str(player_user))

                await player_user.create_dm()

                if player == white_player:
                    await player_user.dm_channel.send("**Tu n'as pas de mot! Good luck!**\n*Cliquez ici pour revenir en jeu : " + party_channel.mention + "*")
                else:
                    await player_user.dm_channel.send("Ton mot est : __**" + players[player]["Word"] + "**__\n*Cliquez ici pour revenir en jeu : " + party_channel.mention + "*")

            await asyncio.wait([dm_game_word(player) for player in players.keys()])

            """for player in players.keys():

                player_user = await self.client.get_user(int(player))

                if player == white_player:
                    await player_user.dm_channel.send("Tu n'as pas de mot! Good luck!")
                    clear()
                    continue
                await player_user.dm_channel.send("Ton mot est : " + players[player]["Word"])"""

            msg_before_game = await party_channel.send(str(5) + " .." + "." * int(1 ** 0.9))
            async with ctx.typing():
                for i in range(4, 0, -1):
                    await msg_before_game.edit(content=(str(i) + " .." + "." * int((6 - i) ** 0.9)))
                    await asyncio.sleep((6 - i) ** 0.5)
                await msg_before_game.edit(content="Let's go!")
                await asyncio.sleep(1)

            begin = random.choice(list(players_random))
            while begin == white_player:
                begin = random.choice(list(players_random))

            begin = self.client.get_user(int(begin))

            await msg_before_game.edit(content=(begin.mention + " commence !"))

            await asyncio.sleep(1)

            while play:
                round += 1

                print(self.parties)

                msg_vote = None
                time_players_no = 30
                list_players_in_order = list(players.keys())

                print(list_players_in_order)

                for player in range(len(list_players_in_order)):

                    if self.client.get_user(int(list_players_in_order[player])) == begin:
                        print(str(list_players_in_order[player]))
                        list_players_in_order = list_players_in_order[player:len(list_players_in_order)] + list_players_in_order[0:player]
                        print(list_players_in_order)
                        break

                msg_play_to_send_content = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n|\tTour n°" + str(round) + "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nVous avez " + str(time_players_no) + " secondes chacun pour dire un mot en rapport avec le votre, vous passez tour par tour dans cette ordre :\n"
                for player in list_players_in_order:

                    msg_play_to_send_content += "\t" + (self.client.get_user(int(player))).mention + "\n"

                msg_play_to_send_content += "**Si vous ne dites rien au bout de " + str(time_players_no) + " secondes, vous n'aurez pas le droit de voter par la suite!**"
                msg_play = await party_channel.send(msg_play_to_send_content)

                for player in list_players_in_order:

                    players[str(player)]["Can Vote"] = True

                    player_play_user = self.client.get_user(int(player))
                    msg_player_play_content = "Au tour de " + player_play_user.mention
                    msg_player_play = await party_channel.send(msg_player_play_content + ", tu as 30 secondes...")

                    async def player_play_waiting(player):

                        await party_channel.set_permissions(player_play_user, send_messages=True, read_messages=True, read_message_history=True)

                        async def player_play_countdown():
                            await asyncio.sleep(10)
                            await msg_player_play.edit(content=(msg_player_play_content + ", il te reste 20 secondes..."))
                            await asyncio.sleep(10)
                            await msg_player_play.edit(content=(msg_player_play_content + ", il te reste 10 secondes..."))
                            await asyncio.sleep(5)
                            await msg_player_play.edit(content=(msg_player_play_content + ", il te reste 5 secondes..."))
                            await asyncio.sleep(1)
                            await msg_player_play.edit(content=(msg_player_play_content + ", il te reste 4 secondes..."))
                            await asyncio.sleep(1)
                            await msg_player_play.edit(content=(msg_player_play_content + ", il te reste 3 secondes..."))
                            await asyncio.sleep(1)
                            await msg_player_play.edit(content=(msg_player_play_content + ", il te reste 2 secondes..."))
                            await asyncio.sleep(1)
                            await msg_player_play.edit(content=(msg_player_play_content + ", il te reste 1 seconde..."))
                            await asyncio.sleep(1)
                            return False

                        async def wait_for_player_play(player):
                            answer_word = await self.client.wait_for('message')
                            print("yup")
                            while not (answer_word.author.id == player_play_user.id and answer_word.channel.id == party_channel.id and is_in_every_single_word(answer_word.content) and answer_word.content not in party["Already said"]):
                                print("ptdrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
                                if answer_word.content in party["Already said"]:
                                    task_delete = asyncio.create_task(answer_word.delete())
                                    task_send = asyncio.create_task(party_channel.send(content="Ce mot a déjà été donné.", delete_after=5.0))
                                    await asyncio.wait([task_delete, task_send])
                                elif not is_in_every_single_word(answer_word.content):
                                    task_delete = asyncio.create_task(answer_word.delete())
                                    task_send = asyncio.create_task(party_channel.send(content="Ce mot n'existe pas.", delete_after=5.0))
                                    await asyncio.wait([task_delete, task_send])
                                answer_word = await self.client.wait_for('message')
                            party["Already said"].add(answer_word.content)
                            return True
                            """async def check_player_play(message):
                                if not (message.author.id == player_play_user.id and message.channel.id == party_channel.id and not is_in_every_single_word(message.content)):
                                    await asyncio.wait(message.delete(), party_channel.send(content="Ce mot n'existe pas.", delete_after=5.0))
                                    return False
                                print(message.author.id == player_play_user.id and message.channel.id == party_channel.id and is_in_every_single_word(message.content))
                                return message.author.id == player_play_user.id and message.channel.id == party_channel.id and is_in_every_single_word(message.content)"""

                        task_player_play_countdown = asyncio.create_task(player_play_countdown())
                        task_wait_for_player_play = asyncio.create_task(wait_for_player_play(player))

                        try:
                            done, pending = await asyncio.wait([task_player_play_countdown, task_wait_for_player_play], return_when=asyncio.FIRST_COMPLETED)
                            result_done = None
                            for task_done in done:
                                result_done = task_done.result()
                            for task_pending in pending:
                                task_pending.cancel()
                            if not result_done:
                                raise asyncio.TimeoutError
                            else:
                                await msg_player_play.edit(content=("Le tour de " + player_play_user.mention + " est terminé!"), delete_after=5.0)
                        except Exception:
                            await msg_player_play.edit(content=("Le tour de " + player_play_user.mention + " est terminé, mais il n'a rien répondu, son vote sera ignoré."), delete_after=5.0)
                            players[str(player)]["Can Vote"] = False
                        finally:
                            await party_channel.set_permissions(player_play_user, send_messages=False, read_messages=True, read_message_history=True)

                    task_player_play_waiting = asyncio.create_task(player_play_waiting(player))
                    await asyncio.wait({task_player_play_waiting})

                msg_vote_to_send = "Vous devez maintenant voter contre quelqu'un, vous avez 30 secondes :\n"
                for player in list_players_in_order:

                    msg_vote_to_send += players[player]["Emoji"] + " : " + (self.client.get_user(int(player))).mention + "\n"

                msg_vote_to_send += "Qui voulez-vous éliminer ?"

                msg_vote = await party_channel.send(msg_vote_to_send)

                for player in list_players_in_order:
                    await msg_vote.add_reaction(players[player]["Emoji"])
                """for player in players.keys():
                    await msg_vote.add_reaction(players[player]["Emoji"])"""

                party["Message"] = msg_vote

                base_msg_vote = msg_vote.content
                await msg_vote.edit(content=(base_msg_vote + "\nCommencez !"))

                await asyncio.sleep(10)
                await msg_vote.edit(content=(base_msg_vote + "\nIl reste 20 secondes..."))
                await asyncio.sleep(10)
                await msg_vote.edit(content=(base_msg_vote + "\nIl reste 10 secondes..."))
                await asyncio.sleep(5)
                await msg_vote.edit(content=(base_msg_vote + "\n5..."))
                await asyncio.sleep(1)
                await msg_vote.edit(content=(base_msg_vote + "\n4..."))
                await asyncio.sleep(1)
                await msg_vote.edit(content=(base_msg_vote + "\n3..."))
                await asyncio.sleep(1)
                await msg_vote.edit(content=(base_msg_vote + "\n2..."))
                await asyncio.sleep(1)
                await msg_vote.edit(content=(base_msg_vote + "\n1..."))
                await asyncio.sleep(1)
                await msg_vote.edit(content=(base_msg_vote + "\nVotes terminé!"))

                """async def voting():

                    pass_30 = False
                    pass_10 = False
                    pass_5 = False
                    pass_4 = False
                    pass_3 = False
                    pass_2 = False
                    pass_1 = False

                    old_time = 0
                    while (int(time.time()) - time_var) < 120:

                        actual_time = int(time.time()) - time_var

                        if actual_time == old_time:
                            continue

                        old_time = actual_time
                        print(actual_time)

                        if actual_time == 120 - 30 and pass_30 is False:
                            await party_channel.send("Il reste 30 secondes.")
                            pass_30 = True
                        if actual_time == 120 - 10 and pass_10 is False:
                            await party_channel.send("Il reste 10 secondes.")
                            pass_10 = True
                        if actual_time == 120 - 5 and pass_5 is False:
                            await party_channel.send("5...")
                            pass_5 = True
                        if actual_time == 120 - 4 and pass_4 is False:
                            await party_channel.send("4...")
                            pass_4 = True
                        if actual_time == 120 - 3 and pass_3 is False:
                            await party_channel.send("3...")
                            pass_3 = True
                        if actual_time == 120 - 2 and pass_2 is False:
                            await party_channel.send("2...")
                            pass_2 = True
                        if actual_time == 120 - 1 and pass_1 is False:
                            await party_channel.send("1...")
                            pass_1 = True

                await asyncio.wait([voting()])"""

                party["Message"] = None

                players_wo_vote = []
                for player in list_players_in_order:
                    if players[player]["Vote"] is None and players[player]["Can Vote"]:
                        players_wo_vote.append(self.client.get_user(int(player)))

                if len(players_wo_vote) > 0:
                    msg_to_send = ""
                    for player in players_wo_vote:
                        msg_to_send += player.mention + "\n"
                    msg_to_send += "Vous n'avez pas voté, veuillez voter.\n" + msg_vote_to_send
                    msg_vote = await party_channel.send(msg_to_send)
                    for player in list_players_in_order:
                        await msg_vote.add_reaction(players[player]["Emoji"])

                    async def vote(player):

                        def check(reaction, user):
                            return user == player and reaction.message.id == msg_vote.id

                        reaction_vote, user_reaction_vote = await self.client.wait_for('reaction_add', check=check)
                        while user_reaction_vote != player and reaction_vote.message.id != msg_vote.id and str(reaction_vote.emoji) not in [str(players[player_var]["Emoji"]) for player_var in players]:
                            if user_reaction_vote not in players_wo_vote:
                                await reaction_vote.remove(user_reaction_vote)
                            reaction_vote, user_reaction_vote = await self.client.wait_for('reaction_add', check=check)

                        await reaction_vote.remove(user_reaction_vote)

                        players[str(player.id)]["Vote"] = str(reaction_vote.emoji)

                    await asyncio.wait([vote(player) for player in players_wo_vote])

                vote_result = dict()
                for player in list_players_in_order:

                    if player not in vote_result.keys():
                        vote_result[player] = 0

                    if players[player]["Vote"] is None:
                        continue

                    for player_var in list_players_in_order:

                        if players[player_var]["Emoji"] == players[player]["Vote"]:
                            if player_var not in vote_result.keys():
                                vote_result[player_var] = 0
                            vote_result[player_var] += 1
                            break

                    players[player]["Vote"] = None

                max = ("", 0)
                max_list = []
                for player, vote_count in vote_result.items():

                    if max[1] < vote_count:
                        max_list = []
                        max = (player, vote_count)
                        max_list.append(max)
                    elif max[1] == vote_count:
                        max_list.append((player, vote_count))

                max = random.choice(max_list)

                deleted_player = max[0]

                players.pop(deleted_player)
                list_players_in_order.remove(deleted_player)

                if deleted_player == undercover:
                    await party_channel.send("Vous avez éliminé l'undercover!\nC'était " + undercover_user.mention + " !")
                    await asyncio.sleep(2)

                elif deleted_player == white_player:
                    await party_channel.send("Vous avez éliminé le white player !\n" + white_player_user.mention + ", quel était le mot ? Envoyez le moi par message privé.")

                    def check(word):
                        return word.channel == white_player_user.dm_channel

                    white_player_answer = await self.client.wait_for('message', check=check)

                    white_player_answer = white_player_answer.content
                    if white_player_answer == citizen_word:
                        await party_channel.send(white_player_user.mention + " a gagné !\nLe mot était \"" + citizen_word + "\".\nLe mot de l'undercover était \"" + undercover_word + "\".")
                        break
                    else:
                        await party_channel.send("Raté...")
                        await asyncio.sleep(2)

                else:
                    await party_channel.send("Aïe! " + (self.client.get_user(int(deleted_player))).mention + " était un citoyen et vous l'avez éliminé...\nContinuons...")
                    await asyncio.sleep(2)

                if undercover not in players.keys() and white_player not in players.keys():
                    await party_channel.send("Les citoyens ont gagné!\nLeur mot était \"**" + citizen_word + "**\".\nLe mot de l'undercover était \"**" + undercover_word + "**\".")
                    break

                elif (undercover in players.keys() or white_player in players.keys()) and len(players.keys()) == 2:
                    if undercover in players.keys() and white_player in players.keys():
                        await party_channel.send("Egalité entre " + (self.client.get_user(int(white_player))).mention + ", le White Player, et " + (self.client.get_user(int(undercover))).mention + ", l'Undercover!\nMais si le White Player à le mot, il gagne! Envoyez moi la réponse par message privé!")

                        def check(word):
                            return word.channel == white_player_user.dm_channel

                        white_player_answer = await self.client.wait_for('message', check=check)

                        white_player_answer = white_player_answer.content
                        if white_player_answer == citizen_word:
                            await party_channel.send(white_player_user.mention + " a gagné !\nLe mot était \"**" + citizen_word + "**\".\nLe mot de l'undercover était \"" + undercover_word + "\".")
                            break
                        else:
                            await party_channel.send("Raté!\nL'undercover a gagné! Son mot était \"**" + undercover_word + "**\".\nLe mot des citoyens était \"**" + citizen_word + "**\".")

                        break

                    elif undercover in players.keys():
                        await party_channel.send((self.client.get_user(int(undercover))).mention + ", l'undercover, a gagné!\nSon mot était \"**" + undercover_word + "**\".\nLe mot des citoyens était \"**" + citizen_word + "**\".")
                        break

                    elif white_player in players.keys():
                        await party_channel.send((self.client.get_user(int(white_player))).mention + ", le white player, a gagné!\nC'était " + white_player_user.mention + " !\nLe mot des citoyens était \"**" + citizen_word + "**\".\nLe mot de " + (self.client.get_user(int(undercover))).mention + ", l'undercover, était \"**" + undercover_word + "**\".")
                        break

            ask_continue = await party_channel.send("Rejouer ?")
            await ask_continue.add_reaction("👍")
            await ask_continue.add_reaction("👎")

            def check(reaction, user):
                return reaction.message.id == ask_continue.id and user == ctx.author

            continue_reaction, continue_user = await self.client.wait_for('reaction_add', check=check)
            if str(continue_reaction.emoji) == "👎":
                break

        self.parties.pop(str(party_no))
        await party_channel.send("Terminé! Merci d'avoir joué!")
        await asyncio.sleep(10)
        for player in base_players.keys():
            try:
                await self.guild_uc2.kick(self.client.get_user(int(player)), reason="Partie terminée !")
            except Exception:
                print("skip admin")
        await party_channel.delete()


def setup(client):
    guild_uc2 = client.get_guild(748932411093549158)
    category = client.get_channel(748933042973704192)
    discord_emojis = dict()
    with open("./emoji_map.json") as f:
        discord_emojis = json.load(f)
    emojis_list = list(str(emoji) for emoji in client.emojis) + list(discord_emojis.values())
    client.add_cog(Undercover(client, emojis_list, guild_uc2, category))

#!/usr/bin/env python3.6

import discord
from discord.ext import commands

class Memes:
    """
    ayy lmao
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))

    # SSS memes

    @commands.command()
    async def gudie(self, ctx):
        """Follow the Gudie to become a l33t Corbenik hax0r."""
        return await ctx.send("https://gudie.racklab.xyz/")

    @commands.command()
    async def rip(self, ctx):
        """F"""
        msg = await ctx.send("Press F to pay respects.")
        await msg.add_reaction("🇫")

    @commands.command()
    async def t3ch(self, ctx):
        """Goddamn Nazimod"""
        return await ctx.send("https://i.imgur.com/4kANai8.png")

    @commands.command()
    async def bigsmoke(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/vo5l6Fo.jpg\nALL YOU HAD TO DO WAS FOLLOW THE DAMN GUIDE CJ!")
 
    @commands.command()
    async def bigorder(self, ctx):
        """Memes."""
        await ctx.send("I'll have two number 9s, a number 9 large, a number 6 with extra dip, a number 7, two number 45s, one with cheese, and a large soda.")
 
    @commands.command()
    async def heil(self, ctx):
        """SIEG HEIL"""
        await ctx.send("HEIL T3CH!")
        
    @commands.command()
    async def lenny(self, ctx):
        """( ͡° ͜ʖ ͡°)"""
        await ctx.send("( ͡° ͜ʖ ͡°)")

    @commands.command()
    async def brickdurr(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/hzuXOHP.png")

    @commands.command()
    async def birds(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/fVAx5oh.png")
	
    @commands.command()
    async def kina(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/8Mm5ZvB.jpg")
	
    @commands.command()
    async def macboy(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/IpQC6IF.png")
    
    # SSS spammy-ish memes that need a cooldown
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    @commands.command(aliases=["astronautlevel"])
    async def astro(self, ctx):
        """MEMES???"""
        await ctx.send(
            "ASTRO DOES IT AGAIN!!!\n" +
            "The peak nazi mod recuperance has occurred, mimicing the occurrence of 2016 where he once emotionally manipulated s_99 and xorhash to die off the server. " +
            "In that time, it was an emotionally draining period in which tensions were high and confusion was all over the place. " +
            "The word on the street places that this time is very similar to that time, in the dark days of the previously old, now defunct, 3d shacks, which was renamed to Nintendo Homebrew as of the final official takeover of Emma in late 2016-early 2017, with the help of Ian. " +
            "However, the old tales of his exploits have been sung across the land, and it is possible that they have led to influence over this most recent attempt of takeover of SSS. " +
            "The real quandry of all this however, is, how will he now react to the new role in taking over SSS? " +
            "Will his potential ownership be riddeled with as much controversy as his old temporary ownership in 3dshacks? The future alone will know."
        )
    
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.channel)
    @commands.command()
    async def xkyup(self, ctx, variant=""):
        """
        MEMES???
        This meme has multiple variants : fr, es, it, jp, de, pl, pt, nl, se, bees
        You can also specify your own variant, and it will automatically generate a copypasta:
        I'm so sorry, I was a fucking retard for saying words that would get me in touble and anger lots of people who {} or who are dating {}.
        I didn't think before I spoke a word so it just came out as something totally wrong, I don't hate anybody who is {}, just the community. I like {}, just not the {} community. I'm sorry for all of this. All I'm asking for is a apology is all. I should have been thinking before I spoke."
        """
        if variant == "":
            await ctx.send(
                "I'm so sorry, I was a fucking retard for saying words that would get me in touble and anger lots of people who are transgender or who are dating a transgender person. " +
                "I didn't think before I spoke a word so it just came out as something totally wrong, I don't hate anybody who is transgender, just the community. I like Aurora, just not the trans community. I'm sorry for all of this. All I'm asking for is a apology is all. I should have been thinking before I spoke."
            )

        elif variant == "fr":
            await ctx.send(
                "Je suis tellement désolé, j'étais un putain d'attardé pour avoir dit des mots qui me mettraient dans le pétrin et qui mettraient beaucoup de personnes qui sont transgenres ou qui sont en couple avec une personne transgenre. Je n'ai pas réfléchi avant d'avoir dit un mot donc c'est juste sorti comme quelque chose de totalement faux, je ne déteste aucune personne transgenre, seulement la communauté. " +
                "J'aime bien Aurora, juste pas la communauté trans. Je suis désolé pour tout ceci. Tout ce que je demande c'est des excuses, c'est tout. J'aurais du réfléchir avant de parler."
            )

        elif variant == "es":
            await ctx.send(
                "Estoy muy arrepentido, fui un estupido retardado por decir esas palabras que me pondrian en problemas y hacer enojar a mucha gente que son transexuales o que estan saliendo con una persona transexual. No pense antes de decir una palabra asi que salio como algo totalmente mal. Yo no odio cualquiera que sea transexual,solo la comunidad. " +
                "Me gusta Aurora, solo no la trans comunidad. Estoy arrepentido por todo esto. Lo unico que pido es una disculpa. Tuve que haer pensado antes de hablar"
            )

        elif variant == "it":
            await ctx.send(
                "Mi dispiace così tanto, sono stato un fottuto idiota per aver detto cose che mi avrebbero messo nei guai e avrebbero fatto arrabbiare un sacco di persone che sono transgender o che stanno insieme ad una persona transgender. Non ho pensato prima di aprire bocca quindi è sembrato qualcosa di completamente sbagliato, non odio nessuno che sia transgender, solo la comunità. " +
                "Mi piace Aurora, solo non la comunità trans. Mi dispiace per tutto questo. Tutto ciò che sto chiedendo è di chiedere scusa, tutto qui. Avrei dovuto pensare prima di parlare."
            )

        elif variant == "jp":
            await ctx.send(
                "本当に申し訳ない, 私は多くのトランス人やトランス人をデートする人を怒らせる言葉で困ってしまった言葉を言ってからクソなリタードだった。 " +
                "言葉を言った前に思ったなかったから全く間違っていた何かを来た、誰でもトランスジェンダは嫌いじゃなくてあのコミュニティだけ嫌い。オーロラが好き、トランスのコミュニティだけではない。これは本当にすみません。私が求めているのは謝罪だけ。話す前に思っていたはずだった。"
            )

        elif variant == "de":
            await ctx.send(
                "Es tut mir sehr Leid, Ich war ein verfickter Behinderter als ich diese Worte sagte und wusste nicht wie sehr ich Ärger kriegen würde und wie sehr ich transsexuelle Menschen oder Menschen die transsexuelle daten erzörnen würde. " +
                "Ich habe nicht gedacht bevor ich das Wort sagte und so kam es raus als was komplett falsches. Ich hasse keine Transsexuellen, nur die Gemeinschaft. Ich mag Transsexuelle, nur nicht die Gemeinschaft. Es tut mir sehr leid für all das. Ich bitte nur um Verzeihung. Ich hätte nachdenken sollen bevor ich den Mund aufgemacht habe."
            )
        
        elif variant == "pl":
            await ctx.send(
                "Bardzo mi przykro, byłem jebanym idiotą gdy wypowiedziałem te słowa i nie zdawałem sobie sprawy z tego jak bardzo naprzykrze sie osobom transseksualnym lub tym którzy chodzą z transseksualistami. Nie myślałem gdy wypowiedziałem te słowa i to co wyszło z moich ust było smutne i nieprawidłowe. Nic nie mam do osób trans, tylko do ich społeczności " +
                " Lubie osoby trans, nie lubie tylko ich społeczności. Bardzo mi za to wszystko przykro. Proszę o przebaczenie. Powinienem był pomyśleć zanim cokolwiek napisałem."
            )

        elif variant == "pt":
            await ctx.send(
                "Peço imensa desculpa. Fui um grande retardado por dizer palavras que me iam meter em sarilhos com pessoas trans ou que estão a namorar com uma pessoa trans. Eu não pensei antes de falar por isso aquilo saiu como algo totalmente mau, eu não detesto ninguem que seja trans, só a comunidade trans. " +
                "Eu gosto da Aurora, só não gosto da comunidade trans. Peço desculpa por tudo isto. Só peço que me desculpem. Devia ter pensado antes de ter falado."
            )

        elif variant == "nl":
            await ctx.send(
                "Het spijt me zo erg, ik was een echt achterlijk om woorden te zeggen die mij in moeite zou brengen en die veel mensen die transgender zijn of die in een relatie zijn met een transgender persoon boos zou maken. Ik heb niet nagedacht voor het spreken, dus kwam het als iets totaal vals, " +
                "ik haat niemand die transgender is, alleen de gemeenschap. Ik hou van Aurora, alleen niet van de trans gemeenschap. Het spijt me voor dit alles. Alles what ik vraag is excuses, dat is alles. Ik had moeten denken voordat ik sprak"
            )
        
        elif variant == "se":
            await ctx.send("hello guys im very sorry for punching a woman in discord chat. i do not understand what i do i am only muslim man coming to sweden from long country away i am very sorry this has been very sad and i only want apology so i do not bring shame on family that come sweden")

        elif variant == "bees":
            await ctx.send(
                "I'm so sorry, I was a fucking retard for saying words that would get me in touble and anger lots of people who are bees or who are dating a bee. I didn't think before I spoke a word so it just came out as something totally wrong, I don't hate anybody who is a bee, just the hive. " +
                "I like bees, just not the beehive. I'm sorry for all of this. All I'm asking for is a apology is all. I should have been thinking before I spoke."
            )
        
        else:
            try:
                variant = variant.replace('@everyone', '`@`everyone').replace('@here', '`@`here')
                words = variant.split(',')
                await ctx.send(
                    "I'm so sorry, I was a fucking retard for saying words that would get me in touble and anger lots of people who {} or who are dating {}. ".format(words[0], words[1]) +
                    "I didn't think before I spoke a word so it just came out as something totally wrong, I don't hate anybody who is {}, just the community. I like {}, just not the {} community. I'm sorry for all of this. All I'm asking for is a apology is all. I should have been thinking before I spoke.".format(words[2], words[3], words[4])
                )
            except:
                return await ctx.send("Your syntax is incorrect. Please use the following syntax : `.xkyup \"word1,word2,word3,word4,word5\"`. You must specify the 5 words.")


    # Kurisu memes
    @commands.command()
    async def s_99(self, ctx):
        """Memes."""
        await ctx.send("**ALL HAIL BRITANNIA!**")

    @commands.command()
    async def screams(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/j0Dkv2Z.png")

    @commands.command()
    async def eeh(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/2SBC1Qo.jpg")

    @commands.command()
    async def dubyadud(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/Sohsi8s.png")

    @commands.command()
    async def megumi(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/GMRp1dj.jpg")

    @commands.command()
    async def inori(self, ctx):
        """Memes."""
        await ctx.send("https://i.imgur.com/WLncIsi.gif")

    @commands.command()
    async def inori3(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/so8thgu.gifv")

    @commands.command()
    async def inori4(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/267IXh1.gif")

    @commands.command()
    async def inori5(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/lKcsiBP.png")

    @commands.command()
    async def inori6(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/SIJzpau.gifv")

    @commands.command()
    async def shotsfired(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/zf2XrNk.gifv")

    @commands.command()
    async def rusure(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/dqh3fNi.png")

    @commands.command()
    async def r34(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/sjQZKBF.gif")

    @commands.command()
    async def permabrocked(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/ARsOh3p.jpg")

    @commands.command()
    async def knp(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/EsJ191C.png")

    @commands.command()
    async def lucina(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/tnWSXf7.png")

    @commands.command()
    async def lucina2(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/ZPMveve.jpg")

    @commands.command()
    async def xarec(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/A59RbRT.png")

    @commands.command()
    async def clap(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/UYbIZYs.gifv")

    @commands.command()
    async def ayyy(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/bgvuHAd.png")

    @commands.command()
    async def hazel(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/vpu8bX3.png")

    @commands.command()
    async def thumbsup(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/hki1IIs.gifv")

    @commands.command()
    async def pbanjo(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/sBJKzuK.png")

    # Cute commands :3
    @commands.command()
    async def headpat(self, ctx):
        """Cute"""
        await ctx.send("http://i.imgur.com/7V6gIIW.jpg")

    @commands.command()
    async def headpat2(self, ctx):
        """Cute"""
        await ctx.send("http://i.imgur.com/djhHX0n.gifv")

    @commands.command()
    async def sudoku(self, ctx):
        """Cute"""
        await ctx.send("http://i.imgur.com/VHlIZRC.png")

    @commands.command()
    async def baka(self, ctx):
        """Cute"""
        await ctx.send("http://i.imgur.com/OyjCHNe.png")

    @commands.command()
    async def mugi(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/lw80tT0.gif")

    @commands.command()
    async def lisp(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/RQeZErU.png")

    @commands.command()
    async def headrub(self, ctx):
        """Cute"""
        await ctx.send("http://i.imgur.com/j6xSoKv.jpg")

    @commands.command()
    async def blackalabi(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/JzFem4y.png")

    @commands.command()
    async def nom(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/p1r53ni.jpg")

    @commands.command()
    async def soghax(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/oQJy2eN.png")

    @commands.command()
    async def whatisr(self, ctx):
        """MEMES?"""
        await ctx.send("http://i.imgur.com/Z8HhfzJ.jpg")
	
    @commands.command()
    async def sn0w(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/sFD5uSB.png")

    @commands.command()
    async def helpers(self, ctx):
        """MEMES?"""
        await ctx.send("http://i.imgur.com/0v1EgMX.png")
    
    @commands.command()
    async def concern(self, ctx):
        """MEMES?"""
        await ctx.send("https://i.imgur.com/cWXBb5g.png")
	
## Ill finish this later
	
##    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.channel)
##    @commands.command()
##    async def dongroder(self, ctx, variant=""):
##        if variant == "piter":
##            await ctx.send(
##                "I'm so sorry, I was a fucking retard for saying words that would get me in touble and anger lots of people who are transgender or who are dating a transgender person. " +
##                "I didn't think before I spoke a word so it just came out as something totally wrong, I don't hate anybody who is transgender, just the community. I like Aurora, just not the trans community. I'm sorry for all of this. All I'm asking for is a apology is all. I should have been thinking before I spoke."
##            )
##        elif variant == "swotch":
##            await ctx.send(
##                "I'm so sorry, I was a fucking retard for saying words that would get me in touble and anger lots of people who are bees or who are dating a bee. I didn't think before I spoke a word so it just came out as something totally wrong, I don't hate anybody who is a bee, just the hive. " +
##                "I like bees, just not the beehive. I'm sorry for all of this. All I'm asking for is a apology is all. I should have been thinking before I spoke."
##            )

def setup(bot):
    bot.add_cog(Memes(bot))

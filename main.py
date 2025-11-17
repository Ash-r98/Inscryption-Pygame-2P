import pygame
from pathlib import Path
from time import sleep
from random import randint

pygame.init()
pygame.display.set_caption('Inscryption - Multiplayer Edition')

# Screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Card:
    dmg = 0
    basedmg = 0
    hp = 1
    basehp = 1
    blood = 0
    bones = 0
    img = ''
    sigillist = []
    sacrificable = True
    sigildict = {
        'rabbit_hole': False,  # done
        'bees_within': False,  # done
        'sprinter': False,  # done (requires checks)
        'touch_of_death': False,  # done
        'fledgling': False,
        'dam_builder': False,
        'hoarder': False,
        'burrower': False,
        'fecundity': False,  # done
        'loose_tail': False,
        'corpse_eater': False,  # done (requires checks)
        'bone_king': False,  # done
        'waterborne': False,
        'unkillable': False,  # done
        'sharp_quills': False,
        'hefty': False,
        'ant_spawner': False,  # done
        'guardian': False,
        'airborne': False,  # done
        'many_lives': False, # done (fix multiple sacrifices on one card)
        'repulsive': False,  # done
        'worthy_sacrifice': False, # done
        'mighty_leap': False,  # done
        'bifurcated_strike': False,
        'trifurcated_strike': False,
        'frozen_away': False,
        'trinket_bearer': False,
        'steel_trap': False,
        'amorphous': False,
        'tidal_lock': False,
        'omni_strike': False,
        'leader': False,
        'bellist': False,
        'stinky': False,
        'ant_damage': False  # Not technically a sigil but necessary for ant cards
    }


    def __init__(self, data):
        # newdmg, newhp, newblood, newbones, newimg, newsigillist, newsacrificable
        self.dmg = data[0]
        self.basedmg = data[0]
        self.hp = data[1]
        self.basehp = data[1]
        self.blood = data[2]
        self.bones = data[3]
        self.img = data[4]
        self.sigillist = data[5]
        self.sacrificable = data[6]
        for i in self.sigildict:
            self.sigildict[i] = False
        for i in range(len(self.sigillist)):
            self.sigildict[self.sigillist[i]] = True

    def takedmg(self, enemycard):
        if 'bees_within' in self.sigillist:
            if p1turn:
                p2hand.append(Card([1, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/bee.png')), ['airborne'], True]))
            else:
                p1hand.append(Card([1, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/bee.png')), ['airborne'], True]))
        if 'touch_of_death' in self.sigillist:
            self.hp = 0
        if 'repulsive' in self.sigillist:
            enemycard.dmg = 0
        self.hp -= enemycard.dmg

def draw(deck):
    if len(deck) <= 0: # If deck is empty draw a starvation card (hopefully prevents softlocking)
        return Card([1, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/starvation.png')), ['repulsive'], False])
    temp = randint(0, len(deck)-1)
    return deck[temp], temp

def displaycard(card, x, y):
    screen.blit(card.img, (x, y))
    if card.dmg == card.basedmg:
        dmgtext = font.render(str(card.dmg), True, (0, 0, 0))
    elif card.dmg > card.basedmg:
        dmgtext = font.render(str(card.dmg), True, (0, 150, 0))
    else:
        dmgtext = font.render(str(card.dmg), True, (150, 0, 0))
    if card.hp == card.basehp:
        hptext = font.render(str(card.hp), True, (0, 0, 0))
    elif card.hp > card.basehp:
        hptext = font.render(str(card.hp), True, (0, 150, 0))
    else:
        hptext = font.render(str(card.hp), True, (150, 0, 0))
    screen.blit(dmgtext, (x + 25, y + 310))
    screen.blit(hptext, (x + 235, y + 345))

def updateboard(p1turn):
    global p1bones
    global p2bones
    # Board placeholder squares
    pygame.draw.rect(screen, (255, 255, 255), emptysquare)
    pygame.draw.rect(screen, (0, 0, 0), emptysquareint1)
    pygame.draw.rect(screen, (0, 0, 0), emptysquareint2)
    pygame.draw.rect(screen, (0, 0, 0), emptysquareint3)
    pygame.draw.rect(screen, (0, 0, 0), emptysquareint4)
    pygame.draw.rect(screen, (0, 0, 0), emptysquareint5)
    pygame.draw.rect(screen, (0, 0, 0), emptysquareint6)
    pygame.draw.rect(screen, (0, 0, 0), emptysquareint7)
    pygame.draw.rect(screen, (0, 0, 0), emptysquareint8)
    for i in range(4): # Kill dead cards
        if p1board[i] != ():
            if p1board[i].hp <= 0:
                # Bones reward p1
                if 'bone_king' in p1board[i].sigillist:
                    p1bones += 4
                else:
                    p1bones += 1
                if 'unkillable' in p1board[i].sigillist:
                    p1hand.append(p1board[i])
                    p1hand[-1].hp = p1hand[-1].basehp
                    p1hand[-1].dmg = p1hand[-1].basedmg
                p1board[i] = ()
                # Corpse eater check (after card death) p1
                for j in range(len(p1hand)):
                    if 'corpse_eater' in p1hand[j].sigillist:
                        p1board[i] = p1hand[j]
                        p1hand.pop(j)
                        break
        if p2board[i] != ():
            if p2board[i].hp <= 0:
                # Bones reward p2
                if 'bone_king' in p2board[i].sigillist:
                    p2bones += 4
                else:
                    p2bones += 1
                if 'unkillable' in p2board[i].sigillist:
                    p2hand.append(p2board[i])
                    p2hand[-1].hp = p2hand[-1].basehp
                    p2hand[-1].dmg = p2hand[-1].basedmg
                p2board[i] = ()
                # Corpse eater check (after card death) p2
                for j in range(len(p2hand)):
                    if 'corpse_eater' in p2hand[j].sigillist:
                        p2board[i] = p2hand[j]
                        p2hand.pop(j)
                        break
    if p1turn: # Render alive cards
        for i in range(4):
            if p1board[i] != ():
                displaycard(p1board[i], ((300*(i+1))+60), 575)
            if p2board[i] != ():
                displaycard(p2board[i], ((300 * (4 - i)) + 60), 75)
    else:
        for i in range(4):
            if p2board[i] != ():
                displaycard(p2board[i], ((300*(i+1))+60), 575)
            if p1board[i] != ():
                displaycard(p1board[i], ((300 * (4 - i)) + 60), 75)


# Button class
class Button:
    def __init__(self, x, y, image, hoverimage, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.hoverimage = pygame.transform.scale(hoverimage, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and click conditions
        if self.rect.collidepoint(pos):
            # Draw hover button to screen
            screen.blit(self.hoverimage, (self.rect.x, self.rect.y))
            if pygame.mouse.get_pressed()[0] and self.clicked == False: # 0 = left click
                self.clicked = True # Can only click once at a time
                action = True
        else:
            # Draw normal button to screen
            screen.blit(self.image, (self.rect.x, self.rect.y))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False # Resets if mouse is not held

        return action




# Card instances data
# Card([dmg, hp, blood, bones, image file, sigil list, sacrificable])
# Template for new instances:
# = [, , , , pygame.image.load(r'CroppedInscryptionCards\.png'), [], True]
adder = [1, 1, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/adder.png')), ['touch_of_death'], True]
alpha = [1, 2, 0, 5, pygame.image.load(Path('CroppedInscryptionCards/alpha.png')), ['leader'], True]
amalgam = [3, 3, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/amalgam.png')), [], True]
amoeba = [1, 2, 0, 2, pygame.image.load(Path('CroppedInscryptionCards/amoeba.png')), ['amorphous'], True]
ant_queen = [0, 3, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/ant_queen.png')), ['ant_damage', 'ant_spawner'], True] # Added 'sigil' for ant damage
bait_bucket = [0, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/bait_bucket.png')), [], False] # Shark spawning not currently coded as it is not a sigil
bat = [2, 1, 0, 4, pygame.image.load(Path('CroppedInscryptionCards/bat.png')), ['airborne'], True]
beaver = [1, 3, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/beaver.png')), ['dam_builder'], True]
bee = [1, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/bee.png')), ['airborne'], True]
beehive = [0, 2, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/beehive.png')), ['bees_within'], True]
black_goat = [0, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/black_goat.png')), ['worthy_sacrifice'], True]
bloodhound = [2, 3, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/bloodhound.png')), ['guardian'], True]
boulder = [0, 5, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/boulder.png')), [], False]
bullfrog = [1, 2, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/bullfrog.png')), ['mighty_leap'], True]
caged_wolf = [0, 6, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/caged_wolf.png')), [], False] # Wolf spawning not currently coded as it is not a sigil
cat = [0, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/cat.png')), ['many_lives'], True]
child_13 = [0, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/child_13.png')), ['many_lives'], True]
child_13_awake = [2, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/child_13_awake.png')), ['airborne', 'many_lives'], True]
chime = [0, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/chime.png')), [], False] # Daus interaction not currently coded as it is not a sigil
cockroach = [1, 1, 0, 4, pygame.image.load(Path('CroppedInscryptionCards/cockroach.png')), ['unkillable'], True]
corpse_maggots = [1, 2, 0, 5, pygame.image.load(Path('CroppedInscryptionCards/corpse_maggots.png')), ['corpse_eater'], True]
coyote = [2, 1, 0, 4, pygame.image.load(Path('CroppedInscryptionCards/coyote.png')), [], True]
dam = [0, 2, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/dam.png')), [], False]
elk = [2, 4, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/elk.png')), ['sprinter'], True]
elk_fawn = [1, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/elk_fawn.png')), ['sprinter', 'fledgling'], True]
field_mice = [2, 2, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/field_mice.png')), ['fecundity'], True]
frozen_opossum = [0, 5, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/frozen_opossum.png')), ['frozen_away'], False]
furry_tail = [0, 2, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/furry_tail.png')), [], False]
geck = [1, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/geck.png')), [], True]
gold_nugget = [0, 2, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/gold_nugget.png')), [], False]
golden_pelt = [0, 3, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/golden_pelt.png')), [], False]
grand_fir = [0, 3, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/grand_fir.png')), ['mighty_leap'], False]
great_white = [4, 2, 3, 0, pygame.image.load(Path('CroppedInscryptionCards/great_white.png')), ['waterborne'], True]
greater_smoke = [1, 3, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/greater_smoke.png')), ['bone_king'], True]
grizzly = [4, 6, 3, 0, pygame.image.load(Path('CroppedInscryptionCards/grizzly.png')), [], True]
kingfisher = [1, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/kingfisher.png')), ['waterborne', 'airborne'], True]
leaping_trap = [0, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/leaping_trap.png')), ['mighty_leap', 'steel_trap'], True]
long_elk = [1, 2, 0, 4, pygame.image.load(Path('CroppedInscryptionCards/long_elk.png')), ['sprinter', 'touch_of_death'], True]
magpie = [1, 1, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/magpie.png')), ['hoarder', 'airborne'], True]
mantis = [1, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/mantis.png')), ['bifurcated_strike'], True]
mantis_god = [1, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/mantis_god.png')), ['trifurcated_strike'], True]
mole = [0, 4, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/mole.png')), ['burrower'], True]
mole_man = [0, 6, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/mole_man.png')), ['burrower', 'mighty_leap'], True]
moose_buck = [3, 7, 3, 0, pygame.image.load(Path('CroppedInscryptionCards/moose_buck.png')), ['hefty'], True]
mothman = [7, 3, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/mothman.png')), ['airborne'], True]
opossum = [1, 1, 0, 2, pygame.image.load(Path('CroppedInscryptionCards/opossum.png')), [], True]
ouroboros = [1, 1, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/ouroboros.png')), ['unkillable'], True]
pack_mule = [0, 5, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/pack_mule.png')), ['sprinter'], True]
pack_rat = [2, 2, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/pack_rat.png')), ['trinket_bearer'], True]
porcupine = [1, 2, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/porcupine.png')), ['sharp_quills'], True]
pronghorn = [1, 3, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/pronghorn.png')), ['sprinter', 'bifurcated_strike'], True]
rabbit = [0, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/rabbit.png')), [], True]
rabbit_pelt = [0, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/rabbit_pelt.png')), [], False]
rat_king = [2, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/rat_king.png')), ['bone_king'], True]
rattler = [3, 1, 0, 6, pygame.image.load(Path('CroppedInscryptionCards/rattler.png')), [], True]
raven = [2, 3, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/raven.png')), ['airborne'], True]
raven_egg = [0, 2, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/raven_egg.png')), ['fledgling'], True]
ring_worm = [0, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/ring_worm.png')), [], True]
river_otter = [1, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/river_otter.png')), ['waterborne'], True]
river_snapper = [1, 6, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/river_snapper.png')), [], True]
skink = [1, 2, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/skink.png')), ['loose_tail'], True]
skunk = [0, 3, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/skunk.png')), ['stinky'], True]
snowy_fir = [0, 4, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/snowy_fir.png')), ['mighty_leap'], False]
sparrow = [1, 2, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/sparrow.png')), ['airborne'], True]
squid_bell = [0, 3, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/squid_bell.png')), [], True] # Damage based on position from left, leftmost = 4, rightmost = 1
squid_cards = [0, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/squid_cards.png')), [], True] # Damage = number of cards in playePath('s hand
squid_mirror = [0, 3, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/squid_mirror.png')), [], True] # Damage = Opposite card's damage
squirrel = [0, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/squirrel.png')), [], True]
starvation = [1, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/starvation.png')), ['repulsive'], False]
starvation_flying = [1, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/starvation_flying.png')), ['airborne'], False]
stinkbug = [1, 2, 0, 2, pygame.image.load(Path('CroppedInscryptionCards/stinkbug_talking.png')), ['stinky'], True]
stoat = [1, 3, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/stoat_talking.png')), [], True]
strange_frog = [1, 2, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/strange_frog.png')), ['mighty_leap'], False]
strange_larva = [0, 3, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/strange_larva.png')), ['fledgling'], True]
strange_pupa = [0, 3, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/strange_pupa.png')), ['fledgling'], True]
stump = [0, 3, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/stump.png')), [], False]
tail_feathers = [0, 2, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/tail_feathers.png')), [], False]
the_daus = [2, 2, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/the_daus.png')), ['bellist'], True]
the_smoke = [0, 1, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/the_smoke.png')), ['bone_king'], True]
turkey_vulture = [3, 3, 0, 8, pygame.image.load(Path('CroppedInscryptionCards/turkey_vulture.png')), ['airborne'], True]
undead_cat = [3, 6, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/undead_cat.png')), [], True]
urayuli = [7, 7, 4, 0, pygame.image.load(Path('CroppedInscryptionCards/urayuli.png')), [], True]
warren = [0, 2, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/warren.png')), ['rabbit_hole'], True]
wolf = [3, 2, 2, 0, pygame.image.load(Path('CroppedInscryptionCards/wolf.png')), [], True]
wolf_cub = [1, 1, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/wolf_cub.png')), ['fledgling'], True]
wolf_pelt = [0, 2, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/wolf_pelt.png')), [], False]
stunted_wolf = [2, 2, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/wolf_talking.png')), [], True]
worker_ant = [0, 2, 1, 0, pygame.image.load(Path('CroppedInscryptionCards/worker_ant.png')), ['ant_damage'], True] # Added 'sigil' for ant damage
wriggling_leg = [0, 2, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/wriggling_leg.png')), [], False]
wriggling_tail = [0, 2, 0, 0, pygame.image.load(Path('CroppedInscryptionCards/wriggling_tail.png')), [], False]




# Button instances
viewhand_button = Button(75, 950, pygame.image.load(Path('OtherSprites/showhand_button.png')), pygame.image.load(Path('OtherSprites/showhand_button_hover.png')), 0.3)
viewboard_button = Button(860, 950, pygame.image.load(Path('OtherSprites/showboard_button.png')), pygame.image.load(Path('OtherSprites/showboard_button_hover.png')), 0.3)
play_button = Button(40, 850, pygame.image.load(Path('OtherSprites/play_button.png')), pygame.image.load(Path('OtherSprites/play_button_hover.png')), 0.4)
exit_button = Button(1820, 20, pygame.image.load(Path('OtherSprites/exit_button.png')), pygame.image.load(Path('OtherSprites/exit_button_hover.png')), 0.4)
backbutton = Button(25, 25, pygame.image.load(Path('OtherSprites/back_arrow.png')), pygame.image.load(Path('OtherSprites/back_arrow_hover.png')), 1)
# Draw pile buttons
normaldeck_button = Button(1580, 800, pygame.image.load(Path('CroppedInscryptionCards/backs/common.png')), pygame.image.load(Path('CroppedInscryptionCards/backs/common.png')), 0.5)
squirreldeck_button = Button(1750, 800, pygame.image.load(Path('CroppedInscryptionCards/backs/squirrel.png')), pygame.image.load(Path('CroppedInscryptionCards/backs/squirrel.png')), 0.5)
# Title screen buttons
title_play_button = Button(500, 650, pygame.image.load(Path('OtherSprites/title_play_button.png')), pygame.image.load(Path('OtherSprites/title_play_button_hover.png')), 0.7)
title_options_button = Button(843, 650, pygame.image.load(Path('OtherSprites/title_options_button.png')), pygame.image.load(Path('OtherSprites/title_options_button_hover.png')), 0.7)
title_quit_button = Button(1186, 650, pygame.image.load(Path('OtherSprites/title_quit_button.png')), pygame.image.load(Path('OtherSprites/title_quit_button_hover.png')), 0.7)
# Options menu buttons



# Play square
emptysquare = pygame.Rect((360, 75, 1200, 950))
emptysquareint1 = pygame.Rect((370, 585, 280, 430)) # 360x575
emptysquareint2 = pygame.Rect((670, 585, 280, 430)) # 660x575
emptysquareint3 = pygame.Rect((970, 585, 280, 430)) # 960x575
emptysquareint4 = pygame.Rect((1270, 585, 280, 430)) # 1260x575
emptysquareint5 = pygame.Rect((370, 85, 280, 430)) # 360x75
emptysquareint6 = pygame.Rect((670, 85, 280, 430)) # 660x75
emptysquareint7 = pygame.Rect((970, 85, 280, 430)) # 960x75
emptysquareint8 = pygame.Rect((1270, 85, 280, 430)) # 1260x75


# Text
# Attack text position (from top left of card) = x+25, y+310
# HP text position (from top left of card) = x+235, y+345
font = pygame.font.Font('HEAVYWEI.TTF', 96)
fontsmall = pygame.font.Font('HEAVYWEI.TTF', 64)
attacktexttest = font.render('3', True, (0, 0, 0))
hptexttest = font.render('2', True, (0, 0, 0))


# Setup variables
state = 4 # 0 = Board, 1 = Player1 Hand, 2 = Player2 Hand, 3 = Sacrificing/playing, 4 = Title Screen, 5 = Options menu
p1turn = True # True = Player 1 turn, False = Player 2 Turn
turnstage = 0 # 0 = Draw, 1 = Human decisions, 2 = execution
firstdraw = True # Will draw to 4 cards on turn one
selectedcard = 0 # Which card is currently being selected in the play stage
firstplayloop = True # Will let the tempblood variable get set on only the first loop of stage 3


# Player 1 variables
p1teeth = 0
p1bones = 0
p1deck = [Card(wolf), Card(mantis), Card(stoat), Card(stinkbug), Card(grand_fir)]
p1hand = []
p1board = [(), (), (), ()]

# Player 2 variables
p2teeth = 0
p2bones = 0
p2deck = [Card(stunted_wolf), Card(mantis_god), Card(mothman), Card(elk_fawn), Card(snowy_fir)]
p2hand = []
p2board = [(), (), (), ()]

sprintertemp = False # Variable to skip for loop if sprinter

# Variable for toggling devmode
toggledev = False
devmode = False


run = True
while run:

    screen.fill((0, 0, 0)) # Black background

    # Devmode displays
    if devmode:
        devmodetext = font.render('DEVMODE', True, (255, 255, 255))
        devmodetext = pygame.transform.rotate(devmodetext, 270)
        screen.blit(devmodetext, (1800, 100))
        statetext = font.render(str(state), True, (255, 255, 255))
        screen.blit(statetext, (0, 0))

    if state != 4 and state != 5: # Exit button is always visible except title screen/options menu (different quit button)
        if exit_button.draw():
            run = False

    # Board view
    if state == 0:
        # Board text top left
        state0text = font.render('Board', True, (255, 255, 255))
        screen.blit(state0text, (0, 0))

        # Draws board squares and cards
        updateboard(p1turn)

        # Creates teeth text for both players
        p1teethtext = fontsmall.render(f'P1 teeth - {str(p1teeth)}', True, (255, 255, 255))
        p2teethtext = fontsmall.render(f'P2 teeth - {str(p2teeth)}', True, (255, 255, 255))

        if p1turn: # Displays text for player 1
            bonestext = fontsmall.render(f'P1 bones - {str(p1bones)}', True, (150, 150, 150))
            screen.blit(p1teethtext, (40, 550))
            screen.blit(p2teethtext, (40, 250))
        else: # Displays text for player 2
            bonestext = fontsmall.render(f'P2 bones - {str(p2bones)}', True, (150, 150, 150))
            screen.blit(p1teethtext, (40, 250))
            screen.blit(p2teethtext, (40, 550))
        screen.blit(bonestext, (40, 750))

        # Moves to the attack stage
        if play_button.draw():
            if turnstage != 0: # Draw stage must be completed first
                turnstage = 2

        # Play stage
        if turnstage == 2:
            viewhand_button.draw() # Must still be visible but unusable

            if p1turn: # Player 1 attack
                for i in range(4):
                    if sprintertemp:
                        sprintertemp = False
                        continue
                    if p1board[i] != ():
                        if p1board[i].dmg > 0: # Only do attack animation if they attack
                            updateboard(p1turn)
                            pygame.draw.rect(screen, (0, 0, 0), eval('emptysquareint'+str(i+1)))
                            displaycard(p1board[i], ((300 * (i + 1)) + 60), 400)
                            if p2board[3 - i] != ():
                                if not 'airborne' in p1board[i].sigillist: # Airborne check
                                    p2board[3-i].takedmg(p1board[i])
                                else:
                                    if 'mighty_leap' in p1board[i].sigillist: # Mighty leap check
                                        p2board[3 - i].takedmg(p1board[i])
                                    else:
                                        p2teeth += p1board[i].dmg
                            else:
                                p2teeth += p1board[i].dmg
                            pygame.display.update()
                            sleep(0.5)
                        # Sprinter movement p1
                        if 'sprinter' in p1board[i].sigillist:
                            if i != 3:
                                if p1board[i+1] == ():
                                    p1board[i+1] = p1board[i]
                                    p1board[i] = ()
                                    sprintertemp = True
                                else:
                                    if i != 1:
                                        if p1board[i-1] == ():
                                            p1board[i-1] = p1board[i]
                                            p1board[i] = ()
                            else:
                                if p1board[i-1] == ():
                                    p1board[i - 1] = p1board[i]
                                    p1board[i] = ()

            else: # Player 2 attack
                for i in range(4):
                    if sprintertemp:
                        sprintertemp = False
                        continue
                    if p2board[i] != ():
                        if p2board[i].dmg > 0: # Only do attack animation if they attack
                            updateboard(p1turn)
                            pygame.draw.rect(screen, (0, 0, 0), eval('emptysquareint'+str(i+1)))
                            displaycard(p2board[i], ((300 * (i + 1)) + 60), 400)
                            if p1board[3 - i] != ():
                                if not 'airborne' in p2board[i].sigillist:
                                    p1board[3 - i].takedmg(p2board[i])
                                else:
                                    if 'mighty_leap' in p2board[i].sigillist:
                                        p1board[3 - i].takedmg(p2board[i])
                                    else:
                                        p1teeth += p2board[i].dmg
                            else:
                                p1teeth += p2board[i].dmg
                            pygame.display.update()
                            sleep(0.5)
                        # Sprinter movement p2
                        if 'sprinter' in p2board[i].sigillist:
                            if i != 3:
                                if p2board[i + 1] == ():
                                    p2board[i + 1] = p2board[i]
                                    p2board[i] = ()
                                    sprintertemp = True
                                else:
                                    if i != 1:
                                        if p2board[i - 1] == ():
                                            p2board[i - 1] = p2board[i]
                                            p2board[i] = ()
                            else:
                                if p2board[i - 1] == ():
                                    p2board[i - 1] = p2board[i]
                                    p2board[i] = ()

            updateboard(p1turn)
            pygame.display.update()
            sleep(1)
            # Fledgling sigil check
            p1turn = not p1turn
            turnstage = 0


        # Switches to the current player's hand if not in play stage
        elif viewhand_button.draw():
            if p1turn:
                state = 1
            else:
                state = 2

        # Draw Stage
        if turnstage == 0:
            if normaldeck_button.draw(): # If the player draws a normal card
                if p1turn:
                    # Draws a card or starvation card
                    temp = draw(p1deck)
                    try:
                        p1hand.append(temp[0])
                        p1deck.remove(p1deck[temp[1]])
                    except:
                        p1hand.append(temp)
                    displaycard(p1hand[-1], 1580, 600)
                    pygame.display.update()
                    sleep(1) # Displays the drawn card for 1 second (all other actions paused)
                else:
                    # Draws a card or starvation card
                    temp = draw(p2deck)
                    try:
                        p2hand.append(temp[0])
                        p2deck.remove(p2deck[temp[1]])
                    except:
                        p2hand.append(temp)
                    displaycard(p2hand[-1], 1580, 600)
                    pygame.display.update()
                    sleep(1) # Displays the drawn card for 1 second (all other actions paused)
                turnstage = 1 # Draw stage is done, move to card selection
            elif squirreldeck_button.draw(): # If player draws from squirrel deck
                if p1turn:
                    p1hand.append(Card(squirrel))
                    displaycard(p1hand[-1], 1580, 600)
                    pygame.display.update()
                    sleep(1)  # Displays the drawn card for 1 second (all other actions paused)
                else:
                    p2hand.append(Card(squirrel))
                    displaycard(p2hand[-1], 1580, 600)
                    pygame.display.update()
                    sleep(1)  # Displays the drawn card for 1 second (all other actions paused)
                turnstage = 1 # Draw stage is done, move to card selection


    # Displays player 1's hand
    elif state == 1:
        # Player 1 Hand text in top left
        state1text = font.render('Player 1 Hand', True, (255, 255, 255))
        screen.blit(state1text, (0, 0))

        # Displays all cards in player 1's hand (old code)
        #for i in range(len(p1hand)):
        #    x = ((1920//(len(p1hand)+1))*(i+1))-150 # Equally spaced out on the screen
        #    y = 315 # Same y value
        #    displaycard(p1hand[i], x, y)

        # Displays all cards in player 1's hand as clickable buttons
        for i in range(len(p1hand)):
            x = ((1920 // (len(p1hand) + 1)) * (i + 1)) - 150  # Equally spaced out on the screen
            y = 315 # Same y value
            cardbuttonimg = pygame.image.load(Path('OtherSprites/blankinscryptioncard.png'))
            cardbutton = Button(x, y, cardbuttonimg, cardbuttonimg, 1)
            cardbuttonvar = cardbutton.draw()
            displaycard(p1hand[i], x, y)  # Draws over the invisible button with the card
            if cardbuttonvar:
                selectedcard = i
                state = 3 # Play state


        # Moves back to board view
        if viewboard_button.draw():
            state = 0

    # Displays player 2's hand
    elif state == 2:
        # Player 2 Hand text in top left
        state2text = font.render('Player 2 Hand', True, (255, 255, 255))
        screen.blit(state2text, (0, 0))

        # Displays all cards in player 2's hand (old code)
        #for i in range(len(p2hand)):
        #    x = ((1920//(len(p2hand)+1))*(i+1))-150
        #    y = 315
        #    displaycard(p2hand[i], x, y)

        # Displays all cards in player 2's hand as clickable buttons
        for i in range(len(p2hand)):
            x = ((1920 // (len(p2hand) + 1)) * (i + 1)) - 150  # Equally spaced out on the screen
            y = 315  # Same y value
            cardbuttonimg = pygame.image.load(Path('OtherSprites/blankinscryptioncard.png'))
            cardbutton = Button(x, y, cardbuttonimg, cardbuttonimg, 1)
            cardbuttonvar = cardbutton.draw()
            displaycard(p2hand[i], x, y)  # Draws over the invisible button with the card
            if cardbuttonvar:
                selectedcard = i
                state = 3  # Play state

        # Moves back to board view
        if viewboard_button.draw():
            state = 0


    # Selecting a spot to play a card (both p1 and p2)
    elif state == 3:
        # Draws board squares and cards
        updateboard(p1turn)

        # Creates temporary variable for on play sigils
        cardplayed = False

        # Draws invisible buttons over the 4 card spaces on the bottom
        inviscardimg = pygame.image.load(Path('OtherSprites/blankinscryptioncard.png'))
        cardspace1button = Button(370, 585, inviscardimg, inviscardimg, 1)
        cardspace2button = Button(670, 585, inviscardimg, inviscardimg, 1)
        cardspace3button = Button(970, 585, inviscardimg, inviscardimg, 1)
        cardspace4button = Button(1270, 585, inviscardimg, inviscardimg, 1)

        if p1turn: # Player 1 playing functionality
            # Back button
            if backbutton.draw():
                state = 1

            if firstplayloop:
                tempblood = p1hand[selectedcard].blood
                firstplayloop = False

            # Draws selected card to screen (p1)
            displaycard(p1hand[selectedcard], 50, 315)

            if cardspace1button.draw():
                if p1board[0] == ():
                    if tempblood <= 0:
                        if p1hand[selectedcard].bones <= p1bones:
                            p1bones -= p1hand[selectedcard].bones
                            p1board[0] = p1hand[selectedcard]
                            p1hand.pop(selectedcard)
                            cardplayed = True
                            newcard = p1board[0]
                            newspace = 0
                            firstplayloop = True
                            state = 0
                else:
                    if p1board[0].sacrificable:
                        if 'worthy_sacrifice' not in p1board[0].sigillist:
                            tempblood -= 1
                        else:
                            tempblood -= 3
                        if 'many_lives' not in p1board[0].sigillist:
                            p1board[0].hp = 0 # Kill card (will be removed next board update)
            elif cardspace2button.draw():
                if p1board[1] == ():
                    if tempblood <= 0:
                        if p1hand[selectedcard].bones <= p1bones:
                            p1bones -= p1hand[selectedcard].bones
                            p1board[1] = p1hand[selectedcard]
                            p1hand.pop(selectedcard)
                            cardplayed = True
                            newcard = p1board[1]
                            newspace = 1
                            firstplayloop = True
                            state = 0
                else:
                    if p1board[1].sacrificable:
                        if 'worthy_sacrifice' not in p1board[1].sigillist:
                            tempblood -= 1
                        else:
                            tempblood -= 3
                        if 'many_lives' not in p1board[1].sigillist:
                            p1board[1].hp = 0 # Kill card (will be removed next board update)
            elif cardspace3button.draw():
                if p1board[2] == ():
                    if tempblood <= 0:
                        if p1hand[selectedcard].bones <= p1bones:
                            p1bones -= p1hand[selectedcard].bones
                            p1board[2] = p1hand[selectedcard]
                            p1hand.pop(selectedcard)
                            cardplayed = True
                            newcard = p1board[2]
                            newspace = 2
                            firstplayloop = True
                            state = 0
                else:
                    if p1board[2].sacrificable:
                        if 'worthy_sacrifice' not in p1board[2].sigillist:
                            tempblood -= 1
                        else:
                            tempblood -= 3
                        if 'many_lives' not in p1board[2].sigillist:
                            p1board[2].hp = 0 # Kill card (will be removed next board update)
            elif cardspace4button.draw():
                if p1board[3] == ():
                    if tempblood <= 0:
                        if p1hand[selectedcard].bones <= p1bones:
                            p1bones -= p1hand[selectedcard].bones
                            p1board[3] = p1hand[selectedcard]
                            p1hand.pop(selectedcard)
                            cardplayed = True
                            newcard = p1board[3]
                            newspace = 3
                            firstplayloop = True
                            state = 0
                else:
                    if p1board[3].sacrificable:
                        if 'worthy_sacrifice' not in p1board[3].sigillist:
                            tempblood -= 1
                        else:
                            tempblood -= 3
                        if 'many_lives' not in p1board[3].sigillist:
                            p1board[3].hp = 0 # Kill card (will be removed next board update)

            # Checking on play sigils (p1)
            if cardplayed:
                if 'rabbit_hole' in newcard.sigillist:
                    p1hand.append(Card(rabbit))
                if 'fecundity' in newcard.sigillist:
                    p1hand.append(newcard)
                if 'ant_spawner' in newcard.sigillist:
                    p1hand.append(Card(worker_ant))
                cardplayed = False

        else: # Player 2 playing functionality
            # Back button
            if backbutton.draw():
                state = 2

            if firstplayloop:
                tempblood = p2hand[selectedcard].blood
                firstplayloop = False

            # Draws selected card to screen (p2)
            displaycard(p2hand[selectedcard], 50, 315)

            if cardspace1button.draw():
                if p2board[0] == ():
                    if tempblood <= 0:
                        if p2hand[selectedcard].bones <= p2bones:
                            p2bones -= p2hand[selectedcard].bones
                            p2board[0] = p2hand[selectedcard]
                            p2hand.pop(selectedcard)
                            cardplayed = True
                            newcard = p2board[0]
                            newspace = 0
                            firstplayloop = True
                            state = 0
                else:
                    if p2board[0].sacrificable:
                        if 'worthy_sacrifice' not in p2board[0].sigillist:
                            tempblood -= 1
                        else:
                            tempblood -= 3
                        if 'many_lives' not in p2board[0].sigillist:
                            p2board[0].hp = 0 # Kill card (will be removed next board update)
            elif cardspace2button.draw():
                if p2board[1] == ():
                    if tempblood <= 0:
                        if p2hand[selectedcard].bones <= p2bones:
                            p2bones -= p2hand[selectedcard].bones
                            p2board[1] = p2hand[selectedcard]
                            p2hand.pop(selectedcard)
                            cardplayed = True
                            newcard = p2board[1]
                            newspace = 1
                            firstplayloop = True
                            state = 0
                else:
                    if p2board[1].sacrificable:
                        if 'worthy_sacrifice' not in p2board[1].sigillist:
                            tempblood -= 1
                        else:
                            tempblood -= 3
                        if 'many_lives' not in p2board[1].sigillist:
                            p2board[1].hp = 0 # Kill card (will be removed next board update)
            elif cardspace3button.draw():
                if p2board[2] == ():
                    if tempblood <= 0:
                        if p2hand[selectedcard].bones <= p2bones:
                            p2bones -= p2hand[selectedcard].bones
                            p2board[2] = p2hand[selectedcard]
                            p2hand.pop(selectedcard)
                            cardplayed = True
                            newcard = p2board[2]
                            newspace = 2
                            firstplayloop = True
                            state = 0
                else:
                    if p2board[2].sacrificable:
                        if 'worthy_sacrifice' not in p2board[2].sigillist:
                            tempblood -= 1
                        else:
                            tempblood -= 3
                        if 'many_lives' not in p2board[2].sigillist:
                            p2board[2].hp = 0 # Kill card (will be removed next board update)
            elif cardspace4button.draw():
                if p2board[3] == ():
                    if tempblood <= 0:
                        if p2hand[selectedcard].bones <= p2bones:
                            p2bones -= p2hand[selectedcard].bones
                            p2board[3] = p2hand[selectedcard]
                            p2hand.pop(selectedcard)
                            cardplayed = True
                            newcard = p2board[3]
                            newspace = 3
                            firstplayloop = True
                            state = 0
                else:
                    if p2board[3].sacrificable:
                        if 'worthy_sacrifice' not in p2board[3].sigillist:
                            tempblood -= 1
                        else:
                            tempblood -= 3
                        if 'many_lives' not in p2board[3].sigillist:
                            p2board[3].hp = 0 # Kill card (will be removed next board update)

            # Checking on play sigils (p2)
            if cardplayed:
                if 'rabbit_hole' in newcard.sigillist:
                    p2hand.append(Card(rabbit))
                if 'fecundity' in newcard.sigillist:
                    p2hand.append(newcard)
                if 'ant_spawner' in newcard.sigillist:
                    p2hand.append(Card(worker_ant))
                cardplayed = False


    elif state == 4: # Title Screen
        screen.blit(pygame.image.load(Path('OtherSprites/title_background.jpg')), (0, 0))

        if title_play_button.draw():
            state = 0

        if title_options_button.draw():
            state = 5

        if title_quit_button.draw():
            run = False


    elif state == 5: # Options menu
        if backbutton.draw():
            state = 4


    else: # If no valid state is selected failsafe
        state0text = font.render('how did you get here you are softlocked', True, (255, 255, 255))
        screen.blit(state0text, (0, 0))


    # Key detection
    key = pygame.key.get_pressed()
    if key[pygame.K_BACKQUOTE]:
        toggledev = True  # Activates toggle flag
    else: # When no keys are held
        if toggledev:
            devmode = not devmode # Inverted boolean
            toggledev = False
    if devmode:
        if key[pygame.K_0]:
            state = 0
        elif key[pygame.K_1]:
            state = 1
        elif key[pygame.K_2]:
            state = 2
        elif key[pygame.K_o]:
            p1turn = True
        elif key[pygame.K_p]:
            p1turn = False
        elif key[pygame.K_SPACE]: # Doesn't work
            if p1turn:
                p1hand.append(draw(p1deck))
            else:
                p2hand.append(draw(p2deck))

    # First draw puts both hands to 4 cards, 1 squirrel and 3 random
    if firstdraw == True:
        p1hand.append(Card(squirrel))
        for i in range(3):
            temp = draw(p1deck)
            try:
                p1hand.append(temp[0])
                p1deck.remove(p1deck[temp[1]])
            except:
                p1hand.append(temp)
        p2hand.append(Card(squirrel))
        for i in range(3):
            temp = draw(p2deck)
            try:
                p2hand.append(temp[0])
                p2deck.remove(p2deck[temp[1]])
            except:
                p2hand.append(temp)

        firstdraw = False # Only happens once

    # Loss detection
    if p1teeth+5 <= p2teeth: # Damage, player loses when teeth exceeds other player by 5
        print("Player 1 wins!")
        run = False
    elif p2teeth+5 <= p1teeth:
        print("Player 2 wins!")
        run = False


    for event in pygame.event.get():
        # If windows X button is used
        if event.type == pygame.QUIT:
            run = False

    # Updates visual display every game loop (tick)
    pygame.display.update()

pygame.quit()

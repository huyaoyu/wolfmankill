
#
# Wolf man kill assistant.
# 
# Author
# ======
#
# Yaoyu Hu <huyaoyu@sjtu.edu.cn>
#
# Date
# ====
#
# Created:  2017-04-02
# Modified: 2017-04-04
# 

import sys
import random
from copy import deepcopy


# Constants

ROLE_UNDEFINED = 0
ROLE_REFEREE   = 0
ROLE_WOLF      = 1
ROLE_PEASANT   = 2
ROLE_PROPHET   = 3
ROLE_WITCH     = 4
ROLE_HUNTER    = 5
ROLE_GUARDIAN  = 6
ROLE_SHERIFF   = 7

ROLE_TYPE_REFEREE = 0
ROLE_TYPE_PEASANT = 1
ROLE_TYPE_WOLF    = 2
ROLE_TYPE_WIZARD  = 3
ROLE_TYPE_DUMMY   = 4

SHERIFF_ID = 0
REFEREE_ID = 0

NUM_WOLF    = 4
NUM_PEASANT = 4
NUM_WIZARD  = 4

TOTAL_PLAYERS = NUM_WOLF + NUM_PEASANT + NUM_WIZARD

players = [ [0] for i in range(TOTAL_PLAYERS) ]

def integer_from_raw_input(prompt = ">>> ", flagLimit = 0, limitMin = 1, limitMax = 2):
	"""Get an integer from raw input."""

	if 1 == flagLimit:
		if limitMin > limitMax:
			print "The limit values are wrong: min = %d, max = %d.\n" & (limitMin, limitMax)
			return -1

	valueObtained = 0

	while 0 == valueObtained:
		str = raw_input(prompt)

		try:
			val = int(str)

			if 1 == flagLimit:
				if val < limitMin or val > limitMax:
					print "The value should be in the range of (%d, %d).\n" % (limitMin, limitMax)
					print "Please re-input."
				else:
					valueObtained = 1
			else:
				valueObtained = 1

		except ValueError:
			print "Please input an integer."

			if 1 == flagLimit:
				print "min = %d, max = %d\n" % (limitMin, limitMax)

	return val


def print_delimiter(c):
	"""Print a dummy delimiter"""

	print " "

	for i in range(30):
		print c,

	print " "
	print " "

def find_killed(p):
	"""Return the killed player id."""

	nPlayers = len(p)

	for i in range(nPlayers):
		if p[i].killed == 1:
			return i

	return -1

def find_player_by_id(p, id):
	"""Find a player by id."""

	nPlayers = len(p)

	for i in range(nPlayers):
		if p[i].id == id:
			return i

	return -1

def find_player_by_role(p, r):
	"""Find an active player by role type."""

	nPlayers = len(p)

	for i in range(nPlayers):
		if p[i].state == 1 and p[i].role == r:
			return i

	return -1

class Player(object):
	"""Base class of player."""
	def __init__(self, id, t, r, name):
		
		self.id        = id
		self.state     = 1 # Inactive.
		self.dead      = 0
		self.killed    = 0
		self.saved     = 0 # Used for the Witch.
		self.poisoned  = 0
		self.type      = t
		self.role      = r
		self.name      = name
		self.guarded   = 0
		self.hunted    = 0
		self.isSheriff = 0

		self.idx       = -1

	def set_idx(self, idx):
		self.idx = idx

	def is_dead(self):
		if self.poisoned == 1 or self.hunted == 1:
			self.dead = 1
		elif self.killed == 1 and self.saved == 0 and self.guarded == 0:
			self.dead = 1
		elif self.saved == 1 and self.guarded == 1:
			self.dead = 1

		return self.dead

		
	def set_state(self, s):
		"""
		Set the state of the player.

		s = 1: Active.
		s = 0: Inactive.
		"""

		if s == 1 or s == 0:
			self.state = s
		else:
			print "Player:set_state:Wrong s value. s = %d." % (s)

	def set_kill(self):
		self.killed = 1

	def clear_kill(self):
		self.killed = 0

	def set_saved(self):
		self.saved = 1

	def set_poison(self):
		self.poisoned = 1

	def set_guard(self):
		self.guarded = 1

	def get_guard_status(self):
		return self.guarded

	def set_hunt(self):
		self.hunted = 1

	def reset(self):
		"""Reset."""

		self.killed   = 0
		self.saved    = 0
		self.poisoned = 0
		self.guarded  = 0
		self.hunted   = 0

	def show_id(self):
		"""Show the id."""

		print "ID = %d" % (self.id)

	def perform(self, p, rn):
		"""
		Perform the player's action.

		rn: the round number, integer, starts from 1.
		"""

	def take_effect(self, p):
		"""Take effect of the performed action."""

	def get_info_string(self):
		"""Return a string containing the informatin."""

class Referee(Player):
	"""Class of the Referee."""
	def __init__(self, id):
		super(Referee, self).__init__(id, ROLE_TYPE_REFEREE, ROLE_REFEREE, "Referee")
	
		self.toVote        = 0
		self.votedPlayerId = 0
		self.votedPlayerName = ""
		self.votedPlayerIsSheriff = 0
		self.toFlush       = 0
		self.votedPlayerIdx = -1

	def set_vote(self):
		self.toVote = 1

	def clear_vote(self):
		self.toVote = 0

	def set_flush(self):
		self.toFlush = 1

	def clear_flush(self):
		self.toFlush = 0

	def vote(self, p, rn):
		"""Vote."""

		self.votedPlayerId = integer_from_raw_input(flagLimit = 1, limitMin = 0, limitMax = TOTAL_PLAYERS)
	
	def take_effect(self, p):
		"""Take effect of the Referee."""

		if self.toVote == 1 and self.votedPlayerId != 0:
			self.votedPlayerIdx = find_player_by_id(p, self.votedPlayerId)

			p[self.votedPlayerIdx].state = 0

			self.votedPlayerName = p[self.votedPlayerIdx].name
			self.votedPlayerIsSheriff = p[self.votedPlayerIdx].isSheriff
		else:
			self.votedPlayerIdx = -1
			self.votedPlayerName = "Nobody"
			self.votedPlayerIsSheriff = 0

		if self.toFlush == 1:
			flush_players(p)

	def get_info_string(self):
		"""Return the info string of the Referee."""

		str = "%s\n" % (self.name)

		if self.toVote == 1:
			temp = "Input vote result. The voted player id is %d(%s %d).\n" \
			% (self.votedPlayerId, self.votedPlayerName, self.votedPlayerIsSheriff)
			str += temp

		if self.toFlush == 1:
			temp = "%s (system) flush the states of the players.\n" % (self.name)
			str += temp

		return str

class Peasant(Player):
	"""Class for peasant."""
	def __init__(self, id):
		super(Peasant, self).__init__(id, ROLE_TYPE_PEASANT, ROLE_PEASANT, "Peasant")


class Wolf(Player):
	"""Class for wolf."""
	def __init__(self, id):
		super(Wolf, self).__init__(id, ROLE_TYPE_WOLF, ROLE_WOLF, "Wolf man")
		
		self.lineFirstRound  = "Please check your teammates."
		self.lineNormalRound = "Please designate which one do you want to kill."

		self.toBeKilled = 0 # The selected killed player id.
		self.toBeKilledName = ""
		self.toBeKilledIsSheriff = 0

	def perform(self, p, rn):
		"""Perform the action of the wolf man."""

		print "Night No. %d." % (rn)

		print self.name
		print "Please open your eyes and look at me."
		
		if rn == 1:
			print self.lineFirstRound

		print self.lineNormalRound

		print "Are you sure? Please close your eyes."

		self.toBeKilled = integer_from_raw_input(flagLimit = 1, limitMin = 0, limitMax = TOTAL_PLAYERS)

	def take_effect(self, p):
		"""Take effect of the Wolfman."""

		idx = find_player_by_id(p, self.toBeKilled)

		if idx != -1:
			p[idx].set_kill()

			self.toBeKilledName = p[idx].name

		# Copy specific properties.

		p[self.idx].toBeKilled          = self.toBeKilled
		p[self.idx].toBeKilledName      = self.toBeKilledName
		p[self.idx].toBeKilledIsSheriff = self.toBeKilledIsSheriff

	def get_info_string(self):
		"""Return the info string of the Wolfman."""

		str = "%s\nThe wolfmen decided to kill the player with id %d(%s %d).\n" \
		% (self.name, self.toBeKilled, self.toBeKilledName, self.toBeKilledIsSheriff)

		return str


class Prophet(Player):
	"""Class for prophet"""
	def __init__(self, id):
		super(Prophet, self).__init__(id, ROLE_TYPE_WIZARD, ROLE_PROPHET, "Prophet")	
		
		self.lineFirstRound  = "This gesture means wolf man, and this means not. Do you understand?" 
		self.lineNormalRound = "Which player do you want to verify?"

		self.idChecked   = 0  # The player id the Prophet want to check.
		self.checkResult = "" # The check result messange.

	def perform(self, p, rn):
		"""Perform the action of the prophet."""

		print "Night No. %d." % (rn)

		print self.name

		self.show_id()

		print "Please open your eyes and look at me."

		if rn == 1:
			print self.lineFirstRound

		print self.lineNormalRound

		if self.state == 0:
			print "(*** The Prophet is dead. ***)"

		self.idChecked = integer_from_raw_input(flagLimit = 1, limitMin = 1, limitMax = TOTAL_PLAYERS)

		idx = find_player_by_id(p, self.idChecked)

		print "This player's result is: (Make the gesture)"
		print " "

		if self.state == 1:
			if p[idx].type == ROLE_TYPE_WOLF:
				self.checkResult = "*** Wolf man. ***"
			else:
				self.checkResult = "*** Not a wolf man. ***"
		else:
			self.checkResult = "(*** The Prophet is dead. No result will be shown. ***)"

		print self.checkResult

		print " "

		print "Please close your eyes."

		str = raw_input("Press Enter.")

	def take_effect(self, p):
		"""Take effect of the Prophet."""

		# Copy specific properties.

		p[self.idx].idChecked   = self.idChecked
		p[self.idx].checkResult = self.checkResult

	def get_info_string(self):
		"""Return the info string of the Prophet."""

		str = "%s(%2d %d)\n" % (self.name, self.id, self.isSheriff)

		if self.state == 0:
			temp = "The %s is dead.\n" % (self.name)
			str += temp
			return str

		temp = "The checked player id is %d.\nResult: %s.\n" % (self.idChecked, self.checkResult)
		str += temp

		return str


class Witch(Player):
	"""Class for witch"""
	def __init__(self, id):
		super(Witch, self).__init__(id, ROLE_TYPE_WIZARD, ROLE_WITCH, "Witch")

		self.haveUsedAntidote = 0
		self.haveUsedPoison   = 0
		self.killedIdx        = -1
		self.toUseAntidote    = 0
		self.toUsePoison      = 0
		self.toUsePoisonPlayerId = 0
		self.toUsePoisonPlayerName = ""
		self.toUsePoisonPlayerIsSheriff = 0
		self.currentRoundUseAntidote = 0
		self.isKilled = 0

	def use_antidote(self):
		"""Mark the use of antidote."""

		self.haveUsedAntidote = 1

	def use_poison(self):
		"""Mark the use of poison."""

		self.haveUsedPoison = 1
		
	def perform(self, p, rn):
		"""Perform the action of the witch."""

		print "Night No. %d." % (rn)

		print self.name

		self.show_id()

		print "Please open your eyes and look at me."

		if self.state == 0:
			print "(*** The Witch is dead. ***)"

		self.killedIdx = find_killed(p)

		print "Last night, this player was killed by the wolf man."

		if self.haveUsedAntidote == 1 or self.killedIdx < 0:
			print "(*** DO NOT SHOW THE DEAD PLAYER'S ID ***)"
		else:
			print "(The killed player id is %d.)" % (p[self.killedIdx].id)
			if p[self.killedIdx].id == self.id:
				print "(The Witch is killed this night!)"
				self.isKilled = 1
			else:
				self.isKilled = 0

		print "You have a bottle of antidote and a bottle of poison."

		print "Do you want to use the antidote? ( 1 - Use. 2 - Do not use.)"

		print "Are you sure?"

		self.currentRoundUseAntidote = 0

		val = integer_from_raw_input(flagLimit = 1, limitMin = 1, limitMax = 2)

		if val == 1 and self.haveUsedAntidote == 0:
			self.toUseAntidote = 1
		elif val == 2:
			self.toUseAntidote = 0
		else:
			self.toUseAntidote = 0

		print "Do you want to use the poison? ( 1 - Use. 2 - Do not use.)"

		if self.haveUsedPoison == 1:
			print "(*** THE POISON HAS BEEN USED ***)"

		val1 = integer_from_raw_input(flagLimit = 1, limitMin = 1, limitMax = 2)

		print "To which player do you want to poison?"
		print "Are you sure?"

		val2 = integer_from_raw_input(flagLimit = 1, limitMin = 1, limitMax = TOTAL_PLAYERS)

		if val1 == 1 and self.haveUsedPoison == 0 and self.toUseAntidote == 0:
			self.toUsePoison = 1
		else:
			self.toUsePoison = 0

		self.toUsePoisonPlayerId = val2
			

		print "Please close your eyes."

	def take_effect(self, p):
		"""Take effect of the Witch."""

		if self.toUseAntidote == 1:
			p[self.killedIdx].set_saved()

			self.haveUsedAntidote = 1
			self.currentRoundUseAntidote = 1

		if self.toUsePoison == 1:
			if self.haveUsedPoison == 0 and self.currentRoundUseAntidote == 0:
				idx = find_player_by_id(p, self.toUsePoisonPlayerId)

				p[idx].set_poison()

				self.toUsePoisonPlayerName = p[idx].name
				self.toUsePoisonPlayerIsSheriff = p[idx].isSheriff

				self.haveUsedPoison = 1

		# self.currentRoundUseAntidote = 0

		# Copy specific properties.
		p[self.idx].haveUsedAntidote           = self.haveUsedAntidote
		p[self.idx].haveUsedPoison             = self.haveUsedPoison
		p[self.idx].killedIdx                  = self.killedIdx
		p[self.idx].toUseAntidote              = self.toUseAntidote
		p[self.idx].toUsePoison                = self.toUsePoison
		p[self.idx].toUsePoisonPlayerId        = self.toUsePoisonPlayerId
		p[self.idx].toUsePoisonPlayerName      = self.toUsePoisonPlayerName
		p[self.idx].toUsePoisonPlayerIsSheriff = self.toUsePoisonPlayerIsSheriff
		p[self.idx].currentRoundUseAntidote    = self.currentRoundUseAntidote
		p[self.idx].isKilled                   = self.isKilled


	def get_info_string(self):
		"""Return the info string of the Witch."""

		str = "%s(%2d %d)\n" % (self.name, self.id, self.isSheriff)

		if self.state == 0:
			temp = "The %s is dead.\n" % (self.name)
			str += temp
			return str

		if self.isKilled == 1:
			temp = "The %s is killed this night. Cannot use the antidote to himself/herself.\n" % (self.name)
			str += temp

		if self.toUseAntidote == 0 and self.haveUsedAntidote == 1:
			temp = "The antidote has been used. %s do not know which player is killed last night.\n" % (self.name)
		else:
			temp = "The antidote is ready.\n"

		str += temp

		if self.toUseAntidote == 1:
			temp = "Use antidote.\n"
		else:
			temp = "Do not use antidote.\n"

		str += temp

		if self.toUsePoison == 0 and self.haveUsedPoison == 1:
			temp = "The poison has been used.\n"
			str += temp

		if self.currentRoundUseAntidote == 1:
			temp = "Current round had used antidote. \n"
			str += temp
		
		if self.toUsePoison == 1 and self.haveUsedPoison == 1 and self.currentRoundUseAntidote == 0:
			temp = "The poison is ready.\n"
			str += temp

		if self.toUsePoison == 1 and self.currentRoundUseAntidote == 0 and self.haveUsedPoison == 1:
			temp = "Use the poison to player id %d(%s %d).\n" \
			% (self.toUsePoisonPlayerId, self.toUsePoisonPlayerName, self.toUsePoisonPlayerIsSheriff)
		else:
			temp = "Do not use the poison.\n"

		str += temp

		return str


class Hunter(Player):
	"""Class for the hunter"""
	def __init__(self, id):
		super(Hunter, self).__init__(id, ROLE_TYPE_WIZARD, ROLE_HUNTER, "Hunter")
		
		self.lineFirstRound  = "This gesture means you can make the hunt."
		self.lineNormalRound = "Your status at last night is this. "

		self.canHunt = 0
		self.daylight = 0

		self.huntTaken = 0

		self.toHunt         = 0
		self.toHuntPlayerId = 0
		self.toHuntPlayerName = ""
		self.toHuntPlayerIsSheriff = 0

	def set_hunt(self):
		self.huntTaken = 1

	def perform(self, p, rn):
		"""Perform the action of the hunter."""

		if self.huntTaken == 1:
			return

		print "Night No. %d." % (rn)

		print self.name

		self.show_id()

		print "Please open your eyes and look at me."

		if self.state == 0:
			print "(*** The Hunter is dead! ***)"

		if rn == 1:
			print self.lineFirstRound

		print self.lineNormalRound

		if self.state == 1:
			if self.poisoned == 0:
				if self.killed == 1:
					if self.guarded == 0 and self.saved == 0:
						print "(Make the gesture.)"
						self.canHunt = 1
					elif self.guarded == 1 and self.saved == 1:
						print "(Make the gesture.)"
						self.canHunt = 1
					else:
						print "(No gesture.)"
						self.canHunt = 0
				else:
					print "(No gesture.)"
					self.canHunt = 0
		else:
			print "(No gesture.)"
			self.canHunt = 0

		print "Do you want to take the hunt? ( 1 - Take. 2 - Do not take.)"

		val = integer_from_raw_input(flagLimit = 1, limitMin = 1, limitMax = 2)

		# if self.state == 1:
		# 	if self.poisoned == 0:
		# 		if self.killed == 1 and val == 1:
		# 			if self.guarded == 0 and self.saved == 0:
		# 				self.toHunt = 1
		# 			elif self.guarded == 1 and self.saved == 1:
		# 				self.toHunt = 1

		if self.canHunt == 1 and val == 1:
			self.toHunt = 1
		else:
			self.toHunt = 0

		print "On which player do you want to take the hunt?"
		print "Are you sure?"

		self.toHuntPlayerId = integer_from_raw_input(flagLimit = 1, limitMin = 1, limitMax = TOTAL_PLAYERS)

		print "Please close your eyes."


	def perform_daylight(self, p, rn):
		"""Perform the action of the hunter in the day light."""

		self.daylight = 1

		print "Night No. %d." % (rn)

		print self.name

		self.show_id()

		self.canHunt = 1

		print "Do you want to take the hunt? ( 1 - Take. 2 - Do not take.)"

		val = integer_from_raw_input(flagLimit = 1, limitMin = 1, limitMax = 2)

		if val == 1:
			print "On which player do you want to take the hunt?"
			print "Are you sure?"
			self.toHunt = 1
			self.toHuntPlayerId = integer_from_raw_input(flagLimit = 1, limitMin = 1, limitMax = TOTAL_PLAYERS)
		else:
			self.toHunt = 0

	def take_effect(self, p):
		"""Take effect of the Hunter."""

		if self.canHunt == 1 and self.toHunt == 1:
			idx = find_player_by_id(p, self.toHuntPlayerId)

			p[idx].set_hunt()

			self.toHuntPlayerName = p[idx].name
			self.toHuntPlayerIsSheriff = p[idx].isSheriff

			self.huntTaken = 1

			# Copy specific properties.
			p[self.idx].canHunt               = self.canHunt
			p[self.idx].daylight              = self.daylight
			p[self.idx].huntTaken             = self.huntTaken
			p[self.idx].toHunt                = self.toHunt
			p[self.idx].toHuntPlayerId        = self.toHuntPlayerId
			p[self.idx].toHuntPlayerName      = self.toHuntPlayerName
			p[self.idx].toHuntPlayerIsSheriff = self.toHuntPlayerIsSheriff

	def get_info_string(self):
		"""Return the info string of the Hunter."""

		str = "%s(%2d %d)\n" % (self.name, self.id, self.isSheriff)

		if self.state == 0 and self.huntTaken == 0:
			temp = "The %s is dead.\n" % (self.name)
			str += temp
		
		if self.daylight == 1:
			temp = "The %s is voted in daylight.\n" % (self.name)
			str += temp

		if self.canHunt == 1:
			temp = "Can hunt.\n"
		else:
			temp = "Cannot hunt.\n"

		str += temp

		if self.toHunt == 1:
			temp = "The %s decided to hunt player id %d(%s %d).\n" \
			% (self.name, self.toHuntPlayerId, self.toHuntPlayerName, self.toHuntPlayerIsSheriff)
		else:
			temp = "The %s decided to not take the shot.\n" % (self.name)

		str += temp

		return str
		

class Guardian(Player):
	"""Class for the guardian."""
	def __init__(self, id):
		super(Guardian, self).__init__(id, ROLE_TYPE_WIZARD, ROLE_GUARDIAN, "Guardian")

		self.lastGuarded = 0

		self.toGuard         = 0
		self.toGuardPlayerId = 0
		self.toGuardPlayerName = ""
		self.toGuardPlayerIsSheriff = 0

	def perform(self, p, rn):
		"""Perform action of the guardian."""

		print "Night No. %d." % (rn)

		print self.name

		self.show_id()

		print "Please open your eyes and look at me."

		print "Which player do you want to guard? ( 0 - Do not guard.)"

		print "Are you sure?"

		print "(Last guarded player id = %d.)" % (self.lastGuarded)

		if self.state == 0:
			print "(*** The Guardian is dead. Please enter 0. ***)"

		self.toGuardPlayerId = self.lastGuarded

		self.toGuard = 1

		while self.toGuardPlayerId == self.lastGuarded:
			self.toGuardPlayerId = integer_from_raw_input(flagLimit = 1, limitMin = 0, limitMax = TOTAL_PLAYERS)

			if self.toGuardPlayerId == self.lastGuarded and self.toGuardPlayerId != 0:
				print "Please select a different player. This player has been guarded last night."
			elif self.toGuardPlayerId == self.lastGuarded and self.toGuardPlayerId == 0:
				self.toGuard = 0
				break

		print "Please close your eyes."

	def take_effect(self, p):
		"""Take effect the Guardian."""

		if self.toGuard == 1:
			idx = find_player_by_id(p, self.toGuardPlayerId)
			p[idx].set_guard()

			self.toGuardPlayerName = p[idx].name
			self.toGuardPlayerIsSheriff = p[idx].isSheriff

		self.lastGuarded = self.toGuardPlayerId

		# Copy specific properties.
		p[self.idx].lastGuarded            = self.lastGuarded
		p[self.idx].toGuard                = self.toGuard
		p[self.idx].toGuardPlayerId        = self.toGuardPlayerId
		p[self.idx].toGuardPlayerName      = self.toGuardPlayerName
		p[self.idx].toGuardPlayerIsSheriff = self.toGuardPlayerIsSheriff


	def get_info_string(self):
		"""Return the info string of the Guardian."""

		str = "%s(%2d %d)\n" % (self.name, self.id, self.isSheriff)

		if self.state == 0:
			temp = "The %s is dead.\n" % (self.name)
			str += temp
			return str

		if self.toGuard == 1:
			temp = "The %s guarded player id %d(%s %d).\n" \
			% (self.name, self.toGuardPlayerId, self.toGuardPlayerName, self.toGuardPlayerIsSheriff)
			if self.toGuardPlayerId == self.id:
				temp += "Self guarded.\n"
		else:
			temp = "The %s guarded nobody.\n" % (self.name)

		str += temp

		return str

class Sheriff(Player):
	"""Class for the Sheriff"""
	def __init__(self, id):
		super(Sheriff, self).__init__(id, ROLE_TYPE_DUMMY, ROLE_SHERIFF, "Sheriff")

		self.reElect = 0
		self.newElected = 0

		self.playerIdx = -1
		self.dead = 0

		self.dayTalkStart = 0

		self.playerName = ""

	def elect(self, p):
		print "The elected Sheriff is (input 0 for no Sheriff.)"

		val = integer_from_raw_input(flagLimit = 1, limitMin = 0, limitMax = TOTAL_PLAYERS)
		self.set_player_id(val)

		self.reElect = 1

	def set_player_id(self, id):
		self.id = id

	def set_palyer_idx(self, idx):
		self.playerIdx = idx

	def perform(self, p, rn):
		self.newElected = 0

		print "Let the Sheriff decide the staring player."

		self.dayTalkStart = integer_from_raw_input(flagLimit = 1, limitMin = 1, limitMax = TOTAL_PLAYERS)
		
	def perform_dead(self, p, rn):
		self.newElected = 0

		print "Let the Sheriff select the new Sheriff."
		self.dead = 1

	def take_effect(self, p):
		"""Take effect of the Sheriff."""

		if self.reElect == 1:
			p[self.playerIdx].isSheriff = 0

			if self.id != 0:
				self.playerIdx = find_player_by_id(p, self.id)
				self.set_palyer_idx(self.playerIdx)
				p[self.playerIdx].isSheriff = 1
				self.playerName = p[self.playerIdx].name
			else:
				self.playerName = "Nobody"

			self.newElected = 1
			self.dead = 0

			self.reElect = 0

		# Copy specific properties.


	def get_info_string(self):
		"""Return the info string of the Sheriff."""

		str = "%s(%2d %s)\n" % (self.name, self.id, self.playerName)

		if self.dead == 1:
			temp = "The %s was dead.\n" % (self.name)
			str += temp

		if self.newElected == 1:
			temp = "Player id %d was elected to be the %s.\n" % (self.id, self.name)
			if self.id == 0:
				temp += "Actually no player is the %s.\n" % (self.name)

			str += temp
		
		if self.dead == 0 and self.newElected == 0:
			temp = "The %s selected player id %d to start talking.\n" % (self.name, self.dayTalkStart)
			str += temp

		return str


class Dumper(object):
	"""docstring for Dumper"""
	def __init__(self):
		self.path = ""

	def set_dump_path(self, path):
		"""Set the path of the dumper."""
		self.path = path

	def prepare(self):
		"""Preparation before dumping operation."""

	def finalize(self):
		"""End the dumping operation."""
		
	def dump(self, str):
		"""Dump str."""

class DumperPlainText(Dumper):
	"""Class DumperPlainText."""
	def __init__(self, fn):
		super(DumperPlainText, self).__init__()
		self.path = fn
		self.fileObj = 0
		self.fileOpened = 0

	def prepare(self):
		"""Open the plain text file for out put. Overwite automatically."""
		self.fileObj = open(self.path, 'w')
		self.fileOpened = 1

	def finalize(self):
		"""Close the plain text file."""

		if self.fileOpened == 1:
			self.fileObj.close()
			self.fileOpend = 0

	def dump(self, str):
		"""Dump str in to a plaine text file."""

		if self.fileOpened == 0:
			print "Error: The file in not opened."
			return

		temp = "\n##########################\n\n"

		self.fileObj.write(temp)
		self.fileObj.write(str)
		

class action(object):
	"""docstring for action"""
	def __init__(self, nDay, bNight, player):
		self.nDay   = nDay
		self.bNight = bNight
		self.player = deepcopy(player)

		self.playerList  = 0
		self.actionTaken = 0

	def take_action(self, playerList, flagSurpassState = 0):
		"""Take the action"""

		self.playerList = deepcopy(playerList)

		if self.player.state == 1 or flagSurpassState == 1:
			self.player.take_effect(self.playerList)

			# # Substitute.
			# if self.player.idx != -1 and self.role != ROLE_SHERIFF:
			# 	self.playerList[self.player.idx] = self.player

			self.actionTaken = 1
		
		
def check_game_status(p):
	"""Check the status of the game. 0 for end of game. 1 for game could continue."""

	nPeasants = 0
	nWizards  = 0
	nWolves   = 0

	voteLimit_Wolfmen    = 0
	voteLimit_NonWolfmen = 0

	for player in p:
		if player.state == 1:
			if player.is_dead() == 0:
				if player.type == ROLE_TYPE_PEASANT:
					nPeasants = nPeasants + 1
					voteLimit_NonWolfmen = voteLimit_NonWolfmen + 1 + 0.5 * player.isSheriff
				elif player.type == ROLE_TYPE_WIZARD:
					nWizards = nWizards + 1
					voteLimit_NonWolfmen = voteLimit_NonWolfmen + 1 + 0.5 * player.isSheriff
				elif player.type == ROLE_TYPE_WOLF:
					nWolves = nWolves + 1
					voteLimit_Wolfmen = voteLimit_Wolfmen + 1 + 0.5 * player.isSheriff


	print "Peasant: %d, Wizards: %d, Wolves: %d" % (nPeasants, nWizards, nWolves)
	print "Vote limit: Wolfmen %1.1f, Non-Wolfmen %1.1f." % (voteLimit_Wolfmen, voteLimit_NonWolfmen)

	if nPeasants == 0 or nWizards == 0 or nWolves == 0:
		return 0
	else:
		return 1


def flush_players(p):
	"""Flush the states of the players."""

	for player in p:
		if player.is_dead() == 1:
			player.state = 0

		if player.state == 0:
			player.dead = 1

		player.reset()

def show_last_night_info(p):
	idxKilled       = -1;
	idxPoisoned     = -1;
	idxHunted       = -1;
	idxDoubleEffect = -1;

	i = 0

	for player in p:
		if player.killed == 1 and player.guarded == 0 and player.saved == 0:
			idxKilled = i
		elif player.poisoned == 1:
			idxPoisoned = i
		elif player.hunted == 1:
			idxHunted = i
		elif player.saved == 1 and player.guarded == 1:
			idxDoubleEffect = i

		i = i + 1

	print "Last night ..."

	if idxKilled != -1:
		print "Player No. %d was dead." % (p[idxKilled].id)

	if idxPoisoned != -1:
		print "Player No. %d was dead." % (p[idxPoisoned].id)

	if idxHunted != -1:
		print "Player No. %d was dead (Hunted by the Hunter)." % (p[idxHunted].id)

		idxHunter = find_player_by_role(p, ROLE_HUNTER)

		print "*** The hunter is Player No. %d." % (p[idxHunter].id)

	if idxDoubleEffect != -1:
		print "Player No. %d was dead (Double effect)." % (p[idxDoubleEffect].id)

	if idxKilled == -1 and idxPoisoned == -1 and idxHunted == -1 and idxDoubleEffect == -1:
		print "Was a peaceful night."

def show_debug_info(p, verbose = 1):
	"""Show the status of p."""

	i = 0

	for player in p:

		if verbose == 1:
			print "idx = %2d, id = %2d (%9s %d), state = %d, killed = %d, saved = %d, poisoned = %d, hunted = %d, guarded = %d." %\
			 (i, player.id, player.name, player.isSheriff, player.state, player.killed, player.saved, player.poisoned, player.hunted, player.guarded)
		else:
			if player.state == 1:
				print "idx = %2d, id = %2d (%9s %d), state = %d, killed = %d, saved = %d, poisoned = %d, hunted = %d, guarded = %d." %\
			 	(i, player.id, player.name, player.isSheriff, player.state, player.killed, player.saved, player.poisoned, player.hunted, player.guarded)

		i = i + 1

if __name__ == '__main__':
	# Manually set player ids and roles

	verbose = 0

	seq = range(1,13)
	random.shuffle(seq)

	# players[ 0] = Peasant(4)
	# players[ 1] = Peasant(6)
	# players[ 2] = Peasant(10)
	# players[ 3] = Peasant(11)
	# players[ 4] = Wolf(3)
	# players[ 5] = Wolf(5)
	# players[ 6] = Wolf(9)
	# players[ 7] = Wolf(12)
	# players[ 8] = Prophet(1)
	# players[ 9] = Witch(8)
	# players[10] = Guardian(2)
	# players[11] = Hunter(7)

	players[ 0] = Peasant(seq[0])
	players[ 1] = Peasant(seq[1])
	players[ 2] = Peasant(seq[2])
	players[ 3] = Peasant(seq[3])
	players[ 4] = Wolf(seq[4])
	players[ 5] = Wolf(seq[5])
	players[ 6] = Wolf(seq[6])
	players[ 7] = Wolf(seq[7])
	players[ 8] = Prophet(seq[8])
	players[ 9] = Witch(seq[9])
	players[10] = Guardian(seq[10])
	players[11] = Hunter(seq[11])

	# The Sheriff
	sh = Sheriff(SHERIFF_ID)
	rf = Referee(REFEREE_ID)

	print_delimiter("#")

	oriPlayersInfo = ""

	for i in range(TOTAL_PLAYERS):

		idx = find_player_by_id(players, i+1)
		players[idx].set_idx(idx)

		temp = "No. %2d, %s\n" % (i+1, players[idx].name)

		oriPlayersInfo += temp

	print oriPlayersInfo

	# Action list
	dummyPlayer = Player(0, -1, -1, "Dummy")
	dummyPlayer.state = 0
	
	actionInitial = action(0, 1, dummyPlayer)
	actionInitial.take_action(players)
	actionList = [actionInitial]

	print_delimiter("#")

	# First round

	idxGuardian = find_player_by_role(players, ROLE_GUARDIAN)
	idxHunter   = find_player_by_role(players, ROLE_HUNTER)
	idxProphet  = find_player_by_role(players, ROLE_PROPHET)
	idxWitch    = find_player_by_role(players, ROLE_WITCH)
	idxOneWolf  = find_player_by_role(players, ROLE_WOLF)

	roundNumber = 0

	sta = 1

	while sta == 1:
		roundNumber = roundNumber + 1

		# Find the Wolfman again.
		idxOneWolf  = find_player_by_role(actionList[-1].playerList, ROLE_WOLF)

		sta = check_game_status(actionList[-1].playerList)

		# ==================== Night. ==========================

		print "It's dark in the night. Please close your eyes."

		# Guardian action.

		print_delimiter("#")
		actionList[-1].playerList[idxGuardian].perform(actionList[-1].playerList, roundNumber)

		actionList.append(action(roundNumber, 1, actionList[-1].playerList[idxGuardian]))
		actionList[-1].take_action(actionList[-2].playerList)

		# Wolf men action.

		print_delimiter("#")
		actionList[-1].playerList[idxOneWolf].perform(actionList[-1].playerList, roundNumber)

		actionList.append(action(roundNumber, 1, actionList[-1].playerList[idxOneWolf]))
		actionList[-1].take_action(actionList[-2].playerList)

		# Prophet action.

		print_delimiter("#")
		actionList[-1].playerList[idxProphet].perform(actionList[-1].playerList, roundNumber)

		actionList.append(action(roundNumber, 1, actionList[-1].playerList[idxProphet]))
		actionList[-1].take_action(actionList[-2].playerList)

		# Witch action.

		print_delimiter("#")
		actionList[-1].playerList[idxWitch].perform(actionList[-1].playerList, roundNumber)

		actionList.append(action(roundNumber, 1, actionList[-1].playerList[idxWitch]))
		actionList[-1].take_action(actionList[-2].playerList)

		print_delimiter("#")

		# ========== Election of the Sheriff. ==============

		if roundNumber == 1:
			print "Please elect the Sheriff."

			print "Starting player ID is %d." % (random.randint(1, TOTAL_PLAYERS))

			dir = random.randint(0,1)

			if dir == 1:
				print "In anti-clockwise direction."
			else:
				print "in clockwise direction."

			sh.elect(actionList[-1].playerList)

			actionList.append(action(roundNumber, 1, sh))
			actionList[-1].take_action(actionList[-2].playerList)

			sh = deepcopy(actionList[-1].player)

			print "Please close your eyes."
			str = raw_input()

		# Hunter action.

		print_delimiter("#")
		if actionList[-1].playerList[idxHunter].state == 0 \
		and actionList[-1].playerList[idxHunter].huntTaken == 1:
			pass
		else:
			actionList[-1].playerList[idxHunter].perform(actionList[-1].playerList, roundNumber)

			actionList.append(action(roundNumber, 1, actionList[-1].playerList[idxHunter]))
			actionList[-1].take_action(actionList[-2].playerList)

		print_delimiter("#")

		show_last_night_info(actionList[-1].playerList)
		show_debug_info(actionList[-1].playerList, verbose)

		# ================== Day time. ===========================

		sta = check_game_status(actionList[-1].playerList)

		if sta == 0:
			print "Game over!"
			# sys.exit()
			break

		print_delimiter("#")

		print "Night No. %d." % (roundNumber)

		# ================= Change the Sheriff. =====================

		if sh.id != 0:
			if actionList[-1].playerList[sh.playerIdx].dead == 1:
				sh.perform_dead(actionList[-1].playerList, roundNumber)

				sh.elect(actionList[-1].playerList)

				actionList.append(action(roundNumber, 1, sh))
				actionList[-1].take_action(actionList[-2].playerList)

				sh = deepcopy(actionList[-1].player)

		print_delimiter("#")

		# ============== Sherfiff action. ========================
		if sh.id != 0:
			sh.perform(actionList[-1].playerList, roundNumber)

			actionList.append(action(roundNumber, 1, sh))
			actionList[-1].take_action(actionList[-2].playerList)

			sh = deepcopy(actionList[-1].player)

		# ============== Voting stage. ======================

		print "Voting stage."

		rf.vote(actionList[-1].playerList, roundNumber)
		rf.set_vote()
		rf.set_flush()

		actionList.append(action(roundNumber, 1, rf))
		actionList[-1].take_action(actionList[-2].playerList)

		rf = deepcopy(actionList[-1].player)

		rf.clear_flush()
		rf.clear_vote()

		show_debug_info(actionList[-1].playerList, verbose)

		sta = check_game_status(actionList[-1].playerList)

		if sta == 0:
			print "Game over!"
			# sys.exit()
			break
		else:
			print "Game continue."

		if rf.votedPlayerIdx != -1 and actionList[-1].playerList[ rf.votedPlayerIdx ].role == ROLE_HUNTER:
			print_delimiter("#")
			print "The Hunter is voted. Let the hunter take the shot."

			actionList[-1].playerList[ rf.votedPlayerIdx ].perform_daylight(actionList[-1].playerList, roundNumber)

			actionList.append(action(roundNumber, 1, actionList[-1].playerList[idxHunter]))
			actionList[-1].take_action(actionList[-2].playerList, flagSurpassState = 1)

			rf.set_flush()
			actionList.append(action(roundNumber, 1, rf))
			actionList[-1].take_action(actionList[-2].playerList)
			rf = deepcopy(actionList[-1].player)
			rf.clear_flush()

			show_debug_info(actionList[-1].playerList, verbose)

			sta = check_game_status(actionList[-1].playerList)

			if sta == 0:
				print "Game over!"
				# sys.exit()
				break
			else:
				print "Game continue."

		# ================= Change the Sheriff. =====================

		if sh.id != 0:
			print_delimiter("#")
			if actionList[-1].playerList[sh.playerIdx].dead == 1:
				sh.perform_dead(actionList[-1].playerList, roundNumber)

				sh.elect(actionList[-1].playerList)

				actionList.append(action(roundNumber, 1, sh))
				actionList[-1].take_action(actionList[-2].playerList)

				sh = deepcopy(actionList[-1].player)

		print_delimiter("#")

	# Game over!

	dp = DumperPlainText("./Replay.txt")

	nActions = len(actionList)

	dp.prepare()

	for i in range(nActions):
		if i == 0:
			dp.dump(oriPlayersInfo)

			continue

		temp = "Day %d, Action %d\n" % (actionList[i].nDay, i)
		dp.dump(temp)

		dp.dump( actionList[i].player.get_info_string() )

	dp.dump("Game over.")

	dp.finalize()

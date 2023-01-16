# ---------------- Database Tables --------------------


class Campaign(db.Model):
    __tablename__ = "campaign"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    subtitle = Column(String(500), nullable=False)
    campaign_image = Column(String, nullable=False)
    page_image = Column(String, nullable=False)
    blurb = Column(Text, nullable=False)
    central_location = Column(String, nullable=False)
    region_summary = Column(Text, nullable=False)
    faction_summary = Column(Text, nullable=False)
    characters = relationship("Character", back_populates="campaign")
    locations = relationship("Location", back_populates="campaign")
    factions = relationship("Faction", back_populates="campaign")
    players = relationship("Player", back_populates="campaign")
    npcs = relationship("NPC", back_populates="campaign")
    sessions = relationship("ScheduledSession", back_populates="campaign")
    sessionreview = relationship("SessionReview", back_populates="campaign")
    house_rules = relationship("HouseRule")


class HouseRule(db.Model):
    __tablename__ = "house_rules"
    id = Column(Integer, primary_key=True)
    character_creation = Column(Text)
    homebrew = Column(Text)
    special = Column(Text)
    races = Column(Text)
    source_material = Column(Text)
    third_party_material = Column(Text)
    campaign_id = Column(Integer, ForeignKey("campaign.id"))


class Player(UserMixin, db.Model):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    characters = relationship("Character", back_populates="player")
    sessionreview = relationship("SessionReview", back_populates="player")
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="players")


class Character(db.Model):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)

    # ----------- Character Details -------------
    name = Column(String(100))
    character_image = Column(String(250), nullable=False)
    token = Column(String(250))
    race = Column(String(50), nullable=False)
    character_class = Column(String(150), nullable=False)
    background = Column(String(50), nullable=False)
    alignment = Column(String(50), nullable=False)
    appearance_summary = Column(String(300), nullable=False)
    personality_traits = Column(String, nullable=False)
    ideals = Column(String, nullable=False)
    bonds = Column(String, nullable=False)
    flaws = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    backstory = Column(Text, nullable=False)
    notes = Column(Text)
    copper = Column(Integer)
    silver = Column(Integer)
    electum = Column(Integer)
    gold = Column(Integer)
    platinum = Column(Integer)

    # ----------- Character Stats ----------------
    level = Column(Integer, nullable=False)
    strength = Column(Integer, nullable=False)
    dexterity = Column(Integer, nullable=False)
    constitution = Column(Integer, nullable=False)
    wisdom = Column(Integer, nullable=False)
    intelligence = Column(Integer, nullable=False)
    charisma = Column(Integer, nullable=False)

    # ----------- Skill Profs --------------------
    acrobatics = Column(Boolean, default=False)
    animal_handling = Column(Boolean, default=False)
    arcana = Column(Boolean, default=False)
    athletics = Column(Boolean, default=False)
    deception = Column(Boolean, default=False)
    history = Column(Boolean, default=False)
    insight = Column(Boolean, default=False)
    intimidation = Column(Boolean, default=False)
    investigation = Column(Boolean, default=False)
    medicine = Column(Boolean, default=False)
    nature = Column(Boolean, default=False)
    perception = Column(Boolean, default=False)
    performance = Column(Boolean, default=False)
    persuasion = Column(Boolean, default=False)
    religion = Column(Boolean, default=False)
    sleight_of_hand = Column(Boolean, default=False)
    stealth = Column(Boolean, default=False)
    survival = Column(Boolean, default=False)
    strength_save = Column(Boolean, default=False)
    dexterity_save = Column(Boolean, default=False)
    constitution_save = Column(Boolean, default=False)
    intelligence_save = Column(Boolean, default=False)
    wisdom_save = Column(Boolean, default=False)
    charisma_save = Column(Boolean, default=False)
    init_bonus = Column(Integer, default=0)
    ac_bonus = Column(Integer, default=0)
    ac_override = Column(Integer, default=0)

    # ------ Skllls, languages and senses --------

    languages = Column(Text, default="Common")
    darkvision = Column(Integer, default=0)
    blindsight = Column(Integer, default=0)
    tremorsense = Column(Integer, default=0)
    truesight = Column(Integer, default=0)
    tool_proficiencies = Column(Text)

    # ------------- Table Relationships ------------
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="characters")
    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="characters")
    actions = relationship("CharacterActions")
    spells = relationship("Spells")
    features = relationship("CharacterFeatures")
    inventory = relationship("CharacterInventory")


class CharacterActions(db.Model):
    __tablename__ = "action"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # Full, bonus, reaction
    damaging_action = Column(Boolean, default=True, nullable=False)  # True or False in table
    saving_action = Column(Boolean, default=False, nullable=False)
    saving_attribute = Column(String(50))  # List Options
    range = Column(String(50))
    target = Column(String(50))
    damage_roll_main = Column(String(50))
    damage_type_main = Column(String(50))
    damage_roll_secondary = Column(String(50))
    damage_type_secondary = Column(String(50))
    character_id = Column(Integer, ForeignKey("characters.id"))


class Spells(db.Model):
    __tablename__ = "spell"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    cast_time = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    range = Column(Integer)  # Note to leave blank for self
    verbal = Column(Boolean, default=True, nullable=False)
    somatic = Column(Boolean, default=True, nullable=False)
    material = Column(Boolean, default=True, nullable=False)
    material_list = Column(String(100))
    level = Column(Integer, nullable=True)
    school = Column(String(50), nullable=True)
    duration = Column(String(50), nullable=True)
    concentration = Column(Boolean, nullable=True)
    damaging = Column(Boolean, nullable=True)
    saving = Column(Boolean, nullable=True)
    save_type = Column(String(50))  # Drop down list for options.
    damage_roll_main = Column(String(50))
    damage_type_main = Column(String(50))
    damage_roll_secondary = Column(String(50))
    damage_type_secondary = Column(String(50))
    ritual = Column(Boolean, default=False, nullable=True)
    character_id = Column(Integer, ForeignKey("characters.id"))


class CharacterFeatures(db.Model):
    __tablename__ = "feature"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    source = Column(String(50), nullable=True)  # have this as drop-down in list
    description = Column(Text, nullable=True)
    character_id = Column(Integer, ForeignKey("characters.id"))


class CharacterInventory(db.Model):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    number_owned = Column(Integer, nullable=True)
    value = Column(String(50))
    character_id = Column(Integer, ForeignKey("characters.id"))


class NPC(db.Model):
    __tablename__ = "npc"
    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)
    npc_image = Column(String, nullable=False)
    npc_description = Column(Text, nullable=False)
    npc_history = Column(Text, nullable=False)
    npc_notes = Column(Text, nullable=False)

    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="npcs")
    faction = Column(String(250))


class Location(db.Model):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)

    place_name = Column(String)
    summary = Column(Text)
    image = Column(String)
    notes = Column(Text)

    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="locations")


class Faction(db.Model):
    __tablename__ = "factions"
    id = Column(Integer, primary_key=True)

    faction_name = Column(String(100))
    faction_description = Column(Text)
    faction_image = Column(String)
    faction_notes = Column(Text)

    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="factions")


class UpcomingCampaign(db.Model):
    __tablename__ = "upcoming_campaign"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    timeslot = Column(String(300), nullable=False)
    image = Column(String, nullable=False)
    premise = Column(Text, nullable=False)
    registered_players = Column(Integer, nullable=False)


class ScheduledSession(db.Model):
    __tablename__ = "scheduledsession"
    id = Column(Integer, primary_key=True)
    day = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    time = Column(String(50), nullable=False)
    preview = Column(String(300))
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="sessions")


class SessionReview(db.Model):
    __tablename__ = "sessionreview"
    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    subtitle = Column(String(500))
    body = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())

    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="sessionreview")

    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign", back_populates="sessionreview")


# db.create_all()


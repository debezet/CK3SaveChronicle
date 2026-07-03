from __future__ import annotations

import re
from dataclasses import dataclass, field
from . import pdx

# CK3 personality traits. This is intentionally a key-level grouping only:
# Archivist reports mechanics from the save; Brother Mateusz interprets them later.
PERSONALITY_TRAITS: set[str] = {
    "lustful", "chaste", "gluttonous", "temperate", "greedy", "generous",
    "lazy", "diligent", "wrathful", "calm", "patient", "impatient",
    "arrogant", "humble", "deceitful", "honest", "craven", "brave",
    "shy", "gregarious", "ambitious", "content", "arbitrary", "just",
    "cynical", "zealous", "paranoid", "trusting", "compassionate", "callous",
    "sadistic", "stubborn", "fickle", "eccentric", "vengeful", "forgiving",
}

CHILDHOOD_TRAITS: set[str] = {
    "rowdy", "charming", "curious", "pensive", "bossy",
}

COPING_TRAITS: set[str] = {
    "drunkard", "hashishiyah", "rakish", "reclusive", "irritable",
    "flagellant", "profligate", "improvident", "contrite", "comfort_eater",
    "inappetetic", "journaller", "confider", "athletic",
}

HEALTH_AND_BODY_PREFIXES: tuple[str, ...] = (
    "depressed", "lunatic", "possessed", "wounded", "beauty_", "intellect_",
    "physique_",
)

HEALTH_AND_BODY_TRAITS: set[str] = {
    "pregnant", "ill", "pneumonic", "great_pox", "early_great_pox",
    "lovers_pox", "leper", "maimed", "one_eyed", "one_legged", "disfigured",
    "infirm", "withering_mind", "clouded_eyes", "faltering_heart",
    "fragile_bones", "incapable", "gout_ridden", "consumption", "cancer",
    "typhus", "bubonic_plague", "smallpox", "measles", "dysentery",
    "ergotism", "sickly", "scarred", "eunuch_1", "beardless_eunuch",
    "blind", "pure_blooded", "fecund", "strong", "shrewd", "clubfooted",
    "hunchbacked", "lisping", "stuttering", "dwarf", "giant", "inbred",
    "weak", "dull", "impotent", "spindly", "scaly", "albino", "wheezing",
    "bleeder", "infertile", "celibate", "whole_of_body", "athletic",
}

COMMANDER_TRAITS: set[str] = {
    "logistician", "military_engineer", "aggressive_attacker", "unyielding_defender",
    "forder", "flexible_leader", "desert_warrior", "jungle_stalker", "reaver",
    "reckless", "holy_warrior", "open_terrain_expert", "rough_terrain_expert",
    "forest_fighter", "cautious_leader", "organizer", "winter_soldier",
    "crusader_king",
}

STATUS_TRAITS: set[str] = {
    "pilgrim", "hajjaj", "excommunicated", "devoted", "sayyid", "saoshyant",
    "saoshyant_descendant", "savior", "divine_blood", "blood_of_prophet",
    "faith_warrior", "saint", "historical_character", "legend", "order_member",
    "berserker", "shieldmaiden", "varangian", "bastard", "legitimized_bastard",
    "disputed_heritage", "child_of_concubine_female", "child_of_concubine_male",
    "wild_oat", "bastard_founder", "twin", "kinslayer_1", "kinslayer_2",
    "kinslayer_3", "deviant", "cannibal", "sodomite", "incestuous", "adulterer",
    "fornicator", "murderer", "born_in_the_purple", "augustus", "viking",
    "reincarnation", "adventurer", "adventurer_follower", "heresiarch",
    "peasant_leader", "populist_leader", "witch", "disinherited", "denounced",
    "decadent", "extolled", "gallivanter", "loyal", "disloyal", "gallowsbait",
    "tourney_participant",
}

@dataclass
class TraitProfile:
    ids: list[int] = field(default_factory=list)
    keys: list[str] = field(default_factory=list)
    unknown_ids: list[int] = field(default_factory=list)

    @property
    def personality(self) -> list[str]:
        return [t for t in self.keys if t in PERSONALITY_TRAITS]

    @property
    def childhood(self) -> list[str]:
        return [t for t in self.keys if t in CHILDHOOD_TRAITS]

    @property
    def education(self) -> list[str]:
        return [t for t in self.keys if t.startswith("education_")]

    @property
    def lifestyle(self) -> list[str]:
        return [t for t in self.keys if t.startswith("lifestyle_")]

    @property
    def coping(self) -> list[str]:
        return [t for t in self.keys if t in COPING_TRAITS]

    @property
    def commander(self) -> list[str]:
        return [t for t in self.keys if t in COMMANDER_TRAITS]

    @property
    def health_and_body(self) -> list[str]:
        return [t for t in self.keys if t in HEALTH_AND_BODY_TRAITS or t.startswith(HEALTH_AND_BODY_PREFIXES)]

    @property
    def status(self) -> list[str]:
        return [t for t in self.keys if t in STATUS_TRAITS]

    @property
    def other(self) -> list[str]:
        grouped = set(
            self.personality
            + self.childhood
            + self.education
            + self.lifestyle
            + self.coping
            + self.commander
            + self.health_and_body
            + self.status
        )
        return [t for t in self.keys if t not in grouped]


def build_trait_lookup(gamestate: str) -> list[str]:
    block = pdx.named_block(gamestate, "traits_lookup")
    if not block:
        return []
    return re.findall(r"[A-Za-z0-9_]+", block)


def parse_trait_profile(raw: str, lookup: list[str]) -> TraitProfile:
    ids = pdx.number_list(raw, "traits")
    keys: list[str] = []
    unknown: list[int] = []
    for trait_id in ids:
        # CK3 save trait IDs are indexes into traits_lookup in observed saves.
        if 0 <= trait_id < len(lookup):
            keys.append(lookup[trait_id])
        else:
            unknown.append(trait_id)
    return TraitProfile(ids=ids, keys=keys, unknown_ids=unknown)

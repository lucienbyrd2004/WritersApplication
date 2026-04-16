import random
from faker import Faker
from sqlalchemy import insert, update, select
import queries as q

fake = Faker()

# ---------- CONFIG ----------
NUM_CONTINENTS = 6
NUM_COUNTRIES = 10
TOWNS_PER_COUNTRY = 50
NUM_PEOPLE = 100000
ADVENTURER_RATIO = 0.2
BATCH_SIZE = 1000
# ----------------------------


def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]


# ---------- PHASE 1 ----------
def seed_base():
    print("Seeding base data...")

    with q.pool.begin() as conn:

        # Continents
        continents = [
            {"Name": fake.unique.word().capitalize(), "Climate": random.choice(["Hot","Cold","Temperate"])}
            for _ in range(NUM_CONTINENTS)
        ]
        conn.execute(insert(q.continent), continents)

        # Countries (no continent yet)
        countries = [
            {"Name": fake.unique.country(), "ContinentID": None}
            for _ in range(NUM_COUNTRIES)
        ]
        conn.execute(insert(q.country), countries)

        # Towns (no country yet)
        towns = []
        for i in range(NUM_COUNTRIES * TOWNS_PER_COUNTRY):
            towns.append({
                "Name": fake.city(),
                "CountryID": None
            })
        conn.execute(insert(q.town), towns)

        # People (no relationships yet)
        people = []
        for i in range(NUM_PEOPLE):
            people.append({
                "Name": fake.name(),
                "Race": random.choice(["Human","Elf","Dwarf","Orc","Tiefling"]),
                "Age": random.randint(10, 90),
                "HomeTownID": None,
                "HomeContinent": None,
                "God": None
            })

        for batch in chunked(people, BATCH_SIZE):
            conn.execute(insert(q.person), batch)


# ---------- PHASE 2 ----------
def resolve_relationships():
    print("Resolving relationships...")

    with q.pool.begin() as conn:

        continents = conn.execute(select(q.continent)).fetchall()
        countries = conn.execute(select(q.country)).fetchall()
        towns = conn.execute(select(q.town)).fetchall()

        # Assign countries → continents
        for c in countries:
            conn.execute(
                update(q.country)
                .where(q.country.c.CountryID == c.CountryID)
                .values(ContinentID=random.choice(continents).ContinentID)
            )

        # Assign towns → countries
        for t in towns:
            conn.execute(
                update(q.town)
                .where(q.town.c.TownID == t.TownID)
                .values(CountryID=random.choice(countries).CountryID)
            )

        # Refresh towns after update
        towns = conn.execute(select(q.town)).fetchall()

        # Assign people → towns + continents
        people_ids = conn.execute(select(q.person.c.PersonID)).scalars().all()

        updates = []
        for pid in people_ids:
            town = random.choice(towns)

            updates.append({
                "PersonID": pid,
                "HomeTownID": town.TownID,
                "HomeContinent": random.choice(continents).Name
            })

        for batch in chunked(updates, BATCH_SIZE):
            for row in batch:
                conn.execute(
                    update(q.person)
                    .where(q.person.c.PersonID == row["PersonID"])
                    .values(
                        HomeTownID=row["HomeTownID"],
                        HomeContinent=row["HomeContinent"]
                    )
                )


# ---------- PHASE 3 ----------
def seed_adventurers():
    print("Creating adventurers...")

    with q.pool.begin() as conn:
        people_ids = conn.execute(select(q.person.c.PersonID)).scalars().all()

        adventurers = []
        for pid in people_ids:
            if random.random() < ADVENTURER_RATIO:
                adventurers.append({
                    "PersonID": pid,
                    "Class": random.choice(["Warrior","Mage","Rogue","Cleric","Ranger"]),
                    "CharLevel": random.randint(1, 20)
                })

        for batch in chunked(adventurers, BATCH_SIZE):
            conn.execute(insert(q.adventurer), batch)


def seed_relationships():
    print("Creating relationships...")

    with q.pool.begin() as conn:
        people_ids = conn.execute(select(q.person.c.PersonID)).scalars().all()

        relationships = []
        for i in range(0, len(people_ids) - 1, 2):
            relationships.append({
                "Person1ID": people_ids[i],
                "Person2ID": people_ids[i + 1],
                "RelationshipType": random.choice(["Friend","Rival","Sibling"])
            })

        for batch in chunked(relationships, BATCH_SIZE):
            conn.execute(insert(q.relationship), batch)


# ---------- MAIN ----------
def main():
    print("=== WORLD GENERATION START ===")

    seed_base()
    resolve_relationships()
    seed_adventurers()
    seed_relationships()

    print("=== WORLD GENERATION COMPLETE ===")


if __name__ == "__main__":
    main()
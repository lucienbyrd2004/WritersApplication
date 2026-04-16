import sqlalchemy as db
from sqlalchemy import insert, delete, update, select, desc, ForeignKey, func
from connector import pool
import networkx as nx
import matplotlib.pyplot as plt

metadata_obj = db.MetaData()

# -------------------- TABLE DEFINITIONS (MATCHED TO DB) --------------------

continent = db.Table('continent', metadata_obj,
    db.Column('ContinentID', db.Integer, primary_key=True, autoincrement=True),
    db.Column('Name', db.String(255)),
    db.Column('Climate', db.String(255))
)

pantheon = db.Table('pantheon', metadata_obj,
    db.Column('PantheonID', db.Integer, primary_key=True, autoincrement=True),
    db.Column('Name', db.String(255))
)

god = db.Table('god', metadata_obj,
    db.Column('GodID', db.Integer, primary_key=True, autoincrement=True),
    db.Column('Name', db.String(255)),
    db.Column('Alignment', db.String(255)),
    db.Column('Domain', db.String(255)),
    db.Column('PantheonID', db.Integer, ForeignKey('pantheon.PantheonID'))
)

person = db.Table('person', metadata_obj,
    db.Column('PersonID', db.Integer, primary_key=True, autoincrement=True),
    db.Column('Name', db.String(255)),
    db.Column('Race', db.String(255)),
    db.Column('Age', db.Integer),
    db.Column('HomeContinent', db.String(255)),
    db.Column('God', db.String(255)),
    db.Column('HomeTownID', db.Integer, ForeignKey('town.TownID'))
)

country = db.Table('country', metadata_obj,
    db.Column('CountryID', db.Integer, primary_key=True, autoincrement=True),
    db.Column('Name', db.String(255)),
    db.Column('RulerID', db.Integer, ForeignKey('person.PersonID')),
    db.Column('ContinentID', db.Integer, ForeignKey('continent.ContinentID'))
)

town = db.Table('town', metadata_obj,
    db.Column('TownID', db.Integer, primary_key=True, autoincrement=True),
    db.Column('Name', db.String(255)),
    db.Column('CountryID', db.Integer, ForeignKey('country.CountryID')),
    db.Column('LeaderID', db.Integer, ForeignKey('person.PersonID'))
)

adventurer = db.Table('adventurer', metadata_obj,
    db.Column('PersonID', db.Integer, ForeignKey('person.PersonID')),
    db.Column('Class', db.String(255)),
    db.Column('CharLevel', db.Integer)
)

relationship = db.Table('relationship', metadata_obj,
    db.Column('RelationshipID', db.Integer, primary_key=True, autoincrement=True),
    db.Column('Person1ID', db.Integer, ForeignKey('person.PersonID')),
    db.Column('Person2ID', db.Integer, ForeignKey('person.PersonID')),
    db.Column('RelationshipType', db.String(255))
)

# -------------------- GENERIC COMMIT --------------------

def commitStatement(stmt):
    with pool.connect() as connection:
        connection.execute(stmt)
        connection.commit()

# -------------------- CREATE (ALL TABLES) --------------------

def create_continent(name, climate):
    commitStatement(insert(continent).values(Name=name, Climate=climate))


def create_pantheon(name):
    commitStatement(insert(pantheon).values(Name=name))


def create_god(name, alignment, domain, pantheon_id):
    commitStatement(insert(god).values(Name=name, Alignment=alignment, Domain=domain, PantheonID=pantheon_id))


def create_person(name, race, age, home_continent, god_name, hometown_id):
    commitStatement(insert(person).values(Name=name, Race=race, Age=age,
        HomeContinent=home_continent, God=god_name, HomeTownID=hometown_id))


def create_country(name, ruler_id, continent_id):
    commitStatement(insert(country).values(Name=name, RulerID=ruler_id, ContinentID=continent_id))


def create_town(name, country_id, leader_id):
    commitStatement(insert(town).values(Name=name, CountryID=country_id, LeaderID=leader_id))


def create_adventurer(person_id, char_class, level):
    commitStatement(insert(adventurer).values(PersonID=person_id, Class=char_class, CharLevel=level))


def create_relationship(p1, p2, rel_type):
    with pool.connect() as conn:
        if not conn.execute(select(person).where(person.c.PersonID == p1)).first():
            print("Person1 does not exist")
            return
        if not conn.execute(select(person).where(person.c.PersonID == p2)).first():
            print("Person2 does not exist")
            return
    commitStatement(insert(relationship).values(Person1ID=p1, Person2ID=p2, RelationshipType=rel_type))

# -------------------- READ (ALL TABLES) --------------------
def get_person_by_id(pid):
    with pool.connect() as conn:
        return conn.execute(select(person).where(person.c.PersonID == pid)).first()

def get_person_by_name(name):
    with pool.connect() as conn:
        return conn.execute(select(person).where(person.c.Name == name)).fetchall()


def get_adventurer_by_person(pid):
    with pool.connect() as conn:
        return conn.execute(select(adventurer).where(adventurer.c.PersonID == pid)).first()


def get_by_id(table, column, value):
    with pool.connect() as conn:
        return conn.execute(select(table).where(column == value)).first()


def get_by_name(table, column, value):
    with pool.connect() as conn:
        return conn.execute(select(table).where(column == value)).fetchall()


def get_gods_in_pantheon(pantheon_id):
    with pool.connect() as conn:
        return conn.execute(select(god).where(god.c.PantheonID == pantheon_id)).fetchall()


def get_all(table):
    with pool.connect() as conn:
        return [row._asdict() for row in conn.execute(select(table))]


def get_people_in_town(town_id):
    with pool.connect() as conn:
        return [row._asdict() for row in conn.execute(select(person).where(person.c.HomeTownID == town_id))]


def get_towns_in_country(country_id):
    with pool.connect() as conn:
        return [row._asdict() for row in conn.execute(select(town).where(town.c.CountryID == country_id))]


def get_countries_in_continent(continent_id):
    with pool.connect() as conn:
        return [row._asdict() for row in conn.execute(select(country).where(country.c.ContinentID == continent_id))]


def get_relationships_for_person(person_id):
    stmt = select(relationship).where((relationship.c.Person1ID == person_id) | (relationship.c.Person2ID == person_id))
    with pool.connect() as conn:
        return [row._asdict() for row in conn.execute(stmt)]

# -------------------- UPDATE (ALL TABLES) --------------------

def update_generic(table, pk_column, pk_value, **kwargs):
    commitStatement(update(table).where(pk_column == pk_value).values(**kwargs))

# Example wrappers (optional clarity)

def update_person(pid, **kwargs): update_generic(person, person.c.PersonID, pid, **kwargs)

def update_town(tid, **kwargs): update_generic(town, town.c.TownID, tid, **kwargs)

def update_country(cid, **kwargs): update_generic(country, country.c.CountryID, cid, **kwargs)

def update_continent(cid, **kwargs): update_generic(continent, continent.c.ContinentID, cid, **kwargs)

def update_god(gid, **kwargs): update_generic(god, god.c.GodID, gid, **kwargs)

def update_pantheon(pid, **kwargs): update_generic(pantheon, pantheon.c.PantheonID, pid, **kwargs)

def update_adventurer(pid, **kwargs): update_generic(adventurer, adventurer.c.PersonID, pid, **kwargs)

def update_relationship(rid, **kwargs): update_generic(relationship, relationship.c.RelationshipID, rid, **kwargs)

# -------------------- DELETE (ALL TABLES) --------------------

def delete_generic(table, pk_column, pk_value):
    if pk_value is None:
        stmt = delete(table)  # delete ALL rows
    else:
        stmt = delete(table).where(pk_column == pk_value)

    commitStatement(stmt)

# Example wrappers

def delete_person(pid): delete_generic(person, person.c.PersonID, pid)

def delete_town(tid): delete_generic(town, town.c.TownID, tid)

def delete_country(cid): delete_generic(country, country.c.CountryID, cid)

def delete_continent(cid): delete_generic(continent, continent.c.ContinentID, cid)

def delete_god(gid): delete_generic(god, god.c.GodID, gid)

def delete_pantheon(pid): delete_generic(pantheon, pantheon.c.PantheonID, pid)

def delete_adventurer(pid): delete_generic(adventurer, adventurer.c.PersonID, pid)

def delete_relationship(rid): delete_generic(relationship, relationship.c.RelationshipID, rid)

# population count
def get_population_by_continent(continent_id):
    with pool.connect() as conn:
        stmt = select(func.count()).select_from(person).where(
            person.c.HomeContinent == select(continent.c.Name)
            .where(continent.c.ContinentID == continent_id)
            .scalar_subquery()
        )
        return conn.execute(stmt).scalar()


def get_population_by_country(country_id):
    with pool.connect() as conn:
        stmt = select(func.count()).select_from(person).where(
            person.c.HomeTownID.in_(
                select(town.c.TownID).where(town.c.CountryID == country_id)
            )
        )
        return conn.execute(stmt).scalar()


def get_population_by_town(town_id):
    with pool.connect() as conn:
        stmt = select(func.count()).select_from(person).where(
            person.c.HomeTownID == town_id
        )
        return conn.execute(stmt).scalar()
    
#average age
def get_avg_age_by_town():
    with pool.connect() as conn:
        stmt = select(
            town.c.Name,
            func.avg(person.c.Age)
        ).join(person, person.c.HomeTownID == town.c.TownID)\
         .group_by(town.c.Name)

        return conn.execute(stmt).fetchall()


def get_avg_age_by_country():
    with pool.connect() as conn:
        stmt = select(
            country.c.Name,
            func.avg(person.c.Age)
        ).join(town, town.c.CountryID == country.c.CountryID)\
         .join(person, person.c.HomeTownID == town.c.TownID)\
         .group_by(country.c.Name)

        return conn.execute(stmt).fetchall()


def get_avg_age_by_continent():
    with pool.connect() as conn:
        stmt = select(
            continent.c.Name,
            func.avg(person.c.Age)
        ).join(country, country.c.ContinentID == continent.c.ContinentID)\
         .join(town, town.c.CountryID == country.c.CountryID)\
         .join(person, person.c.HomeTownID == town.c.TownID)\
         .group_by(continent.c.Name)

        return conn.execute(stmt).fetchall()
    
# number of adventurers
def get_total_adventurers():
    with pool.connect() as conn:
        stmt = select(func.count()).select_from(adventurer)
        return conn.execute(stmt).scalar()
    
# min and max pop
def get_population_extremes():
    with pool.connect() as conn:

        # ---- TOWN ----
        town_pop = select(
            town.c.Name,
            func.count(person.c.PersonID).label("pop")
        ).outerjoin(
            person, person.c.HomeTownID == town.c.TownID
        ).group_by(town.c.Name).subquery()

        max_town = conn.execute(
            select(town_pop).order_by(desc(town_pop.c.pop)).limit(1)
        ).first()

        min_town = conn.execute(
            select(town_pop).order_by(town_pop.c.pop).limit(1)
        ).first()

        # ---- COUNTRY ----
        country_pop = select(
            country.c.Name,
            func.count(person.c.PersonID).label("pop")
        ).outerjoin(
            town, town.c.CountryID == country.c.CountryID
        ).outerjoin(
            person, person.c.HomeTownID == town.c.TownID
        ).group_by(country.c.Name).subquery()

        max_country = conn.execute(
            select(country_pop).order_by(desc(country_pop.c.pop)).limit(1)
        ).first()

        min_country = conn.execute(
            select(country_pop).order_by(country_pop.c.pop).limit(1)
        ).first()

        # ---- CONTINENT ----
        continent_pop = select(
            continent.c.Name,
            func.count(person.c.PersonID).label("pop")
        ).outerjoin(
            country, country.c.ContinentID == continent.c.ContinentID
        ).outerjoin(
            town, town.c.CountryID == country.c.CountryID
        ).outerjoin(
            person, person.c.HomeTownID == town.c.TownID
        ).group_by(continent.c.Name).subquery()

        max_continent = conn.execute(
            select(continent_pop).order_by(desc(continent_pop.c.pop)).limit(1)
        ).first()

        min_continent = conn.execute(
            select(continent_pop).order_by(continent_pop.c.pop).limit(1)
        ).first()

        return {
            "town": (max_town, min_town),
            "country": (max_country, min_country),
            "continent": (max_continent, min_continent)
        }


# -------------------- GRAPH --------------------


def generate_full_world_graph(output_path="world_graph.png", scope="World", value=None):
    import random
    import networkx as nx
    import matplotlib.pyplot as plt
    from sqlalchemy import select

    # -------- SAMPLING LIMITS --------
    MAX_PEOPLE = 150
    MAX_TOWNS = 50
    MAX_COUNTRIES = 25
    MAX_CONTINENTS = 5
    MAX_GODS = 25
    MAX_PANTHEONS = 10

    G = nx.Graph()

    with pool.connect() as conn:
        persons = conn.execute(select(person)).fetchall()
        towns = conn.execute(select(town)).fetchall()
        countries = conn.execute(select(country)).fetchall()
        continents = conn.execute(select(continent)).fetchall()
        relationships = conn.execute(select(relationship)).fetchall()
        gods = conn.execute(select(god)).fetchall()
        pantheons = conn.execute(select(pantheon)).fetchall()
    # -------- FILTERING --------

    if scope != "World" and value:

        if scope == "Continent":
            continents = [c for c in continents if c.Name == value]
            continent_ids = {c.ContinentID for c in continents}

            countries = [c for c in countries if c.ContinentID in continent_ids]
            country_ids = {c.CountryID for c in countries}

            towns = [t for t in towns if t.CountryID in country_ids]
            town_ids = {t.TownID for t in towns}

            persons = [p for p in persons if p.HomeTownID in town_ids]

        elif scope == "Country":
            countries = [c for c in countries if c.Name == value]
            country_ids = {c.CountryID for c in countries}

            towns = [t for t in towns if t.CountryID in country_ids]
            town_ids = {t.TownID for t in towns}

            persons = [p for p in persons if p.HomeTownID in town_ids]

        elif scope == "Town":
            towns = [t for t in towns if t.Name == value]
            town_ids = {t.TownID for t in towns}

            persons = [p for p in persons if p.HomeTownID in town_ids]
    # -------- RANDOM SAMPLING --------
    persons = random.sample(persons, min(MAX_PEOPLE, len(persons)))
    towns = random.sample(towns, min(MAX_TOWNS, len(towns)))
    countries = random.sample(countries, min(MAX_COUNTRIES, len(countries)))
    continents = random.sample(continents, min(MAX_CONTINENTS, len(continents)))
    gods = random.sample(gods, min(MAX_GODS, len(gods)))
    pantheons = random.sample(pantheons, min(MAX_PANTHEONS, len(pantheons)))

    # -------- LOOKUP DICTIONARIES (FAST) --------
    person_dict = {p.PersonID: p for p in persons}
    town_dict = {t.TownID: t for t in towns}
    country_dict = {c.CountryID: c for c in countries}
    continent_dict = {c.ContinentID: c for c in continents}
    god_dict = {g.Name: g for g in gods}
    pantheon_dict = {p.PantheonID: p for p in pantheons}

    # -------- FILTER RELATIONSHIPS --------
    person_ids = set(person_dict.keys())
    filtered_relationships = [
        r for r in relationships
        if r.Person1ID in person_ids and r.Person2ID in person_ids
    ]

    # -------------------- ADD NODES --------------------
    for p in persons:
        G.add_node(f"Person:{p.Name}")

    for t in towns:
        G.add_node(f"Town:{t.Name}")

    for c in countries:
        G.add_node(f"Country:{c.Name}")

    for cont in continents:
        G.add_node(f"Continent:{cont.Name}")

    for g in gods:
        G.add_node(f"God:{g.Name}")

    for p in pantheons:
        G.add_node(f"Pantheon:{p.Name}")

    # -------------------- ADD EDGES --------------------

    # Person → Town
    for p in persons:
        if p.HomeTownID in town_dict:
            t = town_dict[p.HomeTownID]
            G.add_edge(f"Person:{p.Name}", f"Town:{t.Name}")

    # Town → Country
    for t in towns:
        if t.CountryID in country_dict:
            c = country_dict[t.CountryID]
            G.add_edge(f"Town:{t.Name}", f"Country:{c.Name}")

    # Country → Continent
    for c in countries:
        if c.ContinentID in continent_dict:
            cont = continent_dict[c.ContinentID]
            G.add_edge(f"Country:{c.Name}", f"Continent:{cont.Name}")

    # Person → God
    for p in persons:
        if p.God in god_dict:
            g = god_dict[p.God]
            G.add_edge(f"Person:{p.Name}", f"God:{g.Name}")

    # God → Pantheon
    for g in gods:
        if g.PantheonID in pantheon_dict:
            pan = pantheon_dict[g.PantheonID]
            G.add_edge(f"God:{g.Name}", f"Pantheon:{pan.Name}")

    # Person ↔ Person
    for r in filtered_relationships:
        p1 = person_dict[r.Person1ID]
        p2 = person_dict[r.Person2ID]

        if p1.PersonID != p2.PersonID:
            G.add_edge(
                f"Person:{p1.Name}",
                f"Person:{p2.Name}",
                label=r.RelationshipType
            )

    # -------------------- COLORS --------------------
    node_colors = []
    for node in G.nodes():
        if node.startswith("Person:"):
            node_colors.append("#A7C7E7")
        elif node.startswith("Town:"):
            node_colors.append("#A8E6A3")
        elif node.startswith("Country:"):
            node_colors.append("#FFB3B3")
        elif node.startswith("Continent:"):
            node_colors.append("#FFD580")
        elif node.startswith("God:"):
            node_colors.append("#D8BFD8")
        elif node.startswith("Pantheon:"):
            node_colors.append("#FFCCE5")
        else:
            node_colors.append("#DDDDDD")

    # -------------------- DRAW --------------------
    plt.figure(figsize=(16, 12))
    pos = nx.spring_layout(G, k=0.7, seed=random.randint(0, 10000))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=1200,   # smaller nodes
        font_size=7,      # slightly smaller text
        edge_color="gray"
    )

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

    import matplotlib.patches as mpatches

    legend_items = [
        mpatches.Patch(color="#A7C7E7", label="Person"),
        mpatches.Patch(color="#A8E6A3", label="Town"),
        mpatches.Patch(color="#FFB3B3", label="Country"),
        mpatches.Patch(color="#FFD580", label="Continent"),
        mpatches.Patch(color="#D8BFD8", label="God"),
        mpatches.Patch(color="#FFCCE5", label="Pantheon"),
    ]

    plt.legend(handles=legend_items, loc='upper left', bbox_to_anchor=(1, 1))
    plt.title("World Relationship Graph")

    plt.tight_layout()

    # -------- SAVE INSTEAD OF SHOW --------
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    return output_path

def reset_world():
    print("Resetting world safely...")

    with pool.connect() as conn:
        # -------------------- BREAK CIRCULAR FK LINKS --------------------
        conn.execute(update(person).values(HomeTownID=None))
        conn.execute(update(town).values(LeaderID=None))
        conn.execute(update(country).values(RulerID=None))

        # Optional (safe guard)
        conn.execute(update(person).values(God=None))

        conn.commit()

        # -------------------- DELETE DATA (SAFE ORDER) --------------------
        conn.execute(delete(relationship))
        conn.execute(delete(adventurer))

        conn.execute(delete(person))
        conn.execute(delete(town))
        conn.execute(delete(country))

        conn.execute(delete(god))
        conn.execute(delete(pantheon))
        conn.execute(delete(continent))

        conn.commit()

    print("World reset complete.")

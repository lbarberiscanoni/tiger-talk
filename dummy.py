import random
import json
import time

#players = ["Myriel", "Napoleon", "Mlle.Baptistine", "Mme.Magloire", "CountessdeLo", "Geborand", "Champtercier", "Cravatte", "Count", "OldMan", "Labarre", "Valjean", "Marguerite", "Mme.deR", "Isabeau", "Gervais", "Tholomyes", "Listolier", "Fameuil", "Blacheville", "Favourite", "Dahlia", "Zephine", "Fantine", "Mme.Thenardier", "Thenardier", "Cosette", "Javert", "Fauchelevent", "Bamatabois", "Perpetue", "Simplice", "Scaufflaire", "Woman1", "Judge", "Champmathieu", "Brevet", "Chenildieu", "Cochepaille", "Pontmercy", "Boulatruelle", "Eponine", "Anzelma", "Woman2", "MotherInnocent", "Gribier", "Jondrette", "Mme.Burgon", "Gavroche", "Gillenormand", "Magnon", "Mlle.Gillenormand", "Mme.Pontmercy", "Mlle.Vaubois", "Lt.Gillenormand", "Marius", "BaronessT", "Mabeuf", "Enjolras", "Combeferre", "Prouvaire", "Feuilly", "Courfeyrac", "Bahorel", "Bossuet", "Joly", "Grantaire", "MotherPlutarch", "Gueulemer", "Babet", "Claquesous", "Montparnasse", "Toussaint", "Child1", "Child2", "Brujon", "Mme.Hucheloup"]

players = ["Emily", "Isabella", "Emma", "Ava", "Madison", "Sophia", "Olivia", "Abigail", "Hannah", "Elizabeth", "Addison", "Samantha", "Ashley", "Alyssa", "Mia", "Chloe", "Natalie", "Sarah", "Alexis", "Grace", "Ella", "Brianna", "Hailey", "Taylor", "Anna", "Kayla", "Lily", "Lauren", "Victoria", "Savannah", "Nevaeh", "Jasmine", "Lillian", "Julia", "Sofia", "Kaylee", "Sydney", "Gabriella", "Katherine", "Alexa", "Destiny", "Jessica", "Morgan", "Kaitlyn", "Brooke", "Allison", "Makayla", "Avery", "Alexandra", "Jocelyn", "Audrey", "Riley", "Kimberly", "Maria", "Evelyn", "Zoe", "Brooklyn", "Angelina", "Andrea", "Rachel", "Madeline", "Maya", "Kylie", "Jennifer", "Mackenzie", "Claire", "Gabrielle", "Leah", "Aubrey", "Arianna", "Vanessa", "Trinity", "Ariana", "Faith", "Katelyn", "Haley", "Amelia", "Megan", "Isabelle", "Melanie", "Sara", "Sophie", "Bailey", "Aaliyah", "Layla", "Isabel", "Nicole", "Stephanie", "Paige", "Gianna", "Autumn", "Mariah", "Mary", "Michelle", "Jada", "Gracie", "Molly", "Valeria", "Caroline", "Jordan", "Jacob", "Michael", "Ethan", "Joshua", "Daniel", "Christopher", "Anthony", "William", "Matthew", "Andrew", "Alexander", "David", "Joseph", "Noah", "James", "Ryan", "Logan", "Jayden", "John", "Nicholas", "Tyler", "Christian", "Jonathan", "Nathan", "Samuel", "Benjamin", "Aiden", "Gabriel", "Dylan", "Elijah", "Brandon", "Gavin", "Jackson", "Angel", "Jose", "Caleb", "Mason", "Jack", "Kevin", "Evan", "Isaac", "Zachary", "Isaiah", "Justin", "Jordan", "Luke", "Robert", "Austin", "Landon", "Cameron", "Thomas", "Aaron", "Lucas", "Aidan", "Connor", "Owen", "Hunter", "Diego", "Jason", "Luis", "Adrian", "Charles", "Juan", "Brayden", "Adam", "Julian", "Jeremiah", "Xavier", "Wyatt", "Carlos", "Hayden", "Sebastian", "Alex", "Ian", "Sean", "Jaden", "Jesus", "Bryan", "Chase", "Carter", "Brian", "Nathaniel", "Eric", "Cole", "Dominic", "Kyle", "Tristan", "Blake", "Liam", "Carson", "Henry", "Caden", "Brady", "Miguel", "Cooper", "Antonio", "Steven", "Kaden", "Richard", "Timothy"]

numOfFriends = 3
clusterNum = random.randint(3, 6)

data = {"nodes": [], "links": []}

iteration = 0
while True:
    nodes = []
    for player in players:
        internal_ob = {}
        internal_ob["id"] = player
        internal_ob["group"] = random.randint(1, clusterNum)

        nodes.append(internal_ob)

    data["nodes"] = nodes

    links = []
    for player in players:
        internal_ob = {}
        internal_ob["source"] = player
        internal_ob["target"] = players[random.randint(1, len(players) - 1)]
        internal_ob["value"] = random.randint(1, numOfFriends)
        
        links.append(internal_ob)

    #for i in range(len(players) * random.randint(1, numOfFriends)):
    for i in range(len(players) * numOfFriends):
        player = players[random.randint(1, len(players) -1)]
        internal_ob = {}
        internal_ob["source"] = player
        internal_ob["target"] = players[random.randint(1, len(players) - 1)]
        internal_ob["value"] = random.randint(1, numOfFriends)
        
        links.append(internal_ob)

    data["links"] = links

    with open("data/dummy.json", "wb") as f:
        f.write(json.dumps(data))
        f.close()

    print "iteration #", iteration
    iteration += 1
    time.sleep(3)

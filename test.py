class Holder:
    agents = {}
    
Holder.agents["trip"] = "lol"
Holder.agents.pop("trip")
print(Holder.agents)
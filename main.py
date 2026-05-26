import json
import math
def load_data():
    file=open("data.json","r")
    data=json.load(file)
    file.close()
    return data
def calculate(p1,p2):
    x1=p1[0]
    y1=p1[1]
    x2=p2[0]
    y2=p2[1]
    distance=math.sqrt((x2-x1)**2+ (y2-y1)**2)
    return distance 
def nearest_agent(ware_loc,agents):
    nearest_agent=None
    min_dist=999999
    for agent in agents:
        agent_id=agent["id"]
        agent_loc=agent["location"]
        distance=calculate(agent_loc, ware_loc)
        print(agent_id, "distance =", distance)
        if distance<min_dist:
            min_dist=distance
            nearest_agent=agent_id
    return nearest_agent
data=load_data()
warehouses=data["warehouses"]
agents=data["agents"]
packages=data["packages"]
report={}
for agent in agents:
    agent_id=agent["id"]
    report[agent_id]={
        "delivered_package":0,
        "total_dist":0
    }
for package in packages:
    package_id=package["id"]
    warehouse_id=package["warehouse_id"]
    destination=package["destination"]
    print("\nPackage:", package_id)
    ware_loc=None
    for warehouse in warehouses:
        if warehouse["id"]==warehouse_id:
            ware_loc=warehouse["location"]
    nearest=None
    min_dist=999999
    total_dist=0
    for agent in agents:
        agent_id=agent["id"]
        agent_loc=agent["location"]
        agent_ware=calculate(agent_loc,ware_loc)
        ware_destination=calculate(ware_loc,destination)
        delivery_dist=agent_ware + ware_destination
        print(agent_id,"Total delivery distance = ",delivery_dist)
        if delivery_dist<min_dist:
            nearest=agent_id
            min_dist=delivery_dist
            total_dist=delivery_dist
    report[nearest]["delivered_package"]+=1
    report[nearest]["total_dist"]+=total_dist
best_agent= None
best_eff=999999
for agent_id in report:
    delivered=report[agent_id]["delivered_package"]
    total=report[agent_id]["total_dist"]
    if delivered>0:
        efficiency=total/delivered
    else:
        efficiency=0
    report[agent_id]["efficiency"]=round(efficiency,2)
    report[agent_id]["total_dist"]=round(total,2)
    if delivered>0 and efficiency<best_eff:
        best_eff=efficiency
        best_agent=agent_id
report["best_agent"]=best_agent
print("\nFinal Report:")
print(json.dumps(report, indent=4))
file=open("report.json","w")
json.dump(report,file, indent=4)
file.close()
print("\nReport Saved!!")



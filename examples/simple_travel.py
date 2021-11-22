"""
The "travel from home to the park" example from my lectures.
Author: Dana Nau <nau@cs.umd.edu>, May 31, 2013
This file should work correctly in both Python 2.7 and Python 3.2.
"""
from pyhop import hop
from pyhop import helpers

HOME = "home"
PARK = "park"
ME = "me"
TAXI = "taxi"


def taxi_rate(dist):
    return (1.5 + 0.5 * dist)


def walk(state,a,x,y):
    if state.loc[a] == x:
        state.loc[a] = y
        return state
    else: return False


def call_taxi(state,a,x):
    state.loc[TAXI] = x
    return state


def ride_taxi(state,a,x,y):
    if state.loc[TAXI] == x and state.loc[a] == x:
        state.loc[TAXI] = y
        state.loc[a] = y
        state.owe[a] = taxi_rate(state.dist[x][y])
        return state
    else: 
        return False


def give_money_to_driver(state, agent):
    if state.cash[agent] >= state.owe[agent]:
        state.cash[agent] = state.cash[agent] - state.owe[agent]
        state.owe[agent] = 0
        return state
    return False


def look_in_cushions(state, agent):
    state.time += 1
    state.cash[agent] += 2.0
    return state


def look_in_bushes(state, agent):
    state.time += 1
    state.cash[agent] += 1.0
    return state


hop.declare_operators(
    walk,
    call_taxi,
    ride_taxi,
    give_money_to_driver,
    look_in_bushes, 
    look_in_cushions,
)


def travel_by_foot(state,a,x,y):
    if state.dist[x][y] <= 2:
        return [
            ("walk", a, x, y,)
        ]
    return False


def travel_by_taxi(state,a,x,y):
    if state.cash[a] >= taxi_rate(state.dist[x][y]):
        return [
            ('call_taxi',a,x),
            ('ride_taxi',a,x,y),
            ('pay_driver',a)
        ]
    else:
        return [
            ("get_money", a),
            ("travel", a, x, y),
        ]


hop.declare_methods('travel',travel_by_foot,travel_by_taxi)


def pay_driver(state,a):
    if state.cash[a] >= state.owe[a]:
        return [
            ("give_money_to_driver", a)
        ]
    else:
        return [
            ("get_money", a),
            ("pay_driver", a)
        ]


hop.declare_methods("pay_driver", pay_driver)


def get_money(state, agent):
    if state.loc[agent] == HOME:
        return [
            ("look_in_cushions", agent)
        ]
    elif state.loc[agent] == PARK:
        return [
            ("look_in_bushes", agent)
        ]
    else:
        return []


hop.declare_methods("get_money", get_money)


state1 = hop.State('state1')
state1.time = 0
state1.loc = {ME: HOME}
state1.cash = {ME: 1.0}
state1.owe = {ME: 0}
state1.dist = {HOME: {PARK: 8}, PARK: {HOME: 8}}


print("""
********************************************************************************
Call hop.plan(state1,[('travel','me','home','park')]) with different verbosity levels
********************************************************************************
""")

# print("- If verbose=0 (the default), Pyhop returns the solution but prints nothing.\n")
# hop.plan(state1,
#          [('travel','me','home','park')],
#          hop.get_operators(),
#          hop.get_methods())

# print('- If verbose=1, Pyhop prints the problem and solution, and returns the solution:')
# hop.plan(state1,
#          [('travel','me','home','park')],
#          hop.get_operators(),
#          hop.get_methods(),
#          verbose=1)

# print('- If verbose=2, Pyhop also prints a note at each recursive call:')
# hop.plan(state1,
#          [('travel','me','home','park')],
#          hop.get_operators(),
#          hop.get_methods(),
#          verbose=2)

print('- If verbose=3, Pyhop also prints the intermediate states:')
hop.plan(
    state1,
    [('travel','me','home','park')],
    hop.get_operators(),
    hop.get_methods(),
    verbose=4,
    log="./simple_travel.log",
)


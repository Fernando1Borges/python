#step 1 should I turn?
#step 2 - where to turn?
#for coaster game
# reinforcement learning

import gym
import universe
import random

#reinforcement learning step
def determine_turn(turn, observation_n, j, total_sum, prev_total_sum, reward_n):
    #for every 15 iterations, sum the total observations, adn take the average
    #if lower than 0, change the direction
    # if we go 15 iterations and get a reward ech step we're doing somethign right
    # that's when we turn

    if(j >= 15):

        if(total_sum/ j ) == 0:
            turn = True
        else:
            turn = False

        #reset variables
        total_sum = 0
        j = 0
        prev_total_sum = total_sum
        total_sum = 0

    else:
        turn = False
    if(observation_n != None):
        #increment counter and reward sum
        j += 1
        total_sum += reward_n
    return(turn, j, total_sum, prev_total_sum)

def main():
    #init environment
    env = gym.make('flashgames.CoasterRacer-v0')
    # client is the agent, decides the key actions
    # remote is the environment, (local docker container)
    # we can have multiple games running at once on a server
    #^ initialized universe environment
    observation_n = env.reset()


    #initialize variables
    # num of game iterations
    n = 0
    j = 0
    #sum of observations
    total_sum = 0
    prev_total_sum = 0
    turn = False

    #define our turns or keyboard actions
    left = [('KeyEvent', 'ArrowUp', True), ('KeyEvent', 'ArrowLeft', True), ('KeyEvent', 'ArrowRight', False)]
    right = [('KeyEvent', 'ArrowUp', True), ('KeyEvent', 'ArrowLeft', False), ('KeyEvent', 'ArrowRight', True)]
    Forward = [('KeyEvent', 'ArrowUp', True), ('KeyEvent', 'ArrowLeft', False), ('KeyEvent', 'ArrowRight', False)]
    #this is for formatting purposes

    #main logic
    while True:
        #increment a counter for number of iterations
        n += 1

        #if at least one iteration is made, check if turn is needed
        if(n > 1):
            #if at least one iteration check if a turn is needed
            if(observation_n[0] != None):
                #store the reward in the previous score
                prev_score = reward_n[0]

                if(turn):
                    #pick a random event
                    #where to turn?
                    event = random.choice([left, right])
                    #perform an action
                    action_n = [event for ob in observation_n]
                    #set turn to false
                    turn = False
        elif(~turn):
            #if no turn is needed, go straight
            action_n = [Forward for ob in observation_n]


        #if there is an observation, the game has started, check if turn is needed
        if(observation_n[0] != None):
            turn, j, total_sum, prev_total_sum = determine_turn(turn, observation_n[0], j, total_sum, prev_total_sum, reward_n[0])

        #save new variables for each iteration
        observation_n, reward_n, done_n, info = env.step(action_n)

        env.render()

if __name__ == '__main__':
    main()

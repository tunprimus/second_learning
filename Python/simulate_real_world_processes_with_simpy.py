#!/usr/bin/env python3
# Adapted from SimPy: Simulating Real-World Processes With Python -> https://realpython.com/simpy-simulating-with-python/
import random
import simpy
import statistics

wait_times = []


# Creating the Environment: Class Definition
class Theatre(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        """
        Initialise a Theatre object with resources for cashiers, servers, and ushers.

        Parameters
        ----------
        env : simpy.Environment
            The simulation environment in which the processes run.
        num_cashiers : int
            The number of cashiers available in the theatre.
        num_servers : int
            The number of servers available in the theatre.
        num_ushers : int
            The number of ushers available in the theatre.
        """
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.server = simpy.Resource(env, num_servers)
        self.usher = simpy.Resource(env, num_ushers)

    def purchase_ticket(self, movie_goer):
        """
        Simulate the time it takes to purchase a ticket.

        Parameters
        ----------
        movie_goer : str
            The name of the movie goer.

        Yields
        ------
        timeout : simpy.events.Timeout
            A timeout event with a randomly generated time between 1 and 3 minutes.
        """
        # Time it takes to issue tickets from historical data
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, movie_goer):
        """
        Simulate the time it takes to check a ticket.

        Parameters
        ----------
        movie_goer : str
            The name of the movie goer.

        Yields
        ------
        timeout : simpy.events.Timeout
            A timeout event with a fixed time of 3 seconds.
        """
        # Time it takes to check tickets from historical data
        yield self.env.timeout(3 / 60)

    def sell_food(self, movie_goer):
        """
        Simulate the time it takes to sell food to a movie goer.

        Parameters
        ----------
        movie_goer : str
            The name of the movie goer.

        Yields
        ------
        timeout : simpy.events.Timeout
            A timeout event with a randomly generated time between 1 and 5 minutes.
        """
        # Time it takes to buy food from historical data
        yield self.env.timeout(random.randint(1, 5))


# Moving Through the Environment: Function Definition
def go_to_movies(env, movie_goer, theatre):
    """
    Simulates a movie goer going to the movies.

    Parameters
    ----------
    env : simpy.Environment
        The simulation environment
    movie_goer : str
        The name of the movie goer
    theatre : Theatre
        The theatre object

    Yields
    ------
    timeout : simpy.events.Timeout
        A timeout event with the time it takes to go to the movies
    """
    # Movie goer arrives at the theatre
    arrival_time = env.now

    with theatre.cashier.request() as request:
        yield request
        yield env.process(theatre.purchase_ticket(movie_goer))

    with theatre.usher.request() as request:
        yield request
        yield env.process(theatre.check_ticket(movie_goer))

    if random.choice([True, False]):
        with theatre.server.request() as request:
            yield request
            yield env.process(theatre.sell_food(movie_goer))

    wait_times.append(env.now - arrival_time)


# Simulating Multiple Movie Goers: Function Definition
def run_theatre(env, num_cashiers, num_servers, num_ushers, num_movie_goers=5):
    """
    Simulate a movie theatre by running a specified number of movie goers through.

    Parameters
    ----------
    env : simpy.Environment
        The simulation environment
    num_cashiers : int
        The number of cashiers available in the theatre
    num_servers : int
        The number of servers available in the theatre
    num_ushers : int
        The number of ushers available in the theatre
    num_movie_goers : int, optional
        The number of movie goers to simulate. Default is 5.

    Yields
    ------
    timeout : simpy.events.Timeout
        A timeout event with a time of 0.23 seconds, used to pace the simulation
    """
    theatre = Theatre(env, num_cashiers, num_servers, num_ushers)

    for movie_goer in range(num_movie_goers):
        env.process(go_to_movies(env, movie_goer, theatre))

    while True:
        yield env.timeout(0.23)

        movie_goer += 1
        env.process(go_to_movies(env, movie_goer, theatre))


# Calculating the Wait Time: Function Definition
def get_wait_time_statistics(wait_times):
    avg_wait_time = statistics.mean(wait_times)


def calculate_wait_time(wait_times):
    """
    Calculate and format the average wait time given a list of wait times.

    Parameters
    ----------
    wait_times : list
        A list of wait times in minutes

    Returns
    -------
    minutes : int
        The average wait time in minutes
    seconds : int
        The average wait time in seconds
    """
    avg_wait_time = statistics.mean(wait_times)
    # Pretty print the results
    minutes, frac_minutes = divmod(avg_wait_time, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)


# Choosing Parameters: User Input Function Definition
def get_user_input():
    """
    Asks the user to enter the number of cashiers, servers, and ushers working
    and returns these values as a list of integers.

    If the user enters invalid input (i.e. not all inputs are digits), the
    function prints an error message and returns the default values of [1, 1, 1].
    """
    num_cashiers = input("Enter the number of cashiers working: ")
    num_servers = input("Enter the number of servers working: ")
    num_ushers = input("Enter the number of ushers working: ")
    params = [num_cashiers, num_servers, num_ushers]
    if all(str(i).isdigit() for i in params):
        params = [int(x) for x in params]
    else:
        print(
            "Could not pass input. The simulation will use default values (1 cashier, 1 server, 1 usher)."
        )
        params = [1, 1, 1]
    return params


# Finalising the Setup: Main Function Definition
def main():
    """
    The main entry point of the script. Seeds the random number generator with the default value of 42.
    Asks the user for the number of cashiers, servers, and ushers working via the get_user_input function.
    Runs the SimPy simulation for 90 movie goers and prints the average wait time once the simulation is complete.
    """
    # Setup
    random.seed(42)

    num_cashiers, num_servers, num_ushers = get_user_input()
    num_movie_goers = 90

    # Run the simulation
    env = simpy.Environment()
    env.process(
        run_theatre(env, num_cashiers, num_servers, num_ushers, num_movie_goers)
    )
    env.run(until=num_movie_goers)

    # View the results
    mins, secs = calculate_wait_time(wait_times)
    print("Running simulation")
    print(f"The average wait time is {mins} minutes and {secs} seconds.")


if __name__ == "__main__":
    main()

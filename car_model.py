import numpy as np
import pandas
import matplotlib.pyplot as plt

def get_idxs(selection, max_sels):
    sel = np.where(selection)[0][max_sels:]
    selection[sel]=False
    return selection

def car_model(car_cap, car_headway, people_per_hour):
    people = np.sort(np.random.uniform(low=0, high=60, size=(people_per_hour,)))

    not_handled = np.ones((people_per_hour,),dtype=bool)
    load_time = np.zeros((people_per_hour,))
    num_waiting = []
    avg_wait = []
    trip_time = []
    num_people_served = []

    prev_car_time = 0
    while np.sum(not_handled):
        car_time = prev_car_time + car_headway
        sel = (people < car_time) & not_handled
        trip_time.append(car_time)
        num_waiting.append(np.sum(sel))
        sel = get_idxs(sel, car_cap)
        avg_wait.append(np.mean(car_time - people[sel]))
        load_time[sel] = car_time
        num_people_served.append(np.sum(~not_handled))
        not_handled[sel] = False
        prev_car_time = car_time
    per_car_dat = pandas.DataFrame({'line':num_waiting, 'wait_time':avg_wait, 'time':trip_time, 'num_served':num_people_served})
    per_person_dat = pandas.DataFrame({'arrival':people, 'departure':load_time})
    return per_person_dat, per_car_dat



def plot_wait_hist(per_person_dat):
    wait_time = per_person_dat['departure'] - per_person_dat['arrival']
    fig, ax = plt.subplots()
    ax.hist(wait_time, range(0,60))
    ax.set_xlabel('Wait Time (minutes)')
    ax.set_ylabel('Number of people')
    return fig

def plot_wait_line_by_car(per_car_dat, num_people):
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.set_xlabel('Time (minutes)')
    ax.set_ylabel('# of people')
    ax.set_ylim(0,num_people)
    ax.set_xlim(0,55)
    ax2.set_ylim(0,10)

    ax.plot(per_car_dat['time'], per_car_dat['line'], '-r', label='line length')
    ax.plot(per_car_dat['time'], per_car_dat['num_served'], '-.k', label='total served')
    ax2.set_ylabel('Wait Time (minutes)')
    ax2.plot(per_car_dat['time'], per_car_dat['wait_time'], '--b', label='wait time')
    ax2.legend(loc=0)
    ax.legend(loc=0)
    return fig



def plot_wait_bars(arrival, load):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.set_ylim(0,100)
    ax.set_xlim(0,120)

    indiv_height = 100/len(arrival)

    count = 0
    for a,l in zip(arrival, load):
        ax.broken_barh([(a,l-a)],(count*indiv_height, indiv_height))
        count+=1

    return fig



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    people_dat, car_dat = car_model(30, .5, 5000)
    plot_wait_hist(people_dat)
    plot_wait_line_by_car(car_dat)
    


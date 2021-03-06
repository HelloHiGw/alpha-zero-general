import numpy as np
import pandas as pd
import pylab as plt
from matplotlib.ticker import MaxNLocator

from td2020.src.config_class import CONFIG

_skiprows = 73


def fun1(file1, file2):
    df1 = pd.read_csv(file1, skiprows=_skiprows)
    df2 = pd.read_csv(file2, skiprows=_skiprows)

    score1 = df1['score']
    score2 = df2['score']
    score_player1 = score1[(df1.player == 1)]
    score_player2 = score1[(df1.player == -1)]
    score_player3 = score2[(df2.player == 1)]
    score_player4 = score2[(df2.player == -1)]

    score_player3 += 10  # TODO for test

    """
    score_player1 = to_bins_avg(score_player1, int(CONFIG.player1_config.TIMEOUT * 2))
    score_player2 = to_bins_avg(score_player2, int(CONFIG.player1_config.TIMEOUT * 2))
    score_player3 = to_bins_avg(score_player3, int(CONFIG.player1_config.TIMEOUT * 2))
    """
    n_bins = 5
    score_player1 = to_bins_avg(score_player1, int(CONFIG.player1_config.TIMEOUT * 2) * n_bins)
    score_player2 = to_bins_avg(score_player2, int(CONFIG.player1_config.TIMEOUT * 2) * n_bins)
    score_player3 = to_bins_avg(score_player3, int(CONFIG.player1_config.TIMEOUT * 2) * n_bins)
    score_player4 = to_bins_avg(score_player4, int(CONFIG.player1_config.TIMEOUT * 2) * n_bins)

    arrange_both = np.arange(len(score_player1)) + 1

    ax = plt.figure().gca()
    plt.plot(arrange_both, score_player1, 'r--')
    plt.plot(arrange_both, score_player2, 'b--')
    plt.plot(arrange_both, score_player3, 'g--')
    plt.plot(arrange_both, score_player4, 'y--')

    plt.title("Primerjava točk igralcev v koših po " + str(n_bins))
    plt.ylabel("Število točk")
    plt.xlabel("Iteracija igre")
    plt.legend(["Datoteka 1 igralec 1", "Datoteka 1 igralec -1", "Datoteka 2 igralec 1", "Datoteka 2 igralec -1"])
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # force integers on x axis
    plt.show()


def fun2(file, file2=None):
    df_player1 = pd.read_csv(file, skiprows=_skiprows)
    df_player2 = pd.read_csv(file2 or file, skiprows=_skiprows)

    n_bins = 500

    player_1 = df_player1['player']
    act_1 = df_player1['act_rev']

    player_2 = df_player2['player']
    act_2 = df_player2['act_rev']

    move1 = act_1[((df_player1.act_rev == 'up') | (df_player1.act_rev == 'down') | (df_player1.act_rev == 'left') | (df_player1.act_rev == 'right')) & (player_1 == 1)]
    move2 = act_2[((df_player2.act_rev == 'up') | (df_player2.act_rev == 'down') | (df_player2.act_rev == 'left') | (df_player2.act_rev == 'right')) & (player_2 == -1)]

    mine1 = act_1[(df_player1.act_rev == 'mine_resources') & (player_1 == 1)]
    mine2 = act_2[(df_player2.act_rev == 'mine_resources') & (player_2 == -1)]

    return_resources1 = act_1[(df_player1.act_rev == 'return_resources') & (player_1 == 1)]
    return_resources2 = act_2[(df_player2.act_rev == 'return_resources') & (player_2 == -1)]

    attack1 = act_1[((df_player1.act_rev == 'attack_up') | (df_player1.act_rev == 'attack_down') | (df_player1.act_rev == 'attack_right') | (df_player1.act_rev == 'attack_left')) & (player_1 == 1)]
    attack2 = act_2[((df_player2.act_rev == 'attack_up') | (df_player2.act_rev == 'attack_down') | (df_player2.act_rev == 'attack_right') | (df_player2.act_rev == 'attack_left')) & (player_2 == -1)]

    npc1 = act_1[((df_player1.act_rev == 'npc_up') | (df_player1.act_rev == 'npc_down') | (df_player1.act_rev == 'npc_right') | (df_player1.act_rev == 'npc_left')) & (player_1 == 1)]
    npc2 = act_2[((df_player2.act_rev == 'npc_up') | (df_player2.act_rev == 'npc_down') | (df_player2.act_rev == 'npc_right') | (df_player2.act_rev == 'npc_left')) & (player_2 == -1)]

    rifl1 = act_1[((df_player1.act_rev == 'rifle_infantry_up') | (df_player1.act_rev == 'rifle_infantry_down') | (df_player1.act_rev == 'rifle_infantry_right') | (df_player1.act_rev == 'rifle_infantry_left')) & (player_1 == 1)]
    rifl2 = act_2[((df_player2.act_rev == 'rifle_infantry_up') | (df_player2.act_rev == 'rifle_infantry_down') | (df_player2.act_rev == 'rifle_infantry_right') | (df_player2.act_rev == 'rifle_infantry_left')) & (player_2 == -1)]

    barr1 = act_1[((df_player1.act_rev == 'barracks_up') | (df_player1.act_rev == 'barracks_down') | (df_player1.act_rev == 'barracks_right') | (df_player1.act_rev == 'barracks_left')) & (player_1 == 1)]
    barr2 = act_2[((df_player2.act_rev == 'barracks_up') | (df_player2.act_rev == 'barracks_down') | (df_player2.act_rev == 'barracks_right') | (df_player2.act_rev == 'barracks_left')) & (player_2 == -1)]

    th1 = act_1[((df_player1.act_rev == 'town_hall_up') | (df_player1.act_rev == 'town_hall_down') | (df_player1.act_rev == 'town_hall_right') | (df_player1.act_rev == 'town_hall_left')) & (player_1 == 1)]
    th2 = act_2[((df_player2.act_rev == 'town_hall_up') | (df_player2.act_rev == 'town_hall_down') | (df_player2.act_rev == 'town_hall_right') | (df_player2.act_rev == 'town_hall_left')) & (player_2 == -1)]

    heal1 = act_1[((df_player1.act_rev == 'heal_up') | (df_player1.act_rev == 'heal_down') | (df_player1.act_rev == 'heal_right') | (df_player1.act_rev == 'heal_left')) & (player_1 == 1)]
    heal2 = act_2[((df_player2.act_rev == 'heal_up') | (df_player2.act_rev == 'heal_down') | (df_player2.act_rev == 'heal_right') | (df_player2.act_rev == 'heal_left')) & (player_2 == -1)]
    """
    move1= to_bins_count(move1,n_bins)
    move2= to_bins_count(move2,n_bins)

    mine1= to_bins_count(mine1,n_bins)
    mine2= to_bins_count(mine2,n_bins)

    return_resources1= to_bins_count(return_resources1,n_bins)
    return_resources2= to_bins_count(return_resources2,n_bins)

    attack1= to_bins_count(attack1,n_bins)
    attack2= to_bins_count(attack2,n_bins)

    npc1= to_bins_count(npc1,n_bins)
    npc2= to_bins_count(npc2,n_bins)

    rifl1= to_bins_count(rifl1,n_bins)
    rifl2= to_bins_count(rifl2,n_bins)

    barr1= to_bins_count(barr1,n_bins)
    barr2= to_bins_count(barr2,n_bins)

    th1= to_bins_count(th1,n_bins)
    th2= to_bins_count(th2,n_bins)

    heal1= to_bins_count(heal1,n_bins)
    heal2= to_bins_count(heal2,n_bins)
    """

    acts = (  # "Premik",
        "Nabiranje", "Vračanje", "Napad", "Delavec", "Vojak", "Vojašnica", "Glavna hiša", "Zdravljenje")

    # plt.bar(acts, [len(move1), len(mine1), len(return_resources1), len(attack1), len(npc1), len(rifl1), len(barr1), len(th1), len(heal1)], width=0.8)
    # plt.bar(acts, [len(move2), len(mine2), len(return_resources2), len(attack2), len(npc2), len(rifl2), len(barr2), len(th2), len(heal2)], width=0.8, bottom=[len(move1), len(mine1), len(return_resources1), len(attack1), len(npc1), len(rifl1), len(barr1), len(th1), len(heal1)])

    # plt.bar(acts, [len(mine1), len(return_resources1), len(attack1), len(npc1), len(rifl1), len(barr1), len(th1), len(heal1)], width=0.8)
    # plt.bar(acts, [len(mine2), len(return_resources2), len(attack2), len(npc2), len(rifl2), len(barr2), len(th2), len(heal2)], width=0.8, bottom=[len(mine1), len(return_resources1), len(attack1), len(npc1), len(rifl1), len(barr1), len(th1), len(heal1)])

    N = len(acts)
    men_means = (  # len(move1),
        len(mine1), len(return_resources1), len(attack1), len(npc1), len(rifl1), len(barr1), len(th1), len(heal1))
    women_means = (  # len(move2),
        len(mine2), len(return_resources2), len(attack2), len(npc2), len(rifl2), len(barr2), len(th2), len(heal2))

    ind = np.arange(N)
    width = 0.4
    plt.bar(ind, men_means, width)
    plt.bar(ind + width, women_means, width)
    plt.title("Izvajanje akcij dveh igralcev (Izvzeti premiki)")
    plt.xlabel("Akcije (izključeni premiki)")
    plt.ylabel("Število izvedenih akcij")
    plt.xticks(ind, rotation=20, labels=acts)

    plt.legend(["Igralec 1", "Igralec -1"])

    plt.show()


def to_bins_count(x, bins):
    ar = []
    for i in range(0, len(x), bins):
        ar.append(len(x[i:i + bins]))
    return ar


def to_bins_avg(x, bins):
    x = x.astype(int)
    ar = []
    for i in range(0, len(x), bins):
        ar.append(np.average(x[i:i + bins]))
    return ar


def to_bins_sum(x, bins):
    x = x.astype(int)
    ar = []
    for i in range(0, len(x), bins):
        ar.append(sum(x[i:i + bins]))
    return ar


def fun3(file, player):
    df = pd.read_csv(file, skiprows=_skiprows)

    num_bins = 4000

    df_player = df['player']
    act = df['act_rev']

    move1 = (((df.act_rev == 'up') | (df.act_rev == 'down') | (df.act_rev == 'left') | (df.act_rev == 'right')) & (df_player == player))
    move1_bin = to_bins_sum(move1, bins=num_bins)

    mine1 = ((df.act_rev == 'mine_resources') & (df_player == player))
    mine1_bin = to_bins_sum(mine1, bins=num_bins)

    return_resources1 = ((df.act_rev == 'return_resources') & (df_player == player))
    return_resources1_bin = to_bins_sum(return_resources1, bins=num_bins)

    attack1 = (((df.act_rev == 'attack_up') | (df.act_rev == 'attack_down') | (df.act_rev == 'attack_right') | (df.act_rev == 'attack_left')) & (df_player == player))
    attack1_bin = to_bins_sum(attack1, bins=num_bins)

    npc1 = (((df.act_rev == 'npc_up') | (df.act_rev == 'npc_down') | (df.act_rev == 'npc_right') | (df.act_rev == 'npc_left')) & (df_player == player))
    npc1_bin = to_bins_sum(npc1, bins=num_bins)

    rifl1 = (((df.act_rev == 'rifle_infantry_up') | (df.act_rev == 'rifle_infantry_down') | (df.act_rev == 'rifle_infantry_right') | (df.act_rev == 'rifle_infantry_left')) & (df_player == player))
    rifl1_bin = to_bins_sum(rifl1, bins=num_bins)

    barr1 = (((df.act_rev == 'barracks_up') | (df.act_rev == 'barracks_down') | (df.act_rev == 'barracks_right') | (df.act_rev == 'barracks_left')) & (df_player == player))
    barr1_bin = to_bins_sum(barr1, bins=num_bins)

    th1 = (((df.act_rev == 'town_hall_up') | (df.act_rev == 'town_hall_down') | (df.act_rev == 'town_hall_right') | (df.act_rev == 'town_hall_left')) & (df_player == player))
    th1_bin = to_bins_sum(th1, bins=num_bins)

    heal1 = (((df.act_rev == 'heal_up') | (df.act_rev == 'heal_down') | (df.act_rev == 'heal_right') | (df.act_rev == 'heal_left')) & (df_player == player))
    heal1_bin = to_bins_sum(heal1, bins=num_bins)

    all_arrange = np.arange(len(act) / num_bins) + 1

    sum_move_mine = np.add(move1_bin, mine1_bin)
    sum_move_mine_return = np.add(sum_move_mine, return_resources1_bin)
    sum_move_mine_return_attack = np.add(sum_move_mine_return, attack1_bin)
    sum_move_mine_return_attack_npc = np.add(sum_move_mine_return_attack, npc1_bin)
    sum_move_mine_return_attack_npc_rifl = np.add(sum_move_mine_return_attack_npc, rifl1_bin)
    sum_move_mine_return_attack_npc_rifl_barr = np.add(sum_move_mine_return_attack_npc_rifl, barr1_bin)
    sum_move_mine_return_attack_npc_rifl_barr_th = np.add(sum_move_mine_return_attack_npc_rifl_barr, th1_bin)
    sum_move_mine_return_attack_npc_rifl_barr_th_heal = np.add(sum_move_mine_return_attack_npc_rifl_barr_th, heal1_bin)

    """
    plt.plot(all_arrange, move1_bin, color='aqua')
    plt.plot(all_arrange, sum_move_mine, color='gold')
    plt.plot(all_arrange, sum_move_mine_return, color='magenta')
    plt.plot(all_arrange, sum_move_mine_return_attack, color='green')
    plt.plot(all_arrange, sum_move_mine_return_attack_npc, color='orange')
    plt.plot(all_arrange, sum_move_mine_return_attack_npc_rifl, color='teal')
    plt.plot(all_arrange, sum_move_mine_return_attack_npc_rifl_barr, color='orchid')
    plt.plot(all_arrange, sum_move_mine_return_attack_npc_rifl_barr_th, color='lime')
    plt.plot(all_arrange, sum_move_mine_return_attack_npc_rifl_barr_th_heal, color='lightblue')

    plt.fill_between(all_arrange, sum_move_mine_return_attack_npc_rifl_barr_th_heal, color='lightblue')
    plt.fill_between(all_arrange, sum_move_mine_return_attack_npc_rifl_barr_th, color='lime')
    plt.fill_between(all_arrange, sum_move_mine_return_attack_npc_rifl_barr, color='orchid')
    plt.fill_between(all_arrange, sum_move_mine_return_attack_npc_rifl, color='teal')
    plt.fill_between(all_arrange, sum_move_mine_return_attack_npc, color='orange')
    plt.fill_between(all_arrange, sum_move_mine_return_attack, color='green')
    plt.fill_between(all_arrange, sum_move_mine_return, color='magenta')
    plt.fill_between(all_arrange, sum_move_mine, color='gold')
    plt.fill_between(all_arrange, move1_bin, color='aqua')
    
    """
    ax = plt.figure().gca()

    plt.plot(all_arrange, move1_bin, color='aqua')
    plt.plot(all_arrange, mine1_bin, color='gold')
    plt.plot(all_arrange, return_resources1_bin, color='magenta')
    plt.plot(all_arrange, attack1_bin, color='green')
    plt.plot(all_arrange, npc1_bin, color='orange')
    plt.plot(all_arrange, rifl1_bin, color='teal')
    plt.plot(all_arrange, barr1_bin, color='orchid')
    plt.plot(all_arrange, th1_bin, color='lime')
    plt.plot(all_arrange, heal1_bin, color='lightblue')

    plt.legend([
        "Premik",
        "Nabiranje zlatnikov",
        "Vračanje zlatnikov",
        "Napad",
        "Urjenje delavca",
        "Urjenje vojaške enote",
        "Izgradnja vojašnice",
        "Izgradnja glavne hiše",
        "Zdravljenje"
    ])
    plt.title("Izvajanje akcij skozi učni postopek igralca " + str(player))
    plt.xlabel("Število izbranih akcij x " + str(int(num_bins / 2)))
    plt.ylabel("Število odigranih akcij v koših po " + str(int(num_bins / 2)))

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # force integers on x axis
    plt.show()


def fun4(file):
    # this doesn't show any thing useful to viewer

    df = pd.read_csv(file, skiprows=_skiprows)

    num_bins = 200

    player = df['player']
    player1 = player[player == 1]
    output_directionleft_1 = ((df.output_direction == 'left') & (player == 1)) * -1  # multiply with minus for left
    output_directionright_1 = ((df.output_direction == 'right') & (player == 1))

    output_directionleft_2 = ((df.output_direction == 'left') & (player == -1)) * -1  # multiply with minus for left
    output_directionright_2 = ((df.output_direction == 'right') & (player == -1))

    arrange_both = np.arange(len(player1) / (num_bins / 2))

    output_direction_1 = np.add(output_directionleft_1, output_directionright_1)
    output_direction_2 = np.add(output_directionleft_2, output_directionright_2)

    output_direction1_bin = to_bins_sum(output_direction_1, bins=num_bins)
    output_direction2_bin = to_bins_sum(output_direction_2, bins=num_bins)

    plt.plot(output_direction1_bin, arrange_both, 'r--')
    plt.plot(output_direction2_bin, arrange_both, 'b--')
    plt.legend(["Igralec 1", "Igralec -1"])
    plt.title("Smer akcij (levo, desno) v koših po " + str(int(num_bins / 2)))
    plt.ylabel("Število smernih akcij")
    plt.xlabel("Smer izvajanja akcije")
    plt.show()


file1 = ".\\..\\temp\\config_learn.csv"
file2 = ".\\..\\temp\\config_learn.csv"
# file1 = ".\\..\\temp\\config_pit.csv"
# file2 = ".\\..\\temp\\config_pit.csv"

fun1(file1, file2)
# fun2(file1)
# fun2(".\\..\\temp\\config_learn_onehot.csv", ".\\..\\temp\\config_learn_numeric.csv")  # to compare different configs (onehot vs numeric)
fun3(file1, player=1)
fun3(file1, player=-1)
# fun4(".\\..\\temp\\config_learn.csv")
exit(0)

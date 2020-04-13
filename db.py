import sqlite3



def get_id(user_id):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = "SELECT id FROM bj_logs WHERE id=?"
    cur.execute(sql, [user_id])
    return cur.fetchone()

def get_money(user_id):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = "SELECT money FROM bj_logs WHERE id=?"
    cur.execute(sql, [user_id])
    return cur.fetchall()[0][0]

def get_stake(user_id):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = "SELECT stake FROM bj_logs WHERE id=?"
    cur.execute(sql, [user_id])
    return cur.fetchall()[0][0]

def get_pl_taken_cards(user_id):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = "SELECT pl_taken_cards FROM bj_logs WHERE id=?"
    cur.execute(sql, [user_id])
    return cur.fetchall()[0][0]

def get_decks(user_id):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = "SELECT decks FROM bj_logs WHERE id=?"
    cur.execute(sql, [user_id])
    return cur.fetchall()[0][0]

def get_cr_taken_cards(user_id):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = "SELECT cr_taken_cards FROM bj_logs WHERE id=?"
    cur.execute(sql, [user_id])
    return cur.fetchall()[0][0]




def add(id):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    albums = [(id, 100, 0, '0000000000000', 0, '0000000000000')]
    cur.executemany("INSERT INTO bj_logs VALUES (?,?,?,?,?,?)", albums)
    con.commit()

def restart(user_id):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = """
        UPDATE bj_logs 
        SET money = 100
        WHERE id = ?
        """
    cur.execute(sql, [user_id])
    con.commit()



def update_money(user_id,money):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = """
        UPDATE bj_logs 
        SET money = ?
        WHERE id = ?
        """
    cur.execute(sql, [money, user_id])
    con.commit()

def update_stake(user_id,stake):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = """
        UPDATE bj_logs 
        SET stake = ?
        WHERE id = ?
        """
    cur.execute(sql, [stake, user_id])
    con.commit()


def update_pl_taken_cards(user_id, pl_taken_cards):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = """
        UPDATE bj_logs 
        SET pl_taken_cards = ?
        WHERE id = ?
        """
    cur.execute(sql, [pl_taken_cards, user_id])
    con.commit()


def update_decks(user_id, decks):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = """
        UPDATE bj_logs 
        SET decks = ?
        WHERE id = ?
        """
    cur.execute(sql, [decks, user_id])
    con.commit()


def update_cr_taken_cards(user_id, cr_taken_cards):
    con = sqlite3.connect("bj_data_base.db")
    cur = con.cursor()
    sql = """
        UPDATE bj_logs 
        SET cr_taken_cards = ?
        WHERE id = ?
        """
    cur.execute(sql, [cr_taken_cards, user_id])
    con.commit()


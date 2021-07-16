from flask import Flask, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("Meetings.db")

#DATA = {user_token, name, place, city, time, max_amntPeople, description}
#
@app.route("/create_meeting", methods=['POST','GET'])
def create_meeting():
    data = request.form
    sql_append = """insert into meetings (NAME, PLACE, CITY, TIME, AMNT_PEOPLE, DESCRIPTION, RATE, CREATER_TOKEN) VALUES (?,?,?,?,?,?,?,?)"""
    querytoDB(sql_append,(data['name'],data['place'],data['city'],data['time'],data['max_amntPeople'], data['description'],'',data['user_token']),True)
    
    return("hello world")

#DATA = {id, user_token, name, place, city, time, max_amntPeople, description}
#
@app.route("/edit_meeting", methods=['POST'])
def edit_meeting():
    data = request.form 
    sql_edit = """UPDATE meetings SET NAME=?, PLACE=?, CITY=?, TIME=?, AMNT_PEOPLE=?, DESCRIPTION=? WHERE id=?"""
    querytoDB(sql_edit,(data['name'],data['place'],data['city'],data['time'],data['max_amntPeople'],data['description'],data['id']), True)
    return {'OK':200}


#DATA = {id}
#                                                               #FIXME there is no ownership checking
@app.route("/delete_meeting", methods=['POST'])
def delete_meeting():
    data = request.form
    sql_delete = """DELETE FROM meetings WHERE id=?"""
    querytoDB(sql_delete,(data['id'],), True)
    return(data['id'] + " has been deleted")


#DATA = {id}
#
@app.route("/get_meeting", methods=['POST'])
def get_meeting():
    data = request.form
    sql_getting = """SELECT * FROM meetings WHERE id=?"""
    content = querytoDB(sql_getting,(data['id'],),False)
    content = parse_meeting_info(content)
    return content

#Data = {city}
#
@app.route("/get_meetings_of_city", methods=['POST'])
def get_meetings_of_city():
    data = request.form
    sql_getting_city = """SELECT id FROM meetings WHERE CITY=?"""
    res = querytoDB(sql_getting_city,(data['city'],), False)
    res = parse_ids(res)
    return {'ids':res}


@app.route("/")
def hello():
    return("WORKING!!!!")


'''
parsing sqlite output into json
'''
def parse_meeting_info(content):
    content = content[0]
    res = {"id":content[0],"name":content[1],"place":content[2],"city":content[3],"time":content[4],"max_amntPeople":content[5],"description":content[6],"rate":content[7],"creater_token":content[8]}
    return res


def parse_ids(ids):
    list_id = []
    for i in ids:
        list_id.append(i[0])
    return list_id


def querytoDB(query, data, isCommit):
    conn = sqlite3.connect("Meetings.db")
    cursor = conn.cursor()
    cursor.execute(query,data)
    if isCommit:
        conn.commit()
        res = ''
    elif not isCommit:
        res = cursor.fetchall()
    conn.close()
    return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8887)
    

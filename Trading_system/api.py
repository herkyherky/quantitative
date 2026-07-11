from flask import Flask, jsonify
import pymysql

 
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='kali',
    database='tradinghold')
cursor = conn.cursor()
query = "select * from hold where name ='uavs';"
cursor.execute(query)
results = cursor.fetchall()

# print(results[0][2])
cursor.close()
conn.commit()
conn.close()

app=Flask(__name__)
@app.route('/get_data', methods=['GET'])
def get_data():
    data ={
        'name': results[0][1],
        'price': results[0][2],
        'type':results[0][3],
        'num': results[0][4],
        'volume': results[0][5]
    }
    return jsonify(data)
if __name__ =='__main__':
    app.run(debug=True)



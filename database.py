import mysql.connector
import pandas as pd

def get_employee_data():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Windows@11',  # <-- change this
            database='employee_db'
        )
        query = "SELECT * FROM employee_performance"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except mysql.connector.Error as err:
        print("Error:", err)
        return pd.DataFrame()

def get_processed_employee_data():
    df = get_employee_data()
    
    # Normalize the metrics
    df['kpi_norm'] = df['kpi_score'] / df['kpi_score'].max()
    df['attendance_norm'] = df['attendance'] / df['attendance'].max()
    df['appraisal_norm'] = df['appraisal_rating'] / df['appraisal_rating'].max()
    
    # Weighted performance score
    df['performance_score'] = (
        df['kpi_norm'] * 0.4 +
        df['attendance_norm'] * 0.3 +
        df['appraisal_norm'] * 0.3
    )
    
    return df

import sqlite3
import state as state
import memory as mem
from datetime import datetime

def delete_table(c, table):
    c.execute(f"DROP TABLE IF EXISTS {table}")

def get_tables_names(parth):
	with sqlite3.connect(parth) as conn:
		c = conn.cursor() 
		c.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tables = c.fetchall()
	return tables

def get_table(parth: str, table: str):
	with sqlite3.connect(parth) as conn:
		c = conn.cursor() 
		c.execute(f"SELECT * FROM {table}")
		data_from_sql = c.fetchmany(10)
	return data_from_sql

def get_val(db_path: str, table: str, param_list: list, fetch_range: int, case_number: int):

	columns_str = " ,".join(param_list)
	print(f'columns_str -> {columns_str}')
	query = f"""
		SELECT {columns_str}
        FROM {table}
		WHERE case_number = ?""" # ? ist platzhalter für case_number

	with sqlite3.connect(db_path) as conn:
		conn.row_factory = sqlite3.Row
		c = conn.cursor()
		c.execute(query, (case_number,))
		rows = c.fetchmany(fetch_range)

	result = {col: [] for col in param_list}
	for row in rows:
		for col in param_list:
			result[col].append(row[col])

	return result

def get_all_cn(parth: str, table: str):
	try:
		with sqlite3.connect(parth) as conn:
			c = conn.cursor() 
			c.execute(f"SELECT case_number FROM {table}")
			cn_list = c.fetchall()
			cn_arr = []
			for cn in cn_list:
				if not cn[0] in cn_arr:
					cn_arr.append(cn[0])
			return cn_arr
	except Exception as e:
		print('get_all_cn -> casnumbers could not be extracted')
		print(e)
		return None
	

def create_table(c, conn, table_name):
    c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_number INTEGER NOT NULL,
		start_time TEXT,
        clock_time NUMERIC NOT NULL,
        perfusion_time NUMERIC NOT NULL,
		gas_flow NUMERIC,
		fio2 NUMERIC,
        notes TEXT,
        art_flow NUMERIC,
        art_pressure NUMERIC,
        art_temp NUMERIC,
        ven_flow NUMERIC,
        ven_pressure NUMERIC, 
        ven_temp NUMERIC, 
        return_temp NUMERIC, 
        art_ph NUMERIC,
        art_pco2 NUMERIC,
        art_po2 NUMERIC,
        hco3 NUMERIC,
        base NUMERIC,
        cso2 NUMERIC,
        na NUMERIC,
        k NUMERIC,
        ca NUMERIC,
        cl NUMERIC,
        vo2 NUMERIC,
        do2 NUMERIC,
        ven_ph NUMERIC,
        ven_pco2 NUMERIC,
        ven_po2 NUMERIC,
		so2 NUMERIC,
        hct NUMERIC,
        hb NUMERIC,
        lactate NUMERIC,
        glucose NUMERIC,
		bilirubin NUMERIC,
		system_volume NUMERIC,
        filter_flow NUMERIC, 
        substitude_flow NUMERIC,
        biliary_flow NUMERIC,
        biliary_ph NUMERIC,
        biliary_hco3 NUMERIC,
        biliary_glucose NUMERIC,
		biliary_bilirubin NUMERIC,
        med1 NUMERIC,
        med2 NUMERIC,
        med3 NUMERIC,
        med4 NUMERIC,
        med5 NUMERIC,
        med6 NUMERIC,
        med7 NUMERIC,
        med8 NUMERIC,
        med9 NUMERIC,
        med10 NUMERIC,
        med11 NUMERIC,
        med12 NUMERIC,
        med13 NUMERIC,
        med14 NUMERIC,
        med15 NUMERIC
    )""")
    conn.commit()
    return 0

def execute_entry(parth: str, table: str,  sys_state: dict):
	try:
		conn = sqlite3.connect(parth, isolation_level='IMMEDIATE')
		c = conn.cursor() 
		t = datetime.now()
		dt_str = t.strftime("%Y_%m_%d %H:%M:%S")
		print('db entry')
		c.execute(
			f"""INSERT INTO {table} (
				case_number,
				start_time,
				clock_time,
				perfusion_time,
				notes,
				art_flow,
				art_pressure,
				art_temp,
				ven_flow,
				ven_pressure, 
				ven_temp, 
				return_temp,
				art_ph, 
				art_pco2, 
				art_po2, 
				hco3, 
				base, 
				cso2,
				na,
				k,
				ca,
				cl,
				vo2, 
				do2, 
				ven_ph, 
				ven_pco2, 
				ven_po2, 
				ven_temp, 
				so2, 
				hct, 
				hb,  
				lactate,
				glucose,
				bilirubin,
				system_volume,
				filter_flow, 
				substitude_flow,
				biliary_flow,
				biliary_ph,
				biliary_hco3,
				biliary_glucose,
				biliary_bilirubin,
				med1,
				med2,
				med3,
				med4,
				med5,
				med6,
				med7,
				med8,
				med9,
				med10,
				med11,
				med12,
				med13,
				med14,
				med15
			)
			VALUES(
				:case_number,
				:start_time,
				:clock_time,
				:perfusion_time,
				:notes,
				:art_flow,
				:art_pressure,
				:art_temp,
				:ven_flow,
				:ven_pressure, 
				:ven_temp, 
				:return_temp,
				:art_ph, 
				:art_pco2, 
				:art_po2, 
				:hco3, 
				:base, 
				:cso2,
				:na,
				:k,
				:ca,
				:cl,
				:vo2, 
				:do2, 
				:ven_ph, 
				:ven_pco2, 
				:ven_po2, 
				:ven_temp, 
				:so2, 
				:hct, 
				:hb,  
				:lactate,
				:glucose,
				:bilirubin,
				:system_volume,
				:filter_flow, 
				:substitude_flow,
				:biliary_flow,
				:biliary_ph,
				:biliary_hco3,
				:biliary_glucose,
				:biliary_bilirubin,
				:med1,
				:med2,
				:med3,
				:med4,
				:med5,
				:med6,
				:med7,
				:med8,
				:med9,
				:med10,
				:med11,
				:med12,
				:med13,
				:med14,
				:med15
			)""",
			{'case_number':     sys_state['system']['case_number'],
			'start_time':		sys_state['system']['start_time'],
			'clock_time': 		sys_state['system']['clock_time'],
			'perfusion_time':   sys_state['system']['perfusion_time'], 
			'notes':            sys_state['notes'],
			'art_flow':         sys_state['art_flow']['val'],
			'art_pressure':     sys_state['art_pressure']['val'],
			'art_temp':         sys_state['art_temp']['val'],
			'ven_flow':         sys_state['ven_flow']['val'],
			'ven_pressure':     sys_state['ven_pressure']['val'],
			'ven_temp':         sys_state['ven_temp']['val'],
			'return_temp':      sys_state['return_temp']['val'],
			'art_ph':           sys_state['art_ph']['val'],
			'art_pco2':         sys_state['art_pco2']['val'],
			'art_po2':          sys_state['art_po2']['val'],
			'hco3':             sys_state['hco3']['val'],
			'base':             sys_state['base']['val'],
			'cso2':             sys_state['cso2']['val'],
			'na':               sys_state['na']['val'],
			'k':                sys_state['k']['val'],
			'ca':               sys_state['ca']['val'],
			'cl':               sys_state['cl']['val'],
			'vo2':              sys_state['vo2']['val'],
			'do2':              sys_state['do2']['val'],
			'ven_ph':           sys_state['ven_ph']['val'],
			'ven_pco2':         sys_state['ven_pco2']['val'],
			'ven_po2':          sys_state['ven_po2']['val'],
			'so2':              sys_state['so2']['val'],
			'hct':              sys_state['hct']['val'],
			'hb':               sys_state['hb']['val'],
			'lactate':          sys_state['lactate']['val'],
			'glucose':          sys_state['glucose']['val'],
			'bilirubin':		sys_state['lab']['bilirubin'],
			'system_volume':    sys_state['fluid_balance']['system_volume'],
			'filter_flow':      sys_state['fluid_balance']['filter_flow'],
			'substitude_flow':  sys_state['fluid_balance']['substitude_flow'],
			'biliary_flow':		0,
			'biliary_ph':		0,
			'biliary_hco3':		0,
			'biliary_glucose':	0,
			'biliary_bilirubin':0,
			'med1':             0,
			'med2':             0,
			'med3':             0,
			'med4':             0,
			'med5':             0,        
			'med6':             0,
			'med7':             0,        
			'med8':             0,
			'med9':             0,        
			'med10':            0,
			'med11':            0,        
			'med12':            0,
			'med13':            0,        
			'med14':            0,
			'med15':            0
			})
		print('value commited to db')
		conn.commit()
		conn.close()
	except Exception as e:
		print('ERROR : data entry could not be executed')
		print(e)

if __name__ == "__main__":
	import os

	table = 'test'
	db_path = r'C:\Users\whwei\OneDrive\coding\data_vault.db'
	cache_path = r'C:\Temp\diskcache_test'
	os.makedirs(cache_path, exist_ok=True)
	sys_state = state.create_state(db_path)
	sys_state['system']['case_number'] = 2
	sys_state['system']['start_time'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
	graph_list = ["ph_graph", "base_lact_graph", "k_gluc_graph", "do2_vo2_graph", "po2_graph", "pco2_graph", "flow_graph", "pressure_graph", "hb_hct_graph"]
	execute_entry(db_path, table, sys_state)
	# mem.create_cache(cache_path, 'key', sys_state)


	cn = get_all_cn(db_path, table)
	print(f'case numbers -> {cn}')

	graph_data = get_val(db_path, table, ['start_time'], 1, 2)
	print(f'graph data : {graph_data['start_time'][0]}, type{type(graph_data['start_time'][0])}')

	with sqlite3.connect(db_path) as conn:
		c = conn.cursor() 
		create_table(c, conn, 'test')
		tables = get_tables_names(db_path)
		print(f'tables : {tables}')

	# with sqlite3.connect(db_path) as conn:
	# 	c = conn.cursor() 
	# 	delete_table(c, 'test')


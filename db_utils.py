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

def get_val(parth: str, table: str, val: str, range: int, case_number: int):		
	try:
		with sqlite3.connect(parth) as conn:
			c = conn.cursor() 
			c.execute(f"SELECT {val} FROM {table} WHERE case_number = {case_number}")
			if case_number < 0:
				c.execute(f"SELECT {'case_number'} FROM {table}")
			if range > 0:
				values = c.fetchmany(range)
			else:
				values = c.fetchall()
				print('values : ', values)
		val_arr = []	
		for val in values:
			val_arr.append(val[0])
		return val_arr
	except Exception as e:
		print('value array could not be extracted from database')
		print(e)
		return None

def data_request():
	pass

def entry_request():
	pass

def stop_record():
	pass

def change_entry():
	pass

def create_table(c, conn, table_name):
    c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_number INTEGER,
        clock_time NUMERIC NOT NULL,
        perfusion_time NUMERIC NOT NULL,
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
        med15 NUMERNIC
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
			'bilirubin':		sys_state['bilirubin']['val'],
			'system_volume':    sys_state['system_volume'],
			'filter_flow':      sys_state['filter_flow']['val'],
			'substitude_flow':  sys_state['substitude_flow']['val'],
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
	db_parth = r'data_vault.db'
	cache_path = r'C:\Temp\diskcache_test'
	os.makedirs(cache_path, exist_ok=True)
	sys_state = state.create_state(db_parth)
	sys_state['system']['case_number'] = 1
	# print(sys_state)
	execute_entry(db_parth, table, sys_state)
	# mem.create_cache(cache_path, 'key', sys_state)


	tables = get_tables_names(db_parth)
	print(tables)

	val = get_val(db_parth, table, 'case_number', 100, 1)
	print(val)
	
	val_II = get_val(db_parth, table, 'case_number', -1, -1)
	print(val_II)
	# print(type(val_II[2]))

	# with sqlite3.connect(db_parth) as conn:
	# 	c = conn.cursor() 
	# 	create_table(c, conn, 'test')
	# 	tables = get_tables_names('data_vault.db')
	# 	print(tables)

	# with sqlite3.connect(db_parth) as conn:
	# 	c = conn.cursor() 
	# 	delete_table(c, 'test')


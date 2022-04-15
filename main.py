import jaydebeapi
import os
import pandas as pd
conn = jaydebeapi.connect(
'oracle.jdbc.driver.OracleDriver',
'jdbc:oracle:thin:de3hd/bilbobaggins@de-oracle.chronosavant.ru:1521/deoracle',
['de3hd','bilbobaggins'],
'ojdbc7.jar')
curs = conn.cursor()

def init():
	curs.execute('''DROP TABLE de3hd.s_02_DWH_FACT_transactions''')
	curs.execute('''DROP TABLE de3hd.s_02_DWH_FACT_PSSPRT_BLCKLST''')
	curs.execute('''DROP TABLE de3hd.s_02_DWH_DIM_terminals''')
	curs.execute('''DROP TABLE de3hd.s_02_rep_fraud''')
	curs.execute('''DROP TABLE de3hd.s_02_DWH_DIM_transactions_HIST''')
	
	#curs.execute('''DROP TABLE de3hd.s_02_DWH_DIM_PSSPRT_BLCKLST_HIST''')

	curs.execute('''CREATE TABLE de3hd.s_02_DWH_FACT_transactions(
		trans_id varchar(128),
		trans_date timestamp,
		amt decimal,
		card_num varchar(128),
		oper_type varchar(128),
		oper_result varchar(128),
		terminal varchar(128))
	''')

	curs.execute('''CREATE TABLE de3hd.s_02_DWH_DIM_transactions_HIST(
		trans_id varchar(128),
		trans_date timestamp,
		amt decimal,
		card_num varchar(128),
		oper_type varchar(128),
		oper_result varchar(128),
		terminal varchar(128),
		effective_from timestamp default current_timestamp,
		effective_to timestamp default TO_TIMESTAMP('2999-12-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS'),
		deleted_flg integer default 0)
	''')

	curs.execute('''CREATE TABLE de3hd.s_02_DWH_FACT_PSSPRT_BLCKLST(
		passport_num varchar(128),
		entry_dt timestamp)
	''')

	#curs.execute('''CREATE TABLE de3hd.s_02_DWH_DIM_PSSPRT_BLCKLST_HIST(
		#passport varchar(128),
		#entry_dt timestamp,
		#effective_from timestamp default current_timestamp,
		#effective_to timestamp default TO_TIMESTAMP('2999-12-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS'),
		#deleted_flg integer default 0)
	#''')

	curs.execute('''CREATE TABLE de3hd.s_02_DWH_DIM_terminals(
		terminal_id varchar(128),
		terminal_type varchar(128),
		terminal_city varchar(128),
		terminal_address varchar(128),
		create_dt timestamp default current_timestamp,
		update_dt timestamp default TO_TIMESTAMP('2999-12-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS'))
	''')

	curs.execute('''CREATE TABLE de3hd.s_02_rep_fraud(
		event_dt timestamp,
		passport varchar(128),
		fio varchar(128),
		phone varchar(128),
		event_type varchar(128),
		report_dt timestamp default current_timestamp
		)''')

def load_data_transactions(path):
	curs.execute('''CREATE TABLE de3hd.s_02_STG_transactions(
		trans_id varchar(128),
		trans_date timestamp,
		amt decimal,
		card_num varchar(128),
		oper_type varchar(128),
		oper_result varchar(128),
		terminal varchar(128))
	''')

	df = pd.read_csv(path, sep = ';')

	curs.executemany('''
		INSERT INTO de3hd.s_02_STG_transactions (trans_id, trans_date, amt, card_num, oper_type, oper_result, terminal) VALUES (?, TO_TIMESTAMP(?, 'YYYY-MM-DD HH24:MI:SS'), ?, ?, ?, ?, ?)
		''', df.values.tolist())

def load_data_terminals(path):
	curs.execute('''CREATE TABLE de3hd.s_02_STG_terminals(
		terminal_id varchar(128),
		terminal_type varchar(128),
		terminal_city varchar(128),
		terminal_address varchar(128))
	''')

	df = pd.read_excel(path, sheet_name = 'terminals')

	curs.executemany('''
		INSERT INTO de3hd.s_02_STG_terminals (terminal_id, terminal_type, terminal_city, terminal_address) VALUES (?, ?, ?, ?)
		''', df.values.tolist())

def load_data_blacklist(path):
	df = pd.read_excel(path, sheet_name = 'blacklist')
	df['conv'] = df['date'].astype(str)
	df = df.drop('date', axis = 1)

	curs.execute('''CREATE TABLE de3hd.s_02_STG_PSSPRT_BLCKLST(
		passport_num varchar(128), 
		entry_dt timestamp)
	''')

	curs.executemany('''
		INSERT INTO de3hd.s_02_STG_PSSPRT_BLCKLST (passport_num, entry_dt) 
		VALUES (?, TO_TIMESTAMP(?, 'YYYY-MM-DD HH24:MI:SS'))
	''', df.values.tolist())

def update_main_tables():
	curs.execute('''INSERT INTO de3hd.s_02_DWH_FACT_transactions(
		trans_id, 
		trans_date, 
		amt, 
		card_num, 
		oper_type, 
		oper_result, 
		terminal
	) SELECT 
		trans_id, 
		trans_date, 
		amt, 
		card_num, 
		oper_type, 
		oper_result, 
		terminal 
	FROM de3hd.s_02_STG_transactions''')

	curs.execute('''UPDATE de3hd.s_02_DWH_DIM_transactions_HIST
		set effective_to = current_timestamp-1,
		deleted_flg = 1
		where effective_to = TO_TIMESTAMP('2999-12-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
	''')

	curs.execute('''INSERT INTO de3hd.s_02_DWH_DIM_transactions_HIST(
		trans_id, 
		trans_date, 
		amt, 
		card_num, 
		oper_type, 
		oper_result, 
		terminal
	) SELECT 
		trans_id, 
		trans_date, 
		amt, 
		card_num, 
		oper_type, 
		oper_result, 
		terminal 
	FROM de3hd.s_02_STG_transactions''')

	curs.execute('''UPDATE de3hd.s_02_DWH_DIM_terminals
		set update_dt = current_timestamp-1
		where update_dt = TO_TIMESTAMP('2999-12-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
	''')

	curs.execute('''INSERT INTO de3hd.s_02_DWH_DIM_terminals(
		terminal_id, 
		terminal_type, 
		terminal_city, 
		terminal_address
	) SELECT 
		terminal_id, 
		terminal_type, 
		terminal_city, 
		terminal_address
	FROM de3hd.s_02_STG_terminals''')

	curs.execute('''INSERT INTO de3hd.s_02_DWH_FACT_PSSPRT_BLCKLST(
		passport_num, 
		entry_dt
	) SELECT 
		passport_num, 
		entry_dt
	FROM de3hd.s_02_STG_PSSPRT_BLCKLST''')

def report_on_fraud_by_type():
	curs.execute('''CREATE TABLE de3hd.s_02_STG_rep_fraud_type0 as	
		SELECT t1.trans_date as event_dt, 	
		t4.passport_num as passport, 	
		t4.first_name || ' ' || t4.last_name as fio, 	
		t4.phone as phone, 
		'заблокированный паспорт' as event_type 
		FROM de3hd.s_02_DWH_DIM_transactions_HIST t1 
		LEFT JOIN BANK.cards t2 
		ON regexp_replace(t1.card_num, ' ') = regexp_replace(t2.card_num, ' ') 
		LEFT JOIN BANK.accounts t3 
		ON t2.account = t3.account 
		LEFT JOIN BANK.clients t4 
		ON t3.client = t4.client_id 
		INNER JOIN de3hd.s_02_DWH_FACT_PSSPRT_BLCKLST t5 
		ON t4.passport_num = t5.passport_num 
		WHERE t1.trans_date > t5.entry_dt 
		AND t1.deleted_flg = 0''')

	curs.execute('''CREATE TABLE de3hd.s_02_STG_rep_fraud_type1 as
		SELECT t1.trans_date as event_dt, 
		t4.passport_num as passport, 
		t4.first_name || ' ' || t4.last_name as fio, 
		t4.phone as phone, 
		'просроченный паспорт' as event_type 
		FROM de3hd.s_02_DWH_DIM_transactions_HIST t1 
		LEFT JOIN BANK.cards t2 
		ON regexp_replace(t1.card_num, ' ') = regexp_replace(t2.card_num, ' ') 
		LEFT JOIN BANK.accounts t3 
		ON t2.account = t3.account 
		LEFT JOIN BANK.clients t4 
		ON t3.client = t4.client_id 
		WHERE t4.passport_valid_to < t1.trans_date
		AND t1.deleted_flg = 0''')

	curs.execute('''CREATE TABLE de3hd.s_02_STG_rep_fraud_type2 as	
		SELECT t1.trans_date as event_dt, 
		t4.passport_num as passport, 
		t4.first_name || ' ' || t4.last_name as fio, 
		t4.phone as phone, 
		'недействующий договор' as event_type 
		FROM de3hd.s_02_DWH_DIM_transactions_HIST t1 
		LEFT JOIN BANK.cards t2 
		ON regexp_replace(t1.card_num, ' ') = regexp_replace(t2.card_num, ' ') 
		LEFT JOIN BANK.accounts t3 
		ON t2.account = t3.account 
		LEFT JOIN BANK.clients t4 
		ON t3.client = t4.client_id 
		WHERE t1.trans_date > t3.valid_to
		AND t1.deleted_flg = 0''')

	curs.execute('''CREATE TABLE de3hd.s_02_STG_trans_with_cities AS 
		SELECT t1.trans_id, t1.card_num, t1.trans_date, t1.amt, t2.terminal_city, 
		lag(t1.trans_date) over(partition by card_num order by trans_date) as prev_date, 
		lag(t2.terminal_city) over(partition by card_num order by trans_date) as prev_city 
		FROM de3hd.s_02_DWH_DIM_transactions_HIST t1 
		LEFT JOIN de3hd.s_02_DWH_DIM_terminals t2	
		ON t1.terminal = t2.terminal_id
		WHERE current_timestamp between t2.create_dt and t2.update_dt
		AND t1.deleted_flg = 0
	''')

	curs.execute('''CREATE TABLE de3hd.s_02_STG_rep_fraud_type3 as 
		SELECT t1.trans_date as event_dt, 
		t4.passport_num as passport, 
		t4.first_name || ' ' || t4.last_name as fio, 
		t4.phone as phone, 
		'операции в разных городах в течение часа' as event_type 
		FROM de3hd.s_02_STG_trans_with_cities t1 
		LEFT JOIN BANK.cards t2 
		ON regexp_replace(t1.card_num, ' ') = regexp_replace(t2.card_num, ' ') 
		LEFT JOIN BANK.accounts t3 
		ON t2.account = t3.account 
		LEFT JOIN BANK.clients t4 
		ON t3.client = t4.client_id 
		WHERE t1.prev_city <> t1.terminal_city 
		AND TO_TIMESTAMP(t1.trans_date) - TO_TIMESTAMP(t1.prev_date) < INTERVAL '01:00' HOUR TO MINUTE''')

	curs.execute('''CREATE TABLE de3hd.s_02_STG_trans_triplets as 
		SELECT t2.* 
		FROM (SELECT t1.*, 
		lag(t1.trans_date) over(partition by card_num order by trans_date) as prev_date, 
		lag(t1.trans_date, 2) over(partition by card_num order by trans_date) as prev_date_2, 
		lag(t1.oper_result) over(partition by card_num order by trans_date) as prev_res, 
		lag(t1.oper_result, 2) over(partition by card_num order by trans_date) as prev_res_2, 
		lag(t1.amt) over(partition by card_num order by trans_date) as prev_amount, 
		lag(t1.amt, 2) over(partition by card_num order by trans_date) as prev_amount_2 
		FROM de3hd.s_02_DWH_DIM_transactions_HIST t1
		WHERE t1.deleted_flg = 0) t2 
		WHERE prev_res = 'REJECT' AND prev_res_2 = 'REJECT' AND oper_result = 'SUCCESS' \
		AND prev_amount < prev_amount_2 AND amt < prev_amount 
		AND TO_TIMESTAMP(trans_date) - TO_TIMESTAMP(prev_date_2) < INTERVAL '20:00' MINUTE TO SECOND''')

	curs.execute('''CREATE TABLE de3hd.s_02_STG_rep_fraud_type4 as 
		SELECT t1.trans_date as event_dt, 
		t4.passport_num as passport, 
		t4.first_name || ' ' || t4.last_name as fio, 
		t4.phone as phone, 
		'попытка подбора суммы' as event_type 
		FROM de3hd.s_02_STG_trans_triplets t1 
		LEFT JOIN BANK.cards t2 
		ON regexp_replace(t1.card_num, ' ') = regexp_replace(t2.card_num, ' ') 
		LEFT JOIN BANK.accounts t3 
		ON t2.account = t3.account 
		LEFT JOIN BANK.clients t4 
		ON t3.client = t4.client_id''')

def create_final_report():
	curs.execute('''INSERT INTO de3hd.s_02_rep_fraud (event_dt, passport, fio, phone, event_type)
		SELECT * FROM de3hd.s_02_STG_rep_fraud_type0''') 
	curs.execute('''INSERT INTO de3hd.s_02_rep_fraud (event_dt, passport, fio, phone, event_type)
		SELECT * FROM de3hd.s_02_STG_rep_fraud_type1''') 
	curs.execute('''INSERT INTO de3hd.s_02_rep_fraud (event_dt, passport, fio, phone, event_type)
		SELECT * FROM de3hd.s_02_STG_rep_fraud_type2''') 
	curs.execute('''INSERT INTO de3hd.s_02_rep_fraud (event_dt, passport, fio, phone, event_type)
		SELECT * FROM de3hd.s_02_STG_rep_fraud_type3''') 
	curs.execute('''INSERT INTO de3hd.s_02_rep_fraud (event_dt, passport, fio, phone, event_type)
		SELECT * FROM de3hd.s_02_STG_rep_fraud_type4''') 	

def show_data(source):
	curs.execute(f'''SELECT * FROM {source}''')
	for row in curs.fetchall():	
		print(row)

def delete_tmp_tables():
	curs.execute('''DROP TABLE de3hd.s_02_STG_transactions''')
	curs.execute('''DROP TABLE de3hd.s_02_STG_terminals''')
	curs.execute('''DROP TABLE de3hd.s_02_STG_rep_fraud_type1''')
	curs.execute('''DROP TABLE de3hd.s_02_STG_rep_fraud_type2''')
	curs.execute('''DROP TABLE de3hd.s_02_STG_trans_with_cities''')
	curs.execute('''DROP TABLE de3hd.s_02_STG_rep_fraud_type3''')
	curs.execute('''DROP TABLE de3hd.s_02_STG_rep_fraud_type4''')
	curs.execute('''DROP TABLE de3hd.s_02_STG_trans_triplets''')
	curs.execute('''DROP TABLE de3hd.s_02_STG_rep_fraud_type0''')
	curs.execute('''DROP TABLE de3hd.s_02_STG_PSSPRT_BLCKLST''')

def relocate_file_to_archive(file_name):
	source_path = 'C://Users//Федор//env//'
	destination_path = 'C://Users//Федор//env//archive//'
	os.rename(source_path + file_name, destination_path + file_name + '.backup')

init()

load_data_transactions('C://Users//Федор//env//transactions_01032021.csv')
relocate_file_to_archive('transactions_01032021.csv')
load_data_terminals('C://Users//Федор//env//terminals_01032021.xlsx')
relocate_file_to_archive('terminals_01032021.xlsx')
load_data_blacklist('C://Users//Федор//env//passport_blacklist_01032021.xlsx')
relocate_file_to_archive('passport_blacklist_01032021.xlsx')
update_main_tables()
report_on_fraud_by_type()
create_final_report()
delete_tmp_tables()

load_data_transactions('C://Users//Федор//env//transactions_02032021.csv')
relocate_file_to_archive('transactions_02032021.csv')
load_data_terminals('C://Users//Федор//env//terminals_02032021.xlsx')
relocate_file_to_archive('terminals_02032021.xlsx')
load_data_blacklist('C://Users//Федор//env//passport_blacklist_02032021.xlsx')
relocate_file_to_archive('passport_blacklist_02032021.xlsx')
update_main_tables()
report_on_fraud_by_type()
create_final_report()
delete_tmp_tables()

load_data_transactions('C://Users//Федор//env//transactions_03032021.csv')
relocate_file_to_archive('transactions_03032021.csv')
load_data_terminals('C://Users//Федор//env//terminals_03032021.xlsx')
relocate_file_to_archive('terminals_03032021.xlsx')
load_data_blacklist('C://Users//Федор//env//passport_blacklist_03032021.xlsx')
relocate_file_to_archive('passport_blacklist_03032021.xlsx')
update_main_tables()
report_on_fraud_by_type()
create_final_report()
delete_tmp_tables()
show_data('de3hd.s_02_rep_fraud')
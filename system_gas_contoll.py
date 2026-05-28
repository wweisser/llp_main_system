import ser_utils
import ser
import onque as oq

async def regulate_gas(sys_state, tx_q):
	current_po2_flow = sys_state['repiratory_controlls']['air_flow']
	current_air_flow = sys_state['repiratory_controlls']['oxygen_flow']
	set_po2_flow = sys_state['repiratory_controlls']['set_oxygen_flow']
	set_air_flow = sys_state['repiratory_controlls']['set_air_flow']
	gas_flow = current_po2_flow + current_air_flow
	target_gas_flow = sys_state['repiratory_controlls']['set_gas_flow']
	cybernation = sys_state['repiratory_controlls']['gas_cybernation']
	current_po2 = sys_state['art_po2']
	current_pco2 = sys_state['art_pco2']
	set_po2 = sys_state['repiratory_controlls']['set_po2']
	set_pco2 = sys_state['repiratory_controlls']['set_pco2']
	current_fio2 = sys_state['repiratory_controlls']['fio2']
	set_fio2 = sys_state['repiratory_controlls']['set_fio2']

	if cybernation:
		set_po2_flow, set_air_flow = calc_vent_param(current_pco2, set_pco2, current_po2, set_po2, set_fio2, target_gas_flow, gas_flow, current_fio2)
	air_flow_controll_item = oq.create_q_item('controll', 'air_flow', set_air_flow)
	ox_flow_controll_item = oq.create_q_item('controll', 'air_flow', set_po2_flow)
	oq.feed_queue(tx_q, air_flow_controll_item)
	oq.feed_queue(tx_q, ox_flow_controll_item)

async def calc_vent_param(current_pco2, set_pco2, current_po2, set_po2, set_fio2, target_gas_flow, gas_flow, current_fio2):
	delta_pco2 = current_pco2 - set_pco2
	if delta_pco2 > 0 and gas_flow < 1600: # gas flow musst be regualted upwards
		target_gas_flow = target_gas_flow * 1.01
	if delta_pco2 < 0 and gas_flow > 0: # gas flow musst be regualted downwards
		target_gas_flow = target_gas_flow * 0.99

	delta_po2 = current_po2 - set_po2
	if delta_po2 > 0 and set_fio2 < 1.0 and current_fio2 < 1.0: # fio2 musst be regualted upwards
		set_fio2 = set_fio2 * 1.01
	if delta_po2 < 0 and set_fio2 > 0.21 and current_fio2 > 0.21: # flow musst be regualted upwards
		target_gas_flow = set_fio2 * 0.99

	set_o2_flow = set_fio2 * target_gas_flow
	set_air_flow = target_gas_flow - set_o2_flow
	return set_o2_flow, set_air_flow

async def run_vent_test():
	sys_state = {
			"repiratory_controlls": {
			"gas_cybernation": False,
			"set_air_flow": 150,
			"set_oxygen_flow": 20,
			"set_gas_flow": 170,
			"set_po2": 105,
			"set_pco2": 44,
			"fio2": 34,
			"set_fio2": 35,
			"air_flow": 155,
			"oxygen_flow": 22
		}
	}



if __name__ == "__main__":
	
    # main()
    asyncio.run(run_vent_test())

# main.py

from utils import (
    parse_tab_separated_strings, create_sorted_dict, 
    gen_trade_row, extract_first_date, write_post_to_file,
    generate_blog_headline, create_markdown_bulleted_list
)
from templates import (
    call_row_template, put_row_template, html_template
)
import pprint as pp

# Constants for trade types
PUT = 'PUT'.lower()
CALL = 'CALL'.lower()

# Trade data as a string (from your input)
pasted_data = {
    'new_trades': '''10/21/2024	 LIVE 	 SPX 	 Butterfly 	 PUT 	$5,886.50	$5,883.00			$5,914.75			-0.06		0.48		$5,846.11	$5,842.90		$5,874.37		 PUT 	 $ 0.20 	1	 $ 5.00 	 $ 5,870.00 	 $ 5,875.00 	 $ 5,880.00 	 $ 0.20 		10/21/2024 7:47:58	10/21/2024 9:50:28 AM	2:02:30	 $ 45.00 	 $ 45.00 	10/21/2024 Note 1
10/21/2024	 LIVE 	 SPX 	 Butterfly 	 CALL 	$5,886.50	$5,883.00			$5,914.75			-0.06		0.48		$5,846.11	$5,874.37				 CALL 	 $ 0.10 	1	 $ 5.00 	 $ 5,869.00 	 $ 5,874.00 	 $ 5,879.00 	 $ -   				0:00:00		 $ 45.00 	
10/21/2024	 LIVE 	 SPX 	 Butterfly 	 CALL 	$5,886.50	$5,883.00			$5,914.75			-0.06		0.48		$5,846.11	$5,859.69		$5,874.37		 CALL 	 $ 0.10 	1	 $ 5.00 	 $ 5,854.00 	 $ 5,859.00 	 $ 5,864.00 	 $ -   				0:00:00		 $ 45.00 	10/21/2024 Note 2
10/22/2024	 LIVE 	 SPX 	 Butterfly 	 CALL 	$5,865.00	$5,861.50			$5,890.00	$5,876.75	Local High | Volume node Vally	-0.06		0.43	0.21	$5,824.79	$5,849.98	$5,836.22	$5,821.17		 CALL 	 $ 0.20 	1	 $ 5.00 	 $ 5,844.00 	 $ 5,849.00 	 $ 5,854.00 	 $ -   				0:00:00		 $ 45.00 	
10/22/2024	 LIVE 	 SPX 	 Butterfly 	 PUT 	$5,865.00	$5,861.50			$5,890.00	$5,876.75	None - Price falling to new lows	-0.06		0.43	0.21	$5,824.79	$5,849.98	$5,836.22	$5,821.17		 PUT 	 $ 0.20 	1	 $ 5.00 	 $ 5,817.00 	 $ 5,822.00 	 $ 5,827.00 	 $ -   	 $ 4.88 	10/22/2024 7:30:31	10/22/2024 12:09:35 PM	4:39:04	 $ -   	 $ 45.00 	
10/23/2024	 PAPER 	 ES[Z24] 	 Butterfly 	 CALL 	0	0	0	0	0	0	0	0	0	0	0	0	$5,893.75	0	$5,870.75	0	 CALL 	 $ 0.20 	 $ 1.00 	 $ 5.00 	 $ 5,888.00 	 $ 5,893.00 	 $ 5,898.00 					0:00:00		 $ 45.00 	10/23/2024 Note 1
10/23/2024	 PAPER 	 ES[Z24] 	 Butterfly 	 PUT 	0	0	0	0	0	0	0	0	0	0	0	0	$5,893.75	0	$5,870.75	0	 CALL 	 $ 0.20 	 $ 1.00 	 $ 5.00 	 $ 5,888.00 	 $ 5,893.00 	 $ 5,898.00 					0:00:00		 $ 45.00 	
10/23/2024	 LIVE 	 ES[Z24] 	 Butterfly 	 CALL 	0	0	0	0	0	0	0	0	0	0	0	0	$5,893.75	0	$5,870.75	0	 CALL 	 $ 0.20 	 $ 1.00 	 $ 5.00 	 $ 5,888.00 	 $ 5,893.00 	 $ 5,898.00 	 $ -   				0:00:00		 $ 45.00 	10/23/2024 Note 3
10/23/2024	 LIVE 	 ES[Z24] 	 Butterfly 	 PUT 	0	0	0	0	0	0	0	0	0	0	0	0	$5,893.75	0	$5,870.75	0	 CALL 	 $ 0.20 	 $ 1.00 	 $ 5.00 	 $ 5,888.00 	 $ 5,893.00 	 $ 5,898.00 	 $ -   				0:00:00		 $ 45.00 	10/23/2024 Note 4'''
}

# Adding the pasted data into the raw data format with headers
raw_data_with_header = '''date	account	ticker	strategy	type	es_common_low	overnight_es_low	adjusted_es_low	adjusted_es_low_note	overnight_es_high	adjusted_es_high	adjusted_es_high_note	put_offset	put_offset_adjusted	call_offset	call_offset_adjusted	spx_common_low	call_price	call_price_adjusted	put_price	put_price_adjusted	type	limit_price	contract_cnt	spread	left_wing	middle_strike	right_wing	fill_price	fees	entered_ts	exited_ts	time_in_market	p_l	total_p_l	notes
{new_trades}'''.format(**pasted_data)

# Split and prepare raw trades data
raw_trades = raw_data_with_header.split('\n')
trades = [t.split('\t') for t in [trade.strip() for trade in raw_trades]]
tradelist = parse_tab_separated_strings(trades)

# Main logic for generating and saving the daily trade lists
daily_trade_list = create_sorted_dict(tradelist)

for trade_day in daily_trade_list:
    daily_trades = daily_trade_list[trade_day]
    trade_rows = [gen_trade_row(trade, put_row_template, call_row_template, PUT, CALL) for trade in daily_trades]
    rows = "".join(sorted(trade_rows, key=extract_first_date))

    summary = generate_blog_headline(daily_trades)

    notes = create_markdown_bulleted_list([daily_trade["notes"] for daily_trade in daily_trades if 'notes' in daily_trade])

    print(notes)
    print('----------------------------------------------')
    
    # Filling the HTML with the first trade's details
    daily_trades[0]['rows'] = rows
    daily_trades[0]['trade_day'] = trade_day
    daily_trades[0]['summary'] = summary 
    daily_trades[0]['notes'] = notes
    trade_html = html_template.safe_substitute(daily_trades[0])

    # Write to file
    write_post_to_file(trade_day, trade_html)

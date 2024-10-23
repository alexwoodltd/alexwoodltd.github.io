from string import Template

# Templates for PUT and CALL trades
put_row_template = Template('''
<tr>
    <td>$date</td><td>$type</td><td>$contract_cnt</td><td>$put_price</td><td>$middle_strike</td>
    <td>$limit_price</td><td>$spread</td><td>$fill_price</td><td>$entered_ts</td><td>$exited_ts</td>
    <td>$time_in_market</td><td>$p_l</td>
</tr>''')

call_row_template = Template('''
<tr>
    <td>$date</td><td>$type</td><td>$contract_cnt</td><td>$call_price</td><td>$middle_strike</td>
    <td>$limit_price</td><td>$spread</td><td>$fill_price</td><td>$entered_ts</td><td>$exited_ts</td>
    <td>$time_in_market</td><td>$p_l</td>
</tr>''')

# Create HTML template for the day's trades
html_template = Template('''---
title: $title
date: $trade_day
categories: $categories
---

### $summary

<table class="styled-table">
    <thead>
        <tr>
            <th>Date</th>
            <th>TYPE</th>
            <th>Contracts</th>
            <th>Target Level</th>
            <th>Middle Strike</th>
            <th>Limit Price</th>
            <th>Spread</th>
            <th>Fill</th>
            <th>Entered</th>
            <th>Exited</th>
            <th>TIM</th>
            <th>Profit</th>
        </tr>
    </thead>
    <tbody>
        $rows
    </tbody>
</table>

##### Trade Notes: 

$notes''')

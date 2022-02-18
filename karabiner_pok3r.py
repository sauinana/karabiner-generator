#!/usr/bin/env python3
import json

function_key = "caps_lock"
function_key_variable = 'caps_lock_pressed'
function_key_enable = 1
function_key_disable = 0
pok3r_table = """fn + escape = grave_accent_and_tilde
fn + 1 = f1
fn + 2 = f2
fn + 3 = f3
fn + 4 = f4
fn + 5 = f5
fn + 6 = f6
fn + 7 = f7
fn + 8 = f8
fn + 9 = f9
fn + 0 = f10
fn + hyphen = f11
fn + equal_sign = f12
fn + i = up_arrow
fn + j = left_arrow
fn + k = down_arrow
fn + l = right_arrow
fn + p = print_screen
fn + open_bracket = scroll_lock
fn + close_bracket = pause
# fn + z = APP (I don't know what is APP)
fn + h = home
fn + n = end
fn + u = page_up
fn + o = page_down
fn + delete_or_backspace = delete_forward
fn + quote = delete_forward
fn + semicolon = insert"""


def caps_lock_rule():
    rule = {
        "type": "basic",
        "from": {
            "key_code": function_key,
            "modifiers": {
                "optional": [
                    "any"
                ]
            }
        },
        "to": [
            {
                "set_variable": {
                    "name": function_key_variable,
                    "value": function_key_enable
                }
            }
        ],
        "to_after_key_up": [
            {
                "set_variable": {
                    "name": function_key_variable,
                    "value": function_key_disable
                }
            }
        ]
    }
    return rule

def generate_rules(rows):
    manipulators = [caps_lock_rule()]
    for row in rows:
        if row.startswith('#'):
            pass
        else:
            rule_strings = row.split()
            from_key = rule_strings[2]
            to_key = rule_strings[4]
            manipulators.append(generate_single_key_rule(from_key, to_key))
    rules = [{
        "description": "Implement pok3r all composite keys",
        "manipulators": manipulators
    }]
    return rules

def generate_single_key_rule(from_key, to_key):
    single_key_rule = {
        "type": "basic",
        "from": {
            "key_code": from_key,
            "modifiers": {
                "optional": ["any"]
            }
        },
        "to": [
            {
                "key_code": to_key
            }
        ],
        "conditions": [
            {
                "type": "variable_if",
                "name": function_key_variable,
                "value": function_key_enable
            }
        ]
    }
    return single_key_rule

def generate_karabiner_config():
    rows = pok3r_table.split("\n")
    karabiner_config = {
        'title': 'pok3r FN、PN composite keys',
        'maintainer': 'jkcc',
        'rules': generate_rules(rows),
    }
    return karabiner_config
print(json.dumps(generate_karabiner_config()))

import json
import os
from . import create_modify, read, search

def _read_file_or_return(obj, is_json=False):
    if isinstance(obj, str) and os.path.exists(obj):
        with open(obj, 'r') as f:
            return json.load(f) if is_json else f.read()
    return obj

def create_experiment(name=None, body=None, json_data=None, steps=None, content_type=1):
    data = _read_file_or_return(json_data, is_json=True) if json_data else {}
    if name:
        data['title'] = name
    if body:
        data['body'] = _read_file_or_return(body, is_json=False)

    if 'title' not in data:
        raise ValueError("Experiment 'name' is required either via `name` or `json_data`.")

    exp_id = create_modify.create_experiment({'title': data['title']})
    if not exp_id:
        raise RuntimeError("Experiment creation failed.")

    if 'content_type' not in data:
        # Optionally infer from file extension
        if isinstance(body, str):
            if body.endswith('.html'):
                data['content_type'] = 2
            elif body.endswith('.md'):
                data['content_type'] = 1
            else:
                data['content_type'] = content_type
        else:
            data['content_type'] = content_type

    create_modify.modify_experiment(exp_id, data)

    if steps:
        steps_data = _read_file_or_return(steps, is_json=True)
        create_modify.add_steps(exp_id, steps_data)

    return exp_id

def modify_experiment(exp_id, name=None, body=None, json_data=None, steps=None, force=False, body_append=None):
    existing = read.read_experiment(exp_id)
    new_data = _read_file_or_return(json_data, is_json=True) if json_data else {}

    if body and body_append:
        raise ValueError("Pass either `body` or `body_append`, not both.")

    if body:
        new_data['body'] = _read_file_or_return(body, is_json=False)

    if body_append:
        old_body = existing.get("body", "")
        content_type = existing.get("content_type", 1)
        body_append = body_append.replace("\\n", "<br>") if content_type == 2 else body_append
        new_data['body'] = f"{old_body.rstrip()}\\n\\n{body_append.strip()}"

    if name:
        if name != existing.get("title", "") and not force:
            raise ValueError("Provided name differs from existing title. Use force=True to override.")
        new_data['title'] = name

    if new_data:
        create_modify.modify_experiment(exp_id, new_data)

    if steps:
        steps_data = _read_file_or_return(steps, is_json=True)
        create_modify.add_steps(exp_id, steps_data)

    if not new_data and not steps:
        raise ValueError("No new data or steps provided to modify.")

def search_experiments(name_like):
    return search.filter_experiments(name_like)

def read_experiment(exp_id=None, name_like=None, fetch="first"):
    if exp_id:
        return [read.read_experiment(exp_id)]
    ids, _ = search.filter_experiments(name_like)
    if not ids:
        return []
    if fetch == "first":
        return [read.read_experiment(ids[0])]
    elif fetch == "all":
        return [read.read_experiment(i) for i in ids]
    else:
        raise ValueError("Invalid fetch argument: must be 'first' or 'all'")

def complete_step(exp_id, pattern="step_1", done_by=None, change=None):
    '''
    Completes steps matching a pattern in an experiment.

    :param exp_id: Experiment ID
    :param pattern: Step body pattern to match
    :param done_by: Name to append as _done_by_ if not already present
    :param change: None (exactly one match), 'first' (first unfinished), or 'all' (all unfinished)
    '''
    return create_modify.complete_steps(
        exp_id_here=exp_id,
        step_pattern_to_finish=pattern,
        done_by=done_by,
        change=change
    )


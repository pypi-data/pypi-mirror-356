import argparse
import json
import argcomplete
from . import create_modify
from . import read
from . import search
from . import config

def load_body_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def handle_create(args):
    data = {}
    if args.json:
        with open(args.json, 'r') as f:
            data = json.load(f)
    if args.name:
        data['title'] = args.name
    if args.body:
        data['body'] = load_body_from_file(args.body)
    if not data.get('title'):
        print("Error: Experiment 'name' (title) is required.")
        return
    exp_id = create_modify.create_experiment({'title': data['title']})
    if not exp_id:
        print("Experiment creation failed.")
        return
    print(f"Created experiment ID: {exp_id}")
    print("Modifying experiment with provided data...")
    create_modify.modify_experiment(exp_id, data)
    if args.steps:
        with open(args.steps, 'r') as f:
            steps_data = json.load(f)
        create_modify.add_steps(exp_id, steps_data)

def handle_modify(args):
    if not args.exp_id:
        print("Experiment ID is required for modification.")
        return
    existing = read.read_experiment(args.exp_id)
    new_data = {}
    if args.json:
        with open(args.json, 'r') as f:
            new_data = json.load(f)
    if args.body:
        new_data['body'] = load_body_from_file(args.body)
    if args.name:
        if args.name != existing.get("title", ""):
            print("Warning: Provided name differs from existing title.")
            if not args.force:
                print("Use -f to force override.")
                return
        new_data['title'] = args.name
    if not new_data:
        print("No data provided to modify.")
        return
    create_modify.modify_experiment(args.exp_id, new_data)
    if args.steps:
        with open(args.steps, 'r') as f:
            steps_data = json.load(f)
        create_modify.add_steps(args.exp_id, steps_data)

def handle_search(args):
    ids, names = search.filter_experiments(args.name_like)
    for i, n in zip(ids, names):
        print(f"{i}: {n}")

def handle_read(args):
    if args.exp_id:
        result = read.read_experiment(args.exp_id)
        filename = args.outfile if args.outfile else f"{args.exp_id}.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Wrote experiment data to {filename}")
    elif args.name_like:
        ids, names = search.filter_experiments(args.name_like)
        if len(ids) == 0:
            print("No matching experiments found.")
            return
        if len(ids) == 1 or args.first:
            result = read.read_experiment(ids[0])
            filename = args.outfile if args.outfile else f"{ids[0]}.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Wrote experiment data to {filename}")
        elif args.all:
            all_data = []
            for i in ids:
                all_data.append(read.read_experiment(i))
            filename = args.outfile if args.outfile else "multiple_experiments.json"
            with open(filename, 'w') as f:
                json.dump(all_data, f, indent=2)
            print(f"Wrote all experiments data to {filename}")
        else:
            print(f"Found {len(ids)} matches:")
            for idx, (i, n) in enumerate(zip(ids, names)):
                print(f"{idx+1}. {i}: {n}")
            choice = input("Enter f for first, a for all: ").strip().lower()
            if choice == 'f':
                result = read.read_experiment(ids[0])
                filename = args.outfile if args.outfile else f"{ids[0]}.json"
                with open(filename, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"Wrote experiment data to {filename}")
            elif choice == 'a':
                all_data = [read.read_experiment(i) for i in ids]
                filename = args.outfile if args.outfile else "multiple_experiments.json"
                with open(filename, 'w') as f:
                    json.dump(all_data, f, indent=2)
                print(f"Wrote all experiments data to {filename}")

def main():
    parser = argparse.ArgumentParser(description="CLI wrapper for eLabFTW functions")
    subparsers = parser.add_subparsers(dest="command")

    parser_create = subparsers.add_parser("create_experiment")
    parser_create.add_argument("--name", help="Title for experiment")
    parser_create.add_argument("--body", help="HTML/text body file for experiment")
    parser_create.add_argument("--json", help="JSON file with full experiment data")
    parser_create.add_argument("--steps", help="JSON file with steps to be added")

    parser_modify = subparsers.add_parser("modify_experiment")
    parser_modify.add_argument("--exp_id", required=True, help="Experiment ID to modify")
    parser_modify.add_argument("--name", help="New title (discouraged)")
    parser_modify.add_argument("--body", help="HTML/text body file")
    parser_modify.add_argument("--json", help="JSON file with update data")
    parser_modify.add_argument("--steps", help="JSON file with steps to be added")
    parser_modify.add_argument("-f", "--force", action="store_true", help="Force title change")

    parser_search = subparsers.add_parser("search_experiments")
    parser_search.add_argument("--name-like", required=True, help="Search term for experiment names")

    parser_read = subparsers.add_parser("read_experiment")
    parser_read.add_argument("--exp_id", help="Experiment ID to read")
    parser_read.add_argument("--name-like", help="Partial or full experiment name to search")
    parser_read.add_argument("--first", action="store_true", help="Use first match automatically")
    parser_read.add_argument("--all", action="store_true", help="Fetch all matches")
    parser_read.add_argument("--outfile", help="Output JSON filename")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.command == "create_experiment":
        handle_create(args)
    elif args.command == "modify_experiment":
        handle_modify(args)
    elif args.command == "search_experiments":
        handle_search(args)
    elif args.command == "read_experiment":
        handle_read(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

from typing import Any
from pathlib import Path
from collections import defaultdict

TEST_INPUT = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".splitlines()


def parse_input(puzzle: list[str]) -> dict[str, Any]:
    working_dir = "/"
    file_system = {}
    for line in puzzle:
        if line.startswith("$"):
            cmd = line[2:].split()
            if cmd[0] == "cd":
                if cmd[1] == "/":
                    working_dir = "/"
                    file_system.setdefault("/", {})
                elif cmd[1] == "..":
                    if working_dir.endswith("/"):
                        working_dir = working_dir[:-1]
                    working_dir = "/".join(working_dir.split("/")[:-1]) + "/"
                else:
                    working_dir = f"{working_dir}/{cmd[1]}/".replace("//", "/")
                    interim_fs = file_system["/"]
                    for part in (
                        working_dir
                        if not working_dir.endswith("/")
                        else working_dir[:-1]
                    ).split("/"):
                        if part:
                            try:
                                interim_fs = interim_fs[part]
                            except KeyError:
                                interim_fs[part] = {}
                                interim_fs = interim_fs[part]

            elif cmd[0] == "ls":
                continue
            else:
                raise ValueError(f"Unknown command {line}")
            continue
        # we're parrsing a directory output
        interim_fs = file_system["/"]
        for part in (
            working_dir if not working_dir.endswith("/") else working_dir[:-1]
        ).split("/"):
            if part:
                try:
                    interim_fs = interim_fs[part]
                except KeyError:
                    interim_fs[part] = {}
                    interim_fs = interim_fs[part]
        size_or_type, name = line.split()
        if size_or_type == "dir":
            interim_fs[name] = {}
        else:
            interim_fs[name] = int(size_or_type)

    assert list(file_system) == ["/"]
    return file_system


def dir_size(
    current_path: str,
    directory: dict[str, Any],
    result: defaultdict[str, int],
    depth: int = 0,
) -> int:
    retval = 0
    for name, contents in directory.items():
        if isinstance(contents, int):
            # print(' ' * depth, 'found file',name, contents)
            retval += contents
        else:
            # print(' ' * depth, 'entering subdir', name)
            # it's a dict
            # recursively add up its size
            new_dir = f"{current_path}/{name}".replace("//", "/")
            # print(new_dir)
            assert new_dir not in result
            result[new_dir] = dir_size(new_dir, contents, result, depth + 1)
            # and add that child's total to our own
            retval += result[new_dir]
    # print(' ' * depth, f'returning {retval}')
    return retval


def part_one(puzzle: list[str], target: int = 100000) -> int:
    file_system = parse_input(puzzle)
    sizes = defaultdict(int)
    dir_size("", file_system, sizes)
    return sum(size for size in sizes.values() if size <= target)


def part_two(puzzle: list[str]) -> int:
    file_system = parse_input(puzzle)
    sizes = defaultdict(int)
    slash_size = dir_size("", file_system, sizes)
    total_disk_space = 70_000_000
    threshold = 30_000_000
    space_avail = total_disk_space - slash_size
    # print('currently unused:', space_avail)
    for name, space_taken in sorted(sizes.items(), key=lambda k: k[1]):
        if space_avail + space_taken >= threshold:
            # print(f'removing {name} would work')
            return space_taken


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 95437, part_one_result
    puzzle = Path("day07.txt").read_text().splitlines()
    print(part_one(puzzle=puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 24933642, part_two_result
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()

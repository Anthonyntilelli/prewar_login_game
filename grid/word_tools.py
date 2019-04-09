"""Tools to sort word list based on similarity and word size range."""
from typing import List, Iterable, Set, Dict, Tuple, Union
import random
import os
from math import floor
from pathlib import Path
import yaml
import grid.settings as gi_sd


# Black styling Preferred
# pylint: disable=c0330


class WordsTools:
    """Tools to trim word lists and save to file."""

    def __init__(self, file: str = "./setting.yml") -> None:
        """
        Check file conditions for settings.

        :param file: File containing settings.
        """
        random.seed()
        if len(file) <= 4 or file[-4:] != ".yml":  # Last 4 chars
            raise ValueError("file must be <something>.yml")
        self._fpath = Path(file)
        if self._fpath.exists():
            if not self._fpath.is_file():
                raise LookupError("File is not a regular file")
            if not os.access(str(self._fpath), os.R_OK):
                raise PermissionError("No read access on file")

    def write_settings(
        self, setting_data: gi_sd.SettingGridFull, override: bool = False
    ) -> None:
        """
        Write the setting data to a file in yaml format.

        :param setting_data: Data to write to file
        :param override: override existing file if it already exists
        """
        if self._fpath.exists():
            if not override:
                raise LookupError("File already exist(not set to override)")
            if not os.access(str(self._fpath), os.W_OK):
                raise PermissionError("File not writeable")

        if not isinstance(setting_data, gi_sd.SettingGridFull):
            raise ValueError("Not settings Data type")

        # Translate to Dict
        save_data: Dict[str, Union[int, List[str]]] = {}
        save_data["EASY_MIN"] = setting_data.EASY_MIN
        save_data["EASY_MAX"] = setting_data.EASY_MAX
        save_data["ADVANCE_MIN"] = setting_data.ADVANCE_MIN
        save_data["ADVANCE_MAX"] = setting_data.ADVANCE_MAX
        save_data["EXPERT_MIN"] = setting_data.EXPERT_MIN
        save_data["EXPERT_MAX"] = setting_data.EXPERT_MAX
        save_data["MASTER_MIN"] = setting_data.MASTER_MIN
        save_data["MASTER_MAX"] = setting_data.MASTER_MAX
        save_data["NUM_OF_ROWS"] = setting_data.NUM_OF_ROWS
        save_data["FEEDBACK_LINE_SIZE"] = setting_data.FEEDBACK_LINE_SIZE
        save_data["ACTIVE_LINE_SIZE"] = setting_data.ACTIVE_LINE_SIZE
        save_data["HEX_LINE_SIZE"] = setting_data.HEX_LINE_SIZE
        save_data["HEX_COL_MIN"] = setting_data.HEX_COL_MIN
        save_data["HEX_COL_MAX"] = setting_data.HEX_COL_MAX
        save_data["PASS_POOL_SIZE"] = setting_data.PASS_POOL_SIZE
        save_data["FILLER_SYMBOLS"] = setting_data.FILLER_SYMBOLS
        save_data["easy_pass_pool"] = setting_data.easy_pass_pool
        save_data["advanced_pass_pool"] = setting_data.advanced_pass_pool
        save_data["expert_pass_pool"] = setting_data.expert_pass_pool
        save_data["master_pass_pool"] = setting_data.master_pass_pool

        self._fpath.touch(mode=0o600)  # create file
        with self._fpath.open(mode="w") as file_pointer:
            yaml.safe_dump(save_data, file_pointer)

    def load_settings_full(self) -> gi_sd.SettingGridFull:
        """
        Read and return full settings file for Game.

        :return: Setting for game
        """
        if not self._fpath.exists():
            raise FileExistsError("File does not exist")
        if not os.access(str(self._fpath), os.R_OK):
            raise PermissionError("File not readable")
        with self._fpath.open(mode="r") as file_pointer:
            save_data = yaml.safe_load(file_pointer)
        settings = gi_sd.SettingGridFull(
            save_data["EASY_MIN"],
            save_data["EASY_MAX"],
            save_data["ADVANCE_MIN"],
            save_data["ADVANCE_MAX"],
            save_data["EXPERT_MIN"],
            save_data["EXPERT_MAX"],
            save_data["MASTER_MIN"],
            save_data["MASTER_MAX"],
            save_data["NUM_OF_ROWS"],
            save_data["FEEDBACK_LINE_SIZE"],
            save_data["ACTIVE_LINE_SIZE"],
            save_data["HEX_LINE_SIZE"],
            save_data["HEX_COL_MIN"],
            save_data["HEX_COL_MAX"],
            save_data["PASS_POOL_SIZE"],
            save_data["FILLER_SYMBOLS"],
            save_data["easy_pass_pool"],
            save_data["advanced_pass_pool"],
            save_data["expert_pass_pool"],
            save_data["master_pass_pool"],
        )
        return settings

    def load_settings_diff(self, diff: gi_sd.DifficultyType) -> gi_sd.SettingGridDiff:
        """
        Read and return difficulty based setting file for game.

        Theses setting are reduced based on the selected difficulty.
        :param diff: specifies difficulty setting to load.
        :return: Setting for game
        """
        if not isinstance(diff, gi_sd.DifficultyType):
            raise ValueError("Not a valid difficulty")
        if not self._fpath.exists():
            raise FileExistsError("File does not exist")
        if not os.access(str(self._fpath), os.R_OK):
            raise PermissionError("File not readable")
        with self._fpath.open(mode="r") as file_pointer:
            save_data = yaml.safe_load(file_pointer)

        minimum: int
        maximum: int
        pool: List[str]

        if diff == gi_sd.DifficultyType.EASY:
            minimum = save_data["EASY_MIN"]
            maximum = save_data["EASY_MAX"]
            pool = save_data["easy_pass_pool"]
        elif diff == gi_sd.DifficultyType.ADVANCE:
            minimum = save_data["ADVANCE_MIN"]
            maximum = save_data["ADVANCE_MAX"]
            pool = save_data["advanced_pass_pool"]
        elif diff == gi_sd.DifficultyType.EXPERT:
            minimum = save_data["EXPERT_MIN"]
            maximum = save_data["EXPERT_MAX"]
            pool = save_data["expert_pass_pool"]
        elif diff == gi_sd.DifficultyType.MASTER:
            minimum = save_data["MASTER_MIN"]
            maximum = save_data["MASTER_MAX"]
            pool = save_data["master_pass_pool"]
        else:
            raise ValueError(f"Unknown diff (value:{diff}, type:{type(diff)})")

        settings = gi_sd.SettingGridDiff(
            minimum,
            maximum,
            save_data["NUM_OF_ROWS"],
            save_data["FEEDBACK_LINE_SIZE"],
            save_data["ACTIVE_LINE_SIZE"],
            save_data["HEX_LINE_SIZE"],
            save_data["HEX_COL_MIN"],
            save_data["HEX_COL_MAX"],
            save_data["PASS_POOL_SIZE"],
            save_data["FILLER_SYMBOLS"],
            pool,
        )
        return settings

    def set_passwords(
        self, word_subset: List[str], count: int, show_status: bool = False
    ) -> List[str]:
        """
        Find a list of passwords per difficulty for count.

        This function is slow especially with larger word sets and counts
        :param word_subset: lists of words
        :param count: number of passwords to try and find
        :param show_status: print current status (T/F)
        :return: list of passwords per difficulty
        """
        if count <= 0:
            raise ValueError("Count cannot be less then 1")
        if len(word_subset) <= count:
            raise ValueError("Word_subset is to small for the count")
        pass_arr = []
        word_subset_cpy = list(word_subset.copy())
        if show_status:
            print("starting Run")
        random.shuffle(word_subset_cpy)
        for word in word_subset_cpy:
            result = self.similarity_sort(word_subset_cpy, word)
            if result[1]:
                if show_status:
                    print(f"Adding Word: {word} to pass_arr")
                pass_arr.append(word)
            if len(pass_arr) == count:
                break
        if len(pass_arr) < count:
            raise RuntimeError("Could Not meet password count")
        if show_status:
            print("finished")
        return pass_arr

    @staticmethod
    def trim(minimum: int, maximum: int, word_list: Iterable[str]) -> Set[str]:
        """
        Output word list in lowercase based on min/max letter count.

        Does not validate maximum and maximum, expected to be done before calling.
        :param minimum: minimum letters allowed in a word.
        :param maximum: maximum letters allowed in a word.
        :param word_list: source list of words to be trimmed.
        :return: Reduced set of words.
        """
        reduced_words = set()  # prevent duplicates
        word: str
        for word in word_list:
            if minimum <= len(word) <= maximum:
                reduced_words.add(word.lower())
        return reduced_words

    @staticmethod
    def similarity_sort(
        word_list: Iterable[str], compare_string: str
    ) -> Tuple[Dict[int, List[str]], bool]:
        """
        Separate word_list based on similarity.

        :param compare_string: string to compare against for similarity
        :return dictionary with similarity count as keys, was threshold met?
        """
        word_set = frozenset(word_list)  # remove duplicates
        similarity_store: Dict[int, List[str]] = {}
        low_sim = floor(len(compare_string) / 2)
        # number of words that has more then 1/2 words in same place as compare string
        high_sim_count: int = 0
        for word in word_set:
            if word == compare_string:
                continue
            similarity: int = 0
            lj_word = word.ljust(len(compare_string))
            for index, char in enumerate(compare_string):
                if lj_word[index] == char:
                    similarity += 1
            if similarity not in similarity_store:
                similarity_store[similarity] = []
            similarity_store[similarity].append(word)
            if similarity > low_sim:
                high_sim_count += 1
        return similarity_store, high_sim_count >= 15

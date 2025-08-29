import numpy as np
import itertools

class SelectBaseCandidates:
    def __init__(self, X, Y, intervals=3):
        self.X = X
        self.Y = Y
        self.intervals = intervals
        self.x_indexes = range(X.shape[0])
        self.y_indexes = range(Y.shape[0])
        self.x_indexes_sub = self.all_combinations(self.x_indexes)
        self.y_indexes_sub = self.all_combinations(self.y_indexes)

        selected = []
        for x_subset in self.x_indexes_sub:
            for y_subset in self.y_indexes_sub :
                b_index = self.select_best_sum(x_subset, y_subset)
                selected.extend(b_index)


        self.base_indexes = self.unique_indexes_ordered(selected)

    def select_best_sum(self, x_indexes, y_indexes):
        """
        For each interval from max to min, include ALL samples with x_vals >= lo,
        select the unused sample with the highest Y/X ratio in that interval.
        (Cumulative intervals.)
        """
        x_vals = self.X[x_indexes, :].sum(axis=0)
        y_vals = self.Y[y_indexes, :].sum(axis=0)
        x_min, x_max = x_vals.min(), x_vals.max()
        bins = np.linspace(x_min, x_max, self.intervals+1)
        results = []
        used = set()
        n_samples = x_vals.shape[0]
        for i in range(self.intervals-1, -1, -1):  # max to min
            lo = bins[i]
            mask = (x_vals >= lo)
            if used:
                used_mask = np.ones(n_samples, dtype=bool)
                used_mask[list(used)] = False
                mask &= used_mask
            candidates_idx = np.where(mask)[0]
            if len(candidates_idx) == 0:
                continue
            ratios = y_vals[candidates_idx] / (x_vals[candidates_idx] + 1e-8)
            max_idx_local = np.argmax(ratios)
            best_index = candidates_idx[max_idx_local]
            best_ratio = ratios[max_idx_local]
            results.append((best_index, best_ratio))
            used.add(best_index)
        return results



    @staticmethod
    def all_combinations(x_indexes):
        """
        Returns all unique combinations: singles, pairs, triplets, from x_indexes,
        but only up to the length of x_indexes.
        """
        combos = []
        n = len(x_indexes)
        for r in range(1, min(3, n) + 1):
            combos.extend(itertools.combinations(x_indexes, r))
        return combos   

    @staticmethod
    def unique_indexes_ordered(combos):
        seen = set()
        out = []
        for idx, _ in combos:
            if idx not in seen:
                seen.add(idx)
                out.append(idx)
        return sorted(out)
from sample_players import DataPlayer


class CustomPlayer(DataPlayer):
    def get_action(self, state):

#                 === alphabeta basic ====
#                 depth = 1
#                 depth_limit = 50
#                 while True:
#                     self.queue.put(self.alpha_beta_search(state, depth))
#                     depth += 1
#                     if depth > depth_limit:
#                         break


        # === principal_variation_search ===
        depth = 1
        depth_limit = 50
        while True:
            self.queue.put(self.principal_variation_search(state, depth))
            depth += 1
            if depth > depth_limit:
                break

    # ===  alpha_beta basic version =======================================
    def alpha_beta_search(self, state, depth):
        alpha = float("-inf")
        beta = float("inf")
        # best_score = float("-inf")
        # best_move = None
        actions = state.actions()
        if actions:
            best_move = actions[0]
        else:
            best_move = None

        for a in actions:
            v = self.min_value(state.result(a), alpha, beta, depth - 1)
            if v > alpha:
                alpha = v
                best_move = a
        return best_move

    def min_value(self, state, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(self.player_id)

        if depth <= 0:
            return self.score(state)

        v = float("inf")
        for a in state.actions():
            v = min(v, self.max_value(state.result(a), alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, state, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(self.player_id)

        if depth <= 0:
            return self.score(state)

        v = float("-inf")
        for a in state.actions():
            v = max(v, self.min_value(state.result(a), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    

    # ===  principal_variation_search  =======================================
    def principal_variation_search(self, state, depth):
        alpha = float("-inf")
        beta = float("inf")
        v = float("-inf")
        # best_score = float("-inf")
        # best_move = None
        actions = state.actions()
        if actions:
            best_move = actions[0]
        else:
            best_move = None


        for i, ac in enumerate(actions):
            if i == 0:
                v = max(v, self.min_value_pr(state.result(ac), alpha, beta, depth - 1))
            else:
                v = max(v, self.min_value_pr(state.result(ac), alpha, alpha+1, depth - 1))
                if v > alpha:
                    v = max(v, self.min_value_pr(state.result(ac), alpha, beta, depth - 1))
            if v > alpha:
                alpha = v
                best_move = ac
        return best_move

    def min_value_pr(self, state, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(self.player_id)

        if depth <= 0:
            return self.score(state)

        v = float("inf")
        for i, ac in enumerate(state.actions()):
            if i == 0:
                v = min(v, self.max_value_pr(state.result(ac), alpha, beta, depth - 1))
            else:
                v = min(v, self.max_value_pr(state.result(ac), beta-1, beta, depth - 1))
                if v < beta:
                    v = min(v, self.max_value_pr(state.result(ac), alpha, beta, depth - 1))
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v

    def max_value_pr(self, state, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(self.player_id)

        if depth <= 0:
            return self.score(state)

        v = float("-inf")
        for i, ac in enumerate(state.actions()):
            if i == 0:
                v = max(v, self.min_value_pr(state.result(ac), alpha, beta, depth - 1))
            else:
                v = max(v, self.min_value_pr(state.result(ac), alpha, alpha+1, depth - 1))
                if v > alpha:
                    v = max(v, self.min_value_pr(state.result(ac), alpha, beta, depth - 1))
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v


    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

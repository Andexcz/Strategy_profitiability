import numpy as np

# ============================================================
# COMPLETE STRATEGY EVALUATION PIPELINE
# ============================================================

# Define strategy to evaluate
params = np.array([0.55, 120, 100, 8])

# Stress parameters
avg_slippage = 1.7
tail_prob = 0.02
tail_loss = 400

# ============================================================
# STEP 1: Basic Analysis
# ============================================================

p_win = params[0]
win_amount = params[1]
loss_amount = params[2]
cost = params[3]

base_ev = p_win * win_amount - (1 - p_win) * loss_amount - cost
break_even_p = (loss_amount + cost) / (win_amount + loss_amount)
margin = p_win - break_even_p

print("=" * 50)
print("STRATEGY EVALUATION REPORT")
print("=" * 50)
print(f"Win probability:    {p_win*100:.1f}%")
print(f"Win amount:         {win_amount}")
print(f"Loss amount:        {loss_amount}")
print(f"Cost per trade:     {cost}")
print(f"Base EV per trade:  {base_ev:.2f}")
print(f"Break-even prob:    {break_even_p*100:.1f}%")
print(f"Margin above break: {margin*100:.1f}%")

# ============================================================
# STEP 2: Stress Testing
# ============================================================

remaining = 1 - tail_prob
adj_p_win = p_win * remaining
adj_p_loss = (1 - p_win) * remaining

ev_with_tail = (adj_p_win * (win_amount - cost)
              + adj_p_loss * (-loss_amount - cost)
              + tail_prob * (-tail_loss - cost))

stressed_ev = ev_with_tail - avg_slippage

print(f"Slippage per trade: {avg_slippage}")
print(f"Tail probability:   {tail_prob*100:.1f}%")
print(f"Tail loss:          {tail_loss}")
print(f"Stressed EV:        {stressed_ev:.2f}")

# ============================================================
# STEP 3: Monte Carlo Verification
# ============================================================

np.random.seed(42)
n_trades = 1000
n_trials = 500

outcomes = np.random.random((n_trials, n_trades)) < p_win
win_pnl = win_amount - cost
loss_pnl = -loss_amount - cost
trade_pnls = np.where(outcomes, win_pnl, loss_pnl)
final_pnls = np.sum(trade_pnls, axis=1)

print(f"Theoretical total:  {base_ev * n_trades:.0f}")
print(f"Simulated mean:     {np.mean(final_pnls):.0f}")
print(f"Simulated std:      {np.std(final_pnls):.0f}")
print(f"% profitable runs:  {np.mean(final_pnls > 0)*100:.1f}%")

# ============================================================
# STEP 4: Final Verdict
# ============================================================

print("=" * 50)
if stressed_ev > 0:
  print("VERDICT: TRADE")
  print(f"Positive EV of {stressed_ev:.2f} per trade after stress")
else:
  print("VERDICT: DO NOT TRADE")
  print(f"Negative EV of {stressed_ev:.2f} per trade under stress")
print("=" * 50)
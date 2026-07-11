theorem peirce (p q : Prop) : ((p → q) → p) → p := by
  intro h
  rcases Classical.em p with hp | hnp
  · exact hp        -- case 1: p is true.
  · exact h (fun hp => absurd hp hnp)    -- case: neg p, so (p → q) is true.

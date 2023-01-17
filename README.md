# Fantasy Football Scoreboard App
### A Town, A Team, and No Dream 
When my fantasy football league dwindled to an awkwardly obtuse 9 members, we adapted a new scoring method that got us over the hump of relying on the matchup model that would leave one team on the proverbial sidelines each week. Unlike real football, where a week off gives one the chance to rest from the weekly bludgeoning, fantasy foobtall is of zero value to the odd man out, and will often, ironically, yield an excitedly meaningless performance by their team.

The solution to this problem was a scoring methodology in which the entire league competes against itself each week. The fruit of your efforts is a weekly score corresponding to the inverse of your rank that week. For example, in the previously-mentioned 9-team league, the team with the highest score gets 9 points as their plunder; the lowest gets 1 point, etc. This creates a distinct difference from a total points-for model in that it isolates each week, and gives high-performing teams a more meaningful result than the binary "W" or "L". Perhaps the most enticing feature is that it brings league-wide suspense into Monday night, as inidividual performances on MNF can push multiple teams up the scoreboard.

The guts of this is built on [cwendt94/espn-api](https://github.com/cwendt94/espn-api).

The app has the following 4 features: 
1. Scoreboard for the current season
2. Weekly point totals/projections
3. Individual lineups for each team
4. Archived weekly results & lineups

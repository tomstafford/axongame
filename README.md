Tracing the Trajectory of Skill Learning With a Very Large Sample of Online Game Players
========================================================================================

[Tom Stafford](http://www.tomstafford.staff.shef.ac.uk/) & [Mike Dewar](https://github.com/mikedewar)

This code accompanies our paper 

>Stafford, T. & Dewar, M. "Tracing the Trajectory of Skill Learning With a Very Large Sample of Online Game Players" 

which is in press at [Psychological Science](http://pss.sagepub.com/) (expected January 2014). Previously this work was presented at the Cognitive Science Society conference in Berlin in August 2013 under the title "Testing theories of skill learning using a very large sample of online game players"

Abstract
--------
In the present study, we analyzed data from a very large sample (N= 854,064) of players of an online game involving rapid perception, decision making, and motor responding. Use of game data allowed us to connect, for the first time, rich details of training history with measures of performance from participants engaged for a sustained amount of time in effortful practice. We showed that lawful relations exist between practice amount and subsequent performance, and between practice spacing and subsequent performance. Our methodology allowed an in situ confirmation of results long established in the experimental literature on skill acquisition. Additionally, we showed that greater initial variation in performance is linked to higher subsequent performance, a result we link to the exploration/exploitation trade-off from the computational framework of reinforcement learning. We discuss the benefits and opportunities of behavioral data sets with very large sample sizes and suggest that this approach could be particularly fecund for studies of skill acquisition.



Files in this Repository 
------------------------

### NOT ANALYSIS FILES ###

* `stafford_and_dewar_revision.pdf` - the final submitted version of the paper
* `Psychscience__Response_to_Review.pdf` - the accompnanying response to the reviewers. 
* `data_by_cookie.json` - the raw data upon which all the results are based

### ANALYSIS FILES ###

The following are all analysis files, written in Python, for generating the results reported in the paper and reported in the response to reviewers.

* `ps_fig2.py` - make Figure 2 from the Psych Science paper. Control analyses follow.
* `ps_fig2_equate.py` - equates players on first one/two scores. Also allows you to calculate maximum score on Nth play rather than on any (unspecified) play
* `ps_fig2_rebaseline.py` - normalises plots to an initial score of zero
* `ps_fig2_score.py` - compares learning curves for aggregate score vs average score (rather than attempt number vs average score)
* `ps_fig3.py` - make Figure 3 from the Psych Science paper. 
* `ps_fig3obs.py` - extract observsed data (required for ps_fig3.py)
* `ps_fig3boot.py` - bootstrap confidence intervals (required for ps_fig3.py)
* `ps_fig4.py` - make Figure 4 from the Psych Science paper
* `sup_attempts_vs_avscore.py` - supplementary analysis, show attempt number vs average score
* `sup_make_eeheatmap.py` - supplementary graph, performs analysis of the explore exploit result (reported in the paper, page 5)
* `sup_ee_observed.py` - the observed data
* `sup_ee_boot.py` - CIs on the correlation
* `sup_machinechurn.py` - shows that for players with a high number of attempts the lerning curve regularity doesn't hold
* `sup_resters_vs_goers.py` - graph for resters vs goers result (reported in the paper, page 4, column 2)

See `\Figures` for graphs produced by this lot

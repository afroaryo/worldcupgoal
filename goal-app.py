import statsbombpy.sb as sb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pywaffle import Waffle
from matplotlib.patches import Arc
import matplotlib.font_manager
import gawang
import matplotlib as mpl 
import matplotlib.gridspec as gridspec 
import matplotlib.patheffects as path_effects
import matplotlib.font_manager
from PIL import Image
import requests
from io import BytesIO
import streamlit as st
import flag
import pitch_mckeever
import flag
import emoji
from ast import literal_eval


wc = sb.matches(competition_id=43, season_id=3)

st.markdown("""
<style>
.title-font {
    font-size:40px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p style="text-align: center"; class="title-font";"font-family:Courier New"> <b>How Did Your Team Score Goals in Russia 2018 World Cup? ⚽🏆 </b></p>', unsafe_allow_html=True)

st.markdown("""
<style>
.big-font {
    font-size:18px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p style="text-align: center"; class="big-font";"font-family:Courier New"> <b>World Cup 2018 in Russia </b> is one of the most exciting world cup tournaments in history. 168 goals were created by 32 teams from 64 parties. The VAR which was introduced in this competition made the match tension even fiercer due to the high number of penalties in this competition. Let us explore how each team scores, enjoy!! 😊</p>', unsafe_allow_html=True)

st.markdown("""
<style>
.credit {
    font-size:15px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p style="text-align: center"; class="credit";"font-family:Courier New"> Datasource: <a href="https://statsbomb.com/data/">Statsbomb</a> <br> Created by: <a href="https://twitter.com/christopheraryo">@christopheraryo</a>  </p>', unsafe_allow_html=True)




st.write("""
### Choose Your team!
""")

team = st.selectbox("Team: ",['France', 'Nigeria', 'Poland', 'Brazil', 'Germany', 'Australia',
       'Serbia', 'Senegal', 'Panama', 'Switzerland', 'Croatia', 'Uruguay',
       'Russia', 'Denmark', 'Costa Rica', 'Belgium', 'Argentina',
       'Iceland', 'Egypt', 'Spain', 'Peru', 'South Korea', 'Japan',
       'Saudi Arabia', 'Morocco', 'Iran', 'Sweden', 'Portugal', 'Mexico',
       'England', 'Colombia', 'Tunisia'])

flagship = {'France':'FR', 'Nigeria':':NG:', 'Poland':':PL:', 'Brazil':':BR:', 'Germany':':DE:', 'Australia':':AU:',
       'Serbia':':RS:', 'Senegal':':SN:', 'Panama':':PA:', 'Switzerland':':CH:', 'Croatia':':HR:', 'Uruguay':':UY:',
       'Russia':':RU:', 'Denmark':':DK:', 'Costa Rica':':CR:', 'Belgium':':BE:', 'Argentina':':AR:',
       'Iceland':':IS:', 'Egypt':':EG:', 'Spain':':ES:', 'Peru':':PE:', 'South Korea':':KR:', 'Japan':':JP:',
       'Saudi Arabia':':SA:', 'Morocco':':MA:', 'Iran':':IR:', 'Sweden':':SE:', 'Portugal':':PT:', 'Mexico':':MX:',
       'England':':GB:', 'Colombia':':CO:', 'Tunisia':':TN:'}

flag_team = flagship.get(team)

wc_tim = wc[(wc['home_team']==team) | (wc['away_team']==team)]

if team == 'France':
    st.write("### You choose: %s %s %s"%(team, flag.flag(flag_team), emoji.emojize(':trophy:')))
else: 
    st.write("### You choose: %s %s "%(team, flag.flag(flag_team)))

all_shot_comp = pd.read_csv('statsbombdata.csv')
drop = [3848,3850,3852,3849,3851,3855,3857,4892,4894,4896,4898,3714,3718,3720,4891,4893,4897,3763,3765,3769,3713,3717,3719,3721,
       3762,3764]
all_shot_comp = all_shot_comp[~all_shot_comp['index'].isin(drop)]
all_shot_comp = all_shot_comp[all_shot_comp['team']==team] 



#FOR BODY PART VIZ
goal = all_shot_comp[['player','team','shot_outcome','shot_body_part']]
goal = goal[(goal['shot_outcome']=='Goal') & (goal['team']==team)]
goal['jum'] =1
top_skor_tim = goal.groupby(['player'])['jum'].agg('sum').to_frame().reset_index().sort_values(by=['jum'],ascending=False)
top_skor = top_skor_tim.iloc[0][0]
top_skor_gol = top_skor_tim.iloc[0][1]
body_part = goal[['shot_body_part']]
body_part['count'] = 1
body_part = body_part.groupby(['shot_body_part'])['count'].agg('sum').to_frame().sort_values(by=['count'],ascending=False).reset_index()
#body_part
body_part['count'] = body_part['count'].astype(str)
body_part['label'] = body_part['count'] + " " + body_part['shot_body_part']
body_part['count'] = body_part['count'].astype(int)


#FOR Goal Type
goal_type = all_shot_comp[['team','shot_type','shot_outcome']]
goal_type = goal_type[(goal_type['shot_outcome']=='Goal') & (goal_type['team']==team)]
goal_type['count'] = 1
goal_type = goal_type.groupby(['shot_type'])['count'].agg('sum').to_frame().sort_values(by=['count'],ascending=False).reset_index()
goal_type['count'] = goal_type['count'].astype(str)
goal_type['label'] = goal_type['count'] + " " + goal_type['shot_type']
goal_type['count'] = goal_type['count'].astype(int)
play = goal_type['shot_type'].iloc[0]



# FOR ALL SHOTS VIZ
type_shots = all_shot_comp[['player','team','shot_outcome','shot_body_part']]
type_shots = type_shots[(type_shots['team']== team) &( (type_shots['shot_outcome']=='Blocked')| (type_shots['shot_outcome']=='Saved')| (type_shots['shot_outcome']=='Wayward')
                 | (type_shots['shot_outcome']=='Off T')| (type_shots['shot_outcome']=='Goal'))]
all_shots_count = type_shots['shot_outcome'].value_counts().to_frame().reset_index()

all_shots_count = all_shots_count.replace({'index':{'Off T': 'Off Target'}})
#all_shots_count
all_shots_count['shot_outcome'] = all_shots_count['shot_outcome'].astype(str)
all_shots_count['label'] = all_shots_count['shot_outcome'] + " " + all_shots_count['index']
all_shots_count['shot_outcome'] = all_shots_count['shot_outcome'].astype(int)


shot = all_shot_comp[all_shot_comp['type']=='Shot']#.set_index['id']
shots = shot

goal_count = body_part['count'].sum()
body_part_text =  ' and '.join(body_part['label'])

goal_row = len(body_part.index)
if goal_row == 3:
    colors=["#EC4E20", "#FFC914", "#423E37"]
elif goal_row ==2:
    colors=["#EC4E20", "#FFC914"]        
else:
    colors=["#EC4E20"]

#PLOT PERTAMA
fig = plt.figure(
    FigureClass = Waffle,
    rows = 2,
    values = body_part['count'],
    colors=colors,
    title={'label': 'How %s Scores Goals (Body Part)'%(team), 'loc': 'left','fontsize': 30,'pad':25},
    legend={'loc': 'lower left', 'bbox_to_anchor': (0, -0.3), 'ncol': len(body_part), 'framealpha': 0,'fontsize':'15'},
    starting_location='NW',
    block_arranging_style='snake',
    labels=[f" {v}" for k, v in body_part['label'].items()],
    figsize=(9, 5)
)

st.pyplot(fig=fig)
plt.close(fig)


st.markdown('<p align="center"> %s %s scored %s goals all from %s. <br> Top Scorer of %s is <b> %s with %s goals </b>   </p>'%(team, flag.flag(flag_team), goal_count, body_part_text, team, top_skor, top_skor_gol ), unsafe_allow_html=True)

st.markdown('<p style="text-align: center"; class="credit";"font-family:Courier New"> <br>  </p>', unsafe_allow_html=True)


goal_type_row = len(goal_type.index)
if goal_type_row == 3:
    colors2=["#257FB8", "#F2640C", "#1AAD07"]
elif goal_type_row == 2:
    colors2=["#257FB8", "#F2640C"]
else:
    colors2 = ['orange']

#PLOT KEDUA
fig4 = plt.figure(
    FigureClass = Waffle,
    rows = 2,
    values = goal_type['count'],
    colors=colors2,
    title={'label': 'How %s Scores Goals (Build Up Play)'%(team), 'loc': 'left','fontsize': 30,'pad':25},
    legend={'loc': 'lower left', 'bbox_to_anchor': (0, -0.3), 'ncol': len(body_part), 'framealpha': 0,'fontsize':'15'},
    starting_location='NW',
    block_arranging_style='snake',
    labels=[f" {v}" for k, v in goal_type['label'].items()],
    figsize=(9, 5)
)

st.pyplot(fig=fig4)
plt.close(fig4)


st.markdown('<p align="center"> Most of %s %s goals were scored from <b>%s </b>.</p>'%(team, flag.flag(flag_team),play), unsafe_allow_html=True)
st.markdown('<p style="text-align: center"; class="credit";"font-family:Courier New"> <br>  </p>', unsafe_allow_html=True)


all_shots_row = len(all_shots_count.index)
if all_shots_row == 5:
    colors=["#AF3800", "#F7C548", "#4281A4","#202C59","#40F99B"]
else:
    colors=["#AF3800", "#F7C548", "#4281A4", '#40F99B']


total_shot = all_shots_count['shot_outcome'].sum()

conv_goal = (goal_count/(total_shot-goal_count))*100



#PLOT KETIGA
fig2 = plt.figure(
    FigureClass = Waffle,
    rows = 5,
    values = all_shots_count['shot_outcome'],
    colors=colors,
    title={'label': "Shots Outcome of %s's All Shots "%(team), 'loc': 'left','fontsize': 30,'pad':25},
    legend={'loc': 'lower left', 'bbox_to_anchor': (0, -0.38), 'ncol': 3, 'framealpha': 0,'fontsize':'15'},
    starting_location='NW',
    block_arranging_style='snake',
    labels=[f" {v}" for k, v in all_shots_count['label'].items()],   
    figsize=(10, 6)
)

st.pyplot(fig=fig2)
plt.close(fig2)

st.markdown('<p align="center"> %s %s conversion goal rate is <b>%.2f&percnt;</b> <br> Conversion goal rate: Goal per Total Shots <br>     </p>'%(team, flag.flag(flag_team), conv_goal ), unsafe_allow_html=True)


st.markdown('<p align="center"><br>     </p>', unsafe_allow_html=True)


#PLOT KEEMPAT
background = "white"

fig3, ax = plt.subplots(figsize=(11, 7))
fig3.set_facecolor(background)

pitch_mckeever.draw_pitch(orientation="vertical",
           aspect="half",
           pitch_color=background,
           line_color="lightgrey",
           ax=ax)


home_goal = 0  
home_shot_miss=0

#Plot the shots
for i, shots in shots.iterrows():
    shots['location'] = literal_eval(shots['location'])
    x = shots['location'][0]
    y = shots['location'][1]
    
    #Definisi goal dari dataset
    goal = shots['shot_outcome'] == 'Goal'
    team_name = shots['team']
    
    #Ukuran circle tergantung xG
    circlesize = np.sqrt(shots['shot_statsbomb_xg']*15)

    if (team_name == team):
        if goal:
            shotCircle = plt.Circle((y-5,x-15),circlesize,color = 'red') #pitchWidthY-  x-70,y+40
            #plt.text((x+1),pitchWidthY-y+4,shots['player'])
            home_goal += 1
        else:
            shotCircle = plt.Circle((y-5,x-15),circlesize,color='red')
            shotCircle.set_alpha(.2)
            #home_shot_miss += 1
    
    ax.add_patch(shotCircle)
    
plt.title('Where All '+ team +"'s"+' Shots Came From',fontfamily="Source Sans Pro",fontsize=18,fontweight='bold')
plt.text(43,53.4,'pitch template: @petermckeever',fontfamily="Source Sans Pro",fontsize=12,alpha=0.5,style='italic')

plt.text(34,70,team,fontweight='bold',alpha=0.5,fontsize=28,ha='center', va='center')
plt.text(34,66,'Goals: '+ str(goal_count), fontweight='bold',alpha=0.3,fontsize=15,ha='center', va='center')
plt.text(34,63.5,'Total Shots: '+ str(total_shot),fontweight='bold',alpha=0.3,fontsize=15,ha='center', va='center')


plt.tight_layout()
#fig.set_size_inches(5,7)
#plt.xlim(59.6,121)
#plt.show()


#plt.show()

st.pyplot(fig=fig3 , width=40)
plt.close(fig3)


st.markdown('<p align="center"> Can you spot where <b> %s </b> score goals?</p>'%(top_skor), unsafe_allow_html=True)



st.markdown('<p align="center"> Bold red indicates a goal,<br> the bigger the circle, the higher chance a player score a goal <br> otherwise known as <b>Expected Goal (xG)</b>.</p>', unsafe_allow_html=True)


st.markdown('<p align="center"> To learn more about Expected Goal, <br> you can access to this interesting video: <a href="https://www.youtube.com/watch?v=zSaeaFcm1SY">Tifo Football</a> .</p>', unsafe_allow_html=True)

st.markdown('<p style="text-align: center"; class="title-font";"font-family:Courier New"> <br> </p>', unsafe_allow_html=True)


st.markdown('<p style="text-align: center"; class="title-font";"font-family:Courier New"> <b>Thank You ⚽⚽ </b></p>', unsafe_allow_html=True)


